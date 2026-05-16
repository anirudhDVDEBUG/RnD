# Technical Details — Anansi Self-Healing Scraper

## What It Does

Anansi is a Python web scraper designed for "hostile" sites — pages that frequently change their HTML structure, deploy anti-bot measures, or require JavaScript rendering. Its core innovation is **self-healing selectors**: when a CSS selector stops matching (e.g., `.product-name` becomes `.item-title` after a redesign), Anansi automatically searches for semantically similar elements using heuristics — class-name substring matching, HTML tag patterns, and attribute probing — and repairs the selector without human intervention.

When simple HTTP requests fail (403, CAPTCHA walls, empty responses), Anansi **automatically upgrades** to headless browser rendering via Playwright. It mimics real Chrome TLS handshakes (JA3 fingerprinting) so that the TLS layer itself doesn't reveal the scraper as a bot — a technique that defeats fingerprint-based WAFs like Cloudflare, Akamai, and DataDome.

## Architecture

```
User / LLM (via MCP)
    |
    v
Anansi Core
    |--- HTTP layer (requests + TLS fingerprint spoofing)
    |--- Browser layer (Playwright, stealth patches)
    |--- Selector engine
    |       |--- CSS matching (BeautifulSoup / lxml)
    |       |--- Self-healing (heuristic fallback search)
    |       |--- Pydantic output validation
    |--- MCP Server (exposes scrape/crawl tools)
```

**Key files in the source repo:**
- `anansi/core.py` — Main `Anansi` class, orchestrates fetch -> parse -> heal -> validate
- `anansi/selectors.py` — Self-healing selector engine with heuristic fallback
- `anansi/stealth.py` — TLS fingerprint spoofing, user-agent rotation, browser patches
- `anansi/browser.py` — Playwright-based headless browser with anti-detection
- `anansi/mcp.py` — MCP server implementation (tool definitions, request handling)
- `anansi/models.py` — Pydantic models for structured output

**Data flow:**
1. User provides URL + CSS selectors (or LLM sends MCP tool call)
2. Anansi fetches via HTTP first (fast path)
3. If blocked (status 403, empty body, JS-only content), upgrades to Playwright browser
4. Parses HTML, applies selectors
5. If selector fails: runs self-healing — probes heuristic alternatives
6. Returns structured data (Pydantic-validated) + healing log

**Dependencies:**
- `requests` — HTTP client
- `beautifulsoup4` / `lxml` — HTML parsing
- `playwright` — Headless browser (optional, for stealth mode)
- `pydantic` — Output validation
- `tls-client` or custom TLS — Chrome fingerprint spoofing

## Limitations

- **Self-healing is heuristic, not magic.** It works well for common patterns (prices, names, links) but can fail on highly unusual DOM structures. It doesn't use LLM-based selector repair (though that could be layered on).
- **No CAPTCHA solving.** Anansi evades detection but does not solve CAPTCHAs. If a site presents one, the scrape fails.
- **Stealth mode requires Playwright.** The full anti-bot evasion needs `playwright install chromium` — adds ~200MB. HTTP-only mode works without it.
- **No distributed crawling.** Single-machine only. For large-scale crawls, you'd need to orchestrate multiple instances.
- **MCP server is single-tenant.** One scraper instance per MCP connection. No built-in queue or rate-limiting across multiple LLM sessions.
- **Legal/ethical use required.** Scraping may violate site ToS. The user is responsible for compliance.

## Why It Matters for Claude-Driven Products

| Use Case | How Anansi Helps |
|---|---|
| **Lead generation** | Scrape prospect data (pricing, contact info, product listings) from competitor sites that actively block bots. Self-healing means the pipeline doesn't break when sites update. |
| **Marketing / Ad creatives** | Pull real-time product data, reviews, and pricing to feed into ad-copy generators. MCP integration means Claude can drive the scrape inline. |
| **Agent factories** | Any autonomous agent that needs web data can use Anansi's MCP server as a reliable web-access tool — more robust than raw HTTP because of self-healing + stealth. |
| **Competitive intelligence** | Monitor competitor product pages, pricing changes, and inventory status with selectors that survive site redesigns. |
| **Content aggregation** | Build curated feeds by scraping multiple sources. Self-healing reduces maintenance overhead from the typical selector-breakage treadmill. |

The MCP server integration is the key differentiator: it turns web scraping from a "write a script" task into a conversational tool that any LLM agent can invoke on demand.
