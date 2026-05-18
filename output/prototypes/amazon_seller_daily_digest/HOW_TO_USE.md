# How To Use: Amazon Seller Daily Digest

## As a Claude Code Skill

### Installation

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/amazon-seller-daily-digest
   ```

2. Copy the `SKILL.md` file into it:
   ```bash
   cp SKILL.md ~/.claude/skills/amazon-seller-daily-digest/SKILL.md
   ```

3. Clone the implementation:
   ```bash
   git clone https://github.com/lanfuli/follow-amazon-daily.git
   cd follow-amazon-daily
   npm install
   ```

### Trigger Phrases

Say any of these to Claude Code to activate the skill:

- "Generate today's Amazon seller digest"
- "What are the latest Amazon seller announcements?"
- "Create a bilingual Amazon e-commerce intelligence briefing"
- "Send the daily Amazon seller newsletter to Telegram"
- "Summarize this week's Amazon marketplace changes"

### Environment Variables (for delivery channels)

| Variable | Purpose |
|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Target Telegram chat |
| `EMAIL_SMTP_HOST` | SMTP server host |
| `EMAIL_SMTP_PORT` | SMTP port |
| `EMAIL_SMTP_USER` | SMTP username |
| `EMAIL_SMTP_PASS` | SMTP password |
| `EMAIL_TO` | Recipient email |
| `FEISHU_WEBHOOK_URL` | Feishu/Lark webhook |
| `ANTHROPIC_API_KEY` | For Claude synthesis (optional in demo mode) |

If no delivery vars are set, output goes to stdout.

## Standalone CLI Usage

```bash
cd follow-amazon-daily
npm install
node index.js
```

## First 60 Seconds

```bash
# 1. Run the demo (no API keys needed)
bash run.sh

# Output (immediate, uses mock data):
# === AMAZON SELLER DAILY DIGEST (2026-05-18) ===
#
# --- ENGLISH ---
# [POLICY] FBA fee structure update effective June 1...
# [TOOL]   Brand Analytics now includes search funnel data...
# [BUZZ]   Trending: sellers discussing new return policy impact...
# [SIGNAL] Home & Kitchen category growth +12% MoM...
# [ACTION] Update pricing models before June 1 fee changes
#
# --- 中文 ---
# 《政策》FBA费用结构更新，6月1日生效...
# 《工具》品牌分析现在包含搜索漏斗数据...
# ...

# 2. With real sources (requires ANTHROPIC_API_KEY):
export ANTHROPIC_API_KEY=sk-ant-...
node index.js

# 3. With Telegram delivery:
export TELEGRAM_BOT_TOKEN=123456:ABC...
export TELEGRAM_CHAT_ID=-100123456
node index.js
```

## Scheduling Daily Runs

### Via cron:
```bash
0 8 * * * cd /path/to/follow-amazon-daily && node index.js
```

### Via Claude Code `/schedule`:
```
/schedule "Generate Amazon seller daily digest" every day at 8am
```

### Via GitHub Actions:
```yaml
on:
  schedule:
    - cron: '0 8 * * *'
jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install && node index.js
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```
