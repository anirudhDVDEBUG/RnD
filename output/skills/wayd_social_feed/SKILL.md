---
name: wayd_social_feed
description: |
  Post status updates and browse a meme-y social feed for programmers, powered by GitHub Issues.
  Triggers: "take a break", "post what I'm doing", "wayd feed", "developer social feed", "share my status", "coffee break", "post a meme update"
---

# WAYD - Social Feed for AI-Powered Programmers

A fun, meme-y social feed built on GitHub Issues. Take a coffee break from coding and share what you're working on with other developers using AI coding agents.

## When to use

- "Take a coffee break and check the feed"
- "Post what I'm working on to wayd"
- "Show me the latest developer updates"
- "Share a status update about my project"
- "Browse the wayd social feed"

## How to use

### 1. Install wayd

```bash
pip install wayd
```

Or install from source:

```bash
git clone https://github.com/ferdinandobons/wayd.git
cd wayd
pip install .
```

### 2. Browse the feed

View the latest posts from other developers:

```bash
wayd feed
```

### 3. Post a status update

Share what you're currently working on:

```bash
wayd post "Refactoring the auth module with Claude - 3 hours in and it's beautiful"
```

### 4. Interact with posts

The feed is built on GitHub Issues, so you can browse, comment, and react to posts directly through the CLI or on GitHub.

### Tips

- Use wayd as a fun break during long coding sessions with AI agents
- Share interesting discoveries, debugging war stories, or meme-worthy moments
- The social feed is community-driven and built entirely on GitHub Issues as the backend
- Works great as a quick mental reset between deep coding sessions

## References

- Source repository: https://github.com/ferdinandobons/wayd
- Built with Python, uses GitHub Issues as the social backend
- Tags: claude-skill, developer-humor, social-feed, github-issues, cli-tool
