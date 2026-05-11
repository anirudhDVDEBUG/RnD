/**
 * MCP-compatible Second Brain server.
 * Communicates via JSON-RPC over stdin/stdout (stdio transport).
 *
 * In production this runs on Cloudflare Workers with D1 + Vectorize.
 * This local version uses better-sqlite3 + mock embeddings so it works
 * without any API keys.
 *
 * Exposes four MCP tools: remember, recall, forget, list_memories.
 */

import { MemoryStore } from "./db.js";
import { createInterface } from "readline";

const store = new MemoryStore();

// ── MCP tool definitions ────────────────────────────────────────────

const TOOLS = [
  {
    name: "remember",
    description:
      "Store a memory with optional tags and metadata. The memory will be embedded for later semantic search.",
    inputSchema: {
      type: "object",
      properties: {
        content: { type: "string", description: "The text to remember" },
        tags: {
          type: "array",
          items: { type: "string" },
          description: "Optional tags for categorization",
        },
        metadata: {
          type: "object",
          description: "Optional key-value metadata",
        },
      },
      required: ["content"],
    },
  },
  {
    name: "recall",
    description:
      "Semantic search across stored memories. Returns the top-K most relevant results.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
        top_k: {
          type: "number",
          description: "Max results (default 5)",
          default: 5,
        },
      },
      required: ["query"],
    },
  },
  {
    name: "forget",
    description: "Delete a specific memory by its ID.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "number", description: "Memory ID to delete" },
      },
      required: ["id"],
    },
  },
  {
    name: "list_memories",
    description: "List stored memories with optional tag filtering.",
    inputSchema: {
      type: "object",
      properties: {
        tag: { type: "string", description: "Filter by tag" },
        limit: { type: "number", description: "Max results", default: 20 },
      },
    },
  },
];

// ── JSON-RPC handler ────────────────────────────────────────────────

function handleRequest(req) {
  const { method, params, id } = req;

  switch (method) {
    case "initialize":
      return {
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: "2024-11-05",
          capabilities: { tools: {} },
          serverInfo: {
            name: "second-brain",
            version: "1.0.0",
          },
        },
      };

    case "notifications/initialized":
      return null; // no response needed

    case "tools/list":
      return { jsonrpc: "2.0", id, result: { tools: TOOLS } };

    case "tools/call": {
      const { name, arguments: args } = params;
      let result;

      switch (name) {
        case "remember":
          result = store.remember(args);
          break;
        case "recall":
          result = store.recall(args.query, args.top_k);
          break;
        case "forget":
          result = store.forget(args.id);
          break;
        case "list_memories":
          result = store.listMemories(args);
          break;
        default:
          return {
            jsonrpc: "2.0",
            id,
            error: { code: -32601, message: `Unknown tool: ${name}` },
          };
      }

      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        },
      };
    }

    default:
      return {
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method not found: ${method}` },
      };
  }
}

// ── stdio transport ─────────────────────────────────────────────────

const rl = createInterface({ input: process.stdin });

rl.on("line", (line) => {
  try {
    const req = JSON.parse(line);
    const res = handleRequest(req);
    if (res) {
      process.stdout.write(JSON.stringify(res) + "\n");
    }
  } catch (err) {
    const errRes = {
      jsonrpc: "2.0",
      id: null,
      error: { code: -32700, message: "Parse error" },
    };
    process.stdout.write(JSON.stringify(errRes) + "\n");
  }
});

process.stderr.write("Second Brain MCP server running on stdio\n");
