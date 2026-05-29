# How to Use MemoryBridge

## Install

```bash
# Option A: run directly (recommended)
npx memorybridge

# Option B: install globally
npm install -g memorybridge
```

No build step required. The package ships as a ready-to-run MCP server.

## Configure as MCP Server

### Claude Code

Add to `~/.claude.json` (global) or project `.mcp.json`:

```json
{
  "mcpServers": {
    "memorybridge": {
      "command": "npx",
      "args": ["-y", "memorybridge"]
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "memorybridge": {
      "command": "npx",
      "args": ["-y", "memorybridge"]
    }
  }
}
```

### Windsurf / Antigravity / Gemini CLI / Continue.dev

Same pattern — point your MCP client config at `npx -y memorybridge`.

## First 60 Seconds

After adding the MCP config above and restarting your AI tool:

1. **Store a memory** (in Claude Code):
   > "Remember that this project uses Next.js 14 with App Router and Prisma for the database."

   Claude Code calls the `store_memory` MCP tool automatically.

2. **Switch to Cursor** and ask:
   > "What framework does this project use?"

   Cursor calls `retrieve_memories`, gets the answer from the shared store — no re-explaining needed.

3. **Check token usage**: Each retrieval uses ~400 tokens of context, compared to ~4,000 if you pasted the same info manually every session.

## Run the Local Demo

This repo includes a self-contained demo that simulates the cross-tool memory flow without needing any MCP client:

```bash
bash run.sh
```

The demo shows:
- Claude Code storing 3 project memories
- Cursor retrieving shared context via search
- Windsurf adding its own memory
- Token efficiency comparison (~400 vs ~4,000 tokens)
- Cross-tool search across all stored memories

## MCP Tools Provided

| Tool | Description |
|------|-------------|
| `store_memory` | Save a memory with content, tags, and source tool |
| `retrieve_memories` | Search memories by query, returns ranked results |
| `list_memories` | List all stored memories |
| `delete_memory` | Remove a memory by ID |

## Storage Location

Memories are stored as JSON in `~/.memorybridge/memories.json` by default. This single file is shared across all tools.
