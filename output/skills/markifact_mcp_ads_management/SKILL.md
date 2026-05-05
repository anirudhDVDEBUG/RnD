---
name: markifact_mcp_ads_management
description: |
  Set up and use the Markifact MCP server for managing Google Ads, Meta Ads, GA4, TikTok Ads, and LinkedIn Ads from Claude.
  TRIGGER: user wants to manage ads via MCP, set up ad platform integrations, run Google/Meta/TikTok/LinkedIn ad campaigns from Claude, or configure markifact-mcp.
---

# Markifact MCP — Multi-Platform Ad Management

MCP server providing 300+ operations across Google Ads, Meta Ads, GA4, TikTok Ads, and LinkedIn Ads. Human-in-the-loop confirmation on every write operation.

## When to use

- "Set up MCP for managing Google Ads and Meta Ads from Claude"
- "I want to manage ad campaigns across multiple platforms from my AI client"
- "Configure markifact-mcp server for advertising operations"
- "How do I connect Claude to Google Ads, TikTok Ads, or LinkedIn Ads via MCP?"
- "I need an MCP server for multi-platform ad management with human-in-the-loop"

## How to use

### 1. Prerequisites

- Node.js 18+ installed
- API credentials for the ad platforms you want to connect:
  - **Google Ads**: Google Ads API developer token, OAuth2 credentials, customer ID
  - **Meta Ads**: Meta Marketing API access token, ad account ID
  - **GA4**: Google Analytics Data API credentials
  - **TikTok Ads**: TikTok Marketing API access token, advertiser ID
  - **LinkedIn Ads**: LinkedIn Marketing API access token, ad account ID

### 2. Install the MCP server

```bash
npx markifact-mcp
```

Or clone and run locally:

```bash
git clone https://github.com/markifact/markifact-mcp.git
cd markifact-mcp
npm install
npm start
```

### 3. Configure for Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "markifact": {
      "command": "npx",
      "args": ["markifact-mcp"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your-developer-token",
        "GOOGLE_ADS_CUSTOMER_ID": "your-customer-id",
        "META_ADS_ACCESS_TOKEN": "your-meta-token",
        "META_ADS_ACCOUNT_ID": "your-account-id",
        "TIKTOK_ADS_ACCESS_TOKEN": "your-tiktok-token",
        "LINKEDIN_ADS_ACCESS_TOKEN": "your-linkedin-token"
      }
    }
  }
}
```

### 4. Configure for Claude Code

Add to your `.claude/settings.json` or project settings:

```json
{
  "mcpServers": {
    "markifact": {
      "command": "npx",
      "args": ["markifact-mcp"]
    }
  }
}
```

Set environment variables separately for your shell or `.env` file.

### 5. Key features

- **300+ ad operations**: Create, read, update, and manage campaigns, ad groups, ads, keywords, audiences, and more
- **Multi-platform**: Google Ads, Meta Ads, GA4, TikTok Ads, LinkedIn Ads in one server
- **Human-in-the-loop**: Every write operation requires explicit user confirmation before execution
- **Read-safe**: Read operations execute without confirmation prompts
- **Works with any MCP client**: Claude, ChatGPT, Gemini, Cursor, and other AI clients

### 6. Example usage

Once configured, ask Claude:

- "Show me my Google Ads campaigns and their performance this month"
- "Create a new Meta Ads campaign targeting US users aged 25-45"
- "Pause all underperforming ad groups with CPA above $50"
- "Pull GA4 analytics for my top landing pages"
- "List my active LinkedIn Ads campaigns and their budgets"

## References

- **Repository**: [markifact/markifact-mcp](https://github.com/markifact/markifact-mcp)
- **Supported platforms**: Google Ads, Meta Ads, GA4, TikTok Ads, LinkedIn Ads
- **License**: See repository for details
