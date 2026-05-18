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

### Steps

1. **Run the digest:**
   ```bash
   cd ~/.claude/skills/amazon-seller-daily-digest
   node index.js
   ```

2. **With delivery channel:**
   ```bash
   TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=yyy node index.js
   ```

### Example Output

```
=== AMAZON SELLER DAILY DIGEST (2026-05-18) ===

--- ENGLISH ---
[POLICY] FBA fee increase effective June 1...
[TOOL]   Brand Analytics search funnel now available...
[BUZZ]   Return fraud spike reported by sellers...
[SIGNAL] Electronics pricing down 8% WoW...
[ACTION] Update FBA fee projections before June 1...

--- 中文 ---
《政策合规》FBA费用6月1日起上调...
```
