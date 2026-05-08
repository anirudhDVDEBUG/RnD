# Technical Details – Thunderbit Web Scraper

## What it does

Thunderbit MCP Server wraps the Thunderbit Open API to provide AI-powered web scraping and structured data extraction through the Model Context Protocol. Instead of writing CSS selectors or XPath queries, you give it a URL and (optionally) a list of field names. The Thunderbit API fetches the page, runs it through an AI model that understands page semantics, and returns either clean markdown or structured JSON rows matching your requested schema.

The server exposes two MCP tools (`scrape_url` and `extract_data`) that any MCP-compatible client (Claude Desktop, Claude Code, Cursor, Windsurf) can call. It also ships a CLI for standalone use.

## Architecture

```
┌─────────────────┐      MCP / stdio       ┌──────────────────────┐
│  Claude Desktop  │◄──────────────────────►│  thunderbit-mcp-     │
│  Claude Code     │                        │  server (Node.js)    │
│  Cursor / etc.   │                        │                      │
└─────────────────┘                         │  ┌────────────────┐  │
                                            │  │ scrape_url     │  │
                                            │  │ extract_data   │  │
                                            │  └───────┬────────┘  │
                                            └──────────┼───────────┘
                                                       │ HTTPS
                                                       ▼
                                            ┌──────────────────────┐
                                            │  Thunderbit Open API │
                                            │  (cloud, AI models)  │
                                            └──────────────────────┘
```

**Key files** (in the source repo):

- `src/index.ts` – MCP server setup, tool registration, stdio transport
- `src/tools/` – Individual tool handlers for `scrape_url` and `extract_data`
- `src/api.ts` – HTTP client wrapper for the Thunderbit Open API
- `src/cli.ts` – CLI entrypoint (`scrape`, `extract` subcommands)

**Dependencies:** Node.js >= 18, `@modelcontextprotocol/sdk`, Thunderbit API client. No browser/headless Chrome — all rendering happens server-side at Thunderbit.

**Data flow:**

1. MCP client sends a tool call (e.g. `extract_data` with a URL and fields).
2. The server forwards the request to `api.thunderbit.com` with the API key.
3. Thunderbit fetches and renders the page, runs AI extraction, returns JSON.
4. The server relays structured results back to the MCP client.

## Limitations

- **Requires a Thunderbit API key** – free tier available, but rate-limited.
- **Cloud-dependent** – all scraping and AI extraction happens on Thunderbit's servers; no offline mode.
- **No JavaScript interaction** – cannot click buttons, fill forms, or navigate SPAs beyond initial page load (Thunderbit handles rendering, but the exposed tools are single-page-fetch only).
- **No pagination** – one URL per call; you'd need to loop over paginated URLs yourself.
- **Schema is best-effort** – AI extraction may miss or misinterpret fields on unusual page layouts.
- **No caching** – each call fetches the page fresh; high-frequency scraping will burn API quota.

## Why it matters for Claude-driven products

| Use case | How Thunderbit helps |
|----------|---------------------|
| **Lead generation** | Point `extract_data` at directory pages to pull company names, emails, phone numbers into a CRM pipeline. No scraper maintenance. |
| **Marketing / competitive intel** | Scrape competitor pricing, product catalogs, or blog content into structured datasets for analysis. |
| **Ad creatives** | Extract product details (images, descriptions, prices) from landing pages to auto-generate ad copy. |
| **Agent factories** | Give autonomous agents the ability to read arbitrary web pages and extract structured context — a core capability for research agents, comparison-shopping agents, or content-aggregation workflows. |
| **Content pipelines** | Convert any webpage to clean markdown for RAG ingestion, summarization, or repurposing. |

The key value is **zero-maintenance scraping**: no selectors to update when pages change, no headless browser to manage, and structured output that fits directly into downstream pipelines.
