#!/usr/bin/env python3
"""
x-twitter-scraper demo — runs end-to-end with mock data.

This script demonstrates the workflow you'd use with the real
x-twitter-scraper library: search tweets, fetch user profiles,
list trends, and export results to JSON/CSV.

When the real library is installed, swap MockScraper for the real Scraper.
"""

import csv
import json
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Mock scraper (stands in for `from x_twitter_scraper import Scraper`)
# ---------------------------------------------------------------------------
from mock_data import MOCK_TWEETS, MOCK_PROFILES, MOCK_TRENDS


class Tweet:
    """Mirrors the Tweet object from x-twitter-scraper."""

    def __init__(self, data: dict):
        self.id = data["id"]
        self.text = data["text"]
        self.author = data["author"]
        self.author_name = data.get("author_name", "")
        self.created_at = data["created_at"]
        self.likes = data.get("likes", 0)
        self.retweets = data.get("retweets", 0)
        self.replies = data.get("replies", 0)
        self.url = data.get("url", "")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "created_at": self.created_at,
            "likes": self.likes,
            "retweets": self.retweets,
            "replies": self.replies,
            "url": self.url,
        }


class UserProfile:
    def __init__(self, data: dict):
        self.username = data["username"]
        self.name = data["name"]
        self.bio = data["bio"]
        self.followers_count = data["followers_count"]
        self.following_count = data["following_count"]
        self.tweet_count = data["tweet_count"]
        self.verified = data.get("verified", False)


class MockScraper:
    """Drop-in mock for x_twitter_scraper.Scraper."""

    def search(self, query: str, max_results: int = 10):
        q = query.lower()
        matches = [
            Tweet(t)
            for t in MOCK_TWEETS
            if q in t["text"].lower() or q in " ".join(t.get("text", "").lower().split())
        ]
        if not matches:
            # Return all if no keyword match (simulates broad search)
            matches = [Tweet(t) for t in MOCK_TWEETS[:max_results]]
        return matches[:max_results]

    def get_user_tweets(self, username: str, max_results: int = 10):
        return [Tweet(t) for t in MOCK_TWEETS if t["author"] == username][:max_results]

    def get_user_profile(self, username: str):
        data = MOCK_PROFILES.get(username)
        if data:
            return UserProfile(data)
        return None

    def get_trends(self):
        return MOCK_TRENDS


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
SEPARATOR = "=" * 70


def demo_search(scraper):
    print(SEPARATOR)
    print("  1. SEARCH TWEETS — keyword: 'AI agent'")
    print(SEPARATOR)
    tweets = scraper.search("ai agent", max_results=5)
    for i, t in enumerate(tweets, 1):
        print(f"\n  [{i}] @{t.author} ({t.created_at})")
        print(f"      {t.text[:120]}")
        print(f"      Likes: {t.likes:,}  |  Retweets: {t.retweets:,}  |  Replies: {t.replies:,}")
    print()
    return tweets


def demo_user_profile(scraper):
    print(SEPARATOR)
    print("  2. USER PROFILE — @growth_hacker_ai")
    print(SEPARATOR)
    profile = scraper.get_user_profile("growth_hacker_ai")
    if profile:
        print(f"\n  Name:       {profile.name}")
        print(f"  Username:   @{profile.username}")
        print(f"  Bio:        {profile.bio}")
        print(f"  Followers:  {profile.followers_count:,}")
        print(f"  Following:  {profile.following_count:,}")
        print(f"  Tweets:     {profile.tweet_count:,}")
        print(f"  Verified:   {'Yes' if profile.verified else 'No'}")
    print()


def demo_trends(scraper):
    print(SEPARATOR)
    print("  3. TRENDING TOPICS")
    print(SEPARATOR)
    trends = scraper.get_trends()
    for i, trend in enumerate(trends, 1):
        print(f"  {i:>2}. {trend['name']:<20s}  {trend['tweet_count']:>7,} tweets  [{trend['category']}]")
    print()


def demo_export(tweets):
    print(SEPARATOR)
    print("  4. EXPORT RESULTS")
    print(SEPARATOR)
    out_dir = os.path.join(os.path.dirname(__file__) or ".", "output")
    os.makedirs(out_dir, exist_ok=True)

    # JSON
    json_path = os.path.join(out_dir, "tweets.json")
    with open(json_path, "w") as f:
        json.dump([t.to_dict() for t in tweets], f, indent=2, default=str)
    print(f"\n  JSON saved to {json_path}")

    # CSV
    csv_path = os.path.join(out_dir, "tweets.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "text", "author", "created_at", "likes", "retweets", "replies", "url"]
        )
        writer.writeheader()
        for t in tweets:
            writer.writerow(t.to_dict())
    print(f"  CSV  saved to {csv_path}")

    # Summary
    total_likes = sum(t.likes for t in tweets)
    total_rts = sum(t.retweets for t in tweets)
    print(f"\n  Summary: {len(tweets)} tweets | {total_likes:,} total likes | {total_rts:,} total retweets")
    print()


def main():
    print()
    print(SEPARATOR)
    print("  x-twitter-scraper  —  Demo (mock data, no API keys needed)")
    print(SEPARATOR)
    print()

    scraper = MockScraper()

    tweets = demo_search(scraper)
    demo_user_profile(scraper)
    demo_trends(scraper)
    demo_export(tweets)

    print(SEPARATOR)
    print("  Done. Swap MockScraper for the real Scraper to hit live X/Twitter.")
    print(SEPARATOR)
    print()


if __name__ == "__main__":
    main()
