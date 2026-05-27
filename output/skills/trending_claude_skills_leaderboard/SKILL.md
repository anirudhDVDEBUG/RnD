---
name: trending_claude_skills_leaderboard
description: |
  Auto-updated leaderboard of trending Claude skills and AI agent repos. Fetches and displays the most popular claude-skill repositories, refreshed regularly.
  TRIGGER when: user asks about trending Claude skills, popular AI agent repos, top Claude Code skills, skill discovery, or wants to find new skills to install.
  DO NOT TRIGGER when: user wants to build a skill from scratch, needs help with a specific existing skill, or asks about non-Claude AI tools.
---

# Trending Claude Skills Leaderboard

Discover the most popular and trending Claude skills and AI agent repositories.

## When to use

- "What are the trending Claude skills right now?"
- "Show me popular AI agent repos"
- "Find me new Claude Code skills to install"
- "What are the top-starred claude-skill repositories?"
- "Discover trending AI coding tools and skills"

## How to use

1. **Fetch the leaderboard**: Clone or fetch the latest data from the trending-claude-skills repository to get the current rankings.

```bash
# Fetch the latest README which contains the leaderboard
curl -s https://raw.githubusercontent.com/linny006/trending-claude-skills/main/README.md
```

2. **Browse by category**: The leaderboard tracks repos tagged with topics like `claude-skills`, `claude-code`, `mcp-server`, `ai-agents`, `coding-agent`, and `ai-workflow`.

3. **Evaluate skills**: Check star counts, recent activity (pushed_at), and language to find skills that match your needs.

4. **Install a skill**: Once you find a skill you want, follow its installation instructions (typically copying the SKILL.md into your project or `~/.claude/skills/`).

## Key features

- Auto-updated every 15 minutes
- Tracks stars, forks, language, and recency
- Covers Claude skills, MCP servers, AI agents, and coding tools
- Python-based scraper for GitHub topic search

## References

- Source: https://github.com/linny006/trending-claude-skills
- Topics tracked: ai-agents, ai-coding, claude-code, claude-skills, mcp-server, coding-agent, developer-tools
