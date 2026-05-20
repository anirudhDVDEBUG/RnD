---
name: web_researcher_mcp
description: |
  Set up and configure the web-researcher-mcp server for AI-powered web search, content extraction, and academic/patent/news research.
  TRIGGER: user wants web search via MCP, content extraction from URLs, academic research, patent search, news research, multi-provider search routing, or scraping web pages for AI context.
  DO NOT TRIGGER: for simple curl/wget commands, browser automation, or non-MCP web access.
---

# Web Researcher MCP Server

An MCP server (written in Go) that gives AI assistants powerful web research capabilities: web search, content extraction, academic/patent/news research with multi-provider routing and 4-tier scraping. Works with Claude Desktop, Claude Code, Cursor, and any MCP client.

## When to use

- "I need to add web search capabilities to my Claude setup"
- "Set up an MCP server for web research and content extraction"
- "I want to search the web, academic papers, patents, or news from Claude"
- "Configure web-researcher-mcp for my AI assistant"
- "I need to scrape and extract content from web pages via MCP"

## How to use

### 1. Prerequisites

- Docker (recommended) or Go 1.21+
- A search provider API key (Brave Search API key recommended, or self-hosted SearXNG instance)

### 2. Installation

**Option A: Docker (recommended)**

```bash
# Clone the repository
git clone https://github.com/zoharbabin/web-researcher-mcp.git
cd web-researcher-mcp

# Build the Docker image
docker build -t web-researcher-mcp .
```

**Option B: Build from source**

```bash
git clone https://github.com/zoharbabin/web-researcher-mcp.git
cd web-researcher-mcp
go build -o web-researcher-mcp .
```

### 3. Configuration

Set environment variables for your search provider:

| Variable | Description | Required |
|---|---|---|
| `BRAVE_API_KEY` | Brave Search API key | Yes (if using Brave) |
| `SEARXNG_BASE_URL` | SearXNG instance URL | Yes (if using SearXNG) |

Get a Brave Search API key at: https://brave.com/search/api/

### 4. Add to your MCP client

**Claude Desktop (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "web-researcher": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "BRAVE_API_KEY", "web-researcher-mcp"],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key-here"
      }
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add web-researcher -- docker run -i --rm -e BRAVE_API_KEY=your-key web-researcher-mcp
```

**Or with a local binary:**

```bash
claude mcp add web-researcher -- /path/to/web-researcher-mcp
```

### 5. Available MCP Tools

Once configured, the following tools become available to your AI assistant:

- **web_search** - Search the web using Brave Search or SearXNG with multi-provider routing
- **extract_content** - Extract and clean content from any URL using 4-tier scraping (raw fetch, headless browser, etc.)
- **academic_search** - Search academic papers and scholarly content
- **patent_search** - Search patents and patent applications
- **news_search** - Search recent news articles
- **search_lenses** - Apply specialized search lenses/filters for domain-specific research

### 6. Key Features

- **Multi-provider routing**: Automatically routes queries to the best search provider
- **4-tier scraping**: Progressively tries different extraction methods for maximum content recovery
- **Search lenses**: Specialized filters for academic, patent, news, and other research domains
- **Structured output**: Returns clean, AI-friendly content for downstream processing

### 7. Verify it works

After adding the MCP server, restart your MCP client and ask:
> "Search the web for recent developments in quantum computing"

The assistant should use the `web_search` tool from the web-researcher MCP server.

## References

- Source: https://github.com/zoharbabin/web-researcher-mcp
- Brave Search API: https://brave.com/search/api/
- MCP Protocol: https://modelcontextprotocol.io
