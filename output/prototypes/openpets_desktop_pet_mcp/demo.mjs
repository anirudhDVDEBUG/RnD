#!/usr/bin/env node
/**
 * OpenPets MCP Demo — simulates an AI coding agent driving a desktop pet
 * through various states via the MCP tool interface.
 *
 * Run: node demo.mjs
 */

import {
  PET_STATES,
  MCP_TOOLS,
  AVAILABLE_PETS,
  handleToolCall,
  renderPetFrame,
} from "./mcp-server-mock.mjs";

const CYAN = "\x1b[36m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const RED = "\x1b[31m";
const MAGENTA = "\x1b[35m";
const DIM = "\x1b[2m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";

function banner() {
  console.log(`
${CYAN}${BOLD}╔══════════════════════════════════════════════════════════╗
║           OpenPets — Desktop Pet MCP Demo                ║
║     Desktop pets that react to AI coding agent status    ║
╚══════════════════════════════════════════════════════════╝${RESET}
`);
}

function section(title) {
  console.log(`${BOLD}${MAGENTA}── ${title} ${"─".repeat(50 - title.length)}${RESET}`);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function animatePet(state, message, frames = 4, delayMs = 300) {
  for (let i = 0; i < frames; i++) {
    const line = renderPetFrame(state, i, message);
    process.stdout.write(`\r${line}    `);
    await sleep(delayMs);
  }
  console.log();
}

async function simulateToolCall(toolName, args, description) {
  console.log(`${DIM}  Agent calls:${RESET} ${YELLOW}${toolName}${RESET}(${JSON.stringify(args)})`);
  const result = handleToolCall(toolName, args);
  console.log(`${DIM}  Response:${RESET}   ${GREEN}${JSON.stringify(result)}${RESET}`);
  return result;
}

async function main() {
  banner();

  // 1. Show MCP tool definitions
  section("MCP Tools Exposed to Claude Code");
  for (const tool of MCP_TOOLS) {
    const params = tool.inputSchema.properties
      ? Object.keys(tool.inputSchema.properties).join(", ")
      : "none";
    console.log(`  ${CYAN}${tool.name}${RESET}(${params})`);
    console.log(`    ${DIM}${tool.description}${RESET}`);
  }
  console.log();

  // 2. Show available pets
  section("Available Pet Characters");
  for (const pet of AVAILABLE_PETS) {
    const tag = pet.default ? `${GREEN} (default)${RESET}` : "";
    console.log(`  ${BOLD}${pet.name}${RESET} — ${pet.style} ${pet.size}${tag}`);
  }
  console.log();

  // 3. Simulate a coding session
  section("Simulated Agent Session");
  console.log(`${DIM}  Simulating an AI coding agent driving the desktop pet...${RESET}\n`);

  const scenario = [
    { tool: "get_pet_status", args: {}, desc: "Check initial pet state", pause: 500 },
    { tool: "set_pet_status", args: { status: "thinking", message: "Analyzing codebase..." }, desc: "Agent starts reasoning", pause: 1200 },
    { tool: "set_pet_status", args: { status: "coding", message: "Writing auth module" }, desc: "Agent writes code", pause: 1500 },
    { tool: "set_pet_status", args: { status: "coding", message: "Adding unit tests" }, desc: "Agent writes tests", pause: 1200 },
    { tool: "set_pet_status", args: { status: "error", message: "Test assertion failed" }, desc: "A test fails", pause: 1000 },
    { tool: "set_pet_status", args: { status: "thinking", message: "Debugging test..." }, desc: "Agent debugs", pause: 1000 },
    { tool: "set_pet_status", args: { status: "coding", message: "Fixing edge case" }, desc: "Agent fixes bug", pause: 1200 },
    { tool: "set_pet_status", args: { status: "success", message: "All tests pass!" }, desc: "Tests pass", pause: 1500 },
    { tool: "set_pet_status", args: { status: "idle" }, desc: "Agent finishes task", pause: 800 },
  ];

  for (const step of scenario) {
    console.log(`  ${BOLD}${step.desc}${RESET}`);
    await simulateToolCall(step.tool, step.args);
    if (step.args.status) {
      await animatePet(step.args.status, step.args.message);
    }
    await sleep(step.pause);
    console.log();
  }

  // 4. Show all pet states
  section("All Pet States");
  for (const [key, state] of Object.entries(PET_STATES)) {
    const frame = state.frames[0];
    console.log(`  ${frame}  ${BOLD}${state.label}${RESET} — ${state.description}`);
  }
  console.log();

  // 5. Summary
  section("Integration Summary");
  console.log(`
  ${BOLD}How it works in production:${RESET}
  1. OpenPets Electron app runs a pixel-art pet on your desktop
  2. An MCP server (stdio JSON-RPC) exposes tools like ${CYAN}set_pet_status${RESET}
  3. Claude Code connects via mcpServers config in .claude/settings.json
  4. As the agent thinks/codes/errors, it calls MCP tools
  5. The pet animates in real-time on your desktop

  ${BOLD}MCP config snippet:${RESET}
  ${DIM}{
    "mcpServers": {
      "openpets": {
        "command": "bun",
        "args": ["run", "/path/to/openpets/src/mcp-server.ts"]
      }
    }
  }${RESET}

  ${GREEN}${BOLD}Source: https://github.com/alvinunreal/openpets${RESET}
`);
}

main().catch(console.error);
