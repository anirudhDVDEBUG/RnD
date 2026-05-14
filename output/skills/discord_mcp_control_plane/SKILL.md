---
name: discord_mcp_control_plane
description: |
  Set up and configure DiscordMCP — a multi-server Discord control plane that exposes Discord operations as MCP tools, resources, and prompts for AI clients, with a built-in conversational AI agent.
  Triggers: discord mcp, discord bot mcp, discord control plane, discord ai agent, discord automation mcp
---

# Discord MCP Control Plane

Set up and integrate DiscordMCP, a Python-based multi-server Discord control plane that exposes Discord operations (messaging, channel management, server administration) as Model Context Protocol (MCP) tools, resources, and prompts for AI clients.

## When to use

- "Set up an MCP server for Discord so Claude can send messages and manage channels"
- "Build a Discord bot that exposes operations as MCP tools for AI agents"
- "Connect Claude to Discord using Model Context Protocol"
- "Create a Discord automation agent with MCP integration"
- "Configure a multi-server Discord control plane for AI clients"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/Rastrian/DiscordMCP.git
cd DiscordMCP
pip install -r requirements.txt
```

### 2. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and add a Bot
3. Enable required Privileged Gateway Intents:
   - **Message Content Intent**
   - **Server Members Intent**
   - **Presence Intent**
4. Generate an OAuth2 invite URL with the `bot` and `applications.commands` scopes, plus necessary permissions (Send Messages, Read Message History, Manage Channels, etc.)
5. Invite the bot to your server(s)

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

Additional configuration may include API host/port settings for the FastAPI server and any LLM API keys if using the built-in conversational AI agent.

### 4. Run the server

```bash
python main.py
```

This starts both the Discord bot and the MCP server (built on FastAPI), exposing Discord operations as MCP tools.

### 5. Connect from an MCP client

Add the server to your MCP client configuration (e.g., Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "discord": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/DiscordMCP"
    }
  }
}
```

### Key capabilities

The MCP server exposes Discord operations as tools including:

- **Messaging**: Send, read, edit, and delete messages across servers and channels
- **Channel management**: List, create, and manage channels
- **Server operations**: Query server info, list members, manage roles
- **Resources**: Access server metadata, channel lists, and message history as MCP resources
- **Prompts**: Pre-built prompt templates for common Discord workflows
- **Conversational AI agent**: Built-in LLM-powered agent that can respond to Discord messages

### Architecture

- **Python + discord.py**: Core Discord bot framework
- **FastAPI**: HTTP server exposing MCP endpoints
- **MCP Protocol**: Standard Model Context Protocol for AI client integration
- **Multi-server**: Single bot instance manages multiple Discord servers simultaneously

## References

- Source repository: https://github.com/Rastrian/DiscordMCP
- Model Context Protocol: https://modelcontextprotocol.io
- Discord.py documentation: https://discordpy.readthedocs.io
- Discord Developer Portal: https://discord.com/developers/applications
