#!/usr/bin/env node
/**
 * via_server.js — A minimal MCP server that replicates Via's core concept:
 * a shared context, task, and memory bus that multiple AI tools can connect to.
 *
 * Exposes MCP tools for:
 *   - memory_store / memory_retrieve / memory_list   — persistent key-value memory
 *   - task_create / task_update / task_list           — shared task management
 *   - context_push / context_read / context_clear     — shared context bus
 *
 * Data is persisted to a local JSON file so it survives restarts.
 */

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require("@modelcontextprotocol/sdk/types.js");
const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Persistent store
// ---------------------------------------------------------------------------
const DATA_FILE = path.join(__dirname, ".via_data.json");

function loadData() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, "utf-8"));
  } catch {
    return { memory: {}, tasks: [], context: [] };
  }
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

let store = loadData();

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------
const TOOLS = [
  {
    name: "memory_store",
    description: "Store a key-value pair in the shared memory bus. Accessible from any connected AI tool.",
    inputSchema: {
      type: "object",
      properties: {
        key:   { type: "string", description: "Memory key" },
        value: { type: "string", description: "Value to store" },
        tags:  { type: "array", items: { type: "string" }, description: "Optional tags for categorization" },
      },
      required: ["key", "value"],
    },
  },
  {
    name: "memory_retrieve",
    description: "Retrieve a value from shared memory by key.",
    inputSchema: {
      type: "object",
      properties: {
        key: { type: "string", description: "Memory key to retrieve" },
      },
      required: ["key"],
    },
  },
  {
    name: "memory_list",
    description: "List all keys in the shared memory bus, optionally filtered by tag.",
    inputSchema: {
      type: "object",
      properties: {
        tag: { type: "string", description: "Optional tag to filter by" },
      },
    },
  },
  {
    name: "task_create",
    description: "Create a new task on the shared task bus. Visible to all connected AI tools.",
    inputSchema: {
      type: "object",
      properties: {
        title:       { type: "string", description: "Task title" },
        description: { type: "string", description: "Task description" },
        priority:    { type: "string", enum: ["low", "medium", "high"], description: "Priority level" },
        assignee:    { type: "string", description: "Which tool/agent owns this task" },
      },
      required: ["title"],
    },
  },
  {
    name: "task_update",
    description: "Update a task's status on the shared task bus.",
    inputSchema: {
      type: "object",
      properties: {
        task_id: { type: "number", description: "Task ID (1-based index)" },
        status:  { type: "string", enum: ["pending", "in_progress", "done", "blocked"], description: "New status" },
        notes:   { type: "string", description: "Optional status notes" },
      },
      required: ["task_id", "status"],
    },
  },
  {
    name: "task_list",
    description: "List all tasks on the shared task bus.",
    inputSchema: {
      type: "object",
      properties: {
        status: { type: "string", enum: ["pending", "in_progress", "done", "blocked"], description: "Filter by status" },
      },
    },
  },
  {
    name: "context_push",
    description: "Push a context entry to the shared context bus. Other tools see this immediately.",
    inputSchema: {
      type: "object",
      properties: {
        source:  { type: "string", description: "Which tool is pushing context (e.g. 'claude', 'cursor')" },
        content: { type: "string", description: "Context content" },
        type:    { type: "string", enum: ["decision", "finding", "question", "note"], description: "Context type" },
      },
      required: ["source", "content"],
    },
  },
  {
    name: "context_read",
    description: "Read the shared context bus. Returns recent context entries from all connected tools.",
    inputSchema: {
      type: "object",
      properties: {
        limit:  { type: "number", description: "Max entries to return (default 20)" },
        source: { type: "string", description: "Filter by source tool" },
      },
    },
  },
  {
    name: "context_clear",
    description: "Clear the shared context bus.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

// ---------------------------------------------------------------------------
// Tool handlers
// ---------------------------------------------------------------------------
function handleTool(name, args) {
  switch (name) {
    // -- Memory --
    case "memory_store": {
      store.memory[args.key] = {
        value: args.value,
        tags: args.tags || [],
        updated_at: new Date().toISOString(),
      };
      saveData(store);
      return { stored: true, key: args.key };
    }
    case "memory_retrieve": {
      const entry = store.memory[args.key];
      if (!entry) return { found: false, key: args.key };
      return { found: true, key: args.key, ...entry };
    }
    case "memory_list": {
      let keys = Object.keys(store.memory);
      if (args.tag) {
        keys = keys.filter((k) => (store.memory[k].tags || []).includes(args.tag));
      }
      return {
        count: keys.length,
        keys: keys.map((k) => ({
          key: k,
          tags: store.memory[k].tags,
          updated_at: store.memory[k].updated_at,
        })),
      };
    }

    // -- Tasks --
    case "task_create": {
      const task = {
        id: store.tasks.length + 1,
        title: args.title,
        description: args.description || "",
        priority: args.priority || "medium",
        status: "pending",
        assignee: args.assignee || "unassigned",
        created_at: new Date().toISOString(),
      };
      store.tasks.push(task);
      saveData(store);
      return { created: true, task };
    }
    case "task_update": {
      const task = store.tasks[args.task_id - 1];
      if (!task) return { error: `Task ${args.task_id} not found` };
      task.status = args.status;
      if (args.notes) task.notes = args.notes;
      task.updated_at = new Date().toISOString();
      saveData(store);
      return { updated: true, task };
    }
    case "task_list": {
      let tasks = store.tasks;
      if (args.status) tasks = tasks.filter((t) => t.status === args.status);
      return { count: tasks.length, tasks };
    }

    // -- Context Bus --
    case "context_push": {
      const entry = {
        id: store.context.length + 1,
        source: args.source,
        content: args.content,
        type: args.type || "note",
        timestamp: new Date().toISOString(),
      };
      store.context.push(entry);
      saveData(store);
      return { pushed: true, entry };
    }
    case "context_read": {
      let entries = store.context;
      if (args.source) entries = entries.filter((e) => e.source === args.source);
      const limit = args.limit || 20;
      entries = entries.slice(-limit);
      return { count: entries.length, entries };
    }
    case "context_clear": {
      const cleared = store.context.length;
      store.context = [];
      saveData(store);
      return { cleared, message: "Context bus cleared" };
    }

    default:
      return { error: `Unknown tool: ${name}` };
  }
}

// ---------------------------------------------------------------------------
// MCP Server wiring
// ---------------------------------------------------------------------------
async function main() {
  const server = new Server(
    { name: "via-shared-context-bus", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: TOOLS,
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const result = handleTool(name, args || {});
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  // Server is now listening on stdio
}

main().catch((err) => {
  console.error("Via server error:", err);
  process.exit(1);
});
