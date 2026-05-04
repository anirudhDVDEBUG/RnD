# How to Use — Kagi Session MCP Server

## Install

```bash
git clone https://github.com/KSroido/Kagi-Session2API-MCP.git
cd Kagi-Session2API-MCP
pip install -r requirements.txt   # no external deps, stdlib only
```

Or use this prototype directly:

```bash
cd kagi_session_mcp_server
python3 server.py --demo   # verify it runs
```

**Python 3.10+** required. No pip packages needed.

## Get your Kagi session token

1. Log in to [kagi.com](https://kagi.com)
2. Open DevTools (F12) > Application > Cookies > `kagi.com`
3. Copy the value of the `kagi_session` cookie

## MCP server configuration

### Claude Code (recommended)

Add to `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "kagi-search": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "KAGI_SESSION_TOKEN": "your_kagi_session_cookie_value"
      }
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kagi-search": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "KAGI_SESSION_TOKEN": "your_kagi_session_cookie_value"
      }
    }
  }
}
```

### Cursor / Windsurf

Same JSON format — add to the MCP servers section of your editor's config.

## As a Claude Code Skill

To install as a reusable skill:

```bash
mkdir -p ~/.claude/skills/kagi_session_mcp_server
cp SKILL.md ~/.claude/skills/kagi_session_mcp_server/SKILL.md
```

Trigger phrases:
- "Add Kagi search to my MCP setup"
- "Set up Kagi MCP server for Claude Desktop"
- "Configure Kagi session-based search in Cursor"
- "I want to use Kagi search without an API key"

## First 60 seconds

**Input (demo mode, no token needed):**

```bash
bash run.sh
```

**Output:**

```
Kagi Session MCP Server — DEMO (mock data)
============================================================

[Tool: kagi_search]
  Query: 'Model Context Protocol'

  1. Kagi Search Result 1 for 'Model Context Protocol'
     Kagi delivers high-quality, ad-free results for 'Model Context Protocol'...
     https://example.com/result1?q=Model+Context+Protocol

  2. Wikipedia — Model Context Protocol
     An encyclopedic overview of Model Context Protocol...
     https://en.wikipedia.org/wiki/Model_Context_Protocol

  3. GitHub — Open-source projects related to Model Context Protocol
     Browse repositories, libraries, and tools...
     https://github.com/search?q=Model+Context+Protocol

[Tool: kagi_summarize]
  Input: 'https://modelcontextprotocol.io'

  [DEMO MODE — Summary of: https://modelcontextprotocol.io]

  Key points:
  - Kagi's summarizer uses advanced AI to distill content into concise summaries
  - Supports URLs (web pages, articles, PDFs) and raw text input
  - Available summary types: summary, key_moments, takeaway
  - No API key billing — uses your existing Kagi subscription via session cookie
```

**Input (live mode with token):**

```bash
KAGI_SESSION_TOKEN="abc123..." python3 server.py --demo
```

Returns real Kagi search results and AI summaries from your subscription.

## Available MCP tools

| Tool | Description | Required params |
|------|-------------|-----------------|
| `kagi_search` | Web search via Kagi | `query` (string) |
| `kagi_summarize` | Summarize URL or text | `url_or_text` (string) |

Optional params: `limit` (int, default 5) for search; `summary_type` ("summary" / "key_moments" / "takeaway") for summarize.
