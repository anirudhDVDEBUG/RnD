---
name: x_twitter_scraper
description: |
  Scrape tweets, user profiles, and trending topics from X (formerly Twitter) using the x-twitter-scraper tool.
  TRIGGER: user wants to scrape tweets, collect Twitter/X data, extract tweets by keyword or user, gather social media data from X/Twitter, or monitor Twitter hashtags/trends.
---

# X / Twitter Scraper Skill

Scrape and collect data from X (formerly Twitter) including tweets, user profiles, search results, and trending topics using the [x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper) library.

## When to use

- "Scrape tweets from this Twitter/X account"
- "Collect tweets containing a specific keyword or hashtag"
- "Get user profile data from X/Twitter"
- "Monitor trending topics on Twitter/X"
- "Extract social media data from X for analysis"

## How to use

### 1. Install the scraper

```bash
pip install x-twitter-scraper
```

Or clone from source:

```bash
git clone https://github.com/Xquik-dev/x-twitter-scraper.git
cd x-twitter-scraper
pip install -r requirements.txt
```

### 2. Basic usage — Scrape tweets by keyword

```python
from x_twitter_scraper import Scraper

scraper = Scraper()

# Search tweets by keyword
tweets = scraper.search("artificial intelligence", max_results=100)
for tweet in tweets:
    print(tweet.text, tweet.created_at, tweet.author)
```

### 3. Scrape a user's timeline

```python
# Get tweets from a specific user
user_tweets = scraper.get_user_tweets("elonmusk", max_results=50)
for tweet in user_tweets:
    print(tweet.text)
```

### 4. Get user profile information

```python
# Fetch user profile data
profile = scraper.get_user_profile("anthropaboriai")
print(profile.name, profile.followers_count, profile.bio)
```

### 5. Export results

```python
import json
import csv

# Export to JSON
tweets = scraper.search("climate change", max_results=200)
with open("tweets.json", "w") as f:
    json.dump([t.to_dict() for t in tweets], f, indent=2, default=str)

# Export to CSV
with open("tweets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "created_at", "author", "likes", "retweets"])
    writer.writeheader()
    for tweet in tweets:
        writer.writerow(tweet.to_dict())
```

### Key considerations

- **Rate limiting**: The scraper handles rate limits automatically, but be mindful of request volumes.
- **Authentication**: Some features may require X/Twitter credentials or API tokens. Set them via environment variables or pass them to the `Scraper()` constructor.
- **Data compliance**: Ensure your use of scraped data complies with X/Twitter's Terms of Service and applicable data privacy regulations.
- **No official API needed**: This scraper works without requiring official Twitter API access, but respects platform constraints.

## References

- Source repository: [Xquik-dev/x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper)
- Found via: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
