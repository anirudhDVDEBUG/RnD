#!/usr/bin/env node
/**
 * MemoryBridge Demo — simulates the cross-tool AI memory MCP server locally.
 *
 * This demo shows how MemoryBridge stores, retrieves, and shares memories
 * across different AI tools, using ~400 tokens per operation instead of ~4,000.
 *
 * No external API keys required — uses a local JSON file as the memory store.
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const MEMORY_DIR = join(__dirname, ".memorybridge");
const MEMORY_FILE = join(MEMORY_DIR, "memories.json");

// ── Simulated MemoryBridge core ──────────────────────────────────────────

class MemoryBridge {
  constructor(storePath) {
    this.storePath = storePath;
    this.memories = [];
    this._load();
  }

  _load() {
    if (existsSync(this.storePath)) {
      this.memories = JSON.parse(readFileSync(this.storePath, "utf-8"));
    }
  }

  _save() {
    if (!existsSync(dirname(this.storePath))) {
      mkdirSync(dirname(this.storePath), { recursive: true });
    }
    writeFileSync(this.storePath, JSON.stringify(this.memories, null, 2));
  }

  /** Store a memory — equivalent to MCP tool "store_memory" */
  store(content, tags = [], source = "unknown") {
    const memory = {
      id: `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      content,
      tags,
      source,
      createdAt: new Date().toISOString(),
    };
    this.memories.push(memory);
    this._save();
    return memory;
  }

  /** Retrieve memories by query — equivalent to MCP tool "retrieve_memories" */
  retrieve(query, limit = 5) {
    const queryLower = query.toLowerCase();
    const scored = this.memories.map((m) => {
      let score = 0;
      if (m.content.toLowerCase().includes(queryLower)) score += 3;
      for (const tag of m.tags) {
        if (tag.toLowerCase().includes(queryLower)) score += 2;
      }
      // Recency boost
      const ageMs = Date.now() - new Date(m.createdAt).getTime();
      score += Math.max(0, 1 - ageMs / (1000 * 60 * 60 * 24));
      return { ...m, _score: score };
    });
    return scored
      .filter((m) => m._score > 0)
      .sort((a, b) => b._score - a._score)
      .slice(0, limit)
      .map(({ _score, ...rest }) => rest);
  }

  /** List all memories — equivalent to MCP tool "list_memories" */
  list() {
    return this.memories;
  }

  /** Delete a memory by ID */
  delete(id) {
    const before = this.memories.length;
    this.memories = this.memories.filter((m) => m.id !== id);
    this._save();
    return this.memories.length < before;
  }

  /** Token count estimate — shows MemoryBridge efficiency */
  estimateTokens(memories) {
    // Rough estimate: 1 token per 4 chars (GPT/Claude tokenizer average)
    const json = JSON.stringify(memories);
    return Math.ceil(json.length / 4);
  }
}

// ── Demo scenario ────────────────────────────────────────────────────────

function banner(text) {
  const line = "─".repeat(60);
  console.log(`\n${line}`);
  console.log(`  ${text}`);
  console.log(line);
}

function printMemory(mem, indent = "  ") {
  console.log(`${indent}ID:      ${mem.id}`);
  console.log(`${indent}Source:  ${mem.source}`);
  console.log(`${indent}Tags:    [${mem.tags.join(", ")}]`);
  console.log(`${indent}Content: ${mem.content}`);
  console.log(`${indent}Created: ${mem.createdAt}`);
}

async function main() {
  console.log(`
 __  __                            ____       _     _
|  \\/  | ___ _ __ ___   ___  _ __ _   _| __ )_ __(_) __| | __ _  ___
| |\\/| |/ _ \\ '_ \` _ \\ / _ \\| '__| | | |  _ \\| '__| |/ _\` |/ _\` |/ _ \\
| |  | |  __/ | | | | | (_) | |  | |_| | |_) | |  | | (_| | (_| |  __/
|_|  |_|\\___|_| |_| |_|\\___/|_|   \\__, |____/|_|  |_|\\__,_|\\__, |\\___|
                                   |___/                     |___/

  Cross-Tool AI Memory MCP Server Demo
  github.com/IamRamgarhia/memorybridge
`);

  const bridge = new MemoryBridge(MEMORY_FILE);
  // Clear previous demo data
  bridge.memories = [];
  bridge._save();

  // ── Step 1: Simulate Claude Code storing memories ──────────────────
  banner("1. Claude Code stores project context");

  const m1 = bridge.store(
    "Project uses Next.js 14 with App Router, TypeScript strict mode, and Tailwind CSS.",
    ["stack", "nextjs", "typescript", "tailwind"],
    "claude-code"
  );
  console.log("  Stored memory from Claude Code:");
  printMemory(m1);

  const m2 = bridge.store(
    "Auth is handled via NextAuth.js with Google and GitHub providers. Session stored in Prisma/PostgreSQL.",
    ["auth", "nextauth", "prisma", "database"],
    "claude-code"
  );
  console.log("\n  Stored memory from Claude Code:");
  printMemory(m2);

  const m3 = bridge.store(
    "API rate limiting: 100 requests/min per user. Implemented with upstash/ratelimit in middleware.",
    ["api", "rate-limit", "middleware", "upstash"],
    "claude-code"
  );
  console.log("\n  Stored memory from Claude Code:");
  printMemory(m3);

  // ── Step 2: Simulate Cursor reading those memories ─────────────────
  banner("2. Cursor retrieves shared context (cross-tool!)");

  const results = bridge.retrieve("auth");
  console.log(`  Query: "auth"  ->  Found ${results.length} memory(ies)\n`);
  for (const r of results) {
    printMemory(r);
    console.log();
  }

  // ── Step 3: Simulate Windsurf adding its own memory ────────────────
  banner("3. Windsurf adds a new memory");

  const m4 = bridge.store(
    "Deployment pipeline: Vercel preview on PR, production on merge to main. Environment vars in Vercel dashboard.",
    ["deployment", "vercel", "ci-cd"],
    "windsurf"
  );
  console.log("  Stored memory from Windsurf:");
  printMemory(m4);

  // ── Step 4: Show all shared memories ───────────────────────────────
  banner("4. Full memory store (shared across all tools)");

  const all = bridge.list();
  console.log(`  Total memories: ${all.length}\n`);
  for (const mem of all) {
    printMemory(mem);
    console.log();
  }

  // ── Step 5: Token efficiency comparison ────────────────────────────
  banner("5. Token efficiency comparison");

  const compactTokens = bridge.estimateTokens(all);

  // Simulate a naive approach: full file contents, repeated context, etc.
  const naivePayload = all.map((m) => ({
    ...m,
    fullContext: `The following memory was stored by ${m.source} at ${m.createdAt}. ` +
      `It contains the following information that should be used as context ` +
      `for all future interactions. Tags associated: ${m.tags.join(", ")}. ` +
      `Full content follows:\n\n${m.content}\n\n` +
      `End of memory entry. Please keep this in your context window.`,
    metadata: {
      version: "1.0.0",
      schema: "memory-v1",
      encoding: "utf-8",
      source: m.source,
      retrievedAt: new Date().toISOString(),
      priority: "normal",
      ttl: null,
    },
  }));
  const naiveTokens = bridge.estimateTokens(naivePayload);

  console.log(`  MemoryBridge (compact):  ~${compactTokens} tokens`);
  console.log(`  Naive approach:          ~${naiveTokens} tokens`);
  console.log(`  Savings:                 ${Math.round((1 - compactTokens / naiveTokens) * 100)}% fewer tokens`);
  console.log(`  Ratio:                   ~1:${Math.round(naiveTokens / compactTokens)}`);

  // ── Step 6: Search across tools ────────────────────────────────────
  banner("6. Cross-tool search: 'deployment'");

  const deployResults = bridge.retrieve("deployment");
  console.log(`  Found ${deployResults.length} result(s):\n`);
  for (const r of deployResults) {
    printMemory(r);
    console.log();
  }

  // ── Summary ────────────────────────────────────────────────────────
  banner("Summary");
  console.log("  Memories stored by Claude Code: " + all.filter((m) => m.source === "claude-code").length);
  console.log("  Memories stored by Windsurf:    " + all.filter((m) => m.source === "windsurf").length);
  console.log("  Total shared memories:          " + all.length);
  console.log("  Token usage (compact):          ~" + compactTokens);
  console.log("  Memory file:                    " + MEMORY_FILE);
  console.log();
  console.log("  MemoryBridge lets every MCP-compatible AI tool share");
  console.log("  persistent context — no re-explaining your project.");
  console.log();
}

main().catch(console.error);
