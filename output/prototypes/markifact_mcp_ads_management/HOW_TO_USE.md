# How to Use Markifact MCP

## Install

```bash
# Option A: Run directly via npx (recommended)
npx markifact-mcp

# Option B: Clone and run locally
git clone https://github.com/markifact/markifact-mcp.git
cd markifact-mcp
npm install
npm start
```

Requires **Node.js 18+**.

## Configure for Claude Desktop

Add this to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the equivalent on your OS:

```json
{
  "mcpServers": {
    "markifact": {
      "command": "npx",
      "args": ["markifact-mcp"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your-developer-token",
        "GOOGLE_ADS_CUSTOMER_ID": "123-456-7890",
        "GOOGLE_ADS_OAUTH_CLIENT_ID": "your-oauth-client-id",
        "GOOGLE_ADS_OAUTH_CLIENT_SECRET": "your-oauth-secret",
        "GOOGLE_ADS_OAUTH_REFRESH_TOKEN": "your-refresh-token",
        "META_ADS_ACCESS_TOKEN": "your-meta-token",
        "META_ADS_ACCOUNT_ID": "act_123456789",
        "GA4_PROPERTY_ID": "properties/123456789",
        "TIKTOK_ADS_ACCESS_TOKEN": "your-tiktok-token",
        "TIKTOK_ADS_ADVERTISER_ID": "12345678",
        "LINKEDIN_ADS_ACCESS_TOKEN": "your-linkedin-token",
        "LINKEDIN_ADS_ACCOUNT_ID": "urn:li:sponsoredAccount:12345"
      }
    }
  }
}
```

You only need to provide env vars for the platforms you use — others will be skipped.

## Configure for Claude Code

Add to your project's `.claude/settings.json`:

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

Then export credentials in your shell or `.env`:

```bash
export GOOGLE_ADS_DEVELOPER_TOKEN="your-token"
export META_ADS_ACCESS_TOKEN="your-token"
# ... etc
```

## As a Claude Skill

Drop a skill file at `~/.claude/skills/markifact_mcp_ads_management/SKILL.md` with the content from the source repository's skill definition.

**Trigger phrases:**
- "Set up MCP for managing Google Ads and Meta Ads from Claude"
- "Configure markifact-mcp server for advertising operations"
- "I want to manage ad campaigns across multiple platforms"
- "Connect Claude to Google Ads / TikTok Ads / LinkedIn Ads via MCP"

## First 60 Seconds

After configuring the MCP server in Claude Desktop:

**Input (to Claude):**
> "Show me my Google Ads campaigns and their performance this month"

**Output:**
```
Campaign                          Status   Spend      Conv   CPA
Brand Awareness — Q2 2026         ENABLED  $3,240.50  187    $17.33
Product Launch — Widget Pro       ENABLED  $8,450.00  342    $24.71
```

**Input:**
> "Pause all campaigns with CPA above $50"

**Output:**
```
Found 1 campaign with CPA > $50:
- B2B Lead Gen — Enterprise (CPA: $121.90)

[Confirmation required] Pause this campaign? [Approve] [Deny]

> Approved. Campaign paused.
```

## Running the Mock Demo

No credentials needed — see the full flow locally:

```bash
bash run.sh
# or
node mock_server.js
```

This shows the tool registry, read operations, write confirmations, and cross-platform reporting using mock data.
