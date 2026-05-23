# NinjaOne MCP Server

**Give Claude secure, read-only access to your entire NinjaOne RMM fleet — organizations, devices, alerts, patches, and software inventory — via MCP.**

The [Bezalu.NinjaOne.MCP](https://github.com/BezaluLLC/Bezalu.NinjaOne.MCP) server lets an AI assistant query a NinjaOne instance through 6 structured tools instead of raw API calls, with OAuth2 scoping so the assistant only sees what the user is allowed to see.

**Headline result:** Ask Claude *"Which devices have critical alerts right now?"* and get a structured answer across all your managed organizations in seconds — no dashboard clicking required.

## Quick links

| Doc | What it covers |
|-----|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, configure, MCP JSON snippet, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, build-vs-buy analysis |

## Try the demo

```bash
bash run.sh
```

Runs a mock simulation of all 6 MCP tools with realistic sample data — no NinjaOne account needed.
