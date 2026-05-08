---
name: github_repo_stats
description: |
  Fetch and display comprehensive GitHub repository statistics including commit count, stars, forks, issues, and other useful metrics.
  Triggers: "repo stats", "github stats", "how many commits", "repository info", "evaluate repo"
---

# GitHub Repo Stats

Fetch and display key statistics for any GitHub repository, including commit count, stars, forks, open issues, language breakdown, and more.

## When to use

- "Show me stats for owner/repo"
- "How many commits does this GitHub repo have?"
- "Give me an overview of this repository"
- "Evaluate this GitHub project"
- "What are the stats on github.com/owner/repo?"

## How to use

1. **Parse the repo identifier.** Accept either a full GitHub URL (e.g. `https://github.com/simonw/datasette`) or a shorthand `owner/repo` string. Extract the `owner` and `repo` values.

2. **Fetch repository metadata** using the GitHub REST API:

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}" | python3 -m json.tool
```

Extract and display these fields:
- **Full name** (`full_name`)
- **Description** (`description`)
- **Stars** (`stargazers_count`)
- **Forks** (`forks_count`)
- **Open issues** (`open_issues_count`)
- **Primary language** (`language`)
- **License** (`license.spdx_id`)
- **Created** (`created_at`)
- **Last pushed** (`pushed_at`)
- **Default branch** (`default_branch`)
- **Archived** (`archived`)
- **Size** (`size` in KB)

3. **Fetch total commit count** (not directly available from the repo endpoint). Use the Contributors API with `per_page=1` and inspect the `Link` header, or use the Commits API:

```bash
# Method: get commits on default branch, page 1, per_page=1, and read the Link header for last page number
curl -sI "https://api.github.com/repos/{owner}/{repo}/commits?per_page=1" | grep -i '^link:'
```

Parse the `last` page number from the `Link` header — that number equals the total commit count on the default branch.

If no `Link` header is present, there is only 1 page (i.e., very few commits); count them directly:

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/commits?per_page=100" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))"
```

4. **Fetch language breakdown** for richer detail:

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/languages" | python3 -m json.tool
```

5. **Present a summary table** to the user with all gathered stats, formatted cleanly in Markdown.

### Example output

```
## simonw/datasette

| Metric            | Value                  |
|-------------------|------------------------|
| Description       | An open source tool... |
| Stars             | 9,500                  |
| Forks             | 680                    |
| Total Commits     | 4,200                  |
| Open Issues       | 320                    |
| Primary Language  | Python                 |
| License           | Apache-2.0             |
| Created           | 2017-11-13             |
| Last Push         | 2026-05-06             |
| Size              | 45,000 KB              |
| Top Languages     | Python 85%, JS 10%...  |
```

### Notes

- If a `GITHUB_TOKEN` environment variable is available, include it as `Authorization: Bearer $GITHUB_TOKEN` to avoid rate limits and access private repos.
- The unauthenticated GitHub API rate limit is 60 requests/hour. Authenticated is 5,000/hour.
- Commit count via the `Link` header method is an approximation scoped to the default branch.

## References

- Inspired by Simon Willison's [GitHub Repo Stats tool](https://simonwillison.net/2026/May/7/github-repo-stats/#atom-everything)
- [GitHub REST API – Repos](https://docs.github.com/en/rest/repos/repos)
- [GitHub REST API – Commits](https://docs.github.com/en/rest/commits/commits)
