# Anansi Self-Healing Web Scraper

A self-healing web scraper that automatically repairs broken CSS selectors when sites redesign, upgrades to headless browser rendering when HTTP requests get blocked, and mimics Chrome TLS fingerprints to evade bot detection. Ships with an MCP server so Claude can drive scraping via conversation.

**Headline result:** Same selectors, redesigned page — Anansi self-heals all 3 broken selectors and extracts 3/3 products with zero manual fixes.

```
[HEALED] '.product-name' -> '[class*='title']' (2 attempts)
[HEALED] '.product-price' -> '[class*='pricing']' (2 attempts)
[HEALED] '.stock-status' -> '[class*='stock']' (1 attempts)
```

## Quick start

```bash
bash run.sh
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, configure MCP, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations

## Source

https://github.com/mdowis/anansi
