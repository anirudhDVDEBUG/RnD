# How to Use web-researcher-mcp

## Install

### Option A: Docker (recommended)

```bash
git clone https://github.com/zoharbabin/web-researcher-mcp.git
cd web-researcher-mcp
docker build -t web-researcher-mcp .
```

### Option B: Build from source (requires Go 1.21+)

```bash
git clone https://github.com/zoharbabin/web-researcher-mcp.git
cd web-researcher-mcp
go build -o web-researcher-mcp .
```

## Get a search API key

Sign up for a **Brave Search API** key at <https://brave.com/search/api/> (free tier available).
Alternatively, point at a self-hosted **SearXNG** instance.

## MCP config -- paste into `~/.claude.json`

Add this block inside the `"mcpServers"` object:

```json
{
  "mcpServers": {
    "web-researcher": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "BRAVE_API_KEY",
        "web-researcher-mcp"
      ],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY_HERE"
      }
    }
  }
}
```

If you built from source instead of Docker:

```json
{
  "mcpServers": {
    "web-researcher": {
      "command": "/path/to/web-researcher-mcp",
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY_HERE"
      }
    }
  }
}
```

### Claude Code one-liner

```bash
claude mcp add web-researcher -- docker run -i --rm -e BRAVE_API_KEY=YOUR_KEY web-researcher-mcp
```

### Environment variables

| Variable | Description | Required |
|---|---|---|
| `BRAVE_API_KEY` | Brave Search API key | Yes (if using Brave) |
| `SEARXNG_BASE_URL` | SearXNG instance URL (e.g. `http://localhost:8080`) | Yes (if using SearXNG) |

## First 60 seconds

1. **Add the MCP server** using one of the config snippets above.
2. **Restart Claude Desktop / Claude Code** so it picks up the new server.
3. **Try a query:**

```
You: Search the web for "solid-state battery breakthroughs 2026"
```

Claude calls `web_search` and returns something like:

```
Results (Brave Search, 5 hits):

1. "QuantumScape Ships First Solid-State Cells to VW"
   URL: https://example.com/quantumscape-vw
   Snippet: QuantumScape announced shipment of its first commercial
   solid-state lithium-metal battery cells...

2. "Toyota Reveals 900-Mile Solid-State EV Battery"
   URL: https://example.com/toyota-solid-state
   Snippet: Toyota's prototype solid-state battery achieves 900 miles
   on a single charge with 10-minute fast charging...
```

4. **Extract full content from a URL:**

```
You: Extract the content from https://example.com/quantumscape-vw
```

Claude calls `extract_content` and returns cleaned, structured text.

5. **Specialized searches:**

```
You: Search academic papers about "solid-state electrolyte interfaces"
You: Search patents related to "lithium metal anode protection"
You: Search recent news about "battery technology startups"
```

## Available MCP tools

| Tool | Purpose |
|------|---------|
| `web_search` | General web search via Brave or SearXNG |
| `extract_content` | Scrape + clean content from any URL (4-tier) |
| `academic_search` | Scholarly papers and citations |
| `patent_search` | Patent and patent-application search |
| `news_search` | Recent news articles |
| `search_lenses` | Domain-specific search filters |
