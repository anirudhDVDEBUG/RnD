---
name: second_brain_cloudflare_mcp
description: |
  Deploy and configure a personal memory layer MCP server on Cloudflare Workers with semantic search.
  TRIGGER when: user wants to set up a "second brain", deploy an MCP memory server on Cloudflare, add semantic search to Claude via Cloudflare Workers, or configure a personal knowledge management MCP server.
  DO NOT TRIGGER when: user is working with other MCP servers, non-Cloudflare deployments, or unrelated memory/RAG systems.
---

# Second Brain on Cloudflare Workers

Deploy a self-hosted MCP server on Cloudflare Workers that gives Claude a persistent personal memory layer with semantic search. Uses Cloudflare D1 for storage and Vectorize for embeddings.

## When to use

- "Set up a second brain MCP server on Cloudflare"
- "I want Claude to remember things across sessions using Cloudflare Workers"
- "Deploy a personal knowledge base with semantic search as an MCP server"
- "Configure a memory layer MCP server for Claude Desktop/Code"
- "Help me set up RAG with Cloudflare D1 and Vectorize"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/rahilp/second-brain-cloudflare.git
cd second-brain-cloudflare
npm install
```

### 2. Configure Cloudflare resources

Create the required Cloudflare resources:

```bash
# Create D1 database
npx wrangler d1 create second-brain-db

# Create Vectorize index (1536 dimensions for OpenAI embeddings)
npx wrangler vectorize create second-brain-index --dimensions=1536 --metric=cosine
```

Update `wrangler.toml` with the database ID and index name from the output above.

### 3. Set up the database schema

```bash
npx wrangler d1 execute second-brain-db --file=./schema.sql
```

### 4. Configure secrets

```bash
# Set your OpenAI API key for embeddings
npx wrangler secret put OPENAI_API_KEY

# Set an auth token to secure your MCP server
npx wrangler secret put AUTH_TOKEN
```

### 5. Deploy

```bash
npx wrangler deploy
```

### 6. Connect to Claude

Add the MCP server to your Claude configuration:

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "second-brain": {
      "url": "https://your-worker.your-subdomain.workers.dev/sse",
      "headers": {
        "Authorization": "Bearer YOUR_AUTH_TOKEN"
      }
    }
  }
}
```

**Claude Code** (`.claude/settings.json`):
```json
{
  "mcpServers": {
    "second-brain": {
      "url": "https://your-worker.your-subdomain.workers.dev/sse",
      "headers": {
        "Authorization": "Bearer YOUR_AUTH_TOKEN"
      }
    }
  }
}
```

### 7. Available MCP tools

Once connected, Claude has access to:

- **remember** — Store a memory with optional tags and metadata
- **recall** — Semantic search across stored memories
- **forget** — Delete a specific memory by ID
- **list_memories** — List all stored memories with optional filtering

### Key architecture

- **Cloudflare Workers** — Serverless compute, globally distributed
- **D1** — SQLite-compatible database for structured memory storage
- **Vectorize** — Vector database for semantic similarity search
- **OpenAI Embeddings** — Generates vector representations of memories

## References

- Source: https://github.com/rahilp/second-brain-cloudflare
- Cloudflare Workers docs: https://developers.cloudflare.com/workers/
- MCP specification: https://modelcontextprotocol.io/
