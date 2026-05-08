# Thunderbit Web Scraper

AI-powered web scraping and structured data extraction via MCP server, CLI, or Claude Code plugin. Point it at any URL, optionally specify fields (e.g. `name, price, rating`), and get back clean structured JSON or markdown — no CSS selectors or XPath required.

**Headline result:** Extract a typed product catalog from any e-commerce page in one tool call:

```
extract_data("https://store.example.com/widgets", fields=["name","price","in_stock"])
→ 3 rows, JSON, <2 seconds
```

---

- **Quick setup & usage** -- see [HOW_TO_USE.md](HOW_TO_USE.md)
- **Architecture & limitations** -- see [TECH_DETAILS.md](TECH_DETAILS.md)
- **Live demo (mock, no API key)** -- `bash run.sh`
- **Source repo** -- [thunderbit-open/thunderbit-mcp-server](https://github.com/thunderbit-open/thunderbit-mcp-server)
