---
name: mcp_deepcontext_semantic_search
description: |
  Set up and use the mcp-deepcontext MCP server for symbol-aware semantic search in Claude Code.
  TRIGGER when: user wants semantic code search, symbol-aware search, deep context search across a codebase, or asks about mcp-deepcontext.
  DO NOT TRIGGER when: user wants simple grep/ripgrep text search, file globbing, or basic find operations.
---

# MCP DeepContext — Symbol-Aware Semantic Search

An MCP server that enables symbol-aware semantic search within Claude Code, allowing you to search across codebases by meaning rather than just text matching.

## When to use

- "Set up semantic search for my codebase"
- "I want to search my code by meaning, not just text"
- "Install mcp-deepcontext for symbol-aware search"
- "Find all functions related to authentication using semantic search"
- "Configure deep context search in Claude Code"

## How to use

### 1. Prerequisites

- **Node.js** >= 18
- **Claude Code** with MCP server support enabled

### 2. Install the MCP server

Add `mcp-deepcontext` to your Claude Code MCP configuration. Run:

```bash
claude mcp add deepcontext -- npx -y @jmerelnyc/mcp-deepcontext
```

Or manually add to your `.claude/settings.json` or `.mcp.json`:

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

### 3. Index your project

Once the MCP server is running, index your codebase so semantic search has data to work with. The server will typically auto-index on first query or expose an indexing tool.

### 4. Use semantic search

The MCP server exposes tools for:

- **Semantic search** — find code by meaning (e.g., "authentication middleware" finds relevant handlers even if they don't contain those exact words)
- **Symbol search** — look up functions, classes, variables, and types by name or semantic similarity
- **Context retrieval** — get surrounding context for matched symbols including definitions, references, and call sites

### 5. Example queries

Once configured, you can ask Claude Code things like:

- "Search for code that handles user session management"
- "Find all symbols related to database connection pooling"
- "What functions deal with rate limiting?"

Claude Code will automatically use the deepcontext MCP tools to perform symbol-aware semantic search rather than plain text matching.

### 6. Supported languages

The server is built in TypeScript and uses code analysis to extract symbols. It supports TypeScript, JavaScript, and potentially other languages through tree-sitter parsing.

## References

- **Source repository**: https://github.com/jmerelnyc/mcp-deepcontext
- **Topics**: semantic-search, mcp-server, code-analysis, symbol-search, TypeScript
