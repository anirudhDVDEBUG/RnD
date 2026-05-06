---
name: openpets_desktop_pet_mcp
description: |
  Set up OpenPets desktop pets for AI coding agents. Install pixel-art pets that show live coding status on your desktop via MCP server integration with Claude Code.
  TRIGGER when: user wants desktop pets, wants to visualize coding agent status, asks about OpenPets, wants MCP pet integration, or wants pixel-art companions for coding.
  DO NOT TRIGGER when: unrelated to desktop pets or OpenPets.
---

# OpenPets Desktop Pet MCP Integration

Set up and configure [OpenPets](https://github.com/alvinunreal/openpets) — desktop pets for AI coding agents that display live coding status via MCP.

## When to use

- "Set up a desktop pet for Claude Code"
- "I want OpenPets with MCP integration"
- "Show me how to install desktop pets that react to my coding agent"
- "Configure OpenPets MCP server"
- "Add a pixel-art pet that shows coding status"

## How to use

### 1. Install OpenPets

```bash
# Clone the repository
git clone https://github.com/alvinunreal/openpets.git
cd openpets

# Install dependencies (uses Bun)
bun install

# Start the Electron desktop pet app
bun run start
```

### 2. Connect Claude Code via MCP

Add the OpenPets MCP server to your Claude Code configuration (`.claude/settings.json` or project-level):

```json
{
  "mcpServers": {
    "openpets": {
      "command": "bun",
      "args": ["run", "/path/to/openpets/src/mcp-server.ts"]
    }
  }
}
```

### 3. Usage

Once connected, the desktop pet will visually react to coding agent activity:
- Shows idle/thinking/coding/error states
- Pixel-art animations reflect live status
- Pet stays on top of your desktop as a companion

### Key details

- **Runtime**: Bun + Electron + TypeScript
- **Protocol**: Model Context Protocol (MCP) for agent communication
- **Pets**: Pixel-art style, installable/swappable
- **Compatible agents**: Claude Code, OpenCode, and other MCP-aware agents

## References

- Repository: https://github.com/alvinunreal/openpets
- Topics: desktop-pet, mcp-server, electron, pixel-art, claude-code, ai-agents
