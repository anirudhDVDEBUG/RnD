/**
 * Interactive demo — exercises all four MCP tools locally
 * without needing Claude or any API keys.
 */

import { MemoryStore } from "./db.js";

const store = new MemoryStore();

console.log("=".repeat(60));
console.log(" Second Brain MCP — Local Demo (mock embeddings)");
console.log("=".repeat(60));

// ── 1. Remember ─────────────────────────────────────────────────────

const memories = [
  {
    content: "Cloudflare Workers run on V8 isolates at the edge, with sub-millisecond cold starts.",
    tags: ["cloudflare", "architecture"],
    metadata: { source: "docs" },
  },
  {
    content: "MCP (Model Context Protocol) lets AI assistants call external tools via a standard JSON-RPC interface.",
    tags: ["mcp", "protocol"],
    metadata: { source: "spec" },
  },
  {
    content: "D1 is Cloudflare's serverless SQLite database. It replicates globally and costs nothing at rest.",
    tags: ["cloudflare", "database"],
    metadata: { source: "docs" },
  },
  {
    content: "Vectorize is Cloudflare's vector database for similarity search. Supports cosine, euclidean, and dot-product metrics.",
    tags: ["cloudflare", "vectors"],
    metadata: { source: "docs" },
  },
  {
    content: "OpenAI text-embedding-ada-002 produces 1536-dimensional vectors. Good for semantic search over documents.",
    tags: ["openai", "embeddings"],
    metadata: { source: "openai-docs" },
  },
  {
    content: "To deploy a Worker, run npx wrangler deploy. Wrangler handles bundling and uploading automatically.",
    tags: ["cloudflare", "deployment"],
    metadata: { source: "tutorial" },
  },
  {
    content: "Claude Code can connect to MCP servers defined in .claude/settings.json for persistent tool access.",
    tags: ["claude", "mcp"],
    metadata: { source: "anthropic-docs" },
  },
  {
    content: "RAG (Retrieval-Augmented Generation) combines a retriever with a language model to ground answers in facts.",
    tags: ["rag", "architecture"],
    metadata: { source: "paper" },
  },
];

console.log("\n[STEP 1] Storing 8 memories...\n");
for (const m of memories) {
  const result = store.remember(m);
  console.log(`  #${result.id} — ${m.content.slice(0, 70)}...`);
}

// ── 2. Recall (semantic search) ─────────────────────────────────────

console.log("\n" + "-".repeat(60));
console.log("[STEP 2] Semantic search: \"How does Cloudflare store vectors?\"\n");

const results = store.recall("How does Cloudflare store vectors?", 3);
for (const r of results) {
  console.log(`  [score=${r.score.toFixed(3)}] #${r.id}: ${r.content.slice(0, 80)}`);
}

// ── 3. Search again with different query ────────────────────────────

console.log("\n" + "-".repeat(60));
console.log('[STEP 3] Semantic search: "connecting Claude to external tools"\n');

const results2 = store.recall("connecting Claude to external tools", 3);
for (const r of results2) {
  console.log(`  [score=${r.score.toFixed(3)}] #${r.id}: ${r.content.slice(0, 80)}`);
}

// ── 4. List by tag ──────────────────────────────────────────────────

console.log("\n" + "-".repeat(60));
console.log('[STEP 4] List memories tagged "cloudflare"\n');

const tagged = store.listMemories({ tag: "cloudflare" });
for (const m of tagged) {
  console.log(`  #${m.id}: [${m.tags.join(", ")}] ${m.content.slice(0, 70)}`);
}

// ── 5. Forget ───────────────────────────────────────────────────────

console.log("\n" + "-".repeat(60));
console.log("[STEP 5] Forgetting memory #5...\n");

const del = store.forget(5);
console.log(`  Deleted: ${del.deleted}`);

// ── 6. Final listing ────────────────────────────────────────────────

console.log("\n" + "-".repeat(60));
console.log("[STEP 6] Final memory count\n");

const all = store.listMemories({ limit: 100 });
console.log(`  Total memories remaining: ${all.length}`);

console.log("\n" + "=".repeat(60));
console.log(" Demo complete. All operations ran locally with mock embeddings.");
console.log(" In production, swap embeddings.js for OpenAI API calls and");
console.log(" better-sqlite3 for Cloudflare D1 + Vectorize.");
console.log("=".repeat(60));

store.close();
