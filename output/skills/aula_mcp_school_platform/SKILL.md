---
name: aula_mcp_school_platform
description: |
  Set up and configure the Aula MCP server for Denmark's school platform.
  TRIGGER when: user mentions Aula, Danish school platform, MCP server for school, MitID authentication for Aula, ugeplaner, or connecting AI agents to Aula.
  DO NOT TRIGGER when: general MCP server setup unrelated to Aula, other school platforms, or non-Danish education systems.
---

# Aula MCP School Platform

MCP server for Denmark's Aula school platform — TypeScript MitID auth, no headless browser. Exposes profiles, calendar, messages, and ugeplaner to AI agents (Claude/Cursor/etc) via Model Context Protocol.

## When to use

- "Set up an MCP server for Aula so I can access my kids' school info"
- "Connect Claude to Denmark's Aula school platform"
- "I want to read school messages and calendar from Aula via AI"
- "Help me configure aula-mcp with MitID authentication"
- "Access ugeplaner and profiles from Aula in my AI workflow"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/Casperjuel/aula-mcp.git
cd aula-mcp
bun install
```

### 2. Configure environment

Create a `.env` file with your Aula/MitID credentials:

```env
AULA_USERNAME=your_username
AULA_PASSWORD=your_password
```

The server uses TypeScript-based MitID authentication without requiring a headless browser.

### 3. Build and run

```bash
bun run build
bun run start
```

### 4. Connect to Claude or other MCP clients

Add to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "aula": {
      "command": "bun",
      "args": ["run", "start"],
      "cwd": "/path/to/aula-mcp"
    }
  }
}
```

### 5. Available tools

Once connected, the MCP server exposes these capabilities:

- **Profiles** — View child/parent profiles linked to your Aula account
- **Calendar** — Access school calendar events and activities
- **Messages** — Read and manage school communication
- **Ugeplaner** — View weekly plans from teachers

### Key details

- **Runtime**: Bun (TypeScript)
- **Framework**: Hono
- **Auth**: Native MitID authentication (no headless browser needed)
- **Protocol**: Model Context Protocol (MCP)

## References

- Source: https://github.com/Casperjuel/aula-mcp
- Model Context Protocol: https://modelcontextprotocol.io
