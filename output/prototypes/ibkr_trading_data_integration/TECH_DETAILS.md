# Technical Details — IBKR Trading Data Integration

## What It Does

The `osauer/ibkr` project is a Go-based CLI and long-running daemon that connects to the Interactive Brokers Client Portal Gateway REST API. It exposes seven read-only capabilities — account summary, portfolio positions, real-time quotes, option chains with Greeks, daily OHLCV history, predefined market scans, and fixed-fractional position sizing — through three interfaces: a terminal CLI, a Claude Code plugin, and an MCP (Model Context Protocol) server for Claude Desktop. The daemon handles IBKR session management (authentication keep-alive, request throttling) so that Claude can issue natural-language queries that map to structured brokerage data.

All operations are strictly read-only: no order placement, modification, or cancellation is possible through this tool, making it safe to grant Claude unsupervised access to brokerage data.

## Architecture

```
User prompt
    |
    v
Claude (Code or Desktop)
    |
    v
osauer/ibkr binary
  ├── CLI mode      (direct terminal output)
  ├── Plugin mode   (Claude Code tool calls)
  └── MCP mode      (JSON-RPC over stdio for Claude Desktop)
    |
    v
IBKR Client Portal Gateway (localhost:5000)
    |
    v
Interactive Brokers servers
```

### Key Components

| Component | Role |
|-----------|------|
| `main.go` | Entry point; routes to CLI, plugin, or MCP sub-commands |
| `client/` | HTTP client wrapper for IBKR Client Portal REST API |
| `mcp/` | MCP server implementation (JSON-RPC stdio transport) |
| `cmd/` | CLI command definitions (account, positions, quote, chain, history, scan, size) |

### Data Flow

1. Claude receives a user prompt ("Get NVDA quote").
2. Claude invokes the `ibkr` tool via plugin call or MCP `tools/call`.
3. The binary makes an HTTP GET/POST to the local IBKR Client Portal Gateway.
4. Gateway forwards to IBKR servers, returns JSON.
5. The binary formats and returns structured data to Claude.
6. Claude renders a natural-language answer.

### Dependencies

- **Runtime:** Go standard library + IBKR Client Portal Gateway (Java, provided by IBKR)
- **No external Go modules required** beyond stdlib (HTTP client, JSON encoding)
- **Python demo** (this prototype): Python 3.8+ stdlib only (dataclasses, json, random)

## Limitations

- **Read-only.** Cannot place, modify, or cancel orders.
- **Requires running gateway.** The IBKR Client Portal Gateway must be authenticated and running locally. Sessions expire and need periodic re-authentication.
- **Market data subscriptions.** Real-time quotes require active IBKR market data subscriptions; otherwise data is delayed 15-20 minutes.
- **Rate limits.** IBKR throttles API requests (~10 req/sec). The daemon handles this, but rapid-fire queries may queue.
- **No streaming.** Data is request/response, not WebSocket streaming. Each quote is a snapshot.
- **US-centric defaults.** Scans and symbol resolution default to US exchanges; international markets require explicit exchange qualifiers.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | Demonstrates a clean pattern for wrapping a REST API as both a Claude Code plugin and MCP server — reusable for any API integration. |
| **Lead-gen / marketing** | Financial data enrichment: auto-pull portfolio performance for client reporting, market scan results for newsletter generation. |
| **Voice AI** | Natural-language brokerage queries map directly to voice assistant use cases ("What's my P&L today?"). |
| **Ad creatives** | Real-time market data can feed dynamic ad content (trending stocks, sector performance). |
| **Risk management** | Fixed-fractional sizing gives Claude a built-in position-sizing calculator — useful for any trading advisory product. |

The project is a compact, well-scoped example of how to give Claude safe, read-only access to a complex financial system without exposing write operations.
