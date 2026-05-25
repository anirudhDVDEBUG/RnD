# How to Use Knowledge Shelf MCP

## Install

```bash
# Option A: Global install
npm install -g knowledge-shelf

# Option B: Use npx (no install needed)
npx knowledge-shelf
```

Requirements: Node.js 18+.

## Configure as MCP Server for Claude Code

Add the following to your `~/.claude.json` (global) or `.claude/settings.json` (project-level) in the `mcpServers` block:

```json
{
  "mcpServers": {
    "knowledge-shelf": {
      "command": "npx",
      "args": ["-y", "knowledge-shelf"],
      "type": "stdio"
    }
  }
}
```

After saving, restart Claude Code. The server will appear in your MCP connections.

## First 60 Seconds

### 1. Run the demo (no API keys needed)

```bash
cd knowledge_shelf_mcp
bash run.sh
```

**What happens:**
- Installs the `@modelcontextprotocol/sdk` dependency
- Spawns `knowledge-shelf` as an MCP server via `npx`
- Populates 5 sample knowledge items (code patterns, workflows, templates)
- Exercises the server's tools: list, search, and read items

**Expected output:**
```
=== Setting up Knowledge Shelf with sample items ===
Connected to knowledge-shelf MCP server.
Available tools: search_items, get_item, list_items, add_item, ...
  Adding: "API Error Handling Pattern" ... -> OK
  Adding: "Docker Compose PostgreSQL Setup" ... -> OK
  ...

============================================================
  1. Available MCP Tools
============================================================
  [tool] search_items
         Search knowledge items by query
         params: query
  [tool] get_item
         ...
```

### 2. Use from Claude Code

Once configured, ask Claude Code things like:

- *"Search my knowledge shelf for error handling patterns"*
- *"What Docker Compose templates do I have saved?"*
- *"Add this deployment checklist to my knowledge shelf"*

Claude will call the MCP tools to search, read, create, and manage your knowledge items — without you needing to paste anything into the prompt.

### 3. Populate your own knowledge

Add items covering:
- **Code patterns** — reusable snippets, design patterns, idioms
- **Documentation** — API references, architecture notes, internal docs
- **Templates** — project scaffolding, boilerplate, config files
- **Workflows** — deployment checklists, runbooks, review procedures

## File / Directory Structure

Knowledge Shelf stores items on your local filesystem. Default location is typically `~/.knowledge-shelf/` or a directory configured via environment variables. Each item is a structured document with:
- A unique name/key
- Title and content (Markdown)
- Optional tags for search/filtering

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `npx knowledge-shelf` hangs | Ensure Node 18+ is installed; try `npm install -g knowledge-shelf` instead |
| Claude Code doesn't see the server | Restart Claude Code after editing `~/.claude.json`; check `mcpServers` JSON syntax |
| Tools not found | Run `bash run.sh` to verify the server starts and exposes tools |
| Items not persisting | Check filesystem permissions for the knowledge shelf data directory |
