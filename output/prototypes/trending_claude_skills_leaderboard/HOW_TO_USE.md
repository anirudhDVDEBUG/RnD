# How to Use

## Install

```bash
git clone https://github.com/linny006/trending-claude-skills.git
cd trending-claude-skills
pip install -r requirements.txt   # only 'requests' needed
```

Or use the local prototype directly:

```bash
pip install requests
python3 trending_skills.py
```

## Run the demo

```bash
bash run.sh
```

This runs three modes (mock data, no API key needed):
1. Table view (top 12 repos)
2. JSON export (top 5)
3. Topic filter (`claude-skills` only)

### Live mode (optional)

```bash
export GITHUB_TOKEN=ghp_your_token_here
python3 trending_skills.py --live --top 20
```

A token is optional but avoids GitHub's 10-req/min anonymous rate limit.

## As a Claude Skill

Copy the skill definition to your skills directory:

```bash
mkdir -p ~/.claude/skills/trending_claude_skills_leaderboard
cp SKILL.md ~/.claude/skills/trending_claude_skills_leaderboard/SKILL.md
```

### Trigger phrases

- "What are the trending Claude skills right now?"
- "Show me popular AI agent repos"
- "Find me new Claude Code skills to install"
- "What are the top-starred claude-skill repositories?"

When triggered, the skill instructs Claude to fetch the latest leaderboard from the upstream repo's README or run the scraper locally.

## First 60 seconds

```
$ python3 trending_skills.py --top 5

========================================================================
  TRENDING CLAUDE SKILLS LEADERBOARD
  Source: mock data (use --live for real results) | 2026-05-27 06:00 UTC
========================================================================

  #    Repository                               Stars  Lang         Active
  ──── ──────────────────────────────────────── ─────── ──────────── ──────────
  1    anthropics/claude-code                   28,500  TypeScript   1d ago
  2    modelcontextprotocol/servers             19,200  TypeScript   1d ago
  3    punkpeye/awesome-mcp-servers             12,400  Markdown     2d ago
  4    linny006/trending-claude-skills             480  Python       0d ago
  5    pcx-wave/skill-router                       310  Python       6d ago

  Topics tracked: claude-skills, claude-code, mcp-server, ai-agents, coding-agent, ai-workflow
  Total unique repos: 12
========================================================================
```

```
$ python3 trending_skills.py --json --top 2
[
  {
    "repo": "anthropics/claude-code",
    "stars": 28500,
    "forks": 1820,
    "language": "TypeScript",
    "pushed_at": "2026-05-26T18:00:00Z",
    "url": "https://github.com/anthropics/claude-code",
    "description": "Claude Code - an agentic coding tool"
  },
  ...
]
```

## CLI flags

| Flag | Description |
|------|-------------|
| `--live` | Fetch from GitHub API instead of mock data |
| `--top N` | Show top N repos (default: 15) |
| `--json` | Output as JSON |
| `--topic X` | Filter to a single topic (e.g., `claude-skills`, `mcp-server`) |
