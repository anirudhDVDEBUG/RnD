---
name: super_geo_agent_readiness
description: |
  Claude Skill for Generative Engine Optimization (GEO) and AI agent readiness.
  Helps sites get cited by ChatGPT, Perplexity, and Google AI Overviews.
  Audits and implements MCP server endpoints, llms.txt, Schema.org markup, and OAuth for AI agents.
  Triggers: "optimize for AI search", "generative engine optimization", "agent readiness audit",
  "add llms.txt", "get cited by AI", "MCP endpoint setup", "schema.org for AI"
---

# Super GEO & Agent Readiness

Audit and optimize any website or application for Generative Engine Optimization (GEO) and AI agent readiness. Ensure your content gets cited by AI systems like ChatGPT, Perplexity, and Google AI Overviews, and that AI agents can discover and interact with your services.

## When to use

- "How do I get my site cited by ChatGPT or Perplexity?"
- "Audit my site for generative engine optimization"
- "Set up llms.txt for my project"
- "Make my API discoverable by AI agents"
- "Add Schema.org structured data for AI search"

## How to use

### 1. GEO Content Audit

Analyze existing content for AI citation readiness:

- **Structured answers**: Check that pages contain clear, concise, factual statements AI can extract
- **Schema.org markup**: Verify JSON-LD structured data (FAQPage, HowTo, Article, Product schemas)
- **Authority signals**: Ensure citations, author credentials, and source attribution are present
- **Content format**: Confirm content uses lists, tables, and direct answers that AI systems prefer

### 2. llms.txt Implementation

Create and configure `llms.txt` at the site root:

```
# Site Name
> Brief description of what this site/service does

## Docs
- [API Reference](/docs/api): Full API documentation
- [Getting Started](/docs/start): Quick start guide

## Optional
- [Examples](/examples): Code examples and tutorials
```

Also create `llms-full.txt` with expanded content for deeper context.

### 3. MCP Server Exposure

Set up Model Context Protocol endpoints so AI agents can interact with your service:

- Define MCP tool schemas for your core functionality
- Expose a `/mcp` or `/.well-known/mcp.json` endpoint
- Document available tools, resources, and prompts
- Implement proper authentication (OAuth 2.0 / API keys)

### 4. Agent Readiness Checklist

Verify the following are in place:

| Component | File/Endpoint | Purpose |
|-----------|--------------|----------|
| llms.txt | `/llms.txt` | AI-readable site summary |
| MCP manifest | `/.well-known/mcp.json` | Agent tool discovery |
| Schema.org | JSON-LD in `<head>` | Structured data for AI extraction |
| OAuth/Auth | `/.well-known/oauth-authorization-server` | Secure agent authentication |
| robots.txt | `/robots.txt` | Allow AI crawlers (GPTBot, PerplexityBot, Google-Extended) |
| Sitemap | `/sitemap.xml` | Content discovery |

### 5. AI Search Optimization Strategies

- Write content that directly answers questions (featured-snippet style)
- Include statistical claims with sources for citation credibility
- Use unique data, research, or perspectives that AI systems will reference
- Maintain topical authority with comprehensive content clusters
- Ensure fast page loads and clean HTML for efficient crawling

## References

- Source: [fseixas/super-geo-agent-readiness](https://github.com/fseixas/super-geo-agent-readiness)
- [llms.txt specification](https://llmstxt.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Schema.org](https://schema.org/)
- [Google AI Overviews documentation](https://developers.google.com/search/docs/appearance/ai-overviews)
