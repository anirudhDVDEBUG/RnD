# Technical Details

## What it does

Second Brain Cloudflare is a self-hosted MCP (Model Context Protocol) server that gives Claude persistent memory across sessions. When you tell Claude to "remember" something, the server stores the text in a D1 database and generates a vector embedding for it. When you later ask Claude to "recall" a topic, the server performs a cosine-similarity search over all stored embeddings and returns the most relevant memories. This creates a personal RAG (Retrieval-Augmented Generation) layer that turns Claude into a stateful assistant with long-term memory.

The local demo in this repo replaces the cloud dependencies with `better-sqlite3` and hash-based mock embeddings, so you can evaluate the full tool API without API keys or a Cloudflare account.

## Architecture

### Production stack (Cloudflare Workers)

```
Claude  --[MCP/SSE]--> Cloudflare Worker
                            |
                   +--------+--------+
                   |                 |
              D1 (SQLite)     Vectorize
              (raw text,      (1536-dim
               tags,           cosine
               metadata)       index)
                   |                 |
                   +--------+--------+
                            |
                   OpenAI Embeddings API
                   (text-embedding-ada-002)
```

### Key files (upstream repo)

| File | Role |
|------|------|
| `src/index.ts` | Worker entry point, MCP router, JSON-RPC handler |
| `schema.sql` | D1 table definition for memories |
| `wrangler.toml` | Worker config — binds D1 database and Vectorize index |

### Key files (this demo)

| File | Role |
|------|------|
| `src/server.js` | MCP stdio server — reads JSON-RPC from stdin, responds on stdout |
| `src/db.js` | MemoryStore class backed by better-sqlite3 |
| `src/embeddings.js` | Mock embedding generator (64-dim hash vectors) |
| `src/demo.js` | End-to-end demonstration of all four tools |

### Data flow

1. **remember**: text -> generate embedding -> INSERT into SQLite + store vector
2. **recall**: query text -> generate query embedding -> compare against all stored vectors (brute-force cosine similarity) -> return top-K
3. **forget**: DELETE by ID
4. **list_memories**: SELECT with optional tag filter

### Dependencies

- **Production**: Cloudflare Workers, D1, Vectorize, OpenAI API (embeddings)
- **Local demo**: Node.js 18+, `better-sqlite3` (zero external API calls)

## Limitations

- **Mock embeddings are not semantic.** The local demo uses hash-based vectors that approximate word overlap, not true meaning. Production uses OpenAI `text-embedding-ada-002` for real semantic understanding.
- **Brute-force search.** The local demo compares the query against every stored memory. Fine for hundreds of memories; would not scale to millions. Production Vectorize uses approximate nearest neighbor (ANN) search.
- **No chunking or document splitting.** Each memory is stored as a single unit. Long documents should be split before storing.
- **Requires OpenAI API key in production.** The embedding step depends on OpenAI. You could swap in Cloudflare Workers AI embeddings (`@cf/baai/bge-base-en-v1.5`) to stay fully within Cloudflare's ecosystem.
- **Single-user design.** No multi-tenancy or user isolation. The auth token secures the endpoint but doesn't distinguish between users.
- **No memory deduplication.** Storing the same content twice creates two entries.

## Why it matters

For teams building Claude-driven products (lead-gen bots, marketing agents, ad-creative pipelines, voice AI):

- **Session persistence**: Agents can accumulate knowledge over days/weeks without re-prompting. A lead-gen agent remembers past conversations with each prospect.
- **Shared team memory**: Multiple Claude instances can read/write to the same memory layer — useful for agent factories where specialized agents need shared context.
- **Cost-effective RAG**: D1 and Vectorize are included in Cloudflare's free/cheap tiers. Cheaper than running a dedicated vector DB for lightweight use cases.
- **Edge latency**: Workers run in 300+ locations. Memory recalls add ~50ms, not 500ms.
- **Composable with other MCP tools**: The memory layer stacks with other MCP servers (web search, CRM, analytics) to build more capable agent workflows.
