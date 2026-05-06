#!/usr/bin/env node
// End-to-end demo: simulates a full Claude Code session with pet reactions.
// No external dependencies required.

import { PetClient } from "./pet-client.js";

const pet = new PetClient();

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  console.log("╔══════════════════════════════════════════════════════╗");
  console.log("║   Claude Pets — Desktop Pet Demo (Mock Mode)       ║");
  console.log("║   Simulating a Claude Code session with pet        ║");
  console.log("║   reactions at each lifecycle event                ║");
  console.log("╚══════════════════════════════════════════════════════╝\n");

  // --- Session Start ---
  console.log("▸ EVENT: on_session_start");
  await pet.updateStatus("sleeping", "Pet is sleeping...");
  await sleep(300);
  await pet.updateStatus("waking", "Claude Code session detected! Pet wakes up.");
  await sleep(300);
  console.log();

  // --- Simulated tool calls ---
  const toolSequence = [
    { tool: "Read",  file: "src/app.js" },
    { tool: "Grep",  query: "TODO" },
    { tool: "Agent", task: "explore codebase" },
    { tool: "Edit",  file: "src/app.js" },
    { tool: "Bash",  cmd: "npm test" },
    { tool: "Write", file: "src/utils.js" },
  ];

  console.log("▸ EVENT: on_tool_call (simulating 6 tool calls)\n");

  for (const { tool, ...details } of toolSequence) {
    const state = pet.stateForTool(tool);
    const detail = Object.values(details)[0];
    await pet.updateStatus(state, `Claude calls ${tool}: ${detail}`);
    await sleep(250);
  }

  // Success after tool calls
  console.log();
  console.log("▸ EVENT: task completed");
  await pet.updateStatus("success", "All changes applied — tests pass!");
  await sleep(300);

  // --- Session End ---
  console.log();
  console.log("▸ EVENT: on_session_end");
  await pet.updateStatus("goodbye", "Session ending — pet waves goodbye!");
  await sleep(200);
  await pet.updateStatus("sleeping", "Pet goes back to sleep. Goodnight!");

  // --- Summary ---
  console.log("\n" + "─".repeat(55));
  console.log("Activity log:");
  console.log("─".repeat(55));
  for (const entry of pet.getHistory()) {
    const t = entry.timestamp.split("T")[1].split(".")[0];
    console.log(`  ${t}  ${entry.emoji.padEnd(12)} ${entry.message}`);
  }
  console.log("─".repeat(55));
  console.log(`Total status updates: ${pet.getHistory().length}`);
  console.log();
}

main().catch(console.error);
