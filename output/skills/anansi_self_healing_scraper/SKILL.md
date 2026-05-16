---
name: anansi_self_healing_scraper
description: |
  Self-healing web scraper with anti-bot evasion via Anansi. Triggers: "scrape a website", "extract data from a hostile site", "self-healing scraper", "stealth browser scraping", "set up anansi", "MCP scraper server", "crawl with anti-bot", "TLS fingerprint scraping".
---

# Anansi Self-Healing Web Scraper

A self-healing web scraper built for hostile sites. Selectors repair themselves, browser rendering kicks in when needed, and Chrome TLS fingerprinting evades bot detection. Ships with an MCP server so any LLM can drive a full crawl through conversation.

## When to use

- "Scrape data from a website that blocks bots"
- "Set up a self-healing web scraper"
- "Use Anansi to crawl and extract structured data"
- "Configure the Anansi MCP server for web scraping"
- "Extract content from a site with anti-bot protection"

## How to use

### 1. Install Anansi

```bash
pip install anansi-scraper
```

Or clone and install from source:

```bash
git clone https://github.com/mdowis/anansi.git
cd anansi
pip install -e .
```

### 2. Use as a Python library

```python
from anansi import Anansi

# Basic scraping - selectors self-heal if the page structure changes
scraper = Anansi()
result = scraper.scrape("https://example.com", selectors={
    "title": "h1",
    "content": ".main-content",
    "links": "a[href]"
})
print(result)
```

### 3. Use stealth browser mode for hostile sites

Anansi automatically upgrades to browser rendering when simple HTTP requests are blocked. It uses Chrome TLS fingerprinting to evade bot detection:

```python
from anansi import Anansi

scraper = Anansi(stealth=True)
result = scraper.scrape("https://hostile-site.com", selectors={
    "price": ".product-price",
    "name": ".product-name"
})
```

### 4. Run as an MCP server

Anansi ships with an MCP server so Claude or any LLM can drive scraping through conversation:

```bash
# Start the MCP server
anansi serve
```

Add to your Claude Code MCP config (`~/.claude/settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "anansi": {
      "command": "anansi",
      "args": ["serve"]
    }
  }
}
```

### 5. Key features

- **Self-healing selectors**: CSS selectors automatically repair themselves when page structure changes
- **Adaptive rendering**: Starts with fast HTTP requests, upgrades to headless browser when needed
- **Chrome TLS fingerprinting**: Mimics real Chrome TLS handshakes to evade bot detection
- **Stealth browser**: Full browser rendering with anti-detection measures
- **Pydantic models**: Structured, validated output using Pydantic
- **MCP server**: Expose scraping tools to any LLM via Model Context Protocol
- **Crawl orchestration**: Full site crawling with depth control and link following

### 6. Configuration options

```python
scraper = Anansi(
    stealth=True,           # Enable stealth browser mode
    headless=True,          # Run browser headlessly
    max_retries=3,          # Retry on failure
    timeout=30,             # Request timeout in seconds
)
```

## References

- **Repository**: https://github.com/mdowis/anansi
- **Topics**: web-scraping, mcp-server, anti-bot, self-healing, stealth-browser, tls-fingerprint, pydantic, python
- **Language**: Python
