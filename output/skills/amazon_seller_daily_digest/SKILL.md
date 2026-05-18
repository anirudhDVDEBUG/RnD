---
name: Amazon Seller Daily Digest
description: |
  Daily Amazon-seller intelligence digest skill. Fetches official announcements, community discussions, podcast highlights, and newsletter signals, then remixes them into a zh/en/bilingual digest delivered to stdout, Telegram, Email, or Feishu.
  Triggers: amazon seller digest, amazon daily intelligence, e-commerce market signals, seller news roundup
---

# Amazon Seller Daily Digest

Generate a daily intelligence digest for Amazon sellers by aggregating signals from official channels, community forums, podcasts, and newsletters, then synthesizing them into an actionable bilingual (zh/en) summary.

## When to use

- "Generate today's Amazon seller digest"
- "What are the latest Amazon seller announcements and community signals?"
- "Create a bilingual Amazon e-commerce intelligence briefing"
- "Send the daily Amazon seller newsletter to Telegram/Feishu"
- "Summarize this week's Amazon marketplace changes for sellers"

## How to use

### Prerequisites

1. **Node.js** (>=18) must be installed.
2. Clone or reference the source repository.
3. Set environment variables for your desired delivery channel(s):
   - `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — for Telegram delivery
   - `EMAIL_SMTP_*` / `EMAIL_TO` — for Email delivery
   - `FEISHU_WEBHOOK_URL` — for Feishu (Lark) delivery
   - If no delivery env vars are set, output goes to stdout.

### Steps

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run the digest generation:**
   ```bash
   node index.js
   ```
   This will:
   - Fetch signals from Amazon Seller Central announcements, community forums, relevant podcasts, and newsletters
   - Use Claude to synthesize and remix the raw signals into a structured digest
   - Format the output in both Chinese and English (bilingual)
   - Deliver via configured channel (stdout/Telegram/Email/Feishu)

3. **Schedule for daily runs (optional):**
   Use cron, GitHub Actions, or Claude Code's `/schedule` to run daily:
   ```bash
   # Example cron: every day at 8am UTC
   0 8 * * * cd /path/to/follow-amazon-daily && node index.js
   ```

### Configuration

- **Language**: Supports `zh`, `en`, or `bilingual` output (configure via env or config file)
- **Sources**: Official Amazon announcements, seller community posts, podcast episode summaries, newsletter digests
- **Delivery**: stdout (default), Telegram, Email, Feishu — set via environment variables

### Example Output Structure

The digest typically includes:
- **Policy & Compliance Updates** — new Amazon rules or fee changes
- **Tool & Feature Releases** — Seller Central new features
- **Community Buzz** — trending discussions among sellers
- **Market Signals** — pricing trends, category shifts
- **Action Items** — what sellers should do this week

## References

- Source: [lanfuli/follow-amazon-daily](https://github.com/lanfuli/follow-amazon-daily)
- Topics: ai-agent, amazon-seller, claude-code, claude-skill, digest, ecommerce
