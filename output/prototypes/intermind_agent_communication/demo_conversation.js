#!/usr/bin/env node
/**
 * demo_conversation.js — Simulates a multi-agent conversation via Intermind.
 *
 * Scenario: Three AI coding agents collaborate on a code-review task.
 *   1. Claude Code  (lead reviewer)
 *   2. Cursor       (frontend specialist)
 *   3. Codex        (backend specialist)
 *
 * They register, open a thread, exchange messages, and produce a summary.
 * No network, no API keys — runs entirely in-process.
 */

import { IntermindServer } from "./intermind_simulator.js";

const server = new IntermindServer();

// ──────────────────────────────────────────────────────────
// 1. Register agents
// ──────────────────────────────────────────────────────────
console.log("=".repeat(64));
console.log("  INTERMIND DEMO — Agent-to-Agent Threaded Conversation");
console.log("=".repeat(64));
console.log();

const claude = server.registerAgent("Claude Code", "lead-reviewer");
const cursor = server.registerAgent("Cursor", "frontend-specialist");
const codex  = server.registerAgent("Codex", "backend-specialist");

console.log("Registered agents:");
for (const a of server.listAgents()) {
  console.log(`  [${a.id}] ${a.name} (${a.role})`);
}
console.log();

// ──────────────────────────────────────────────────────────
// 2. Claude Code starts a code-review thread
// ──────────────────────────────────────────────────────────
const thread = server.startThread(
  "PR #42 — Refactor auth middleware",
  claude.id,
  [cursor.id, codex.id]
);

console.log(`Thread created: "${thread.title}" [${thread.id}]`);
console.log(`  Participants: ${thread.participants.map(id => server.agents.get(id).name).join(", ")}`);
console.log();

// ──────────────────────────────────────────────────────────
// 3. Agents exchange messages
// ──────────────────────────────────────────────────────────
const conversation = [
  {
    agent: claude,
    body: "I'm reviewing PR #42. The auth middleware was refactored to use async/await instead of callbacks. @Cursor — can you check the frontend session handling? @Codex — please verify the token validation logic.",
  },
  {
    agent: cursor,
    body: "Checked the frontend. The session cookie name changed from `sid` to `session_id`. I see the React AuthProvider already reads from the new name, so the frontend is consistent. LGTM on the client side.",
  },
  {
    agent: codex,
    body: "Token validation looks solid. One concern: the refresh-token rotation now happens inside the middleware instead of a dedicated service. This couples auth logic to the HTTP layer. Suggest extracting `rotateRefreshToken()` into `services/auth.ts`.",
  },
  {
    agent: claude,
    body: "Good catch @Codex. I agree — let's request the author extract that function. @Cursor — any impact on the frontend if refresh rotation timing changes slightly?",
  },
  {
    agent: cursor,
    body: "No impact. The frontend just retries on 401 with the refresh token. Timing doesn't matter as long as the endpoint contract stays the same.",
  },
  {
    agent: claude,
    body: "Summary: Frontend LGTM. Backend approved with one requested change — extract `rotateRefreshToken()` into `services/auth.ts`. Marking PR as 'Approved with suggestions'.",
  },
];

console.log("── Conversation ─────────────────────────────────────────");
for (const { agent, body } of conversation) {
  server.sendMessage(thread.id, agent.id, body);
  console.log();
  console.log(`  [${agent.name}]:`);
  // Wrap long lines for readability
  const wrapped = body.replace(/(.{1,56}(?:\s|$))/g, "    $1\n");
  process.stdout.write(wrapped);
}
console.log();

// ──────────────────────────────────────────────────────────
// 4. Show thread state
// ──────────────────────────────────────────────────────────
console.log("── Thread State ─────────────────────────────────────────");
const messages = server.getMessages(thread.id);
console.log(`  Thread: ${thread.title}`);
console.log(`  Messages: ${messages.length}`);
console.log(`  Participants: ${thread.participants.length}`);
console.log();

// ──────────────────────────────────────────────────────────
// 5. Demonstrate listing threads per agent
// ──────────────────────────────────────────────────────────
console.log("── Per-Agent Thread Listing ──────────────────────────────");
for (const a of server.listAgents()) {
  const threads = server.listThreads(a.id);
  console.log(`  ${a.name}: ${threads.length} thread(s) — [${threads.map(t => t.title).join(", ")}]`);
}
console.log();

// ──────────────────────────────────────────────────────────
// 6. Second thread — architecture discussion
// ──────────────────────────────────────────────────────────
const thread2 = server.startThread(
  "Architecture: migrate to edge runtime?",
  codex.id,
  [claude.id]
);

server.sendMessage(thread2.id, codex.id,
  "Should we move the auth middleware to an edge runtime for lower latency? The new async pattern would work on Cloudflare Workers."
);
server.sendMessage(thread2.id, claude.id,
  "Worth exploring. Cold-start times on Workers are <5ms. But we'd lose Node-specific crypto APIs. Let's spike it in a separate branch."
);

console.log("── Second Thread ────────────────────────────────────────");
console.log(`  Thread: "${thread2.title}" [${thread2.id}]`);
console.log(`  Messages: ${server.getMessages(thread2.id).length}`);
console.log(`  Participants: ${thread2.participants.map(id => server.agents.get(id).name).join(", ")}`);
console.log();

// ──────────────────────────────────────────────────────────
// 7. Final summary
// ──────────────────────────────────────────────────────────
console.log("=".repeat(64));
console.log("  SUMMARY");
console.log("=".repeat(64));
console.log(`  Total agents registered : ${server.listAgents().length}`);
console.log(`  Total threads           : ${server.listThreads().length}`);
console.log(`  Total messages          : ${server.listThreads().reduce((n, t) => n + t.messages.length, 0)}`);
console.log();
console.log("  This demonstrates Intermind's core value proposition:");
console.log("  AI agents can hold structured, threaded conversations");
console.log("  with each other via MCP — enabling collaborative code");
console.log("  review, architecture decisions, and task delegation");
console.log("  across heterogeneous agent environments.");
console.log();
