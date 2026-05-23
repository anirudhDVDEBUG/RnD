#!/usr/bin/env node

/**
 * End-to-end demo of the MCP Server Manager.
 * Adds servers, lists them, validates, exports for Claude, and cleans up.
 */

const path = require("path");
const fs = require("fs");
const { MCPServerManager } = require("./manager");

const CONFIG = path.join(__dirname, "..", "demo-mcp-servers.json");

// Clean slate
if (fs.existsSync(CONFIG)) fs.unlinkSync(CONFIG);

const mgr = new MCPServerManager(CONFIG);

function hr() { console.log("─".repeat(60)); }

console.log();
hr();
console.log("  MCP SERVER MANAGER - End-to-End Demo");
console.log("  Inspired by https://github.com/hacimertgokhan/openmcp");
hr();

// --- Step 1: Add servers ---
console.log("\n1. Adding MCP server configurations...\n");

const servers = [
  {
    name: "filesystem",
    config: {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"],
      type: "stdio",
    },
  },
  {
    name: "github",
    config: {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-github"],
      env: { GITHUB_TOKEN: "ghp_xxxxxxxxxxxx" },
      type: "stdio",
    },
  },
  {
    name: "postgres",
    config: {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-postgres"],
      env: { DATABASE_URL: "postgresql://user:pass@localhost:5432/mydb" },
      type: "stdio",
    },
  },
  {
    name: "brave-search",
    config: {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-brave-search"],
      env: { BRAVE_API_KEY: "BSA_xxxxxxxxxxxx" },
      type: "stdio",
    },
  },
  {
    name: "custom-sse-server",
    config: {
      command: "node",
      args: ["./my-server/index.js"],
      env: { PORT: "3001" },
      type: "sse",
    },
  },
];

for (const { name, config } of servers) {
  const result = mgr.add(name, config);
  console.log(`   ${result.ok ? "+" : "!"} ${result.message}`);
}

// --- Step 2: List all servers ---
console.log("\n2. Listing all configured MCP servers...\n");

const list = mgr.list();
console.log(`   Total servers: ${list.length}\n`);

for (const s of list) {
  const envKeys = s.env ? Object.keys(s.env) : [];
  console.log(`   [${s.type}] ${s.name}`);
  console.log(`     cmd: ${s.command} ${s.args.join(" ")}`);
  if (envKeys.length) console.log(`     env: ${envKeys.join(", ")}`);
}

// --- Step 3: Validate ---
console.log("\n3. Validating server configurations...\n");

for (const s of list) {
  const v = mgr.validate(s.name);
  console.log(`   ${s.name}: ${v.valid ? "VALID" : "INVALID - " + v.errors.join(", ")}`);
}

// --- Step 4: Show one server ---
console.log("\n4. Detailed view of 'github' server...\n");

const gh = mgr.get("github");
console.log("   " + JSON.stringify(gh, null, 2).replace(/\n/g, "\n   "));

// --- Step 5: Update a server ---
console.log("\n5. Updating 'custom-sse-server' port to 4000...\n");

const updateResult = mgr.update("custom-sse-server", { env: { PORT: "4000" } });
console.log(`   ${updateResult.message}`);
const updated = mgr.get("custom-sse-server");
console.log(`   New env.PORT = ${updated.env.PORT}`);

// --- Step 6: Remove a server ---
console.log("\n6. Removing 'brave-search' server...\n");

const rmResult = mgr.remove("brave-search");
console.log(`   ${rmResult.message}`);
console.log(`   Remaining servers: ${mgr.count()}`);

// --- Step 7: Export for Claude Code ---
console.log("\n7. Exporting for Claude Code (~/.claude.json format)...\n");

const exported = mgr.exportForClaude();
const snippet = JSON.stringify({ mcpServers: exported }, null, 2);
console.log(snippet.split("\n").map((l) => "   " + l).join("\n"));

// --- Cleanup ---
hr();
console.log("  Demo complete. Config written to: demo-mcp-servers.json");
hr();
console.log();
