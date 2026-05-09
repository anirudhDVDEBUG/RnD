# How to Use — x-twitter-scraper

## Install

### Option A: pip (library only)

```bash
pip install x-twitter-scraper
```

### Option B: from source

```bash
git clone https://github.com/Xquik-dev/x-twitter-scraper.git
cd x-twitter-scraper
pip install -r requirements.txt
```

### This prototype (no external deps)

```bash
# Already in this directory — just run:
bash run.sh
```

No API keys, no network access, no auth needed. The demo uses mock data.

---

## Claude Code Skill setup

This is a **Claude Code Skill** (not an MCP server).

1. Copy the skill folder into your skills directory:

```bash
mkdir -p ~/.claude/skills/x_twitter_scraper
cp SKILL.md ~/.claude/skills/x_twitter_scraper/SKILL.md
```

2. The skill activates on trigger phrases like:
   - "Scrape tweets from this Twitter/X account"
   - "Collect tweets containing a specific keyword"
   - "Get user profile data from X/Twitter"
   - "Monitor trending topics on Twitter/X"
   - "Extract social media data from X for analysis"

3. Once triggered, Claude will use `x-twitter-scraper` to scrape, collect, and export X/Twitter data.

---

## First 60 seconds

```bash
# 1. Run the demo
bash run.sh

# 2. You'll see:
#    - 5 tweets matching "AI agent" with engagement stats
#    - Profile for @growth_hacker_ai (followers, bio, tweet count)
#    - Top 10 trending hashtags with volume
#    - JSON + CSV files written to output/

# 3. Inspect the exported data
cat output/tweets.json
head output/tweets.csv
```

### Switching to live data

Replace `MockScraper` with the real scraper in `demo_scraper.py`:

```python
# Before (mock)
scraper = MockScraper()

# After (live)
from x_twitter_scraper import Scraper
scraper = Scraper()  # optionally pass auth credentials
```

Then call the same methods — `.search()`, `.get_user_tweets()`, `.get_user_profile()` — against live X/Twitter.

---

## Environment variables (for live usage)

Some scraper features may require authentication. Set these if needed:

```bash
export X_AUTH_TOKEN="your_auth_token"
export X_CSRF_TOKEN="your_csrf_token"
```

Check the [source repo](https://github.com/Xquik-dev/x-twitter-scraper) for the latest auth requirements.
