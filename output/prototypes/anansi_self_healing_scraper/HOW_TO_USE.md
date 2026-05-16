# How to Use Anansi

## Install

### Option A: pip (recommended)

```bash
pip install anansi-scraper
```

### Option B: From source

```bash
git clone https://github.com/mdowis/anansi.git
cd anansi
pip install -e .
```

### Option C: This demo (no install needed)

```bash
pip install beautifulsoup4 requests
python3 demo_scraper.py
```

## Configure as MCP Server

Add to `~/.claude.json` (global) or project `.mcp.json`:

```json
{
  "mcpServers": {
    "anansi": {
      "command": "anansi",
      "args": ["serve"],
      "env": {}
    }
  }
}
```

After adding, restart Claude Code. The MCP server exposes scraping tools that Claude can invoke directly in conversation — e.g. "scrape the top 10 products from example-shop.com".

No API keys are needed. The MCP server runs locally.

## Use as a Claude Skill

Drop the skill into your skills directory:

```bash
mkdir -p ~/.claude/skills/anansi_self_healing_scraper
cp SKILL.md ~/.claude/skills/anansi_self_healing_scraper/SKILL.md
```

**Trigger phrases:**
- "Scrape data from a website that blocks bots"
- "Set up a self-healing web scraper"
- "Use Anansi to crawl and extract structured data"
- "Configure the Anansi MCP server for web scraping"
- "Extract content from a site with anti-bot protection"

## First 60 Seconds

### 1. Run the demo

```bash
bash run.sh
```

**Input:** Two mock e-commerce pages — same products, different HTML structure (simulating a site redesign).

**Output:**

```
DEMO 1: Normal Scrape (selectors match)
  Extracted 3 items in 2ms
  {"name": "Wireless Headphones", "price": "$79.99", "status": "In Stock"}
  {"name": "Mechanical Keyboard", "price": "$149.00", "status": "In Stock"}
  {"name": "USB-C Hub", "price": "$34.50", "status": "Out of Stock"}
  Selector healing needed: 0 repairs

DEMO 2: Site Redesign — Self-Healing Selectors
  Using SAME selectors on redesigned page (classes changed)...
  Extracted 3 items in 3ms
  [HEALED] '.product-name' -> '[class*='title']' (2 attempts)
  [HEALED] '.product-price' -> '[class*='pricing']' (2 attempts)
  [HEALED] '.stock-status' -> '[class*='stock']' (1 attempts)
```

### 2. Use as a Python library

```python
from anansi import Anansi

scraper = Anansi(stealth=True)
result = scraper.scrape("https://example.com", selectors={
    "title": "h1",
    "content": ".main-content",
    "links": "a[href]"
})
print(result)
```

### 3. Use via MCP (after configuring above)

Just tell Claude:
> "Scrape the product names and prices from https://example-shop.com/products"

Claude will invoke the Anansi MCP tools automatically.

## Configuration Options

```python
scraper = Anansi(
    stealth=True,        # Chrome TLS fingerprinting + anti-detection
    headless=True,        # Run browser headlessly (default: True)
    max_retries=3,        # Retry on failure
    timeout=30,           # Request timeout in seconds
)
```
