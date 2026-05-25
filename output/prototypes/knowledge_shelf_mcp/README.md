# Knowledge Shelf MCP — Evaluation Prototype

**A local-first knowledge management MCP server that lets AI coding assistants pull documentation, code patterns, templates, and workflows on demand — keeping context windows lean and answers grounded.**

## Headline Result

```
> node demo_client.mjs
Connected to knowledge-shelf MCP server.
Available tools: search_items, get_item, list_items, add_item, ...
Calling "search_items" with query "error handling" ...
  Found: API Error Handling Pattern (api-error-handling)
```

Your AI assistant gets a **personal knowledge base** it can query mid-conversation — no vector DB, no cloud sync, just files on disk exposed via MCP.

## Quick Links

| Doc | What it covers |
|-----|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, configure for Claude Code, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, strategic fit |

## Run the Demo

```bash
bash run.sh
```

No API keys needed. The demo populates sample knowledge items (code patterns, workflows, templates) and exercises the MCP server's tools.
