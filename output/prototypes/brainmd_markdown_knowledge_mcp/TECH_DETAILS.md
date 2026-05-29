# Technical Details — brain.md

## What It Does

brain.md is a local-first markdown knowledge management system that exposes its full functionality through the Model Context Protocol (MCP). It runs as a single Bun (TypeScript) binary, watches a folder of markdown files, builds a LanceDB vector index for semantic search, and serves 16 tools + 2 resources over the MCP stdio transport. Any MCP-compatible client — Claude Code, Claude Desktop, Cursor, or custom agents — can create, read, update, delete, search, and organize notes without touching the filesystem directly.

The key technical differentiator is **local vector search**: brain.md generates embeddings at index time using a lightweight model bundled with LanceDB, enabling semantic similarity queries with sub-100ms latency and zero API calls. This makes it viable as an always-on second brain for AI coding agents that need to retrieve context from a personal knowledge base.

## Architecture

```
┌─────────────────┐    MCP (stdio)    ┌──────────────────────┐
│  Claude Code /   │◄────────────────►│  brain.md server     │
│  Claude Desktop  │                  │  (Bun + TypeScript)  │
│  Cursor / Agent  │                  │                      │
└─────────────────┘                  │  ┌────────────────┐  │
                                      │  │ Permission      │  │
                                      │  │ Layer           │  │
                                      │  └───────┬────────┘  │
                                      │          │           │
                                      │  ┌───────▼────────┐  │
                                      │  │ Note CRUD      │  │
                                      │  │ (fs read/write) │  │
                                      │  └───────┬────────┘  │
                                      │          │           │
                                      │  ┌───────▼────────┐  │
                                      │  │ LanceDB Vector │  │
                                      │  │ Index (local)  │  │
                                      │  └────────────────┘  │
                                      └──────────────────────┘
                                                │
                                      ┌─────────▼─────────┐
                                      │  Markdown Vault   │
                                      │  (your notes dir) │
                                      └───────────────────┘
```

### Key Files (in the source repo)

- `src/index.ts` — MCP server entry point, tool/resource registration
- `src/tools/` — Individual tool implementations (CRUD, search, tags, etc.)
- `src/vector/` — LanceDB integration, embedding generation, index management
- `src/permissions.ts` — Per-folder access control logic
- `src/config.ts` — Configuration loading (env vars, config files)

### Data Flow

1. **Startup**: Server reads `BRAIN_MD_ROOT`, scans all `.md` files, parses YAML frontmatter
2. **Indexing**: Generates embeddings for each note, stores in a local LanceDB table
3. **Tool calls**: MCP client sends JSON-RPC requests → permission check → execute → return result
4. **Search**: Query text → embedding → LanceDB nearest-neighbor lookup → ranked results
5. **Mutations**: File written to disk → vector index updated incrementally

### Dependencies

- **Runtime**: [Bun](https://bun.sh) (TypeScript runtime + package manager)
- **Vector DB**: [LanceDB](https://lancedb.com) (embedded, columnar, no separate server)
- **MCP SDK**: `@modelcontextprotocol/sdk` (stdio transport)
- **Frontmatter**: YAML parser for note metadata
- **License**: AGPL-3.0

## Limitations

- **Bun-only**: Does not run on Node.js — requires Bun runtime
- **Embedding model**: Uses a bundled lightweight model; quality may not match OpenAI/Cohere embeddings for very nuanced queries
- **No real-time sync**: File watcher detects changes, but there's a small delay before the index updates
- **No multi-user**: Designed for single-user local use; no auth/authorization beyond folder permissions
- **No cloud backup**: Purely local — you need your own sync solution (git, Syncthing, etc.)
- **AGPL license**: Copyleft — derivatives must also be AGPL, which may not suit commercial use

## Why It Matters for Claude-Driven Products

| Use Case | How brain.md Helps |
|---|---|
| **Agent factories** | Give every spawned agent a persistent, searchable memory layer without cloud infra |
| **Lead-gen / marketing** | Store research notes, competitor analysis, and content drafts in a vault that Claude can search and reference during generation |
| **Ad creatives** | Maintain a knowledge base of brand guidelines, past campaigns, and performance data that Claude retrieves via semantic search |
| **Voice AI** | Backend knowledge store for voice agents — semantic lookup of FAQs, scripts, and policies |
| **Developer tooling** | Second brain for coding agents — architecture decisions, API docs, and debugging notes always one MCP call away |

The MCP interface means any of these can be built without custom file-handling code. The agent just calls `brain_search` or `brain_read_note` and gets structured results.
