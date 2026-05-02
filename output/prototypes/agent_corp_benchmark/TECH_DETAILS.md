# Technical Details

## What It Does

Agent-corp is a benchmark framework that evaluates AI coding agents on realistic software engineering tasks set inside a simulated company environment. Unlike synthetic benchmarks (HumanEval, MBPP), agent-corp tasks include team context — PRs, issues, existing codebases, multi-file changes — mirroring what agents actually face in production. Tasks span bug fixes, feature development, refactoring, code review, and test writing.

This demo repo provides a self-contained simulation of the benchmark loop: define tasks, run agents through them, collect structured results, and compare agents side-by-side — all without API keys or external dependencies.

## Architecture

```
agent_corp_demo/
  tasks.py          # Task definitions + simulated agent execution
  evaluate.py       # Scoring, aggregation, and tabular reporting
  run_benchmark.py  # Orchestrator: runs agents, prints results, writes JSON
results/
  benchmark_results.json   # Structured output (auto-generated)
run.sh              # Entry point
```

**Data flow:**

1. `tasks.py` defines 7 tasks across 5 categories with difficulty ratings
2. `run_benchmark.py` loops 3 simulated agents over all tasks
3. `simulate_agent_run()` produces deterministic results (seeded RNG per task+agent)
4. `evaluate.py` aggregates into per-category and per-agent summaries
5. Results are printed as tables and saved as JSON

**Dependencies:** Only `tabulate` (for terminal tables). The real agent-corp repo requires Python 3.9+ and whatever SDK your agent uses.

**Model calls:** This demo makes zero API calls. The real framework delegates to your agent adapter, which makes whatever LLM calls it needs.

## Evaluation Metrics

| Metric | What It Measures |
|--------|-----------------|
| Completion rate | Did the agent produce a correct solution? |
| Code quality | Cleanliness, idiomaticity, structure of the diff |
| Steps | Number of tool calls / actions taken |
| Tokens used | Total token consumption (cost proxy) |
| Tool usage score | How effectively the agent used available tools |

## Limitations

- **Simulated results only** — this demo does not run real agents; it generates plausible scores via seeded RNG to demonstrate the framework's reporting and comparison features.
- **No sandboxed execution** — the real agent-corp runs agents against isolated copies of a codebase; this demo skips that entirely.
- **Limited task set** — 7 tasks across 5 categories; the real benchmark may include more.
- **No automatic correctness checking** — the real framework likely uses test suites or human review; this demo uses pass/fail simulation.

## Why This Matters for Claude-Driven Products

- **Agent factories / agent-as-a-service** — if you're building products that deploy coding agents to customers, you need a repeatable way to measure how well your agent handles real-world SWE tasks before shipping. Agent-corp provides that evaluation harness.
- **CI/CD quality gates** — structured JSON output means you can integrate benchmark runs into CI: fail the build if completion rate drops below a threshold after a model or prompt change.
- **Competitive positioning** — side-by-side comparison tables (as shown in the demo) are exactly what you'd put in sales decks or blog posts when comparing your Claude-based agent to alternatives.
- **Prompt engineering feedback loop** — run the benchmark after every prompt change to quantify impact on code quality, efficiency, and tool usage.
