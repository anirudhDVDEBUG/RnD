# Technical Details — DemandBird

## What It Does

DemandBird is a social media management platform that unifies content creation, scheduling, publishing, and analytics across six major platforms (Twitter/X, LinkedIn, YouTube, Bluesky, Threads, Substack). Its differentiator is AI-native design: it exposes an MCP (Model Context Protocol) server so that AI agents like Claude can programmatically create, schedule, repurpose, and analyze social media content without human interaction with platform UIs.

The tool targets teams and agencies managing multiple brands or clients. Instead of logging into six dashboards, users (or their AI agents) interact through a single API or MCP interface that handles platform-specific formatting, rate limits, and publishing constraints.

## Architecture

```
User / Claude Agent
        │
        ├── MCP Server (demandbird-mcp)
        │     ├── demandbird_list_platforms
        │     ├── demandbird_create_post
        │     ├── demandbird_list_posts
        │     ├── demandbird_repurpose
        │     └── demandbird_analytics
        │
        └── REST API (api.demandbird.com/v1/...)
              ├── /posts (CRUD + scheduling)
              ├── /platforms (connection management)
              ├── /analytics (engagement metrics)
              └── /repurpose (content adaptation)
                    │
                    ▼
           Platform APIs (Twitter, LinkedIn, etc.)
```

**Key files in this prototype:**
- `demo.js` — Main demo runner; exercises all workflows end-to-end
- `lib/mock-client.js` — Simulated DemandBird API client with mock data
- `lib/mcp-server-mock.js` — MCP tool definitions matching the real server's schema

**Dependencies:** `chalk` (terminal styling), `cli-table3` (table formatting). Both are optional — demo degrades gracefully without them.

**Data flow:**
1. Agent sends a request (create post, schedule, repurpose) via MCP tool call or API
2. DemandBird normalizes content for each target platform (character limits, hashtag handling, formatting)
3. Content is queued or published via platform-specific APIs
4. Engagement data flows back through polling/webhooks into the analytics layer

## Limitations

- **No free tier confirmed** — The repo is open-source but API key provisioning / pricing is unclear; may require a DemandBird account
- **Platform API credentials required** — Each connected platform needs its own OAuth tokens or API keys (Twitter developer account, LinkedIn app, etc.)
- **Rate limits** — Subject to each platform's individual rate limits; DemandBird manages these but high-volume publishing may hit caps
- **No real-time engagement** — Analytics are polled, not streamed; expect some delay in metrics
- **MCP server maturity** — As a newer tool, the MCP server interface may change between versions; pin your version
- **This prototype uses mock data** — To evaluate the real tool, you need platform credentials and a DemandBird API key

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|---|---|
| **Lead-gen / Marketing** | Automate multi-platform content distribution. Claude can draft platform-optimized posts, schedule them at optimal times, and track engagement — closing the loop from content creation to lead measurement. |
| **Ad Creatives** | Repurposing workflow transforms a single creative brief into platform-specific variants (short tweet, LinkedIn article, YouTube description), reducing creative production cost. |
| **Agent Factories** | The MCP server makes DemandBird a composable building block. Chain it with research agents (find trending topics) → content agents (draft posts) → DemandBird (publish + measure). |
| **Agency Automation** | Teams managing multiple client accounts can build Claude-powered workflows that handle content calendars, approval queues, and cross-platform analytics at scale. |

The MCP integration is the key value: it turns social media management from a manual UI task into a programmable capability that AI agents can invoke as part of larger automated workflows.
