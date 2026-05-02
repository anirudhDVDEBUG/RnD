# How to Use mcp-deepcontext

## Prerequisites

- Node.js >= 18
- Claude Code with MCP server support

## Install the MCP Server

### Option A: One-liner (recommended)

```bash
claude mcp add deepcontext -- npx -y @jmerelnyc/mcp-deepcontext
```

### Option B: Manual config

Add this to your `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "deepcontext": {
      "command": "npx",
      "args": ["-y", "@jmerelnyc/mcp-deepcontext"]
    }
  }
}
```

Or add to your project-level `.mcp.json` for per-repo config.

### Option C: Claude Code Skill

Drop the SKILL.md into your skills directory:

```bash
mkdir -p ~/.claude/skills/mcp_deepcontext_semantic_search
cp SKILL.md ~/.claude/skills/mcp_deepcontext_semantic_search/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Set up semantic search for my codebase"
- "Find all functions related to authentication using semantic search"
- "I want to search my code by meaning, not just text"
- "Configure deep context search in Claude Code"

## First 60 Seconds

1. Add the MCP server (Option A above)
2. Open Claude Code in any project
3. Ask: **"Search for code that handles user session management"**
4. Claude Code automatically calls the deepcontext MCP tools instead of grep
5. You get results ranked by semantic relevance, with symbol context

**Example interaction:**

```
You: "Find all functions related to database connection pooling"

Claude Code (using deepcontext):
  Found 3 relevant symbols:

  [function] createConnectionPool — database.ts:17
    Creates a connection pool with health-check pinging

  [function] queryWithRetry — database.ts:28
    Runs a single query with automatic retry on connection errors

  [function] withTransaction — database.ts:52
    Transaction wrapper with automatic rollback on error
```

## MCP Tools Exposed

The server registers these tools with Claude Code:

| Tool | Purpose |
|------|---------|
| `semantic_search` | Find code by meaning — returns ranked symbols with context |
| `symbol_lookup` | Look up specific functions/classes/types by name |
| `index_project` | Index or re-index the current project's source files |

## Running the Local Demo

```bash
bash run.sh
```

This runs a self-contained mock that mirrors the real server's behavior
without needing an embedding model or MCP transport. No API keys required.
