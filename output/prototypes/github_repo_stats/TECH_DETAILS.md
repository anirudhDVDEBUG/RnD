# Technical Details — GitHub Repo Stats

## What It Does

This skill instructs Claude Code to query three GitHub REST API endpoints for any given repository and compile the results into a single summary table. It extracts metadata (stars, forks, description, license, dates), estimates total commit count via pagination header inspection, and computes a percentage-based language breakdown — all without any external dependencies.

The core technique for commit counting is noteworthy: rather than paginating through every commit, the skill requests `per_page=1` and reads the `rel="last"` page number from the HTTP `Link` header. That page number equals the total commit count on the default branch, turning an O(n) operation into a single request.

## Architecture

```
User prompt ("repo stats for owner/repo")
        |
        v
  Claude Code activates SKILL.md
        |
        v
  Three GitHub REST API calls (via curl):
    1. GET /repos/{owner}/{repo}         → metadata
    2. HEAD /repos/{owner}/{repo}/commits → commit count (Link header)
    3. GET /repos/{owner}/{repo}/languages → language bytes
        |
        v
  Claude formats Markdown summary table
```

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill definition — Claude Code reads this to learn the procedure |
| `github_repo_stats.py` | Standalone Python implementation (same logic, runnable outside Claude) |
| `run.sh` | Demo runner with mock data fallback |

### Dependencies

- **Runtime:** Python 3.8+ (standard library only — `urllib.request`, `json`, `re`)
- **Optional:** `GITHUB_TOKEN` env var for authenticated requests (5,000 req/hr vs 60)
- **No pip packages required**

## API Endpoints Used

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/repos/{owner}/{repo}` | GET | Stars, forks, issues, description, license, dates, size |
| `/repos/{owner}/{repo}/commits?per_page=1` | HEAD | `Link` header with last page = commit count |
| `/repos/{owner}/{repo}/languages` | GET | Language → bytes mapping |

## Limitations

- **Commit count is an approximation.** It counts commits on the default branch only. Merge commits, squash merges, and orphan branches can skew the number.
- **Rate limits.** Unauthenticated: 60 requests/hour (each skill invocation uses 3 requests). Authenticated: 5,000/hour.
- **Private repos** require a `GITHUB_TOKEN` with appropriate scopes.
- **No historical trending.** This is a point-in-time snapshot, not a time series.
- **No contributor stats.** The Contributors API is expensive and often returns 202 (computing); the skill deliberately skips it.
- **Large monorepos** (e.g., chromium) may have unreliable commit counts due to GitHub's internal pagination limits.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Lead-gen / sales intelligence** | Quickly qualify open-source prospects by repo activity, popularity, and tech stack before outreach. |
| **Agent factories** | Composable skill pattern — this is a clean example of teaching Claude a multi-step API workflow via a single markdown file. Fork it to build skills for any REST API. |
| **Marketing / content** | Generate data-backed content ("Top 10 fastest-growing Python repos this month") by scripting skill invocations across repo lists. |
| **Due diligence** | Evaluate open-source dependencies before adopting them — last push date, issue backlog, license compatibility. |

## References

- Inspired by Simon Willison's [GitHub Repo Stats tool](https://simonwillison.net/2026/May/7/github-repo-stats/#atom-everything)
- [GitHub REST API — Repos](https://docs.github.com/en/rest/repos/repos)
- [GitHub REST API — Commits](https://docs.github.com/en/rest/commits/commits)
