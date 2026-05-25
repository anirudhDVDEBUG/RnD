# Technical Details — Knowledge Shelf MCP

## What It Does

Knowledge Shelf is an MCP (Model Context Protocol) server that exposes a personal knowledge base to AI coding assistants. It stores documentation, code patterns, templates, and workflows as structured items on your local filesystem. When an AI assistant needs context — e.g., "how do we handle errors in this project?" — it queries the shelf via MCP tools and retrieves only the relevant items, keeping the context window efficient.

The server implements the MCP stdio transport. It registers tools for CRUD operations (add, read, update, delete items) and search/listing. The AI assistant discovers these tools at connection time and calls them as needed during a conversation.

## Architecture

```
Claude Code (or any MCP client)
       |
       | stdio (JSON-RPC over stdin/stdout)
       |
   knowledge-shelf (Node.js MCP server)
       |
       | filesystem read/write
       |
   ~/.knowledge-shelf/    (local data directory)
       ├── items/
       │   ├── api-error-handling.md
       │   ├── docker-compose-postgres.md
       │   └── ...
       └── index.json      (metadata + tags index)
```

### Key Components

| Component | Role |
|-----------|------|
| MCP Server (TypeScript) | Handles JSON-RPC messages, registers tools |
| Item Store | Reads/writes Markdown files + metadata to disk |
| Search Engine | Tag-based + text matching across stored items |
| CLI Entry Point | `npx knowledge-shelf` starts the stdio server |

### Dependencies

- **@modelcontextprotocol/sdk** — MCP server/client protocol implementation
- **TypeScript** — source language
- **Node.js 18+** — runtime

No external databases, no cloud services, no API keys.

## MCP Surface

### Tools (typical)

| Tool | Purpose |
|------|---------|
| `add_item` / `create_item` | Store a new knowledge item |
| `get_item` / `read_item` | Retrieve a specific item by name |
| `search_items` | Full-text/tag search across items |
| `list_items` | List all stored items (optionally filtered by tag) |
| `update_item` | Modify an existing item |
| `delete_item` | Remove an item |

*(Exact tool names depend on the version — the demo auto-discovers them.)*

### Resources

May expose resources for browsing the shelf contents via `resource://` URIs.

## Limitations

- **No vector/semantic search** — search is keyword/tag-based, not embedding-based. Good enough for a curated personal shelf; won't scale to thousands of unstructured docs.
- **Single-user, local only** — no multi-user collaboration, no sync, no cloud backup. This is by design (privacy-first).
- **No versioning** — items are overwritten in place. Use git on the data directory if you want history.
- **No access control** — any MCP client on the machine can read/write items.
- **Markdown only** — no binary attachments, images, or rich media.

## Why It Matters for Claude-Driven Products

| Use Case | How Knowledge Shelf Helps |
|----------|--------------------------|
| **Agent Factories** | Give each agent instance a curated knowledge base of domain patterns, reducing hallucination and prompt size |
| **Lead-Gen / Marketing** | Store proven copy templates, ad frameworks, persona docs — agents pull the right template per campaign |
| **Ad Creatives** | Maintain a shelf of brand guidelines, past winners, compliance rules that creative agents reference |
| **Voice AI** | Store conversation scripts, FAQ answers, escalation procedures for voice agent grounding |
| **Dev Tooling** | Team coding standards, architecture decisions, migration guides — always available to Claude Code without pasting |

The core value proposition: **deterministic, curated context injection** vs. hoping the model remembers or searching the web. For production agent systems, this kind of grounding layer is critical for reliability.

## Source Repository

- **GitHub**: https://github.com/joutvhu/knowledge-shelf
- **npm**: `knowledge-shelf`
- **License**: Check repository for current license
