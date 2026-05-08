# Claude Feature Navigator

**A Claude Code skill that discovers, browses, and recommends Claude skills and MCP servers from curated awesome lists and the Composio marketplace.** Say "find me Claude skills for code review" and it searches an 18-entry catalog across 6 categories, returns ranked results, and prints exact install commands.

> **Headline result:** `navigator> recommend deployment` returns docker-compose-gen, ci-fix, and dep-update with one-liner install instructions -- zero Googling required.

## Quick links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install the skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, data flow, limitations, builder relevance
- **[SKILL.md](SKILL.md)** -- The actual skill file to drop into Claude
- **[run.sh](run.sh)** -- `bash run.sh` for a full CLI demo (no API keys needed)

## Source

Based on [Composio Top Claude Skills](https://composio.dev/content/top-claude-skills) and the [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) awesome list.
