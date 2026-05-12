# How to Use

## Install (standalone)

```bash
git clone <this-repo> && cd chatgpt_adoption_trends_q1_2026
# No external dependencies — Python 3.10+ stdlib only
pip install -r requirements.txt   # (no-op, included for convention)
```

## As a Claude Code Skill

This is a **Claude Code skill**. To install:

1. Copy the `SKILL.md` file into your skills directory:

```bash
mkdir -p ~/.claude/skills/chatgpt_adoption_trends_q1_2026
cp SKILL.md ~/.claude/skills/chatgpt_adoption_trends_q1_2026/SKILL.md
```

2. **Trigger phrases** that activate the skill in Claude Code:
   - "What are the latest ChatGPT adoption numbers?"
   - "How has AI usage demographics changed in 2026?"
   - "Summarize the mainstream AI adoption trends"
   - "Who is using ChatGPT now vs a year ago?"
   - "What does OpenAI's Q1 2026 user data show?"
   - Any mention of: `chatgpt adoption`, `ai demographics 2026`, `mainstream ai usage`, `chatgpt growth trends`, `openai user stats`

3. Claude will respond with structured analysis including demographic data, competitive context, and product-builder implications — no API keys needed.

## CLI Usage

```bash
# Full report to stdout
python3 analyze_trends.py

# Full report + JSON export
python3 analyze_trends.py --json
# -> creates output.json with structured data
```

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output (abbreviated):**
```
========================================================================
  CHATGPT ADOPTION TRENDS — Q1 2026 ANALYSIS
  Source: OpenAI Signals Research — Q1 2026 Update
  Weekly active users: 600M
  Quarterly growth: +18.4%
========================================================================

  AGE GROUP DISTRIBUTION (share % of user base)
  18-24 (YoY +12%)       [###############################---------] 22.0%
  25-34 (YoY +15%)       [########################################] 28.0%
  35-44 (YoY +38%)       [################################--------] 23.0%
  ...

  KEY INSIGHTS
  [1] Demographics: Fastest-growing age group: 65+
      Users aged 65+ grew 89% YoY...
  [2] Demographics: Users 35+ now represent 50% of the base
      Average YoY growth across 35+ cohorts is 52%...
  [3] Demographics: Gender gap narrowed significantly
      Male-female gap shrank from 30pp to 8pp...

  Structured data exported to output.json
```

The JSON export (`output.json`) contains all raw data and computed insights for downstream programmatic use.
