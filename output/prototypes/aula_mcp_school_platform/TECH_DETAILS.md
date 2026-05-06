# Technical Details: Aula MCP School Platform

## What It Does

This is a Model Context Protocol (MCP) server that authenticates against Denmark's Aula school platform using native TypeScript HTTP requests for MitID login (no Selenium/Puppeteer). Once authenticated, it exposes four read-only tools — profiles, calendar, messages, and ugeplaner (weekly plans) — that any MCP-compatible AI client can call. The server maintains session cookies and handles token refresh transparently.

## Architecture

```
Claude Desktop / Cursor / AI Client
        |
        | (MCP stdio protocol)
        v
+------------------+
|  aula-mcp server |  (Bun + Hono framework)
|                  |
|  - MCP handler   |  Parses tool calls, returns JSON
|  - Auth module   |  MitID login flow via HTTP (no browser)
|  - API client    |  Calls Aula REST endpoints
+------------------+
        |
        | (HTTPS)
        v
   Aula Platform API
   (aula.dk backend)
```

### Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | MCP server entry point, tool registration |
| `src/auth.ts` | MitID authentication flow (HTTP-based) |
| `src/api.ts` | Aula API client (profiles, calendar, messages, ugeplaner) |
| `src/types.ts` | TypeScript interfaces for Aula data |
| `.env` | Credentials (not committed) |

### Data Flow

1. MCP client sends a `tools/call` request (e.g., `get_messages`)
2. Server checks session validity; re-authenticates if expired
3. Server calls Aula's REST API with session cookies
4. Response is parsed, formatted as MCP tool result (JSON)
5. Client receives structured data for LLM consumption

### Dependencies

- **Bun** — Runtime and package manager
- **Hono** — Lightweight web framework (used for request handling patterns)
- **@modelcontextprotocol/sdk** — Official MCP SDK for tool/resource registration
- No headless browser dependencies (Puppeteer, Playwright, etc.)

## Limitations

- **Read-only**: Cannot send messages, create events, or modify data on Aula
- **MitID changes**: If Aula/MitID updates their auth flow, the HTTP-based login may break until updated
- **Single household**: Designed for one set of credentials at a time
- **No push notifications**: Polling only — no real-time updates
- **Danish only**: Aula is Denmark-specific; data returned in Danish
- **Rate limits**: Aula may throttle frequent API calls; no built-in retry/backoff

## Why This Matters for Claude-Driven Products

- **Agent factories**: Template for building MCP servers that authenticate against national platforms (school, health, tax) without browser automation — a pattern applicable to any country's gov-tech APIs.
- **Lead-gen / marketing**: Agencies serving Danish families or schools could build notification summaries, auto-translated parent updates, or school-event-driven ad triggers.
- **Voice AI**: A voice assistant that reads out the weekly plan at breakfast — "Hey Claude, what's on Magnus's schedule today?" — using this MCP as the data source.
- **Multi-agent orchestration**: Combine with a calendar MCP and a todo MCP to auto-schedule pickup times, pack-list reminders, or homework follow-ups.
