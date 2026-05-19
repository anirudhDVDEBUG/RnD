---
name: demandbird_social_media_management
description: |
  Set up and use DemandBird, an AI-native social media management tool for teams and agencies. Supports multi-platform publishing (Twitter/X, LinkedIn, YouTube, Bluesky, Threads, Substack), content scheduling, analytics, and repurposing workflows via MCP server and API.
  Triggers: demandbird, social media management tool, multi-platform publishing, content scheduling MCP, social media MCP server
---

# DemandBird Social Media Management

Set up and integrate DemandBird — an AI-native social media management platform for teams and agencies. DemandBird provides a unified content creation pipeline with scheduling, analytics, and repurposing workflows across major social platforms.

## When to use

- "Set up DemandBird for social media management"
- "Configure the DemandBird MCP server for multi-platform publishing"
- "Schedule and publish content across Twitter, LinkedIn, YouTube, Bluesky, Threads, and Substack"
- "Build a social media content pipeline with DemandBird API"
- "Repurpose content across social platforms using DemandBird"

## How to use

### 1. Clone and install DemandBird

```bash
git clone https://github.com/DemandBird/demandbird.git
cd demandbird
```

Review the repository README for the latest installation instructions, dependencies, and environment setup.

### 2. Configure platform connections

DemandBird supports the following platforms:
- **Twitter/X** — Post tweets, threads, and media
- **LinkedIn** — Publish professional content and articles
- **YouTube** — Manage video content and metadata
- **Bluesky** — Post to the AT Protocol network
- **Threads** — Publish to Meta's Threads platform
- **Substack** — Create and manage newsletter content

Set up API credentials for each platform you want to use, following the configuration guide in the repository.

### 3. MCP Server integration

DemandBird provides an MCP (Model Context Protocol) server, allowing AI agents like Claude to interact with your social media accounts programmatically.

Add DemandBird to your MCP configuration (e.g., in `claude_desktop_config.json` or `.mcp.json`):

```json
{
  "mcpServers": {
    "demandbird": {
      "command": "npx",
      "args": ["demandbird-mcp"],
      "env": {
        "DEMANDBIRD_API_KEY": "your-api-key"
      }
    }
  }
}
```

> **Note:** Check the repository README for the exact MCP server command and required environment variables, as they may change between versions.

### 4. Core workflows

- **Content creation**: Draft posts optimized for each platform's format and audience
- **Scheduling**: Queue content for optimal posting times across all connected platforms
- **Analytics**: Track engagement, reach, and performance metrics
- **Repurposing**: Transform a single piece of content into platform-specific variants (e.g., blog post to tweet thread to LinkedIn article)
- **Team collaboration**: Manage approval workflows for agency and team use cases

### 5. API usage

DemandBird exposes an API for programmatic access to all features. Refer to the repository documentation for endpoint details, authentication, and rate limits.

```bash
# Example: List scheduled posts (check docs for actual endpoints)
curl -H "Authorization: Bearer $DEMANDBIRD_API_KEY" \
  https://api.demandbird.com/v1/posts/scheduled
```

## Key considerations

- Store API keys and credentials securely using environment variables — never commit them to version control
- Each social platform has its own rate limits and content policies; DemandBird handles these but be aware of per-platform constraints
- The MCP server enables AI-driven content workflows — pair with Claude for automated content generation and scheduling
- Review the repository for B2B marketing templates and automation presets

## References

- **Repository**: https://github.com/DemandBird/demandbird
- **Topics**: social-media-management, mcp-server, content-marketing, ai-tools, b2b-marketing
- **Supported platforms**: Twitter/X, LinkedIn, YouTube, Bluesky, Threads, Substack
