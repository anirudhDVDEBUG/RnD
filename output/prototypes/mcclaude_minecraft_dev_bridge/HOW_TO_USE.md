# How to Use McClaude

## Quick Demo (no server needed)

```bash
bash run.sh
```

This spins up a mock Minecraft server and exercises all four MCP capabilities (console, commands, Skript editing, eval) with simulated data.

---

## Real Setup — Three Components

McClaude has three parts: a **Paper plugin** (runs on your Minecraft server), an **MCP server** (npm package Claude Code talks to), and a **shared secret** for encryption.

### 1. Install the Minecraft Plugin

```bash
# Download the latest .jar from GitHub Releases
curl -L -o McClaude.jar \
  https://github.com/LightningReflex/mcclaude/releases/latest/download/McClaude.jar

# Place in your Paper/Spigot server's plugins directory
cp McClaude.jar /path/to/minecraft-server/plugins/

# Restart the server — the plugin generates config at plugins/McClaude/config.yml
```

After first run, edit `plugins/McClaude/config.yml` to set your encryption secret and port:

```yaml
port: 25580
secret: "your-strong-random-secret-here"
```

### 2. Configure Claude Code MCP Server

Add this to your Claude Code MCP config (`~/.claude.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "mcclaude": {
      "command": "npx",
      "args": ["mcclaude-mcp"],
      "env": {
        "MCCLAUDE_HOST": "your-server-ip-or-localhost",
        "MCCLAUDE_PORT": "25580",
        "MCCLAUDE_SECRET": "your-strong-random-secret-here"
      }
    }
  }
}
```

The `MCCLAUDE_SECRET` must match the one in your server's `config.yml`.

### 3. Install as a Claude Code Skill (optional)

To get trigger-phrase activation, drop the skill file:

```bash
mkdir -p ~/.claude/skills/mcclaude_minecraft_dev_bridge
cp SKILL.md ~/.claude/skills/mcclaude_minecraft_dev_bridge/SKILL.md
```

**Trigger phrases:** "minecraft plugin development", "minecraft server bridge", "mcclaude", "skript editing", "minecraft console MCP", "minecraft eval"

---

## First 60 Seconds

Once MCP is configured and the server is running:

**You say:** "Read the server console"

**Claude does:** Calls the `read_console` MCP tool, returns live log lines:
```
[Server] Done (3.241s)! For help, type "help"
[Skript] Loaded 4 scripts with 12 triggers and 3 commands
[Server] Steve joined the game
```

**You say:** "List all Skript files and show me welcome.sk"

**Claude does:** Calls `list_scripts` then `read_script`:
```
Files: welcome.sk, shop.sk, anticheat.sk, events.sk

welcome.sk:
  on join:
      send "&aWelcome to the server, %player%!" to player
      broadcast "&e%player% &7has joined the game"
```

**You say:** "Add a sound effect when players join"

**Claude does:** Calls `write_script` with updated content, then `run_command` with `/sk reload welcome`:
```
Script saved: welcome.sk
[Skript] Reloaded welcome.sk successfully
```

The change is live immediately — next player who joins hears the sound.

---

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `read_console` | Stream live server console output |
| `run_command` | Execute any Minecraft server command |
| `list_scripts` | List all .sk Skript files on the server |
| `read_script` | Read the contents of a Skript file |
| `write_script` | Write/update a Skript file on the server |
| `eval` | Evaluate Java/Groovy code on the running server |

## Security

- All traffic is **AES-256-GCM encrypted** between Claude Code and the server
- Never commit `MCCLAUDE_SECRET` to version control — use environment variables
- The plugin exposes a WebSocket + WebDAV interface — firewall port 25580 to trusted IPs only
