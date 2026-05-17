# How to Use taw-computer MCP Server

## Install Steps

```bash
# 1. Clone the repo
git clone https://github.com/the-agents-work/taw-computer.git
cd taw-computer

# 2. Install dependencies
npm install

# 3. Start the Docker sandbox (requires Docker)
docker compose up -d
```

This launches an Ubuntu 22.04 desktop with VNC, Playwright/Chromium, and all automation tools pre-installed.

## MCP Server Configuration

Paste this into your `~/.claude.json` under the `mcpServers` block:

```json
{
  "taw-computer": {
    "command": "npx",
    "args": ["-y", "@the-agents-work/taw-computer"],
    "env": {}
  }
}
```

For local development (if you cloned the repo):

```json
{
  "taw-computer": {
    "command": "node",
    "args": ["/path/to/taw-computer/dist/index.js"]
  }
}
```

After adding the config, restart Claude Code. The server will appear in your MCP tool list.

## First 60 Seconds

Once the Docker container is running and MCP is configured:

**Input (ask Claude):**
> "Go to https://news.ycombinator.com, take a screenshot, and extract the top 5 story titles."

**What happens:**
1. Claude calls `browser_navigate` → opens HN in the sandboxed Chromium
2. Claude calls `browser_screenshot` → captures the page as PNG
3. Claude calls `browser_get_text` with selector `.titleline` → extracts story titles
4. Claude presents the screenshot and text to you

**Output you see:**
```
Here are the top 5 Hacker News stories:
1. Show HN: I built an open-source MCP server for computer control
2. The future of AI agents is sandboxed environments
3. Docker-based development environments are eating the world
...

[Screenshot attached showing the Hacker News homepage]
```

## Trigger Phrases (if using as a Claude Skill)

Drop the skill folder into `~/.claude/skills/taw_computer_mcp_sandbox/` and it activates on:

- "Give my AI agent access to a real computer"
- "Set up browser automation with MCP in a sandbox"
- "I need desktop control and screen interaction tools"
- "Run computer-use in a Docker container"
- "Sandboxed Ubuntu environment my AI can control"

## Verifying It Works

```bash
# Check the Docker container is running
docker ps | grep taw-computer

# Access VNC to see the desktop (default port 6080)
open http://localhost:6080

# Test a tool directly via the MCP inspector
npx @the-agents-work/taw-computer --inspect
```
