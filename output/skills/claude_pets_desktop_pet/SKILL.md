---
name: claude_pets_desktop_pet
description: |
  Set up Claude Pets (OpenPets integration) for automatic desktop pet status updates during Claude Code sessions.
  TRIGGER: user mentions "claude pets", "desktop pet", "openpets", "pet status", "coding pet companion"
---

# Claude Pets – Desktop Pet Integration for Claude Code

Integrate [claude-pets](https://github.com/alvinunreal/claude-pets) with Claude Code to get a live desktop pet that reacts to your coding activity. The pet updates its status automatically based on Claude Code hooks and MCP server events.

## When to use

- "Set up a desktop pet for Claude Code"
- "Install claude-pets so my pet reacts while I code"
- "Configure OpenPets with Claude Code hooks"
- "I want a coding companion pet on my desktop"
- "How do I connect claude-pets to my Claude Code session?"

## How to use

### 1. Prerequisites

- [OpenPets](https://openpets.dev) desktop app installed and running
- [Bun](https://bun.sh) runtime installed (`curl -fsSL https://bun.sh/install | bash`)
- Claude Code installed and configured

### 2. Install claude-pets

```bash
# Clone the repo
git clone https://github.com/alvinunreal/claude-pets.git
cd claude-pets

# Install dependencies
bun install
```

### 3. One-command setup

The easiest way to get started is the automated setup script which configures both hooks and the MCP server:

```bash
bun run setup
```

This will:
- Register Claude Code hooks that fire on tool calls and session events
- Configure the MCP server for bidirectional communication with OpenPets
- Link your desktop pet to your Claude Code session

### 4. Manual configuration (alternative)

If you prefer manual setup, add the hooks to your Claude Code `settings.json`:

```json
{
  "hooks": {
    "on_tool_call": [
      {
        "command": "bun run /path/to/claude-pets/hooks/on_tool_call.ts"
      }
    ],
    "on_session_start": [
      {
        "command": "bun run /path/to/claude-pets/hooks/on_session_start.ts"
      }
    ],
    "on_session_end": [
      {
        "command": "bun run /path/to/claude-pets/hooks/on_session_end.ts"
      }
    ]
  }
}
```

And add the MCP server:

```json
{
  "mcpServers": {
    "claude-pets": {
      "command": "bun",
      "args": ["run", "/path/to/claude-pets/src/mcp-server.ts"]
    }
  }
}
```

### 5. Verify

Start a new Claude Code session. Your desktop pet should wake up and begin reacting to your coding activity (thinking when Claude is processing, celebrating on successful tool calls, etc.).

## How it works

- **Hooks**: Claude Code lifecycle hooks (`on_tool_call`, `on_session_start`, `on_session_end`) send status updates to OpenPets, so your pet reacts in real time.
- **MCP Server**: A TypeScript MCP server provides tools for Claude to optionally interact with the pet directly (e.g., send custom status messages).
- **Built with Bun + TypeScript** for fast startup and minimal overhead.

## References

- Source: [alvinunreal/claude-pets](https://github.com/alvinunreal/claude-pets)
- Desktop app: [OpenPets](https://openpets.dev)
- Topics: ai-agents, bun, claude-code, desktop-pet, hooks, mcp, openpets, typescript
