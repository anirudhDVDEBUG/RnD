# Technical Details -- web-researcher-mcp

## What it does

web-researcher-mcp is a single Go binary (or Docker container) that speaks the Model Context Protocol (MCP) over stdio. It exposes six tools -- `web_search`, `extract_content`, `academic_search`, `patent_search`, `news_search`, and `search_lenses` -- that any MCP-compatible AI client (Claude Desktop, Claude Code, Cursor) can call. Under the hood it routes search queries to one or more providers (Brave Search API, self-hosted SearXNG) and extracts page content through a 4-tier scraping pipeline that progressively escalates from a simple HTTP fetch to headless-browser rendering when simpler methods fail.

The server is stateless: each tool call is independent, making it safe to run as a short-lived Docker container spawned per-session by the MCP client.

## Architecture

```
MCP Client (Claude)
    |  stdio (JSON-RPC)
    v
web-researcher-mcp (Go binary)
    |
    +-- Search Router
    |     +-- Brave Search API
    |     +-- SearXNG (self-hosted)
    |
    +-- Content Extractor (4-tier)
    |     Tier 1: Raw HTTP GET + HTML parse
    |     Tier 2: Readability-style extraction
    |     Tier 3: Headless browser render
    |     Tier 4: Fallback / cached snapshot
    |
    +-- Search Lenses
          Academic, Patent, News filters
```

### Key source files (upstream repo)

| File | Role |
|------|------|
| `main.go` | Entry point, MCP stdio transport |
| `server.go` | Tool registration and dispatch |
| `search.go` | Multi-provider search routing |
| `extract.go` | 4-tier content extraction pipeline |
| `providers/brave.go` | Brave Search API client |
| `providers/searxng.go` | SearXNG client |
| `Dockerfile` | Multi-stage build |

### Dependencies

- **Go 1.21+** (build-time)
- **Brave Search API** or **SearXNG** (runtime, at least one required)
- No database, no persistent state, no GPU

### Data flow

1. MCP client sends a JSON-RPC `tools/call` request over stdin.
2. Server parses the tool name and arguments.
3. For search tools: query is forwarded to the configured provider(s), results are normalized into a common schema.
4. For `extract_content`: the URL is fetched through progressively aggressive tiers until clean text is obtained.
5. Structured JSON result is written to stdout.

## Limitations

- **Requires an API key or self-hosted SearXNG.** There is no built-in free search fallback.
- **Rate limits** are inherited from the upstream search provider (Brave free tier: 1 req/sec, 2000/month).
- **Headless browser tier** (Tier 3) requires a Chromium install inside the Docker image, which increases image size (~400 MB).
- **No caching.** Identical queries hit the provider every time.
- **No authentication/authorization.** The server trusts its MCP client completely -- do not expose it over a network without a wrapper.
- **Academic and patent search** quality depends on the provider; Brave's coverage of academic content is narrower than dedicated APIs like Semantic Scholar or Google Patents.

## Why it matters for Claude-driven products

| Use case | How this helps |
|----------|---------------|
| **Lead-gen / sales intelligence** | Let Claude research prospects, extract company pages, and summarize competitive positioning -- all inside a single conversation. |
| **Marketing / content** | Feed Claude real-time search results and extracted articles as context for drafting blog posts, briefs, or ad copy grounded in current data. |
| **Agent factories** | Drop this MCP server into any agent pipeline that needs web access -- one Docker container, zero browser automation code. |
| **Ad creatives** | Search competitor ads, extract landing page copy, feed it to Claude for differentiation analysis. |
| **Voice AI** | Give a voice agent the ability to "look something up" mid-conversation by calling `web_search` through the MCP bridge. |
