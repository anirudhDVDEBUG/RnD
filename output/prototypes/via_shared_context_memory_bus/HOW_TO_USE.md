# How to Use Via — Shared Context & Memory Bus

## Install (the real Via)

```bash
git clone https://github.com/Vektor-Memory/Via.git
cd Via
npm install
```

## Configure as MCP Server

### Claude Code

Add to `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "via": {
      "command": "node",
      "args": ["/absolute/path/to/Via/index.js"],
      "type": "stdio"
    }
  }
}
```

### Cursor / Windsurf / Other MCP Clients

Same JSON structure — add it to each tool's MCP configuration file. The key insight is that **every tool points to the same Via server data directory**, so they all share one memory/task/context store.

### This Demo (standalone, no clone needed)

This prototype includes a self-contained Via-style MCP server. To run:

```bash
bash run.sh
```

Or manually:

```bash
npm install
node demo_client.js
```

## First 60 Seconds

**What you'll see when you run `bash run.sh`:**

1. The demo spawns a Via MCP server as a child process (stdio transport)
2. A client simulates three AI tools (Claude Code, Cursor, Windsurf) all talking to the same bus
3. You see 9 MCP tools listed, then a multi-step workflow:

```
============================================================
  2. Memory Bus — Claude Code stores architectural decisions
============================================================
  Stored: arch/database
  Stored: arch/auth
  Stored: conventions/naming

============================================================
  3. Memory Bus — Cursor retrieves decisions
============================================================
  Cursor reads arch/database:
  { "found": true, "key": "arch/database",
    "value": "Using PostgreSQL with pgvector for embeddings..." }
```

4. Tasks are created by different tools and visible to all:

```
  Created task #1: Implement user registration API [claude-code]
  Created task #2: Write unit tests for auth module [cursor]
  Created task #3: Design landing page mockup [windsurf]
```

5. Context bus shows cross-tool conversation:

```
  [FINDING] claude-code: Registration endpoint is live...
  [FINDING] cursor: Found potential SQL injection...
  [QUESTION] windsurf: Should we use shadcn/ui or custom components?
  [DECISION] claude-code: Decision: Use shadcn/ui for consistency.
```

6. Final summary shows all shared state counts + persistence file.

**Total runtime: ~2 seconds. No API keys needed.**

## Using Via in Production

Once Via is configured as an MCP server for multiple tools:

| Tool action | Via MCP call | What happens |
|---|---|---|
| Store a decision | `memory_store` | Persisted, visible to all tools |
| Check past decisions | `memory_retrieve` / `memory_list` | Any tool reads any tool's memories |
| Create a task | `task_create` | Tracked across all agents |
| Update task status | `task_update` | All tools see progress |
| Share a finding | `context_push` | Real-time cross-tool context |
| Catch up on context | `context_read` | See what other tools discovered |

## MCP Tools Reference

| Tool | Parameters | Description |
|---|---|---|
| `memory_store` | `key`, `value`, `tags[]` | Store key-value in shared memory |
| `memory_retrieve` | `key` | Get value by key |
| `memory_list` | `tag?` | List all keys, optionally filtered |
| `task_create` | `title`, `description?`, `priority?`, `assignee?` | Create shared task |
| `task_update` | `task_id`, `status`, `notes?` | Update task status |
| `task_list` | `status?` | List tasks, optionally filtered |
| `context_push` | `source`, `content`, `type?` | Push to context bus |
| `context_read` | `limit?`, `source?` | Read context entries |
| `context_clear` | — | Clear context bus |
