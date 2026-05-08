---
name: thunderbit_web_scraper
description: |
  Set up and use Thunderbit MCP server for AI-powered web scraping and structured data extraction.
  TRIGGER when: user wants to scrape web pages with AI, extract structured data from URLs, set up Thunderbit MCP server, use Thunderbit CLI for web scraping, or configure Thunderbit as a Claude Code plugin.
  DO NOT TRIGGER when: user asks about other scraping tools (Puppeteer, Playwright, Cheerio), non-web data extraction, or unrelated MCP servers.
---

# Thunderbit Web Scraper MCP Server

AI-powered web scraping and structured data extraction via CLI, MCP server, or Claude Code plugin using the Thunderbit Open API.

## When to use

- "Scrape this webpage and extract structured data"
- "Set up Thunderbit MCP server for web scraping"
- "Extract product names and prices from this URL"
- "Configure an AI-powered web scraper in my MCP setup"
- "Use Thunderbit to convert a webpage to markdown"

## How to use

### 1. Get a Thunderbit API key

1. Visit [thunderbit.com](https://www.thunderbit.com) and create an account
2. Navigate to your account settings or API section
3. Generate an API key

### 2. Install the package

```bash
npm install -g thunderbit-mcp-server
```

Or clone from source:

```bash
git clone https://github.com/thunderbit-open/thunderbit-mcp-server.git
cd thunderbit-mcp-server
npm install
```

### 3. Configure environment

Set your Thunderbit API key:

```bash
export THUNDERBIT_API_KEY=your_api_key_here
```

### 4. Add to MCP client configuration

For Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "thunderbit": {
      "command": "npx",
      "args": ["thunderbit-mcp-server"],
      "env": {
        "THUNDERBIT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

For Claude Code (`.mcp.json` in project root):

```json
{
  "mcpServers": {
    "thunderbit": {
      "command": "npx",
      "args": ["thunderbit-mcp-server"],
      "env": {
        "THUNDERBIT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 5. Available tools

Once configured, the MCP server provides:

- **scrape_url** — Scrape a webpage and extract its content as structured data or markdown
- **extract_data** — Extract specific structured fields (e.g., product name, price, description) from a given URL using AI-powered extraction

### 6. CLI usage

You can also use Thunderbit directly from the command line:

```bash
# Scrape a URL to markdown
npx thunderbit-mcp-server scrape https://example.com

# Extract structured data with custom fields
npx thunderbit-mcp-server extract https://example.com --fields "title,price,description"
```

### Important notes

- Requires a valid Thunderbit API key (set via `THUNDERBIT_API_KEY` environment variable)
- The server uses AI to intelligently parse and structure web content
- Supports extracting custom fields/schemas from any webpage
- Works with any MCP-compatible client (Claude Desktop, Claude Code, Cursor, Windsurf, etc.)

## References

- Source repository: https://github.com/thunderbit-open/thunderbit-mcp-server
- Thunderbit: https://www.thunderbit.com
- MCP specification: https://modelcontextprotocol.io
