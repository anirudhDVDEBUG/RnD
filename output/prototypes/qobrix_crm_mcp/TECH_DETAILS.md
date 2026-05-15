# Technical Details — Qobrix CRM MCP Server

## What it does

The Qobrix CRM MCP server wraps the Qobrix CRM REST API (v2) as a Model Context Protocol server, exposing 42 read-only tools across 13 entity groups. Each tool maps to a specific Qobrix API endpoint (e.g., `GET /contacts`, `GET /properties/{id}`), translating Qobrix's native field names into RESO Data Dictionary 2.0 canonical names before returning results to the LLM. This means Claude sees `ListPrice` instead of Qobrix's internal `listing_price`, `StandardStatus` instead of `listing_status`, etc.

The server runs as a stdio-based MCP process — Claude Desktop or Claude Code spawns it, sends JSON-RPC tool calls over stdin, and reads structured results from stdout. No HTTP server, no ports, no CORS.

## Architecture

```
Claude ←→ MCP stdio transport ←→ qobrix-crm-mcp server ←→ Qobrix REST API v2
                                        │
                                   RESO DD 2.0
                                   field mapper
```

### Key files (in the source repo)

| File | Purpose |
|------|---------|
| `src/index.ts` | MCP server entry point, tool registration |
| `src/tools/` | One file per entity group (contacts, properties, leads, etc.) |
| `src/api/client.ts` | HTTP client wrapping Qobrix REST API v2 |
| `src/mapping/reso.ts` | Field name translation: Qobrix → RESO DD 2.0 |
| `dist/index.js` | Compiled output, what you point MCP config at |

### Key files (in this demo repo)

| File | Purpose |
|------|---------|
| `mock-server.js` | MCP server with mock data (same tool interface) |
| `mock-data.js` | Sample CRM records using RESO DD 2.0 field names |
| `demo.js` | Standalone demo exercising 7 query patterns |
| `run.sh` | One-command evaluator |

### Dependencies

- `@modelcontextprotocol/sdk` — MCP server framework (stdio transport)
- `zod` (transitive via MCP SDK) — Input schema validation
- Node.js 18+

## Data flow

1. Claude decides to call a tool (e.g., `properties_search` with `{location: "Dubai Marina", maxPrice: 2000000}`)
2. MCP transport delivers the call to the server process via stdin
3. Server validates input with Zod schemas
4. Server calls Qobrix REST API: `GET /api/v2/properties?subdivision=Dubai+Marina&max_price=2000000`
5. Server maps response fields to RESO DD 2.0 names
6. Server returns JSON result via stdout to Claude

In the mock server, step 4 is replaced by in-memory array filtering.

## RESO DD 2.0 mapping

The server normalizes Qobrix fields to RESO standards so downstream tools and agents can work with consistent field names across different CRM systems:

| Qobrix internal | RESO DD 2.0 | Description |
|----------------|-------------|-------------|
| `listing_price` | `ListPrice` | Property asking price |
| `property_category` | `PropertyType` | Apartment, Villa, etc. |
| `listing_status` | `StandardStatus` | Active, Pending, Sold |
| `bedrooms` | `BedroomsTotal` | Total bedroom count |
| `bathrooms` | `BathroomsTotalInteger` | Total bathroom count |
| `area_sqft` | `LivingArea` | Interior living area |
| `subdivision` | `SubdivisionName` | Neighborhood/community |

## Limitations

- **Read-only** — No create, update, or delete operations. You cannot modify CRM data through this server.
- **Qobrix-specific** — Only works with Qobrix CRM instances. Not a generic real-estate MCP.
- **No pagination cursor** — Uses offset/limit, not cursor-based pagination. Large datasets require manual offset management.
- **No webhook/streaming** — Polls on-demand only. No real-time event subscriptions.
- **Auth model** — Single API token per server instance. No per-user or per-team scoping.
- **RESO mapping is partial** — Covers core property and listing fields. Custom fields pass through unmapped.
- **Rate limits** — Subject to Qobrix API rate limits (varies by plan).

## Why it matters for Claude-driven products

**Lead-gen & sales agents**: An AI agent can query the full CRM — contacts, leads, opportunities, tasks — to prepare meeting briefs, prioritize follow-ups, or generate pipeline reports without manual data export.

**Real-estate marketing**: Pull live property data (RESO-normalized) to auto-generate listing descriptions, ad copy, or market reports directly from the CRM.

**Agent factories**: The standardized tool interface (search/get/list per entity) is a clean pattern for building MCP servers around other CRMs. The RESO DD 2.0 mapping shows how to normalize domain-specific APIs for LLM consumption.

**Multi-CRM orchestration**: Because fields use RESO standards, you could swap this for another RESO-aligned MCP server and your prompts/agents would still work — a practical example of schema-driven interoperability.
