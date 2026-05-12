# Technical Details — capsulemcp

## What it does

capsulemcp is a Node.js MCP (Model Context Protocol) server that wraps the [Capsule CRM v2 REST API](https://developer.capsulecrm.com/). It runs locally via `npx` and exposes Capsule CRM operations as MCP tools that Claude can call during conversation. The server handles authentication, request formatting, pagination, and error mapping so that Claude can interact with CRM data using simple tool calls rather than raw HTTP.

When launched with `--read-only`, the server registers only read tools (list/get), omitting create/update/delete operations entirely — this isn't just a permission check, the tools are never registered, so Claude can't even attempt writes.

## Architecture

```
User prompt
  → Claude (decides to query CRM)
    → MCP tool call (e.g. list_opportunities)
      → capsulemcp server (local Node.js process)
        → Capsule CRM REST API (https://api.capsulecrm.com/api/v2/*)
          → JSON response
        ← parsed + formatted result
      ← MCP tool response
    ← Claude incorporates data into reply
  ← User sees CRM data in conversation
```

### Key components

- **MCP server entry point** — registers tools with the MCP SDK, handles stdio transport
- **Capsule API client** — thin HTTP wrapper around Capsule v2 endpoints, uses Bearer token auth
- **Tool definitions** — each CRM operation (list_parties, create_task, etc.) is a separate tool with typed input schemas
- **Read-only gate** — `--read-only` flag filters which tools get registered at startup

### Dependencies

- `@anthropic-ai/sdk` — MCP server SDK for tool registration and stdio transport
- `node-fetch` or Node built-in `fetch` — HTTP calls to Capsule API
- No database, no background processes, no Docker required

## Limitations

- **Capsule CRM only** — does not work with Salesforce, HubSpot, or other CRMs.
- **No bulk operations** — designed for conversational use (single-record creates/updates), not batch imports.
- **No webhook support** — Claude can query CRM state but won't be notified of changes.
- **No offline cache** — every tool call hits the live Capsule API; latency depends on Capsule's servers.
- **API rate limits** — Capsule enforces rate limits (typically 4,000 requests/hour); heavy conversational use is unlikely to hit this, but automated loops could.
- **No custom field creation** — can read and write custom field values but cannot define new custom field schemas.
- **Single-user auth** — the API token is tied to one Capsule user's permissions; it sees what that user sees.

## What it does NOT do

- Does not sync data bidirectionally or maintain local state.
- Does not provide analytics, dashboards, or reporting beyond raw data retrieval.
- Does not handle file attachments or email integration.
- Does not manage Capsule billing, user accounts, or admin settings.

## Why it matters

For teams building Claude-driven products:

- **Lead-gen / sales agents** — Claude can qualify leads, update deal stages, and create follow-up tasks directly in the CRM during a conversation, closing the loop between AI analysis and CRM hygiene.
- **Marketing automation** — tag contacts by segment, pull opportunity data for personalized outreach, or audit pipeline health through natural language.
- **Agent factories** — capsulemcp demonstrates a clean pattern for wrapping any REST API as an MCP server: typed tool schemas, read-only mode, stdio transport. The same pattern applies to any SaaS with a REST API.
- **Low-friction adoption** — `npx` install with a single env var means a sales team can try it in under a minute without IT involvement. Read-only mode lowers the risk bar for initial evaluation.

## References

- [capsulemcp source](https://github.com/soil-dev/capsulemcp)
- [Capsule CRM API docs](https://developer.capsulecrm.com/)
- [MCP specification](https://modelcontextprotocol.io/)
- [Claude Code MCP setup guide](https://docs.anthropic.com/en/docs/claude-code/tutorials#set-up-model-context-protocol-mcp)
