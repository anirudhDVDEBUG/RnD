---
name: openmcp_server_manager
description: |
  Set up and manage MCP servers using OpenMCP, a desktop and CLI manager for OpenCode MCP servers.
  Triggers: openmcp, mcp server manager, manage mcp servers, desktop mcp, mcp cli manager
---

# OpenMCP Server Manager

Set up and manage MCP (Model Context Protocol) servers using [OpenMCP](https://github.com/hacimertgokhan/openmcp), a TypeScript-based desktop and CLI manager.

## When to use

- "Set up OpenMCP to manage my MCP servers"
- "I need a desktop app to manage MCP server configurations"
- "Help me install and configure OpenMCP for MCP server management"
- "I want a CLI tool to manage my MCP servers"
- "How do I use OpenMCP to add and configure MCP servers?"

## How to use

### 1. Clone and install OpenMCP

```bash
git clone https://github.com/hacimertgokhan/openmcp.git
cd openmcp
npm install
```

### 2. Run in development mode

```bash
npm run dev
```

This launches the OpenMCP desktop application (Electron-based) or CLI interface for managing MCP servers.

### 3. Build for production

```bash
npm run build
```

### 4. Key capabilities

- **Add MCP servers**: Register new MCP server configurations through the desktop UI or CLI
- **Manage server lifecycle**: Start, stop, and monitor MCP servers from a single interface
- **Configure server settings**: Edit server configurations including transport type, command, args, and environment variables
- **Desktop GUI**: Visual interface for managing all your MCP server instances
- **CLI mode**: Command-line interface for scripting and automation of MCP server management

### 5. Integration with Claude Code

Once MCP servers are configured in OpenMCP, you can reference their configurations when setting up MCP servers in Claude Code's `settings.json`:

```json
{
  "mcpServers": {
    "your-server": {
      "command": "node",
      "args": ["path/to/your/mcp-server.js"],
      "type": "stdio"
    }
  }
}
```

## References

- **Repository**: https://github.com/hacimertgokhan/openmcp
- **Language**: TypeScript
- **Topics**: desktop-app, mcp, mcp-manager, mcp-server
