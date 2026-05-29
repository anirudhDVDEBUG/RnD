# Technical Details — MemoryBridge

## What It Does

MemoryBridge is a lightweight MCP (Model Context Protocol) server written in TypeScript that acts as a shared memory layer across AI coding tools. When any MCP-compatible tool (Claude Code, Cursor, Windsurf, Gemini CLI, etc.) stores a memory, it gets persisted to a local JSON file. Any other MCP-compatible tool on the same machine can then retrieve that memory. The key innovation is the compact serialization format: memory retrievals cost approximately 400 tokens of context window space, compared to roughly 4,000 tokens with naive full-context approaches.

MemoryBridge solves the "re-explain your project" problem — where switching between AI tools or starting new sessions forces you to re-describe your tech stack, conventions, and decisions every time.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Claude Code │   │    Cursor    │   │   Windsurf   │
│  (MCP client)│   │  (MCP client)│   │  (MCP client)│
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │     MCP protocol (stdio)            │
       │                  │                  │
       └──────────┬───────┴──────────┬───────┘
                  │                  │
           ┌──────▼──────────────────▼──────┐
           │       MemoryBridge Server       │
           │  (npx memorybridge — Node.js)   │
           │                                 │
           │  Tools:                         │
           │   - store_memory                │
           │   - retrieve_memories           │
           │   - list_memories               │
           │   - delete_memory               │
           └────────────┬────────────────────┘
                        │
                        ▼
              ~/.memorybridge/memories.json
```

### Key Files (in the source repo)

| File | Purpose |
|------|---------|
| `src/index.ts` | MCP server entry point, tool registration |
| `src/memory-store.ts` | Memory CRUD operations, JSON persistence |
| `src/tools/` | Individual MCP tool handlers (store, retrieve, list, delete) |
| `package.json` | Dependencies: `@modelcontextprotocol/sdk` |

### Data Flow

1. AI tool sends an MCP `tool_call` request (e.g., `store_memory`) over stdio.
2. MemoryBridge server parses the request using the MCP SDK.
3. For **store**: serializes memory object (content + tags + source + timestamp) to the JSON file.
4. For **retrieve**: loads the JSON file, scores memories against the query using keyword matching and recency, returns top-N results in a compact format.
5. Response is sent back over stdio to the calling tool.

### Dependencies

- `@modelcontextprotocol/sdk` — Anthropic's MCP SDK for building MCP servers
- Node.js >= 18 (uses native `fs`, `path`, `crypto`)
- No database, no network calls, no external APIs

### Token Efficiency

The ~400 vs ~4,000 token difference comes from:
- **Compact JSON**: Only `id`, `content`, `tags`, `source`, `createdAt` fields — no verbose wrappers
- **Selective retrieval**: Returns only relevant memories (scored + ranked), not the full store
- **No redundant metadata**: No schema versions, encoding headers, or retrieval timestamps in the response

## Limitations

- **Local only**: Memories are stored in a local JSON file. No cloud sync, no team sharing.
- **No semantic search**: Retrieval uses keyword matching, not embeddings. Queries must contain words present in the stored memory.
- **Single-machine**: All tools must run on the same machine to share the memory file.
- **No encryption**: Memories are stored as plaintext JSON. Don't store secrets.
- **No conflict resolution**: Concurrent writes from multiple tools could theoretically race, though in practice MCP tool calls are sequential per-client.
- **Flat storage**: All memories go in one file. No namespacing by project — you get cross-project bleed unless you manage tags carefully.

## Why It Matters for Claude-Driven Products

- **Agent factories**: Agents that spawn sub-agents across tools (Claude Code for backend, Cursor for frontend) can share context without passing massive prompts. Cuts token costs significantly.
- **Lead-gen / marketing pipelines**: Multi-step workflows that use different AI tools at each stage (research in one, copywriting in another) keep accumulated context without token bloat.
- **Voice AI / ad creative workflows**: Any pipeline where context must survive across tool switches and sessions benefits from persistent, token-efficient memory.
- **Cost reduction**: At scale, reducing per-call context from 4,000 to 400 tokens is a direct 10x reduction in token-related costs for memory retrieval operations.
