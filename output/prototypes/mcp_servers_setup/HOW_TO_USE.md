# How to Use — MCP Servers Setup

## Install (this demo)

```bash
# No dependencies — pure Python 3.10+ stdlib
git clone <this-repo>
cd mcp_servers_setup
bash run.sh
```

## Install real MCP servers

**TypeScript servers** (most of the collection):

```bash
# No global install needed — npx runs them on-demand
# Just configure and Claude Desktop/Code launches them automatically
```

**Python servers:**

```bash
pip install mcp-server-git mcp-server-sqlite mcp-server-fetch
# or use uvx (uv's npx equivalent) — no install needed
```

## Configure for Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/projects"],
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

Restart Claude Desktop. The server tools appear automatically.

## Configure for Claude Code

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"]
    }
  }
}
```

Or add to `~/.claude.json` for global availability.

## As a Claude Skill

Drop the `SKILL.md` into your skills directory:

```bash
mkdir -p ~/.claude/skills/mcp_servers_setup
cp SKILL.md ~/.claude/skills/mcp_servers_setup/SKILL.md
```

**Trigger phrases:**
- "Set up an MCP server for filesystem access"
- "How do I connect GitHub to Claude via MCP?"
- "Install and configure an official MCP server"
- "What MCP servers are available?"

## First 60 seconds

```bash
$ bash run.sh

======================================================================
  Official MCP Servers — modelcontextprotocol/servers
======================================================================

  TypeScript servers (npx):
  ----------------------------------------
    filesystem             Read/write local files, directory listing, search
    github                 GitHub API — repos, issues, PRs [API key required]
    memory                 Knowledge-graph persistent memory for Claude
    ...

──────────────────────────────────────────────────────────────────────────
  Claude Desktop config (no API keys needed)
──────────────────────────────────────────────────────────────────────────
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
    },
    "memory": { ... },
    "sequential-thinking": { ... }
  }
}

──────────────────────────────────────────────────────────────────────────
  Demo MCP Server (JSON-RPC protocol walkthrough)
──────────────────────────────────────────────────────────────────────────
  1. Client sends initialize       → server responds with capabilities
  2. Client lists available tools   → server returns tool schemas
  3. Client calls 'echo'           → "Echo: Hello from Claude!"
  4. Client calls 'word_count'     → "Words: 11, Characters: 83, Lines: 2"
```

Copy the JSON block into your config file, restart Claude, and you're connected.

## Available servers (quick reference)

| Server | Runtime | API Key? | Use case |
|--------|---------|----------|----------|
| filesystem | npx | No | Read/write files, search directories |
| github | npx | Yes | Repos, issues, PRs, code search |
| slack | npx | Yes | Channel messages, users |
| memory | npx | No | Persistent knowledge graph |
| puppeteer | npx | No | Browser automation, screenshots |
| brave-search | npx | Yes | Web search |
| google-maps | npx | Yes | Geocoding, directions, places |
| sequential-thinking | npx | No | Step-by-step reasoning |
| git | uvx | No | Git log, diff, status, commit |
| sqlite | uvx | No | SQL queries on local databases |
| fetch | uvx | No | Fetch web pages as markdown |
| sentry | uvx | Yes | Error tracking integration |
