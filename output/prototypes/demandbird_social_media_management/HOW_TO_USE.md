# How to Use DemandBird

## Install (this demo)

```bash
git clone <this-repo> && cd demandbird_social_media_management
bash run.sh
```

Requires Node.js 18+. Dependencies (`chalk`, `cli-table3`) install automatically.

## Install the real DemandBird

```bash
git clone https://github.com/DemandBird/demandbird.git
cd demandbird
# Follow the repo README for env setup and platform API credentials
```

## MCP Server Setup

Add to your `~/.claude.json` under the `mcpServers` block:

```json
{
  "mcpServers": {
    "demandbird": {
      "command": "npx",
      "args": ["demandbird-mcp"],
      "env": {
        "DEMANDBIRD_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

After adding, restart Claude Code. You can then ask Claude to use DemandBird tools directly (e.g., "schedule a LinkedIn post for tomorrow at 9am").

## Claude Skill Setup

To install as a Claude Code skill:

1. Copy the `SKILL.md` file to `~/.claude/skills/demandbird_social_media_management/SKILL.md`
2. Trigger phrases that activate it:
   - "Set up DemandBird for social media management"
   - "Configure the DemandBird MCP server"
   - "Schedule and publish content across Twitter, LinkedIn, YouTube"
   - "Repurpose content across social platforms"
   - "Build a social media content pipeline with DemandBird API"

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output (abbreviated):**
```
  ╔═══════════════════════════════════════════════════╗
  ║         DemandBird Social Media Manager           ║
  ╚═══════════════════════════════════════════════════╝

  1. Connected Platforms
  Twitter    | Connected | @demo_twitter
  LinkedIn   | Connected | @demo_linkedin
  Bluesky    | Connected | @demo_bluesky
  ...

  3. Create & Schedule a New Post
  Post created successfully:
    ID:         post_006
    Status:     scheduled
    Platforms:  twitter, linkedin, bluesky
    Scheduled:  2026-05-22T10:00:00Z

  4. Content Repurposing — post_001 → 4 Platforms
  LINKEDIN   [draft]  "Excited to announce... #ProfessionalGrowth"
  BLUESKY    [draft]  "Excited to announce our new AI-powered..."
  THREADS    [draft]  "Excited to announce... [thread]"
  SUBSTACK   [draft]  "## Excited to announce..."

  5. Analytics Dashboard
  Total Impressions  | 7,920
  Engagement Rate    | 3.94%

  Demo complete. All workflows executed with mock data.
```

The demo exercises all five core workflows (platform listing, post CRUD, scheduling, repurposing, analytics) plus MCP tool discovery — no API keys needed.

## Real Usage with API Keys

Set environment variables for each platform you want to connect:

```bash
export DEMANDBIRD_API_KEY="your-demandbird-key"
# Platform-specific credentials per the DemandBird repo docs
```

Then use the MCP server or API endpoints for production workflows. See the [DemandBird repository](https://github.com/DemandBird/demandbird) for full credential setup.
