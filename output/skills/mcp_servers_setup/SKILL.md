---
name: mcp_servers_setup
description: |
  Set up and configure official Model Context Protocol (MCP) servers for Claude and other AI assistants.
  TRIGGER: user mentions MCP server, Model Context Protocol, tool integration with Claude, connecting external tools, or asks about filesystem/GitHub/Slack/database MCP servers.
---

# MCP Servers Setup

Set up and configure official Model Context Protocol (MCP) servers from the [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) repository — the canonical collection of reference MCP server implementations.

## When to use

- "Set up an MCP server for filesystem access"
- "How do I connect GitHub/Slack/PostgreSQL to Claude via MCP?"
- "Install and configure an official MCP server"
- "Add tool integrations to my Claude setup using Model Context Protocol"
- "What MCP servers are available and how do I use them?"

## How to use

### 1. Choose an MCP server

The repository provides reference servers in two categories:

**TypeScript servers (installed via npx):**
- `@modelcontextprotocol/server-filesystem` — Read/write local files, search, and directory operations
- `@modelcontextprotocol/server-github` — GitHub API integration (repos, issues, PRs, files)
- `@modelcontextprotocol/server-slack` — Slack workspace integration (channels, messages)
- `@modelcontextprotocol/server-google-maps` — Google Maps API (geocoding, directions, places)
- `@modelcontextprotocol/server-memory` — Knowledge graph-based persistent memory
- `@modelcontextprotocol/server-puppeteer` — Browser automation and web scraping
- `@modelcontextprotocol/server-brave-search` — Brave Search API integration
- `@modelcontextprotocol/server-everart` — AI image generation
- `@modelcontextprotocol/server-sequential-thinking` — Dynamic problem-solving through sequential thought

**Python servers (installed via uvx or pip):**
- `mcp-server-git` — Git repository operations (log, diff, status, commits)
- `mcp-server-sqlite` — SQLite database operations
- `mcp-server-fetch` — Fetch and process web content
- `mcp-server-sentry` — Sentry.io issue tracking integration

### 2. Install and configure

**For Claude Desktop (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-token>"
      }
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/database.db"]
    }
  }
}
```

**For Claude Code (`.mcp.json` in project root):**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ]
    }
  }
}
```

### 3. Verify the server is running

- Restart Claude Desktop or Claude Code after configuration changes
- The MCP server tools should appear in the tool list
- Test by invoking a basic operation (e.g., list files for filesystem server)

### 4. Build a custom MCP server

Use the reference servers as templates. Each server follows the MCP specification:

```bash
# Clone the repo for reference implementations
git clone https://github.com/modelcontextprotocol/servers.git
cd servers/src/<server-name>
```

Key patterns:
- Servers expose **tools**, **resources**, and/or **prompts**
- TypeScript servers use `@modelcontextprotocol/sdk`
- Python servers use `mcp` package
- Each server has its own README with specific configuration options

## References

- **Repository**: https://github.com/modelcontextprotocol/servers
- **MCP Specification**: https://spec.modelcontextprotocol.io
- **MCP Documentation**: https://modelcontextprotocol.io
