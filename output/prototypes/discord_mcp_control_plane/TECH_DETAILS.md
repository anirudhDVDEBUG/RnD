# Technical Details — Discord MCP Control Plane

## What it does

DiscordMCP is a Python application that runs a Discord bot (via `discord.py`) alongside a FastAPI HTTP server. The bot connects to one or more Discord guilds and maintains live state — channels, members, messages. The FastAPI layer exposes that state through the Model Context Protocol (MCP), giving any MCP-compatible AI client (Claude Desktop, Claude Code, custom agents) the ability to read and write Discord data using structured tool calls, resource URIs, and prompt templates.

The key insight is treating Discord as a **control plane**: instead of building one-off bots with hardcoded commands, you expose primitive operations (send, read, list, create, delete) as MCP tools and let the AI client compose them into arbitrary workflows — summarize a channel, draft announcements, moderate content, triage support threads — without writing new bot code.

## Architecture

```
┌─────────────────┐     MCP (JSON-RPC / stdio)     ┌──────────────────┐
│  Claude / AI    │ ◄──────────────────────────────► │  FastAPI + MCP   │
│  Client         │                                  │  Server          │
└─────────────────┘                                  └────────┬─────────┘
                                                              │
                                                     discord.py bot
                                                              │
                                                   ┌──────────▼─────────┐
                                                   │  Discord Gateway   │
                                                   │  (multiple guilds) │
                                                   └────────────────────┘
```

### Key files (upstream repo)

| File | Role |
|------|------|
| `main.py` | Entry point — starts both the Discord bot and FastAPI server |
| `bot/` | discord.py bot: event handlers, command routing |
| `mcp/` | MCP tool/resource/prompt definitions and dispatch |
| `api/` | FastAPI routes that bridge HTTP to MCP calls |
| `.env` | `DISCORD_BOT_TOKEN` and optional LLM API keys |

### Key files (this demo)

| File | Role |
|------|------|
| `discord_mcp_server.py` | Mock implementation of all 7 tools, 3 resources, 3 prompts with in-memory data |
| `demo.py` | Exercises every MCP surface end-to-end |
| `run.sh` | One-command entry point |

### Dependencies

- **discord.py >=2.3** — async Discord gateway client
- **FastAPI + uvicorn** — HTTP server for MCP endpoints
- **python-dotenv** — environment variable management
- **httpx** — HTTP client (used for LLM API calls in the built-in agent)

### Data flow

1. AI client sends an MCP `tool_call` (e.g., `send_message`) over stdio or HTTP.
2. FastAPI handler deserializes the request, validates parameters.
3. Handler calls the corresponding `discord.py` method (e.g., `channel.send()`).
4. Discord API processes the request; bot receives confirmation.
5. Result is serialized back to the MCP client as a JSON response.

Resources work similarly but are read-only (guild metadata, channel lists, message history). Prompts return templated strings that the AI client fills and executes.

## Limitations

- **No webhook or event push** — the MCP server is request/response only. The bot receives Discord events but does not push them to the AI client proactively.
- **Authentication is bot-scoped** — all operations run as the bot user. No per-user OAuth or impersonation.
- **Rate limits** — Discord API rate limits apply. High-frequency tool calls (e.g., bulk message reads across many channels) can hit 429s.
- **No file/attachment support** — current tools handle text messages only.
- **Single-process** — bot and MCP server run in one Python process. No horizontal scaling story.
- **No persistent state** — message history is fetched live from Discord; no local database or cache.

## Why this matters for Claude-driven products

| Use case | How Discord MCP helps |
|----------|----------------------|
| **Agent factories** | Expose Discord as a tool surface for autonomous agents — support bots, onboarding flows, community managers — without custom bot code per workflow. |
| **Lead-gen / marketing** | Monitor community channels for buying signals, auto-respond to inquiries, post campaign announcements across multiple servers from a single agent. |
| **Ad creatives** | Share generated creatives directly into review channels, collect emoji-reaction feedback, iterate in-loop. |
| **Voice AI** | Pair with Discord voice channel metadata to coordinate voice-agent sessions — list active voice channels, move users, post transcripts. |
| **Internal ops** | CI/CD notifications, on-call alerts, standup summaries — all driven by Claude composing MCP tool calls instead of maintaining separate integrations. |

The broader pattern: any SaaS with an API can be wrapped as an MCP server, turning Claude into a universal control plane operator. Discord is one of the highest-leverage targets because of its ubiquity in developer, gaming, and community-driven businesses.
