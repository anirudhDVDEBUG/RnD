#!/usr/bin/env node
// Hook: on_tool_call — updates pet status based on which tool Claude is using.
// In production, Claude Code passes the tool name via stdin JSON.
import { PetClient } from "../src/pet-client.js";

const pet = new PetClient();

// Read hook input from stdin (Claude Code sends JSON with tool_name, etc.)
let toolName = "default";
try {
  let input = "";
  for await (const chunk of process.stdin) {
    input += chunk;
  }
  if (input.trim()) {
    const data = JSON.parse(input);
    toolName = data.tool_name || "default";
  }
} catch {
  // No stdin or invalid JSON — use default
}

const state = pet.stateForTool(toolName);
await pet.updateStatus(state, `Claude is using ${toolName}`);
