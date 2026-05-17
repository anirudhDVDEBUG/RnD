# Technical Details: Multi-Agent Orchestration Engine

## What It Does

This is a lightweight orchestration framework that coordinates multiple AI agents across three execution patterns: sequential pipelines (agents pass output forward), parallel fan-outs (independent tasks run concurrently via ThreadPoolExecutor), and hierarchical delegation (a coordinator breaks down work and assigns it to specialists). The framework uses Python's stdlib threading primitives and dataclasses — no external dependencies.

The source project (harmonist-orchestral) provides these patterns as a reusable engine for Claude Code agent swarms, where each "agent" maps to a Claude Code sub-agent invocation via the Agent tool.

## Architecture

```
orchestrator.py (single file, ~280 lines)
├── Data models: Agent, AgentResult, TaskStatus
├── Pipeline       — sequential stage execution with output forwarding
├── FanOut         — concurrent execution via ThreadPoolExecutor
├── Coordinator    — hierarchical delegation pattern
└── Demo handlers  — simulated agent work (research, plan, implement, review)
```

### Key Files

| File | Purpose |
|------|---------|
| `orchestrator.py` | Core engine: Agent, Pipeline, FanOut, Coordinator classes |
| `run.sh` | Entry point — runs the full demo |
| `requirements.txt` | Dependencies (stdlib only) |

### Data Flow

1. **Pipeline:** `initial_input -> Agent1.execute() -> merged_output -> Agent2.execute() -> ... -> final_result`
2. **FanOut:** `[task1, task2, ...] -> ThreadPoolExecutor -> [result1, result2, ...]` (concurrent)
3. **Hierarchical:** `task -> Coordinator.plan() -> [delegate1, delegate2, ...] -> aggregated_results`

### Dependencies

- Python 3.10+ (for `type | None` syntax and `match` support)
- `concurrent.futures` (stdlib) for parallel execution
- `threading` (stdlib) for thread safety
- `dataclasses` (stdlib) for data models

### Model Calls

None in the demo. In production use with Claude Code, each `Agent.execute()` maps to a Claude API call via the Agent tool. The framework is model-agnostic — handlers can wrap any LLM call.

## Limitations

- **No persistent state:** Agent results live in memory only; no database or file-based persistence between runs.
- **No retry/backoff:** Failed agents don't automatically retry. You'd need to wrap handlers with retry logic.
- **No real LLM calls:** The demo uses simulated handlers. Real deployment requires connecting handlers to Claude API or using Claude Code's Agent tool directly.
- **No distributed execution:** All agents run in a single process. For true distributed swarms, you'd need a message queue (Redis, RabbitMQ) or task framework (Celery).
- **Thread-based parallelism:** Limited by GIL for CPU-bound tasks. Fine for I/O-bound LLM API calls.

## Why It Matters

For teams building Claude-driven products:

- **Agent factories:** This is the coordination layer for spawning and managing multiple specialized agents. If you're building an agent factory that produces domain-specific agents, this framework handles their orchestration.
- **Lead-gen / marketing pipelines:** The sequential pattern maps perfectly to research -> qualify -> personalize -> outreach workflows. Each stage is a focused agent.
- **Ad creative generation:** Fan-out pattern lets you generate multiple ad variants in parallel (different angles, audiences, formats) then use a reviewer agent to select winners.
- **Voice AI post-processing:** Hierarchical pattern works for transcription -> extraction -> action pipelines where a coordinator routes different intents to specialized handlers.
- **Complex code tasks:** Claude Code already uses sub-agents internally. This skill teaches Claude to be explicit about orchestration patterns, improving reliability on multi-step tasks.

## Source

[2508965-ship-it/harmonist-orchestral](https://github.com/2508965-ship-it/harmonist-orchestral) — Multi-Agent Orchestration Engine 2026
