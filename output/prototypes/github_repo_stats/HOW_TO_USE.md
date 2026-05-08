# How to Use — GitHub Repo Stats Skill

## What This Is

A **Claude Code skill** — a markdown file that teaches Claude Code how to fetch GitHub repository statistics on demand. No server, no MCP, no binary. Just drop a file and start asking.

## Install (30 seconds)

```bash
# 1. Create the skill directory
mkdir -p ~/.claude/skills/github_repo_stats

# 2. Copy the skill file
cp SKILL.md ~/.claude/skills/github_repo_stats/SKILL.md
```

That's it. Claude Code picks up skills from `~/.claude/skills/` automatically.

### Optional: Set a GitHub Token

Without a token you get 60 API requests/hour. With one, 5,000/hour.

```bash
export GITHUB_TOKEN="ghp_yourTokenHere"
```

Or add it to your shell profile (`~/.bashrc`, `~/.zshrc`).

## Trigger Phrases

Say any of these to Claude Code and the skill activates:

| Phrase | Example |
|--------|---------|
| `repo stats` | "repo stats for facebook/react" |
| `github stats` | "github stats on torvalds/linux" |
| `how many commits` | "how many commits does langchain have?" |
| `repository info` | "repository info for anthropics/claude-code" |
| `evaluate repo` | "evaluate repo https://github.com/simonw/datasette" |

Both `owner/repo` shorthand and full `https://github.com/owner/repo` URLs work.

## First 60 Seconds

1. Open Claude Code in any project directory:
   ```bash
   claude
   ```

2. Type a query:
   ```
   > Show me stats for simonw/datasette
   ```

3. Claude will:
   - Hit the GitHub REST API (`/repos`, `/commits`, `/languages`)
   - Parse the response and commit count from pagination headers
   - Print a clean Markdown summary table

### Example Output

```
## simonw/datasette

| Metric           | Value                                   |
|------------------|-----------------------------------------|
| Description      | An open source multi-tool for exploring… |
| Stars            | 9,842                                   |
| Forks            | 702                                     |
| Total Commits    | 4,217                                   |
| Open Issues      | 318                                     |
| Primary Language | Python                                  |
| License          | Apache-2.0                              |
| Created          | 2017-11-13                              |
| Last Push        | 2026-05-06                              |
| Size             | 45,320 KB                               |
| Archived         | No                                      |
| Top Languages    | Python 88.2%, JavaScript 7.1%, HTML 4.0%|
```

## Running the Standalone Demo

```bash
# Uses mock data — no API key needed
bash run.sh

# Or run directly against the live API
python3 github_repo_stats.py simonw/datasette
```

## Dependencies

- Python 3.8+
- No pip packages required (uses only `urllib` and standard library)
