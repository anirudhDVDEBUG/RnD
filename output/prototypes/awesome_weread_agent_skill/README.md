# Awesome WeRead Agent Skill

**TL;DR**: A curated catalog of projects built on WeChat Reading's (微信读书) official Agent Skill, with a working demo that exports reading highlights to Obsidian markdown, JSON, and generates MCP server configs for Claude integration.

## Headline Result

```
  Exported 6 highlights from 3 books -> Obsidian vault
  Generated MCP config for Claude integration
  Browsed 6 ecosystem projects across 3 categories
```

Run it yourself in under 10 seconds:

```bash
bash run.sh
```

No API keys or external dependencies required — uses mock WeRead data to demonstrate the full pipeline.

## What's Inside

| File | Purpose |
|------|---------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install steps, skill setup, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations |
| `weread_demo.py` | Main demo: catalog browser, Obsidian export, JSON export, MCP config |
| `run.sh` | One-command end-to-end runner |

## Source

[BENZEMA216/awesome-weread](https://github.com/BENZEMA216/awesome-weread) — Curated projects built on WeRead's official Agent Skill (released 2026-05-17)
