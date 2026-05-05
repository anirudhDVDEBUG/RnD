# Tech Details — MCP Servers Setup

## What it does

The [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) repository provides 12+ reference MCP server implementations — each one a standalone process that exposes tools, resources, or prompts to AI assistants like Claude over a JSON-RPC 2.0 protocol via stdio. When you add a server to your Claude Desktop or Claude Code config, Claude spawns it as a child process and communicates through stdin/stdout. The server advertises its capabilities (e.g., "I can read files" or "I can query GitHub"), and Claude calls those tools during conversations exactly like it calls its built-in tools.

This demo repo includes two files: a **config generator** (`mcp_config_generator.py`) that produces copy-paste-ready JSON config for all 12 official servers, and a **protocol demo** (`demo_mcp_server.py`) that implements a minimal MCP server from scratch, showing the exact JSON-RPC messages exchanged during initialization, tool discovery, and tool invocation.

## Architecture

### The MCP protocol (what every server implements)

```
Claude Desktop / Claude Code
  │
  ├─ spawns server as child process
  │    command: "npx -y @modelcontextprotocol/server-filesystem /path"
  │
  ├─ stdin  → JSON-RPC requests  → Server
  └─ stdout ← JSON-RPC responses ← Server

Session lifecycle:
  1. initialize    → server returns protocolVersion + capabilities
  2. tools/list    → server returns tool schemas (name, description, inputSchema)
  3. tools/call    → server executes tool, returns content blocks
  4. (repeat 3 as needed)
```

### Key files in this demo

| File | Purpose |
|------|---------|
| `mcp_config_generator.py` | Registry of all 12 official servers + config builder for `claude_desktop_config.json` and `.mcp.json` |
| `demo_mcp_server.py` | Minimal MCP server implementing `initialize`, `tools/list`, `tools/call` with two tools (echo, word_count) |
| `run.sh` | Runs both demos end-to-end |

### Key files in the upstream repo

```
modelcontextprotocol/servers/
  src/
    filesystem/     — TypeScript, uses @modelcontextprotocol/sdk
    github/         — TypeScript, GitHub REST API wrapper
    slack/          — TypeScript, Slack Web API wrapper
    memory/         — TypeScript, JSON-based knowledge graph
    puppeteer/      — TypeScript, Puppeteer browser control
    ...
    git/            — Python, uses mcp package + GitPython
    sqlite/         — Python, uses mcp package + sqlite3
    fetch/          — Python, uses mcp package + httpx
```

### Dependencies

- **TypeScript servers**: `@modelcontextprotocol/sdk` (official SDK), plus domain-specific libs (Octokit for GitHub, etc.)
- **Python servers**: `mcp` package (official SDK), plus domain libs (GitPython, httpx, etc.)
- **This demo**: Python 3.10+ stdlib only — no external deps

### Data flow for a real deployment

1. User edits `claude_desktop_config.json` with server entries
2. Claude Desktop reads config on startup, spawns each server process
3. During conversation, Claude decides to use a tool → sends `tools/call` via stdin
4. Server executes (reads file, queries API, runs SQL...) → returns result via stdout
5. Claude incorporates the result into its response

## Limitations

- **No server-to-server communication**: each MCP server is isolated; they don't share state
- **Stdio only in most implementations**: no HTTP/WebSocket transport in the reference servers (the spec supports it, but reference servers use stdio)
- **No auth between Claude and server**: the trust boundary is the process spawn — anyone who can edit the config can add arbitrary servers
- **Cold start latency**: npx downloads packages on first run; subsequent starts use cache
- **No streaming for tool results**: tool responses are returned as complete JSON, not streamed
- **API key management is manual**: keys go in plaintext JSON config files (no vault/secrets integration)

## Why this matters for Claude-driven products

**Lead-gen / marketing:** The GitHub and Slack MCP servers let Claude agents monitor repos for signals (new issues, PR activity) and post to Slack channels — a building block for automated competitor tracking or community engagement bots.

**Agent factories:** MCP is the standard interface for giving agents tools. If you're building an agent platform, adopting MCP means your agents can use any MCP server (filesystem, database, browser, custom) without custom integration code. The sequential-thinking server adds chain-of-thought scaffolding.

**Ad creatives:** The fetch + puppeteer servers enable agents to scrape competitor landing pages, screenshot them, and feed visual context back to Claude for creative generation.

**Voice AI:** MCP servers could back a voice agent's tool use — "check my calendar" (custom MCP server), "look up this address" (Google Maps MCP), "search for that" (Brave Search MCP) — all through the same protocol.

**Data pipelines:** The SQLite and filesystem servers let Claude operate directly on local data without custom API wrappers, useful for ETL prototyping or data analysis agents.

## References

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Source repo](https://github.com/modelcontextprotocol/servers) — 54 stars/day velocity
