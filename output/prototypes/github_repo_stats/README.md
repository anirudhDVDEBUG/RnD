# GitHub Repo Stats — Claude Code Skill

**One-line summary:** A Claude Code skill that fetches and displays comprehensive GitHub repository statistics (stars, forks, commits, language breakdown, and more) from a simple natural-language prompt like *"show me stats for simonw/datasette"*.

## Headline Result

```
$ claude "repo stats for simonw/datasette"

## simonw/datasette
| Metric           | Value                          |
|------------------|--------------------------------|
| Stars            | 9,842                          |
| Forks            | 702                            |
| Total Commits    | 4,217                          |
| Open Issues      | 318                            |
| Primary Language | Python                         |
| License          | Apache-2.0                     |
| Top Languages    | Python 88.2%, JS 7.1%, HTML 4% |
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the skill, trigger phrases, first-60-seconds walkthrough.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, API details, limitations, and strategic relevance.

## Try the Demo

```bash
bash run.sh
```

Runs against mock data (no GitHub token needed) and shows exactly what the skill output looks like.
