# How to Use OpenPets

## Install the real OpenPets app

```bash
# Requires Bun (https://bun.sh)
curl -fsSL https://bun.sh/install | bash

# Clone and install
git clone https://github.com/alvinunreal/openpets.git
cd openpets
bun install

# Launch the desktop pet (Electron window)
bun run start
```

The pet appears as an always-on-top pixel-art sprite on your desktop.

## Connect Claude Code via MCP

Add this to your Claude Code MCP config (`~/.claude.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "openpets": {
      "command": "bun",
      "args": ["run", "/absolute/path/to/openpets/src/mcp-server.ts"]
    }
  }
}
```

Replace `/absolute/path/to/openpets` with the actual clone location.

After restarting Claude Code, the MCP tools (`set_pet_status`, `get_pet_status`, `list_pets`, `set_pet_character`) become available. Claude Code can then automatically update your pet's animation state as it works.

## First 60 seconds

```
# Terminal 1 — start the pet
cd openpets && bun run start
# → Electron window appears with pixel-art cat sitting idle on desktop

# Terminal 2 — start Claude Code in any project
claude
# → Claude Code detects the openpets MCP server
# → As Claude thinks, the pet tilts its head
# → As Claude writes code, the pet types on a keyboard
# → If an error occurs, the pet shows an alert animation
# → On success, the pet celebrates with sparkles
```

## Running this demo (no Electron needed)

```bash
bash run.sh
```

This runs a Node.js simulation showing:
1. The MCP tool definitions OpenPets exposes
2. Available pet characters
3. A full agent session driving the pet through all states with ASCII animations
4. The MCP config snippet for Claude Code

## Skill installation (optional)

To install as a Claude Code skill so Claude knows when to mention OpenPets:

```bash
mkdir -p ~/.claude/skills/openpets_desktop_pet_mcp
cp SKILL.md ~/.claude/skills/openpets_desktop_pet_mcp/SKILL.md
```

Trigger phrases: "set up a desktop pet", "OpenPets MCP", "pixel-art coding companion", "visualize agent status".
