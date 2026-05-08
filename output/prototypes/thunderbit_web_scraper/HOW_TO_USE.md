# How to Use Thunderbit Web Scraper

## Install

```bash
npm install -g thunderbit-mcp-server
```

Or from source:

```bash
git clone https://github.com/thunderbit-open/thunderbit-mcp-server.git
cd thunderbit-mcp-server
npm install
```

## Get an API key

1. Create an account at [thunderbit.com](https://www.thunderbit.com).
2. Go to account settings and generate an API key.
3. Export it:

```bash
export THUNDERBIT_API_KEY=tb_live_abc123...
```

## Configure as MCP server (Claude Code)

Add this block to `.mcp.json` in your project root (or `~/.claude.json` for global):

```json
{
  "mcpServers": {
    "thunderbit": {
      "command": "npx",
      "args": ["thunderbit-mcp-server"],
      "env": {
        "THUNDERBIT_API_KEY": "tb_live_abc123..."
      }
    }
  }
}
```

For **Claude Desktop**, put the same `mcpServers` block in `claude_desktop_config.json`.

## Configure as Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/thunderbit_web_scraper
cp SKILL.md ~/.claude/skills/thunderbit_web_scraper/SKILL.md
```

Trigger phrases that activate the skill:

- "Scrape this webpage and extract structured data"
- "Set up Thunderbit MCP server for web scraping"
- "Extract product names and prices from this URL"
- "Use Thunderbit to convert a webpage to markdown"

## Available MCP tools

| Tool | Description |
|------|-------------|
| `scrape_url` | Scrape a webpage and return content as markdown |
| `extract_data` | Extract specific structured fields from a URL using AI |

### `scrape_url` parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | The webpage URL to scrape |

### `extract_data` parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | The webpage URL to scrape |
| `fields` | string[] | no | Field names to extract (e.g. `["title","price"]`). Omit for auto-detect. |

## CLI usage

```bash
# Scrape a URL to markdown
npx thunderbit-mcp-server scrape https://example.com

# Extract structured data with custom fields
npx thunderbit-mcp-server extract https://example.com --fields "title,price,description"
```

## First 60 seconds

Run the local demo (no API key needed):

```bash
bash run.sh
```

**Input:** The demo calls `scrape_url` and `extract_data` against mock product and blog pages.

**Output preview:**

```
[1] scrape_url("https://example.com/products")
──────────────────────────────────────────────
# Acme Widget Store
## Products
### Ultra Widget Pro
- Price: $49.99
- Rating: 4.8/5 (2,341 reviews)
...

[2] extract_data("https://example.com/products", fields=["name","price","rating","in_stock"])
──────────────────────────────────────────────
{
  "success": true,
  "row_count": 3,
  "data": [
    { "name": "Ultra Widget Pro", "price": "$49.99", "rating": "4.8/5", "in_stock": true },
    { "name": "Mini Widget Lite", "price": "$19.99", "rating": "4.5/5", "in_stock": true },
    { "name": "Widget Enterprise X", "price": "$199.99", "rating": "4.9/5", "in_stock": false }
  ]
}
```

With a real API key, replace the mock URLs with any live webpage URL and get the same structured output.
