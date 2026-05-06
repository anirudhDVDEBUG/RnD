# AI Dev Effectiveness: Git Analysis

**Point it at any git repo. Get back: which commits were AI-assisted (Claude/Copilot/Cursor/Codex), how many lines each tool wrote, and a productivity multiplier estimate.**

## Headline Result (demo)

```
  AI-assisted commits : 142 (40.9%)
  Combined multiplier : 1.73x
  Top tool            : Claude Code (89 commits)
```

## Quick Start

```bash
bash run.sh                              # demo mode, no keys needed
python3 analyze.py --repo /path/to/repo  # analyze a real repo
python3 analyze.py --repo . --output json | jq .combined_multiplier
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) -- install, configure as a Claude skill, trigger phrases
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, detection heuristics, limitations

## Source

Upstream: [denn-gubsky/ai-dev-effectiveness](https://github.com/denn-gubsky/ai-dev-effectiveness)
