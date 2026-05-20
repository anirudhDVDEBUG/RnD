# web-researcher-mcp

**A Go-based MCP server that gives Claude (and any MCP client) web search, content extraction, academic/patent/news research -- all through a single server with multi-provider routing and 4-tier scraping.**

> **Headline result:** Ask Claude "search for recent breakthroughs in solid-state batteries" and it fans out across Brave Search, SearXNG, or academic indexes, scrapes the top results through 4 progressively aggressive extraction tiers, and hands back clean, structured text -- no browser tab required.

---

| Doc | What's inside |
|-----|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, MCP config JSON, first-60-seconds walkthrough |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, build-vs-buy analysis |

## Quick demo (no API keys needed)

```bash
bash run.sh
```

Runs a local Python simulation of the six MCP tools (`web_search`, `extract_content`, `academic_search`, `patent_search`, `news_search`, `search_lenses`) using mock data, so you can see the shape of responses before wiring up real keys.

## Source

<https://github.com/zoharbabin/web-researcher-mcp>
