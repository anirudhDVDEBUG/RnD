---
name: memorybridge_cross_tool_ai_memory
description: |
  Set up and use MemoryBridge, a cross-tool AI memory MCP server that works across Claude Code, Cursor, Antigravity, Windsurf, Gemini CLI, and other MCP-compatible AI tools. Uses ~400 tokens instead of ~4,000 for efficient context management.
  Triggers: cross-tool memory, shared AI memory, MCP memory server, memorybridge, token-efficient context
---

# MemoryBridge — Cross-Tool AI Memory MCP Server

MemoryBridge is an MCP server that provides persistent, shared memory across multiple AI coding tools. It lets Claude Code, Cursor, Antigravity, Windsurf, Gemini CLI, and any MCP-compatible AI share context — using only ~400 tokens instead of ~4,000.

## When to use

- "Set up shared memory between Claude Code and Cursor"
- "I need my AI tools to share context across sessions"
- "Install memorybridge MCP server for cross-tool memory"
- "How do I persist AI memory across different coding agents?"
- "Reduce token usage for AI context with memorybridge"

## How to use

### 1. Install MemoryBridge

```bash
npx memorybridge
```

Or install globally:

```bash
npm install -g memorybridge
```

### 2. Configure as MCP Server

**For Claude Code** — add to your MCP settings (`.claude/settings.json` or project `.mcp.json`):

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

**For Cursor** — add to `.cursor/mcp.json`:

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

**For Windsurf / Antigravity / other MCP clients** — use the same server configuration pattern with `npx memorybridge`.

### 3. Use Memory Tools

Once configured, the MCP server provides tools to:

- **Store memories** — save context, decisions, and learnings that persist across sessions
- **Retrieve memories** — pull relevant context back into any MCP-compatible tool
- **Share context** — memories stored in one tool (e.g., Claude Code) are available in another (e.g., Cursor)

### 4. Token Efficiency

MemoryBridge is designed to be token-efficient, using approximately 400 tokens per memory retrieval compared to ~4,000 tokens with naive approaches. This keeps your context window lean while maintaining full memory capabilities.

## Key Features

- **Cross-tool compatibility**: Works with Claude Code, Cursor, Antigravity, Windsurf, Gemini CLI, Continue.dev, and any MCP client
- **Token-optimized**: ~400 tokens per operation instead of ~4,000
- **Persistent storage**: Memories survive across sessions and tool switches
- **TypeScript implementation**: Built in TypeScript for reliability
- **Zero config**: Run with `npx memorybridge` — no setup required

## References

- **Source**: [IamRamgarhia/memorybridge](https://github.com/IamRamgarhia/memorybridge)
- **npm**: `memorybridge`
- **License**: See repository for details
