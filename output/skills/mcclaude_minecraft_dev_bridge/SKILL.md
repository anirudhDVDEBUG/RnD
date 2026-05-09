---
name: mcclaude_minecraft_dev_bridge
description: |
  Set up and use McClaude — an MCP bridge between Claude Code and a live Minecraft server for plugin development.
  TRIGGER: minecraft plugin development, minecraft server bridge, mcclaude, skript editing, minecraft console MCP, minecraft eval, minecraft claude code integration
---

# McClaude — Minecraft Dev Bridge

Develop Minecraft plugins with Claude Code on a live server. Read console output, run commands, edit Skript files, and eval code — all from your IDE via an end-to-end encrypted MCP bridge.

## When to use

- "Set up Claude Code to develop Minecraft plugins on a live server"
- "I want to read my Minecraft server console and run commands from Claude"
- "Help me edit Skript files on my Minecraft server with Claude Code"
- "Configure mcclaude MCP bridge for Minecraft development"
- "I need to eval code on my Minecraft server from Claude Code"

## How to use

### 1. Install the McClaude Plugin

1. Download the latest McClaude `.jar` from [GitHub Releases](https://github.com/LightningReflex/mcclaude/releases).
2. Place the `.jar` in your Minecraft server's `plugins/` directory.
3. Restart the server. The plugin will generate its configuration files.

### 2. Configure the MCP Server in Claude Code

Add the McClaude MCP server to your Claude Code configuration (`.claude/settings.json` or project-level MCP config):

```json
{
  "mcpServers": {
    "mcclaude": {
      "command": "npx",
      "args": ["mcclaude-mcp"],
      "env": {
        "MCCLAUDE_HOST": "your-server-host",
        "MCCLAUDE_PORT": "25580",
        "MCCLAUDE_SECRET": "your-encryption-secret"
      }
    }
  }
}
```

Adjust `MCCLAUDE_HOST`, `MCCLAUDE_PORT`, and `MCCLAUDE_SECRET` to match your server's plugin configuration.

### 3. Use the MCP Tools

Once connected, the following capabilities are available through the MCP bridge:

- **Console Reading**: Read live server console output to monitor logs, errors, and events.
- **Command Execution**: Run Minecraft server commands (e.g., `/reload`, `/give`, `/tp`) directly from Claude Code.
- **Skript File Editing**: Edit `.sk` Skript files on the server via WebDAV, enabling live Skript plugin development.
- **Code Eval**: Evaluate code snippets directly on the running server for rapid testing and debugging.

### 4. Development Workflow

1. Start your Minecraft server with the McClaude plugin installed.
2. Open your project in Claude Code with the MCP server configured.
3. Ask Claude to read the console, run commands, or edit Skript files.
4. Changes are applied live — test immediately on the running server.

### 5. Security Notes

- Communication between Claude Code and the Minecraft server is **end-to-end encrypted**.
- Keep your `MCCLAUDE_SECRET` private and never commit it to version control.
- The plugin uses WebDAV for file access — ensure your server firewall is configured appropriately.

## References

- **Repository**: [LightningReflex/mcclaude](https://github.com/LightningReflex/mcclaude)
- **Topics**: MCP Server, Minecraft, Claude Code, Skript, Paper Plugin, WebDAV
- **Language**: Java
