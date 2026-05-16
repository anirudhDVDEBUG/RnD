# Polis Protocol — Multi-Agent Routing

**TL;DR:** A markdown-based protocol for orchestrating multi-vendor AI agent teams (Claude, GPT, Gemini, Codex) using capability cards, Thompson Sampling bandit routing, and a compounding lessons ledger. Zero dependencies, pure Python.

## Headline Result

After 60 simulated routing rounds the bandit router learns to pick the optimal agent **~75% of the time**, with average reward climbing as lessons compound — no manual routing rules needed.

```
  Optimal agent selected: 45/60 (75.0%)
  Average reward:         0.812
```

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, skill setup, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations

## Source

[yehudalevy-collab/polis-protocol](https://github.com/yehudalevy-collab/polis-protocol)
