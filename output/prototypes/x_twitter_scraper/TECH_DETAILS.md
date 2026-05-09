# Technical Details — x-twitter-scraper

## What it does

x-twitter-scraper is a Python library that scrapes data from X (formerly Twitter) without requiring official API access. It provides a high-level `Scraper` class with methods to search tweets by keyword, fetch a user's timeline, retrieve profile metadata, and list trending topics. Results come back as structured Python objects (`Tweet`, `UserProfile`) with fields like text, engagement counts, timestamps, and author info. The library handles rate limiting and session management internally.

Unlike the official Twitter/X API (which requires developer approval, has restrictive rate limits, and costs $100+/month for basic access), this scraper works by making direct HTTP requests that mimic browser behavior — parsing the responses into clean data objects.

## Architecture

```
x-twitter-scraper/
  Scraper          - Main entry point; manages sessions, auth, rate limits
    .search()      - Keyword/hashtag tweet search (returns List[Tweet])
    .get_user_tweets() - User timeline scrape
    .get_user_profile() - Profile metadata fetch
    .get_trends()  - Trending topics

  Tweet            - Dataclass: id, text, author, created_at, likes, retweets, replies
  UserProfile      - Dataclass: username, name, bio, followers, following, tweet_count
```

**Data flow:** `Scraper` -> HTTP requests to X endpoints -> HTML/JSON parsing -> Python objects -> user exports to JSON/CSV/DB.

**Dependencies:** Standard Python (requests, json, csv). No heavyweight frameworks, no Selenium/Playwright — pure HTTP-based scraping.

## Limitations

- **Fragile to X/Twitter changes:** Scraping relies on undocumented endpoints and HTML structure. X frequently changes these, which can break the scraper without notice.
- **Rate limits:** While the library handles rate limiting, aggressive scraping can lead to IP blocks or account suspension.
- **No streaming:** This is pull-based (batch scrape), not a real-time firehose. For continuous monitoring, you'd need a polling loop.
- **Auth may be required:** Some data (protected accounts, full search results) requires valid X session cookies or tokens.
- **ToS risk:** Web scraping X likely violates their Terms of Service. Use at your own risk and for legitimate purposes (research, personal use, authorized testing).
- **No write operations:** Read-only; cannot post tweets, like, or retweet.

## Why it matters for Claude-driven products

| Use case | How x-twitter-scraper fits |
|---|---|
| **Lead generation** | Scrape tweets with buying signals ("looking for a tool that...", "anyone recommend..."), score them with Claude, push to CRM. The mock demo shows exactly this pattern. |
| **Marketing / trend monitoring** | Track hashtag volumes and trending topics daily. Feed trends into Claude to generate content calendars or ad copy aligned with what's hot. |
| **Ad creatives** | Scrape competitor ad accounts or viral tweets in your niche. Use Claude to analyze what copy patterns work, then generate variations. |
| **Agent factories** | Build autonomous agents that: (1) scrape X for signals, (2) analyze with Claude, (3) take action (email, Slack, CRM update). The scraper is the "eyes" of the agent. |
| **Voice AI** | Scrape customer complaints or praise from X, feed into voice AI training data or use as context for voice agent responses. |

The key value: **X/Twitter is the fastest public signal source for tech trends, customer sentiment, and competitive intelligence.** This scraper turns that signal into structured data that Claude can reason over.
