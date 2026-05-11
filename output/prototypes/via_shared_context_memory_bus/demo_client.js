#!/usr/bin/env node
/**
 * demo_client.js — Exercises the Via MCP server by spawning it as a child
 * process and calling every tool through the MCP client SDK.
 *
 * Simulates a multi-tool workflow:
 *   1. "Claude Code" stores architectural decisions in shared memory
 *   2. "Cursor" pushes code-review context to the context bus
 *   3. Tasks are created and updated across tools
 *   4. Everything is read back to show cross-tool visibility
 *
 * No API keys required — runs entirely locally.
 */

const { Client } = require("@modelcontextprotocol/sdk/client/index.js");
const { StdioClientTransport } = require("@modelcontextprotocol/sdk/client/stdio.js");
const path = require("path");

const SERVER_PATH = path.join(__dirname, "via_server.js");

// Helpers
function section(title) {
  const bar = "=".repeat(60);
  console.log(`\n${bar}\n  ${title}\n${bar}`);
}

function pretty(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

async function callTool(client, name, args) {
  const result = await client.callTool({ name, arguments: args });
  return JSON.parse(result.content[0].text);
}

async function main() {
  console.log("Via Shared Context & Memory Bus — Demo\n");
  console.log("Connecting to Via MCP server via stdio...");

  // Spawn the server as a child process
  const transport = new StdioClientTransport({
    command: "node",
    args: [SERVER_PATH],
  });
  const client = new Client(
    { name: "via-demo-client", version: "1.0.0" },
    { capabilities: {} }
  );
  await client.connect(transport);

  // List available tools
  section("1. Available MCP Tools");
  const { tools } = await client.listTools();
  console.log(`Via exposes ${tools.length} tools:`);
  tools.forEach((t) => console.log(`  - ${t.name}: ${t.description.slice(0, 70)}...`));

  // -----------------------------------------------------------------------
  // MEMORY BUS — simulate Claude Code storing decisions
  // -----------------------------------------------------------------------
  section("2. Memory Bus — Claude Code stores architectural decisions");

  await callTool(client, "memory_store", {
    key: "arch/database",
    value: "Using PostgreSQL with pgvector for embeddings. Schema in db/schema.sql.",
    tags: ["architecture", "database"],
  });
  console.log("  Stored: arch/database");

  await callTool(client, "memory_store", {
    key: "arch/auth",
    value: "JWT-based auth with refresh tokens. Provider: auth0. Config in src/auth/.",
    tags: ["architecture", "auth"],
  });
  console.log("  Stored: arch/auth");

  await callTool(client, "memory_store", {
    key: "conventions/naming",
    value: "snake_case for DB columns, camelCase for JS/TS, kebab-case for URLs.",
    tags: ["conventions"],
  });
  console.log("  Stored: conventions/naming");

  // Retrieve from another tool's perspective
  section("3. Memory Bus — Cursor retrieves decisions");
  const dbDecision = await callTool(client, "memory_retrieve", { key: "arch/database" });
  console.log("  Cursor reads arch/database:");
  pretty(dbDecision);

  const allKeys = await callTool(client, "memory_list", { tag: "architecture" });
  console.log("\n  All 'architecture' tagged memories:");
  pretty(allKeys);

  // -----------------------------------------------------------------------
  // TASK BUS — cross-tool task management
  // -----------------------------------------------------------------------
  section("4. Task Bus — Create tasks from different tools");

  const t1 = await callTool(client, "task_create", {
    title: "Implement user registration API",
    description: "POST /api/auth/register with email/password validation",
    priority: "high",
    assignee: "claude-code",
  });
  console.log(`  Created task #${t1.task.id}: ${t1.task.title} [${t1.task.assignee}]`);

  const t2 = await callTool(client, "task_create", {
    title: "Write unit tests for auth module",
    description: "Cover register, login, refresh, and logout flows",
    priority: "medium",
    assignee: "cursor",
  });
  console.log(`  Created task #${t2.task.id}: ${t2.task.title} [${t2.task.assignee}]`);

  const t3 = await callTool(client, "task_create", {
    title: "Design landing page mockup",
    description: "Hero section, feature grid, CTA. Use Figma.",
    priority: "low",
    assignee: "windsurf",
  });
  console.log(`  Created task #${t3.task.id}: ${t3.task.title} [${t3.task.assignee}]`);

  // Update task status
  section("5. Task Bus — Claude Code completes a task");
  const updated = await callTool(client, "task_update", {
    task_id: 1,
    status: "done",
    notes: "Implemented with input validation and rate limiting. PR #42 merged.",
  });
  console.log("  Task #1 updated:");
  pretty(updated.task);

  // List remaining tasks
  const pending = await callTool(client, "task_list", { status: "pending" });
  console.log(`\n  Pending tasks (visible to all tools): ${pending.count}`);
  pending.tasks.forEach((t) =>
    console.log(`    #${t.id} [${t.priority}] ${t.title} → ${t.assignee}`)
  );

  // -----------------------------------------------------------------------
  // CONTEXT BUS — real-time cross-tool context sharing
  // -----------------------------------------------------------------------
  section("6. Context Bus — Cross-tool context sharing");

  await callTool(client, "context_push", {
    source: "claude-code",
    content: "Registration endpoint is live at /api/auth/register. Returns 201 on success.",
    type: "finding",
  });
  console.log("  claude-code pushed: API endpoint finding");

  await callTool(client, "context_push", {
    source: "cursor",
    content: "Found potential SQL injection in user search query. See src/search.js:47.",
    type: "finding",
  });
  console.log("  cursor pushed: security finding");

  await callTool(client, "context_push", {
    source: "windsurf",
    content: "Should we use shadcn/ui or custom components for the landing page?",
    type: "question",
  });
  console.log("  windsurf pushed: design question");

  await callTool(client, "context_push", {
    source: "claude-code",
    content: "Decision: Use shadcn/ui for consistency. Custom only where needed.",
    type: "decision",
  });
  console.log("  claude-code pushed: decision");

  // Read full context bus
  section("7. Context Bus — Full conversation visible to all tools");
  const allContext = await callTool(client, "context_read", { limit: 10 });
  console.log(`  ${allContext.count} context entries on the bus:\n`);
  allContext.entries.forEach((e) => {
    console.log(`  [${e.type.toUpperCase()}] ${e.source}: ${e.content}`);
  });

  // -----------------------------------------------------------------------
  // Summary
  // -----------------------------------------------------------------------
  section("Summary");
  const memCount = (await callTool(client, "memory_list", {})).count;
  const taskCount = (await callTool(client, "task_list", {})).count;
  const ctxCount = (await callTool(client, "context_read", {})).count;
  console.log(`  Memory entries:  ${memCount}`);
  console.log(`  Tasks tracked:   ${taskCount}`);
  console.log(`  Context entries: ${ctxCount}`);
  console.log(`\n  All data persisted to .via_data.json`);
  console.log(`  Any MCP-compatible tool can connect and see this shared state.`);
  console.log();

  // Clean up
  await client.close();
  process.exit(0);
}

main().catch((err) => {
  console.error("Demo error:", err);
  process.exit(1);
});
