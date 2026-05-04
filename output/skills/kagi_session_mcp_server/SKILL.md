---
name: kagi_session_mcp_server
description: |
  Set up and configure Kagi-Session2API-MCP server for free Kagi Search and Summarizer access via session tokens.
  TRIGGER when: user wants to add Kagi search to MCP, use Kagi without API key, set up Kagi session-based search, configure Kagi MCP server, or integrate Kagi with Claude Desktop/Cursor/Windsurf.
  DO NOT TRIGGER when: user asks about other search providers, paid Kagi API key setup, or unrelated MCP servers.
---

# Kagi Session2API MCP Server

Set up a free Kagi Search MCP server that uses session tokens instead of API keys to access Kagi Search and Summarizer tools.

## When to use

- "Add Kagi search to my MCP setup"
- "I want to use Kagi search without an API key"
- "Set up Kagi MCP server for Claude Desktop"
- "Configure Kagi session-based search in Cursor"
- "How do I get Kagi summarizer working with MCP?"

## How to use

### 1. Clone and install the server

```bash
git clone https://github.com/KSroido/Kagi-Session2API-MCP.git
cd Kagi-Session2API-MCP
pip install -r requirements.txt
```

### 2. Get your Kagi session token

1. Log in to [kagi.com](https://kagi.com) in your browser
2. Open Developer Tools (F12) → Application/Storage → Cookies
3. Copy the value of the `kagi_session` cookie

### 3. Configure environment

Create a `.env` file or set the environment variable:

```bash
KAGI_SESSION_TOKEN=your_session_token_here
```

### 4. Add to MCP client configuration

For Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kagi-search": {
      "command": "python",
      "args": ["path/to/Kagi-Session2API-MCP/server.py"],
      "env": {
        "KAGI_SESSION_TOKEN": "your_session_token_here"
      }
    }
  }
}
```

For Claude Code (`.mcp.json` in project root):

```json
{
  "mcpServers": {
    "kagi-search": {
      "command": "python",
      "args": ["path/to/Kagi-Session2API-MCP/server.py"],
      "env": {
        "KAGI_SESSION_TOKEN": "your_session_token_here"
      }
    }
  }
}
```

### 5. Available tools

Once configured, the MCP server provides:

- **kagi_search** — Perform web searches via Kagi
- **kagi_summarize** — Summarize URLs or text using Kagi's summarizer

### Important notes

- Session tokens expire periodically; you'll need to refresh them from your browser cookies
- This uses your existing Kagi subscription — no separate API billing
- Works with any MCP-compatible client (Claude Desktop, Cursor, Windsurf, Hermes, etc.)

## References

- Source repository: https://github.com/KSroido/Kagi-Session2API-MCP
- MCP specification: https://modelcontextprotocol.io
