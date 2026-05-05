# Technical Details

## What It Does

Markifact MCP is a Model Context Protocol (MCP) server that bridges AI clients (Claude, ChatGPT, Gemini, Cursor) to five major advertising platforms: Google Ads, Meta Ads, GA4, TikTok Ads, and LinkedIn Ads. It exposes 300+ platform-specific operations as MCP tools, letting an AI agent list campaigns, pull analytics, create/update/pause campaigns, manage audiences, and adjust budgets — all through natural language with programmatic precision underneath.

The critical design choice is **human-in-the-loop on all writes**: any tool that modifies state (create, update, pause, delete) surfaces a confirmation dialog to the user before execution. Read operations (list, get, report) execute immediately without prompts.

## Architecture

```
AI Client (Claude/ChatGPT/Cursor)
    │
    │ MCP Protocol (stdio/SSE)
    ▼
┌──────────────────────────────────┐
│  markifact-mcp server (Node.js)  │
│                                  │
│  ┌─────────────────────────────┐ │
│  │ Tool Router                 │ │
│  │  - classifies read vs write │ │
│  │  - enforces confirmation    │ │
│  └─────────────────────────────┘ │
│           │                      │
│  ┌────┬───┴───┬────┬─────────┐  │
│  │ GA │ Meta  │ TT │ LI │ GA4│  │
│  │Ads │ Ads   │Ads │Ads │    │  │
│  └────┴───────┴────┴────┴────┘  │
│     (platform API adapters)      │
└──────────────────────────────────┘
    │         │         │
    ▼         ▼         ▼
  Google    Meta     TikTok/LI
  Ads API   Mktg API   APIs
```

**Key files (in the real repo):**
- `src/server.ts` — MCP server entry, tool registration
- `src/tools/` — Per-platform tool definitions (Google, Meta, TikTok, LinkedIn, GA4)
- `src/adapters/` — API client wrappers for each platform
- `src/confirmation.ts` — Human-in-the-loop confirmation flow
- `src/schemas/` — Input/output JSON schemas for each tool

**Dependencies:**
- `@modelcontextprotocol/sdk` — MCP server SDK
- Platform-specific API clients (google-ads-api, facebook-nodejs-business-sdk, etc.)
- Node.js 18+ runtime

## Data Flow

1. AI client sends a `tools/call` request (e.g., `google_ads_list_campaigns`)
2. Server classifies tool as read or write via naming convention
3. **Read**: executes immediately, returns result to client
4. **Write**: returns a `confirmation_required` response → client shows UI → user approves/denies → server executes or aborts

## Limitations

- **No real-time bidding / automation rules** — it's request/response, not a continuous optimizer
- **No creative generation** — manages campaigns/budgets, doesn't create ad images or copy
- **API rate limits apply** — each platform has its own quotas; the server doesn't pool or batch
- **OAuth token management is manual** — you must provide valid refresh tokens; no built-in auth flow
- **Single-tenant** — designed for one user's credentials at a time, not multi-user SaaS
- **No cross-platform unified schema** — each platform's tools use that platform's native terminology

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Lead-gen / Marketing automation** | Directly manage and optimize campaigns from Claude without switching to platform UIs |
| **Ad creative pipelines** | Combine with image/copy generation — Claude creates the creative, then uses Markifact to deploy it |
| **Agent factories** | A single MCP server that an agent can call to manage $X00K+ in ad spend with guardrails |
| **Multi-platform reporting** | Pull GA4 + Google Ads + Meta in one conversation for unified performance views |
| **Budget optimization** | AI identifies underperformers and pauses/reallocates with human approval |

The human-in-the-loop pattern is especially important for advertising — one wrong API call can burn budget or pause revenue-generating campaigns. This makes Markifact a safer path to AI-driven ad management than raw API access.
