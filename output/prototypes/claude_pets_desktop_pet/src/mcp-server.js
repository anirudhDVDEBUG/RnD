#!/usr/bin/env node
// Minimal MCP server that exposes pet-control tools to Claude.
// In production this runs as a stdio MCP server registered in ~/.claude.json.
// This demo version prints the JSON-RPC exchange to stdout for illustration.

import { PetClient, PET_STATES } from "./pet-client.js";

const pet = new PetClient();

// MCP tool definitions that Claude can call
const TOOLS = [
  {
    name: "set_pet_status",
    description: "Set the desktop pet's current status and mood",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "string",
          enum: Object.keys(PET_STATES),
          description: "The pet state to set",
        },
        message: {
          type: "string",
          description: "Optional message to display with the pet",
        },
      },
      required: ["status"],
    },
  },
  {
    name: "get_pet_status",
    description: "Get the desktop pet's current status and activity history",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

// Simulate MCP JSON-RPC request handling
function handleRequest(method, params) {
  switch (method) {
    case "tools/list":
      return { tools: TOOLS };

    case "tools/call": {
      const { name, arguments: args } = params;
      if (name === "set_pet_status") {
        const entry = pet.updateStatus(args.status, args.message);
        return { content: [{ type: "text", text: `Pet status set to: ${args.status}` }] };
      }
      if (name === "get_pet_status") {
        const history = pet.getHistory();
        const current = history.length > 0 ? history[history.length - 1] : { state: "sleeping" };
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ current, recentHistory: history.slice(-5) }, null, 2),
            },
          ],
        };
      }
      return { error: { code: -32601, message: `Unknown tool: ${name}` } };
    }

    default:
      return { error: { code: -32601, message: `Unknown method: ${method}` } };
  }
}

// Demo: exercise the MCP tools
function runDemo() {
  console.log("=== MCP Server Tool Definitions ===\n");
  const toolList = handleRequest("tools/list", {});
  for (const tool of toolList.tools) {
    console.log(`  Tool: ${tool.name}`);
    console.log(`  Desc: ${tool.description}`);
    const states = tool.inputSchema?.properties?.status?.enum;
    if (states) {
      console.log(`  States: ${states.join(", ")}`);
    }
    console.log();
  }

  console.log("=== MCP Tool Calls (simulated) ===\n");

  handleRequest("tools/call", {
    name: "set_pet_status",
    arguments: { status: "thinking", message: "Claude is pondering your question..." },
  });

  handleRequest("tools/call", {
    name: "set_pet_status",
    arguments: { status: "success", message: "Task completed successfully!" },
  });

  console.log();
  console.log("=== Pet History via get_pet_status ===\n");
  const result = handleRequest("tools/call", {
    name: "get_pet_status",
    arguments: {},
  });
  console.log(result.content[0].text);
}

// If run directly, execute demo
runDemo();

export { handleRequest, TOOLS };
