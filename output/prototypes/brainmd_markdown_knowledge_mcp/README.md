# brain.md — Local-First Markdown Knowledge Base with MCP Server

**TL;DR:** brain.md is a local-first markdown notes system that ships as a single Bun binary and exposes 16 MCP tools + 2 resources. Point it at a folder of `.md` files and get semantic vector search (LanceDB), per-folder permissions, and full CRUD — accessible from Claude Code, Claude Desktop, Cursor, or any MCP client.

## Headline Result

```
MCP Tool Call: brain_search
params: {"query": "vector embeddings local search", "top_k": 3}
result [OK]:
  1. projects/vector-search-notes.md  (score: 0.82)
  2. projects/api-design.md            (score: 0.15)
```

Semantic search across your entire markdown vault, running locally with sub-100ms latency — no API keys, no cloud.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure MCP, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **[run.sh](run.sh)** — `bash run.sh` to see the demo immediately (no install needed)
- **[Source repo](https://github.com/mi4uu/brain.md)** — AGPL, requires Bun
