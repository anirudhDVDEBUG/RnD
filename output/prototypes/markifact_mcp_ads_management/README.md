# Markifact MCP — Multi-Platform Ad Management from Claude

**TL;DR:** MCP server exposing 300+ tools across Google Ads, Meta Ads, GA4, TikTok Ads, and LinkedIn Ads — all operable from Claude (Desktop or Code), ChatGPT, Cursor, or any MCP client. Every write operation requires explicit human approval before execution.

## Headline Result

```
Registered 31 MCP tools across 5 platforms:
  Google Ads: 10 tools    Meta Ads: 9 tools    GA4: 4 tools
  TikTok Ads: 4 tools     LinkedIn Ads: 4 tools

> "Pause all campaigns with CPA > $25"
  [HUMAN-IN-THE-LOOP] Approve each pause individually
  Paused: Product Launch — Widget Pro (CPA: $24.71)
  Paused: Gen-Z Awareness — Summer (CPA: $27.79)
  Paused: B2B Lead Gen — Enterprise (CPA: $121.90)
```

## Quick Start

```bash
bash run.sh
```

No API keys required — the demo uses mock data to show the full tool schema and human-in-the-loop flow.

## More Info

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Setup for Claude Desktop, Claude Code, and other MCP clients
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, limitations, and why this matters

## Source

- [markifact/markifact-mcp](https://github.com/markifact/markifact-mcp)
