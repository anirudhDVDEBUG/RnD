# WPVibe AI — WordPress MCP Server

**TL;DR:** WPVibe is a WordPress plugin that turns any self-hosted WordPress site into an MCP server. Claude Code (or any MCP client) can then create/edit posts, modify theme files, run WP-CLI commands, and call the REST API — all through natural language.

**Headline result:** Ask Claude "create a draft post titled 'Summer Sale' in the Marketing category" and it appears in your WordPress dashboard, ready to publish — no browser, no wp-admin, no copy-paste.

---

| File | What it covers |
|------|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install the plugin, configure MCP, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, relevance to AI products |
| `run.sh` | Run `bash run.sh` for a mock demo (no WordPress needed) |

## Quick demo

```bash
bash run.sh
```

Starts a mock WordPress MCP server on `localhost:3100` and exercises all 12 tools with realistic output. No API keys or WordPress install required.

## Source

- **GitHub:** https://github.com/awesomemotive/wpvibe-ai-mcp
- **WordPress.org:** Search "Vibe AI" by Awesome Motive
