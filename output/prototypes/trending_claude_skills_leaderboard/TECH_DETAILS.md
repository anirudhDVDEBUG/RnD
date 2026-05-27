# Technical Details

## What it does

The trending-claude-skills project is a Python scraper that queries GitHub's Search API across six topic tags (`claude-skills`, `claude-code`, `mcp-server`, `ai-agents`, `coding-agent`, `ai-workflow`), deduplicates results by repository full name, and renders a star-sorted leaderboard. The upstream repo runs on a 15-minute cron via GitHub Actions, committing the updated README automatically.

This local prototype mirrors the core logic: topic-based fetch, dedup, sort, and render. It includes embedded mock data so the demo runs without any API credentials.

## Architecture

```
trending_skills.py        # Single-file implementation
  |
  +-- fetch_github_repos()   # GET /search/repositories?q=topic:{X}&sort=stars
  +-- fetch_all_topics()     # Iterates 6 topics, deduplicates by full_name
  +-- render_leaderboard()   # ASCII table with rank, stars, language, recency
  +-- render_json()          # Structured JSON output
  +-- main()                 # CLI entry point (argparse)
```

**Data flow:**
1. For each of 6 topics, query GitHub Search API (or use mock data)
2. Collect results into a set keyed by `full_name` to avoid duplicates
3. Sort by `stargazers_count` descending
4. Render as table or JSON to stdout

**Dependencies:** `requests` (for live mode only). No other external packages. Python 3.10+.

**No model calls.** This is pure API scraping and formatting -- no LLM inference involved.

## Limitations

- **Rate limits:** GitHub anonymous API allows ~10 requests/minute. With 6 topics, a single run is fine but rapid repeated calls will hit limits. Use a `GITHUB_TOKEN` for 30 req/min.
- **Topic coverage only:** Only finds repos that self-tag with the tracked topics. Repos without these tags are invisible.
- **No quality scoring:** Ranks purely by stars. Doesn't assess code quality, maintenance status, or actual usefulness.
- **No skill installation:** Shows what's trending but doesn't auto-install skills. You still copy SKILL.md files manually.
- **Snapshot, not stream:** Each run is a point-in-time snapshot. The upstream repo's 15-min cron provides near-real-time tracking, but this local version is on-demand only.

## Why it matters

For teams building Claude-driven products:

- **Skill discovery for agent factories:** If you're assembling multi-skill Claude agents, this leaderboard surfaces the most-adopted building blocks -- which skills have traction and which are experimental.
- **Competitive intelligence:** Track which MCP servers and AI agent patterns are gaining stars fastest. Useful for lead-gen and marketing teams positioning Claude-based offerings.
- **Build-vs-buy signals:** High-star repos with active development suggest community-maintained alternatives to building from scratch. Low-star repos in your domain might signal an underserved niche worth filling.
- **Integration into pipelines:** The JSON output can feed into dashboards, Slack bots, or CI checks that alert when a new skill crosses a star threshold -- useful for automated agent-factory discovery pipelines.
