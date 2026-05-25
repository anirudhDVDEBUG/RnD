#!/usr/bin/env node
// demo_client.mjs — Demonstrate knowledge-shelf MCP server capabilities
// Connects via stdio, lists tools/resources, and exercises search/read operations.

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

function banner(text) {
  const line = "=".repeat(60);
  console.log(`\n${line}\n  ${text}\n${line}`);
}

function printResult(result) {
  if (!result || !result.content) {
    console.log("  (no content returned)");
    return;
  }
  for (const block of result.content) {
    if (block.type === "text") {
      const lines = block.text.split("\n");
      for (const l of lines) {
        console.log("  " + l);
      }
    } else {
      console.log(`  [${block.type}]`, JSON.stringify(block).slice(0, 200));
    }
  }
}

async function main() {
  banner("Knowledge Shelf MCP — Demo Client");
  console.log("Spawning knowledge-shelf server via npx ...\n");

  const transport = new StdioClientTransport({
    command: "npx",
    args: ["-y", "knowledge-shelf"],
  });

  const client = new Client(
    { name: "demo-client", version: "1.0.0" },
    { capabilities: {} }
  );

  await client.connect(transport);
  console.log("Connected!\n");

  // ── 1. List Tools ──
  banner("1. Available MCP Tools");
  const { tools } = await client.listTools();
  if (tools.length === 0) {
    console.log("  (no tools exposed)");
  }
  for (const tool of tools) {
    console.log(`  [tool] ${tool.name}`);
    if (tool.description) {
      console.log(`         ${tool.description.slice(0, 120)}`);
    }
    if (tool.inputSchema && tool.inputSchema.properties) {
      const params = Object.keys(tool.inputSchema.properties).join(", ");
      console.log(`         params: ${params}`);
    }
    console.log();
  }

  // ── 2. List Resources ──
  banner("2. Available MCP Resources");
  try {
    const { resources } = await client.listResources();
    if (!resources || resources.length === 0) {
      console.log("  (no resources exposed)");
    } else {
      for (const r of resources) {
        console.log(`  [resource] ${r.uri}`);
        if (r.name) console.log(`             name: ${r.name}`);
        if (r.description) console.log(`             ${r.description.slice(0, 120)}`);
        console.log();
      }
    }
  } catch (e) {
    console.log(`  Resources not supported: ${e.message}`);
  }

  // ── 3. List Resource Templates ──
  banner("3. Resource Templates");
  try {
    const { resourceTemplates } = await client.listResourceTemplates();
    if (!resourceTemplates || resourceTemplates.length === 0) {
      console.log("  (no resource templates)");
    } else {
      for (const rt of resourceTemplates) {
        console.log(`  [template] ${rt.uriTemplate}`);
        if (rt.name) console.log(`             name: ${rt.name}`);
        if (rt.description) console.log(`             ${rt.description.slice(0, 120)}`);
        console.log();
      }
    }
  } catch (e) {
    console.log(`  Resource templates not supported: ${e.message}`);
  }

  // ── 4. List Prompts ──
  banner("4. Available Prompts");
  try {
    const { prompts } = await client.listPrompts();
    if (!prompts || prompts.length === 0) {
      console.log("  (no prompts exposed)");
    } else {
      for (const p of prompts) {
        console.log(`  [prompt] ${p.name}`);
        if (p.description) console.log(`           ${p.description.slice(0, 120)}`);
        console.log();
      }
    }
  } catch (e) {
    console.log(`  Prompts not supported: ${e.message}`);
  }

  // ── 5. Exercise Tools ──
  banner("5. Exercising Tools");

  const toolNames = tools.map((t) => t.name);

  // Try search/list/query tools
  const searchTool = toolNames.find((n) =>
    /search|find|query|list|browse|get_all/i.test(n)
  );
  if (searchTool) {
    console.log(`\n  Calling "${searchTool}" with query "error handling" ...`);
    try {
      const result = await client.callTool({
        name: searchTool,
        arguments: { query: "error handling" },
      });
      printResult(result);
    } catch (e) {
      // Try without arguments
      try {
        console.log(`  Retrying "${searchTool}" with no arguments ...`);
        const result = await client.callTool({
          name: searchTool,
          arguments: {},
        });
        printResult(result);
      } catch (e2) {
        console.log(`  Error: ${e2.message}`);
      }
    }
  }

  // Try get/read tools
  const readTool = toolNames.find((n) =>
    /^(get|read|fetch|load|view|show)(?!.*all)/i.test(n)
  );
  if (readTool) {
    console.log(`\n  Calling "${readTool}" ...`);
    try {
      const result = await client.callTool({
        name: readTool,
        arguments: { name: "api-error-handling" },
      });
      printResult(result);
    } catch (e) {
      try {
        const result = await client.callTool({
          name: readTool,
          arguments: { key: "api-error-handling" },
        });
        printResult(result);
      } catch (e2) {
        console.log(`  Error: ${e2.message}`);
      }
    }
  }

  // Try a list-all tool
  const listTool = toolNames.find((n) =>
    /list|all|browse|index|catalog/i.test(n)
  );
  if (listTool && listTool !== searchTool) {
    console.log(`\n  Calling "${listTool}" ...`);
    try {
      const result = await client.callTool({
        name: listTool,
        arguments: {},
      });
      printResult(result);
    } catch (e) {
      console.log(`  Error: ${e.message}`);
    }
  }

  // If no tools matched, just call each tool with empty args to show behavior
  if (!searchTool && !readTool && !listTool) {
    for (const tool of tools.slice(0, 3)) {
      console.log(`\n  Calling "${tool.name}" with empty args ...`);
      try {
        const result = await client.callTool({
          name: tool.name,
          arguments: {},
        });
        printResult(result);
      } catch (e) {
        console.log(`  Error: ${e.message}`);
      }
    }
  }

  // ── Done ──
  banner("Demo Complete");
  console.log("  Knowledge Shelf MCP server is working.");
  console.log("  See HOW_TO_USE.md for integration with Claude Code.\n");

  await client.close();
}

main().catch((err) => {
  console.error("Demo error:", err.message);
  process.exit(1);
});
