# Technical Details — Kagi Session MCP Server

## What it does

This MCP server bridges Kagi's web-facing search and summarizer with any MCP-compatible client. Instead of requiring a paid Kagi API key ($25/mo minimum), it authenticates via your browser's `kagi_session` cookie — the same session token your browser uses when you search on kagi.com. The server exposes two MCP tools (`kagi_search` and `kagi_summarize`) over stdio JSON-RPC, conforming to the Model Context Protocol spec (2024-11-05).

When invoked by a Claude agent or other MCP client, the server forwards the request to Kagi's web endpoints with the session cookie attached, parses the JSON response, and returns structured results. When no session token is set, it falls back to mock data for testing and evaluation.

## Architecture

```
MCP Client (Claude Desktop / Cursor / Claude Code)
  |
  |  stdio (JSON-RPC, Content-Length framed)
  v
server.py
  |-- read_message() / send_message()   # MCP transport
  |-- handle_tool_call()                 # tool dispatch
  |-- kagi_search()                      # GET kagi.com/search?q=...
  |-- kagi_summarize()                   # POST kagi.com/mother/summary_labs
  |
  v
Kagi Web Endpoints (authenticated via Cookie header)
```

### Key files

| File | Purpose |
|------|---------|
| `server.py` | Complete MCP server — transport, tool definitions, Kagi API calls, mock data |
| `run.sh` | One-command demo runner |
| `requirements.txt` | Declares zero external deps (stdlib only) |

### Data flow

1. MCP client sends `tools/list` → server returns tool schemas
2. MCP client sends `tools/call` with tool name + arguments
3. Server calls Kagi's web endpoint with session cookie in `Cookie` header
4. Server parses response JSON, formats text, returns via MCP `content` array
5. Client displays results to user

### Dependencies

- **Python 3.10+** — uses stdlib only (`json`, `urllib.request`, `os`, `sys`)
- **No pip packages** — zero install friction
- The upstream repo (KSroido/Kagi-Session2API-MCP) may use `httpx` or `requests`; this prototype uses `urllib` for portability

## Limitations

- **Session tokens expire.** Kagi session cookies typically last days to weeks, but you'll need to re-extract from your browser periodically. There's no refresh mechanism.
- **No official API.** This uses Kagi's web endpoints, not a documented REST API. Endpoint URLs or response formats could change without notice.
- **Rate limits unknown.** Kagi may throttle or block automated requests from a session token. Heavy use could trigger CAPTCHAs or session invalidation.
- **Search results format is approximate.** Kagi's web search doesn't return clean JSON via a public endpoint — the upstream project reverse-engineers the response structure.
- **Single-user only.** One session token = one Kagi account. Not suitable for multi-tenant deployments.
- **Terms of service.** Automated use of Kagi via session cookies may violate their ToS. Check before relying on this in production.

## Why it matters

For teams building Claude-driven products:

- **Lead-gen and marketing agents** can search the web for prospects, competitors, and market data through Kagi's ad-free, high-quality results — avoiding the SEO spam that pollutes Google results.
- **Research agents** get Kagi's summarizer as a tool, condensing long articles or documentation into actionable briefs without leaving the agent loop.
- **Cost reduction** — Kagi API keys start at $25/mo for 1,000 searches. Session-based access piggybacks on existing $10/mo Kagi subscriptions with no per-query billing.
- **Zero-dependency MCP server** pattern — this prototype demonstrates how to build an MCP server in pure Python stdlib, useful as a template for wrapping any web service as an MCP tool.

## References

- Source: [KSroido/Kagi-Session2API-MCP](https://github.com/KSroido/Kagi-Session2API-MCP)
- MCP spec: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- Kagi: [kagi.com](https://kagi.com)
