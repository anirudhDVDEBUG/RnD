# Technical Details — Multi-Agent Market Lab

## What It Does

The Multi-Agent Market Lab is an orchestration framework that runs multiple autonomous research agents in parallel, each assigned to a specific market segment. Agents independently discover market signals (opportunities, threats, trends, anomalies), while a central orchestrator manages experiment lifecycle and dynamically rebalances resource allocation based on observed agent performance. The system uses hypothesis-driven experiment tracking — you define success metrics upfront and evaluate results against them.

In this demo, agents use mock signal generation (random with configurable parameters). In production, you'd wire each agent's `research()` method to real data sources (news APIs, social listening, patent databases, earnings feeds).

## Architecture

```
Orchestrator
├── AgentFleet
│   ├── ResearchAgent (voice_ai)      → MarketSignal[]
│   ├── ResearchAgent (ad_creatives)  → MarketSignal[]
│   ├── ResearchAgent (agent_factories) → MarketSignal[]
│   └── ResearchAgent (lead_gen)      → MarketSignal[]
├── ExperimentTracker
│   └── Experiment (hypothesis + metrics + results)
└── AllocationEngine
    └── rebalance() → score-based budget redistribution
```

### Key Files

| File | Purpose |
|------|---------|
| `market_lab/orchestrator.py` | Central coordinator — runs iterations, rebalances, manages experiments |
| `market_lab/agent.py` | `ResearchAgent` class — autonomous signal discovery per segment |
| `market_lab/experiment.py` | `Experiment` + `ExperimentTracker` — hypothesis-driven lifecycle |
| `demo.py` | End-to-end demo showing full pipeline |

### Data Flow

1. **Config** defines agents (name, segment, budget, capabilities)
2. **Orchestrator.run_iteration()** calls each agent's `research()` in sequence
3. Each agent produces `MarketSignal` objects (source, type, confidence, summary)
4. **Experiment.record_iteration()** logs aggregate metrics per iteration
5. **Orchestrator.rebalance()** redistributes budgets proportional to performance scores
6. **Experiment.evaluate()** checks results against predefined success metrics

### Dependencies

- **Runtime:** Python 3.10+ (stdlib only — `dataclasses`, `random`, `time`, `json`, `enum`)
- **No external packages** for the demo
- **Production additions:** `httpx` for async HTTP, `anthropic` SDK for Claude-powered reasoning, `pydantic` for config validation

## Limitations

- **Mock data only** — no real market data sources connected in this demo
- **Sequential execution** — agents run in a loop, not truly parallel (add `asyncio` for production)
- **No persistence** — state lives in memory; add SQLite/Redis for durable experiment tracking
- **No Claude integration** — agents don't use LLM reasoning; they'd need Claude API calls to analyze/summarize real signals
- **Simple rebalancing** — linear score-based; no multi-armed bandit or Bayesian optimization

## Why This Matters for Claude-Driven Products

| Domain | Application |
|--------|-------------|
| **Lead-gen** | Deploy agents per ICP segment, auto-discover buying signals, rebalance toward highest-converting segments |
| **Ad creatives** | Track competitor creative strategies across channels, surface winning patterns |
| **Agent factories** | Meta-layer: orchestrate specialized Claude agents that each handle a different research vertical |
| **Voice AI** | Monitor voice-tech landscape (new STT/TTS providers, pricing changes, API launches) |
| **Marketing** | Hypothesis-driven A/B research — "Does segment X respond to messaging Y?" with structured tracking |

The pattern of autonomous agents + experiment tracking + dynamic allocation is directly applicable to any Claude Code skill that needs to coordinate multiple research or generation tasks with measurable outcomes.
