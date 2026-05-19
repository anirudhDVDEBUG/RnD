# Technical Details

## What It Does

The Open Agent Leaderboard is an evaluation platform from IBM Research that benchmarks **complete agent systems** — not just underlying models. It measures the combined effect of model choice, agent architecture (ReAct, tool use patterns, planning strategies), and tooling across six diverse benchmarks covering code repair, web research, app automation, and customer service. The Exgentic framework provides a unified evaluation protocol so a single agent implementation can be tested across all benchmarks without per-benchmark adaptation.

This demo prototype simulates that evaluation flow locally using mock task execution, letting you explore the leaderboard's structure, metrics, and cost analysis without needing API keys or the full benchmark datasets.

## Architecture

### Files

| File | Role |
|------|------|
| `evaluate.py` | Main entry point. Implements `ExgenticProtocol` class that creates task envelopes (Task/Context/Actions), runs mock evaluations, and renders results. |
| `leaderboard_data.py` | Static dataset of published leaderboard scores (~6 agent configurations). Used for comparison ranking. |
| `run.sh` | Orchestrates three demo modes: full eval, single benchmark, leaderboard comparison. |

### Data Flow

```
CLI args → ExgenticProtocol.evaluate_benchmark()
         → For each task in benchmark:
             create_task_envelope() → run_task() → collect result
         → Aggregate metrics (success rate, cost)
         → Rank against leaderboard_data
         → Print tables + optional JSON export
```

### The Exgentic Protocol (Real Version)

The real framework uses three components shared across all benchmarks:

- **Task** — structured description of what the agent must accomplish
- **Context** — benchmark rules, available tools, constraints, max steps
- **Actions** — allowed operations (observe, think, act, submit)

This means one agent speaks one language across SWE-Bench, AppWorld, BrowseComp+, and all three tau2-Bench domains. The protocol handles benchmark-specific setup (repo checkout for SWE-Bench, API mocking for AppWorld, policy loading for tau2) transparently.

### Key Dependencies (Real Framework)

- `exgentic` — evaluation orchestrator (install from GitHub, not yet on PyPI)
- LLM API access (Anthropic, OpenAI, Google, or open-weight model endpoints)
- Benchmark-specific datasets (downloaded automatically by Exgentic)

### Model Calls

The demo makes zero API calls. The real framework makes LLM calls per agent step (typically 5-25 steps per task), with costs tracked per-call and aggregated.

## Limitations

- **Mock data only** — this prototype simulates results with random outcomes seeded for reproducibility. It does not run real agent logic.
- **Scores are approximate** — leaderboard numbers are based on the published blog post and may not reflect the latest live leaderboard state.
- **No trajectory recording** — the real Exgentic framework captures full agent trajectories (every thought, action, observation). This demo only tracks step counts.
- **Single-agent only** — the demo evaluates one mock agent. The real framework supports batch evaluation of multiple agent configurations.
- **No benchmark data** — SWE-Bench repos, AppWorld APIs, and tau2 policy databases are not included. The real framework downloads these automatically.

## Why This Matters for Claude-Driven Products

### Agent Factories
If you're building systems that generate or configure agents, the leaderboard provides empirical data on which architecture choices matter. Tool shortlisting improved every configuration tested — that's a concrete design pattern to bake into agent factory defaults.

### Lead-Gen / Marketing Agents
The tau2-Bench results (airline, retail, telecom) directly measure customer-service agent quality. A marketing team deploying Claude-powered chat agents can use these benchmarks to validate their agent handles policy-constrained conversations correctly before going live.

### Cost Optimization
The leaderboard tracks $/task alongside accuracy. The finding that failed runs cost 20-54% more than successful ones means early failure detection (circuit breakers, confidence thresholds) directly reduces spend. The 2x+ cost difference between architectures using the same model means architecture choice is a first-class cost lever.

### Multi-Domain Agents
The key finding that general-purpose agents can match specialized ones challenges the assumption that you need a separate agent per domain. A single well-architected Claude agent with tool shortlisting can handle code, customer service, and web research — simplifying deployment and maintenance.
