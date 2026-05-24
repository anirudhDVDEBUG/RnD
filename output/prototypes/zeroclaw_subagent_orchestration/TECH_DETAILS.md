# Technical Details — ZeroClaw Subagent Orchestration

## What It Does

ZeroClaw is a **task decomposition and multi-agent routing pattern** for Claude Code. Given a complex user request, it breaks the work into specialized subtasks (research, implementation, review), dispatches each to a focused subagent with scoped tools, runs them in parallel where possible, and merges results with conflict detection. The pattern uses Claude Code's built-in `Agent` tool with `subagent_type` to spawn real subagents — each gets its own context window, reducing token usage on the main conversation.

The core insight: instead of one monolithic Claude conversation juggling research, coding, and validation, you get three (or more) focused agents that each do one thing well and return only their findings. The orchestrator handles coordination, error recovery, and synthesis.

## Architecture

```
demo.py                  Entry point — defines tasks, runs orchestrator
zeroclaw/
  orchestrator.py        Top-level: decompose -> route -> merge
  router.py              RouterConfig + Router: maps subtasks to agents
  agents.py              AgentSpec + AgentResult: agent definitions + mock execution
  merger.py              merge_results(): combines outputs, detects conflicts
```

### Data Flow

```
User Task (string)
    |
    v
Orchestrator.decompose()    ->  list[{agent, task, context}]
    |
    v
Router.dispatch()           ->  ThreadPoolExecutor (parallel) or sequential loop
    |         |         |
    v         v         v
AgentSpec.execute()         ->  AgentResult per agent
    |
    v
merge_results()             ->  MergedResult (status, summary, conflicts)
```

### Key Files

| File | Purpose | Lines |
|---|---|---|
| `orchestrator.py` | Pipeline coordination, task decomposition | ~45 |
| `router.py` | Agent registry, parallel/sequential dispatch | ~75 |
| `agents.py` | Agent specs, mock execution, result dataclass | ~95 |
| `merger.py` | Result aggregation, conflict detection | ~55 |
| `demo.py` | CLI demo with 3 scenarios | ~90 |

### Dependencies

- **Python 3.10+** (uses `X | Y` union syntax)
- **Zero external packages** — only `concurrent.futures`, `dataclasses`, `time`, `random`, `json` from stdlib
- In production, you'd call the Anthropic API or use Claude Code's Agent tool instead of mock execution

### Model Calls

The demo uses **no model calls** — agent execution is simulated with deterministic mock logic. In real usage as a Claude Code skill, the `Agent` tool spawns actual Claude subagents:

- `subagent_type=Explore` for research (read-only, cheaper)
- `subagent_type=Code` for implementation (can write files)
- Custom review agents validate outputs

## Limitations

- **Skill-only pattern.** This is an orchestration *pattern* taught via SKILL.md, not a standalone framework. It depends on Claude Code's Agent tool for real subagent spawning.
- **No real Claude API calls in demo.** The mock agents return synthetic data. Production use requires Claude Code or Anthropic API access.
- **Decomposition is rule-based.** The demo always splits into research/code/review. A real implementation would use Claude to intelligently decompose arbitrary tasks.
- **No persistent state.** Each orchestration run is stateless. There's no memory of previous runs or agent outputs.
- **No MCP server bundled.** MCP integration relies on whatever servers the user already has configured in `~/.claude.json`.
- **No error recovery in demo.** Production should retry failed agents and handle partial failures gracefully.

## Why This Matters

For teams building Claude-driven products:

- **Agent factories:** This is the core pattern for building multi-agent systems. The router + agent registry is reusable across lead-gen pipelines, content creation workflows, and automated QA.
- **Token efficiency:** Subagents with `subagent_type=Explore` protect the main context window. A research agent that reads 50 files only returns a summary — the orchestrator never sees the raw file contents.
- **Parallelism:** Independent subtasks run concurrently. A research + code + review pipeline completes in wall-clock time of the slowest agent, not the sum.
- **Marketing/ad automation:** The decompose-route-merge pattern maps directly to content pipelines: research competitor ads -> generate creative variants -> review for brand compliance.
- **Extensibility:** Adding a new specialist (security auditor, SEO reviewer, translation agent) is one `AgentSpec` definition and one `config.register()` call.
