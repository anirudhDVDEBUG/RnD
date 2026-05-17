---
name: taw_computer_mcp_sandbox
description: |
  Set up and use the taw-computer MCP server to give AI agents a real Ubuntu computer sandbox with browser automation, desktop control, and 30+ tools.
  TRIGGER when: user wants computer-use capabilities, browser automation via MCP, desktop sandbox for AI, screen interaction tools, or Playwright-based web automation in a Docker container.
  DO NOT TRIGGER when: user wants simple local shell commands, non-MCP browser testing, or standard Playwright without sandboxing.
---

# TAW Computer MCP Server

Give any AI a real computer. Open source MCP server with Ubuntu sandbox, browser automation, desktop control, and 30+ tools. Works with Claude Code, Cursor, and Claude Desktop.

## When to use

- "I need to give my AI agent access to a real computer environment"
- "Set up browser automation with an MCP server in a sandbox"
- "I want desktop control and screen interaction tools for Claude"
- "How do I run computer-use in a Docker container with MCP?"
- "I need a sandboxed Ubuntu environment my AI can control"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/the-agents-work/taw-computer.git
cd taw-computer
npm install
```

### 2. Build and start the Docker sandbox

```bash
docker compose up -d
```

This launches an Ubuntu desktop environment with VNC access and all automation tools pre-installed.

### 3. Configure as MCP server

Add to your Claude Code MCP settings (`.claude/settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "taw-computer": {
      "command": "npx",
      "args": ["-y", "@the-agents-work/taw-computer"],
      "env": {}
    }
  }
}
```

Or for local development:

```json
{
  "mcpServers": {
    "taw-computer": {
      "command": "node",
      "args": ["path/to/taw-computer/dist/index.js"]
    }
  }
}
```

### 4. Available capabilities

The server provides 30+ tools across these categories:

- **Browser automation**: Navigate, click, type, screenshot, extract content (Playwright-based)
- **Desktop control**: Mouse movement, keyboard input, screen capture
- **File operations**: Read, write, list files in the sandbox
- **Shell execution**: Run commands in the sandboxed Ubuntu environment
- **Window management**: Focus, resize, list open windows

### 5. Usage patterns

Once configured, ask Claude to:
- Browse websites and extract information
- Fill out forms and interact with web UIs
- Take screenshots and analyze screen content
- Run desktop applications in the sandbox
- Automate multi-step workflows involving GUI interaction

## Key details

- **Language**: TypeScript
- **Sandbox**: Docker-based Ubuntu with VNC
- **Browser engine**: Playwright (Chromium)
- **Protocol**: Model Context Protocol (MCP)
- **Security**: All actions run inside an isolated container

## References

- Repository: https://github.com/the-agents-work/taw-computer
- Topics: MCP, computer-use, browser-automation, sandbox, desktop-automation, Docker, Playwright
