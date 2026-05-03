# Technical Details

## What it does

ZeroClaw Plugin Hub is a routing layer that sits between Claude Code (or any MCP client) and multiple MCP-compatible tool servers. Instead of configuring each MCP server individually in Claude Code's settings, you register them all with ZeroClaw, which exposes a single unified MCP interface. When Claude Code calls a tool, ZeroClaw inspects the tool name, matches it against its routing table, and forwards the request to the correct backend server. Responses flow back through the same path.

The SDK toolkit portion provides scaffolding for building new MCP-compatible plugins that slot into the router without modifying core config.

## Architecture

```
Claude Code  --->  ZeroClaw Router (single MCP server)
                        |
                +-------+-------+-------+
                |       |       |       |
              MCP-A   MCP-B   MCP-C   MCP-N
              (fs)    (db)    (web)   (custom)
```

**Key components:**
- `router.py` (this demo) / `index.js` (real project) — core dispatch logic
- `config.json` — backend registry with tool-to-server mappings
- `backends/` — individual backend adapters
- `sdk/` — plugin template and builder utilities

**Data flow:**
1. Claude Code sends JSON-RPC `tools/call` to ZeroClaw's stdio transport
2. Router looks up tool name in routing table
3. Request is forwarded to the matched backend via its configured transport (stdio/SSE/HTTP)
4. Response is relayed back to Claude Code unchanged

**Dependencies:** Node.js (real project), Python 3.8+ (this demo — stdlib only)

## Limitations

- **Not a load balancer** — routes by tool name, not by load or latency
- **No auth aggregation** — each backend manages its own credentials; ZeroClaw passes env vars through but doesn't unify auth
- **Single-client** — designed for one Claude Code session at a time; no concurrent multi-user support
- **Early-stage** — the upstream repo is evolving rapidly; APIs and config formats may change
- **No tool conflict resolution** — if two backends expose the same tool name, first-registered wins

## Why it matters

For teams building Claude-driven products:

- **Agent factories:** When your agent needs filesystem, database, and web tools simultaneously, ZeroClaw avoids per-project config sprawl. One router config covers all environments.
- **Lead-gen / marketing automation:** Combine CRM tools, email senders, and enrichment APIs behind one MCP facade. Claude Code orchestrates without knowing which backend serves which capability.
- **Plugin marketplace potential:** The hub model enables a registry where teams share MCP plugins — install with one CLI command, instantly available to Claude Code.
- **Reduced config drift:** Single source of truth for MCP server registrations across dev, staging, and production Claude Code setups.
