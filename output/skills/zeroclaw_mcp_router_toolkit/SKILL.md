---
name: zeroclaw_mcp_router_toolkit
description: |
  Set up and configure ZeroClaw Plugin Hub — a multi-MCP router and SDK toolkit for Claude Code.
  TRIGGER: user mentions zeroclaw, multi-mcp router, mcp plugin hub, claude code router, or wants to route between multiple MCP servers.
---

# ZeroClaw MCP Router & SDK Toolkit

Configure and use the ZeroClaw Plugin Hub to route Claude Code requests across multiple MCP servers with a single CLI-based toolkit.

## When to use

- "Set up ZeroClaw for multi-MCP routing in Claude Code"
- "I want to route Claude Code requests across multiple MCP servers"
- "Configure ZeroClaw plugin hub for my Claude Code project"
- "How do I use ZeroClaw CLI to manage MCP plugins?"
- "Connect multiple MCP servers through a single router in Claude Code"

## How to use

### 1. Clone and install ZeroClaw Plugin Hub

```bash
git clone https://github.com/IKingBarou/Zeroclaw-Plugin-Hub.git
cd Zeroclaw-Plugin-Hub
```

Review the repository README for the latest install instructions, as the project is actively evolving.

### 2. Configure MCP server routing

ZeroClaw acts as a router layer that sits between Claude Code and multiple MCP servers. Configure your MCP servers in the project configuration so that requests are dispatched to the correct backend.

- Define each MCP server endpoint in the ZeroClaw config
- Set routing rules to determine which server handles which tool calls
- Use the CLI to verify connectivity to all registered MCP servers

### 3. Integrate with Claude Code

Register ZeroClaw as the MCP entry point in your Claude Code settings (`settings.json` or `.mcp.json`):

```json
{
  "mcpServers": {
    "zeroclaw": {
      "command": "npx",
      "args": ["zeroclaw-plugin-hub"],
      "env": {}
    }
  }
}
```

Adjust the command and args based on the actual install method documented in the repo.

### 4. Use the CLI toolkit

- List available plugins and MCP backends
- Add or remove MCP server registrations
- Test routing and tool dispatch
- Use SDK helpers for building custom plugins

### 5. Build custom plugins

Use the SDK toolkit portion of ZeroClaw to create new MCP-compatible plugins that integrate into the routing layer. Follow the plugin template structure provided in the repository.

## Key features

- **Multi-MCP routing**: Single entry point that dispatches to multiple MCP servers
- **CLI management**: Add, remove, list, and test MCP server connections
- **SDK toolkit**: Build custom plugins compatible with the ZeroClaw router
- **Claude Code native**: Designed specifically for the Claude Code agent workflow
- **Plugin hub**: Community plugin registry for discovering and sharing MCP tools

## References

- Source: [IKingBarou/Zeroclaw-Plugin-Hub](https://github.com/IKingBarou/Zeroclaw-Plugin-Hub)
- Topics: claude-code, mcp-router, sdk-toolkit, agent-plugin, cli-tool
