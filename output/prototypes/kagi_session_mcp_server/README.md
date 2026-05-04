# Kagi Session MCP Server

**Free Kagi Search and Summarizer as MCP tools — no API key, just your browser session cookie.**

Drop this MCP server into Claude Desktop, Cursor, Windsurf, or Claude Code and get ad-free Kagi search results and AI-powered summaries directly in your agent workflow. Uses your existing Kagi subscription via a session token extracted from browser cookies — zero extra billing.

## Headline result

```
$ bash run.sh

Kagi Session MCP Server — DEMO (mock data)
============================================================

[Tool: kagi_search]
  Query: 'Model Context Protocol'

  1. Kagi Search Result 1 for 'Model Context Protocol'
     Kagi delivers high-quality, ad-free results...
  2. Wikipedia — Model Context Protocol
     An encyclopedic overview of Model Context Protocol...
  3. GitHub — Open-source projects related to Model Context Protocol
     Browse repositories, libraries, and tools...

[Tool: kagi_summarize]
  Input: 'https://modelcontextprotocol.io'

  Key points:
  - Kagi's summarizer uses advanced AI to distill content
  - Supports URLs (web pages, articles, PDFs) and raw text
  - No API key billing — uses your existing Kagi subscription
```

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, and run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
