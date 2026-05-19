# Open Agent Leaderboard Evaluator

**TL;DR:** Benchmark full AI agent systems — not just models — across 6 realistic task suites using the Exgentic framework from IBM Research. Compare your agent's accuracy, cost, and architecture against published results on the Open Agent Leaderboard.

## Headline Result

> **Tool shortlisting alone improved agent performance across every configuration tested, while cutting costs by up to 50%.** The same Claude Sonnet 4 model scored 51.9% average with vanilla ReAct but 51.9% → 62.1% on SWE-Bench when paired with tool shortlisting — at lower cost.

## Quick Start

```bash
bash run.sh
```

Runs a mock evaluation across all 6 benchmarks, shows per-task results, cost analysis, and ranks your agent against the leaderboard. No API keys needed.

## What's Here

| File | Purpose |
|------|---------|
| `evaluate.py` | Main evaluator — runs benchmarks via Exgentic protocol |
| `leaderboard_data.py` | Published leaderboard scores for comparison |
| `run.sh` | End-to-end demo script |
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install steps, skill setup, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations |

## Source

- [Open Agent Leaderboard Blog Post](https://huggingface.co/blog/ibm-research/open-agent-leaderboard) (IBM Research)
- [Interactive Leaderboard](https://huggingface.co/spaces/open-agent-leaderboard/leaderboard)
- [Exgentic Framework](https://github.com/Exgentic/exgentic)
