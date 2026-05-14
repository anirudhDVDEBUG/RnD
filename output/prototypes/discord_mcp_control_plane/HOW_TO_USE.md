# How to Use — Discord MCP Control Plane

## Install (real project)

```bash
git clone https://github.com/Rastrian/DiscordMCP.git
cd DiscordMCP
pip install -r requirements.txt
```

Dependencies: `discord.py`, `fastapi`, `uvicorn`, `python-dotenv`, `httpx`.

## Install (this demo)

```bash
# No installs — uses Python stdlib only
bash run.sh
```

## MCP client configuration

### Option A: Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "discord": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/absolute/path/to/DiscordMCP",
      "env": {
        "DISCORD_BOT_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Option B: Claude Code (`~/.claude.json`)

Add to the `mcpServers` block:

```json
{
  "mcpServers": {
    "discord": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/absolute/path/to/DiscordMCP",
      "env": {
        "DISCORD_BOT_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Discord bot setup (required for real use)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications) and create an application.
2. Add a **Bot** and copy the token.
3. Enable **Privileged Gateway Intents**: Message Content, Server Members, Presence.
4. Generate an OAuth2 invite URL with scopes `bot` + `applications.commands` and permissions: Send Messages, Read Message History, Manage Channels, Manage Roles.
5. Invite the bot to your server(s).
6. Set `DISCORD_BOT_TOKEN=<your_token>` in a `.env` file or in the MCP config above.

## First 60 seconds

```
$ bash run.sh

  Discord MCP Control Plane — Interactive Demo
  (all data is mock — no Discord token required)

================================================================
  MCP Manifest (tools / resources / prompts)
================================================================
{
  "name": "discord-mcp",
  "version": "1.0.0",
  "tools": [ ... 7 tools ... ],
  "resources": [ ... 3 resources ... ],
  "prompts": [ ... 3 prompts ... ]
}

================================================================
  Tool: server_info(guild_id='1001')
================================================================
{
  "id": "1001",
  "name": "AI Builders Hub",
  "member_count": 342,
  "channel_count": 3
}

================================================================
  Tool: send_message(guild_id='1001', channel_id='3001', ...)
================================================================
{
  "ok": true,
  "message": {
    "author": "claude-bot",
    "content": "Automated update: build #47 passed all checks."
  }
}

  ... (15 operations total — tools, resources, prompts, error handling)
```

## What Claude can do once connected

| Tool | Description |
|------|-------------|
| `send_message` | Post a message to any channel on any joined server |
| `read_messages` | Retrieve recent messages from a channel |
| `list_channels` | Enumerate channels in a guild |
| `list_members` | Enumerate members and their roles |
| `server_info` | Get guild metadata (name, owner, counts) |
| `create_channel` | Create a new text or voice channel |
| `delete_message` | Remove a message by ID |

Resources provide read-only access to guild metadata, channel lists, and message history via `discord://` URIs. Prompt templates offer pre-built workflows for summarization, announcements, and moderation.
