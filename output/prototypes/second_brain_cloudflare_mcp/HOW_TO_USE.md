# How to Use

## Quick local demo (no keys needed)

```bash
cd second_brain_cloudflare_mcp
bash run.sh
```

This installs `better-sqlite3`, seeds 8 sample memories, runs semantic search queries, filters by tag, and deletes a memory — all locally with mock embeddings.

## First 60 seconds

**Input (what `run.sh` does internally):**

```
remember("Cloudflare Workers run on V8 isolates at the edge...")
remember("MCP lets AI assistants call external tools...")
recall("How does Cloudflare store vectors?")
```

**Output:**

```
[score=0.812] #4: Vectorize is Cloudflare's vector database for similarity search...
[score=0.743] #1: Cloudflare Workers run on V8 isolates at the edge...
[score=0.691] #3: D1 is Cloudflare's serverless SQLite database...
```

---

## Production deployment (Cloudflare Workers)

### 1. Clone the upstream repo

```bash
git clone https://github.com/rahilp/second-brain-cloudflare.git
cd second-brain-cloudflare
npm install
```

### 2. Create Cloudflare resources

```bash
npx wrangler d1 create second-brain-db
npx wrangler vectorize create second-brain-index --dimensions=1536 --metric=cosine
```

Copy the database ID from the output into `wrangler.toml`.

### 3. Initialize the database

```bash
npx wrangler d1 execute second-brain-db --file=./schema.sql
```

### 4. Set secrets

```bash
npx wrangler secret put OPENAI_API_KEY    # for embeddings
npx wrangler secret put AUTH_TOKEN         # to secure the endpoint
```

### 5. Deploy

```bash
npx wrangler deploy
```

Note the URL: `https://second-brain-cloudflare.<your-subdomain>.workers.dev`

---

## Connect to Claude

### Option A: Claude Code (MCP server via stdio — this demo)

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "node",
      "args": ["/absolute/path/to/second_brain_cloudflare_mcp/src/server.js"]
    }
  }
}
```

This runs the local stdio server with mock embeddings (no API keys). Good for evaluation.

### Option B: Claude Code / Claude Desktop (remote Worker)

After deploying to Cloudflare, add to your Claude config:

```json
{
  "mcpServers": {
    "second-brain": {
      "url": "https://second-brain-cloudflare.YOUR_SUBDOMAIN.workers.dev/sse",
      "headers": {
        "Authorization": "Bearer YOUR_AUTH_TOKEN"
      }
    }
  }
}
```

### Option C: As a Claude Skill

Drop the SKILL.md file into:

```
~/.claude/skills/second_brain_cloudflare_mcp/SKILL.md
```

Trigger phrases:
- "Set up a second brain MCP server on Cloudflare"
- "I want Claude to remember things across sessions"
- "Deploy a personal knowledge base with semantic search"
- "Help me set up RAG with Cloudflare D1 and Vectorize"

---

## Available MCP tools

| Tool | Description |
|------|-------------|
| `remember` | Store text with optional tags and metadata. Auto-embedded for search. |
| `recall` | Semantic search — returns top-K memories ranked by similarity. |
| `forget` | Delete a memory by ID. |
| `list_memories` | List all memories, optionally filtered by tag. |
