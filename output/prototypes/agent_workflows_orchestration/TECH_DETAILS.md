# Technical Details

## What it does

`agent-workflows` (CLI: `owf`) is a zero-dependency Python runtime for orchestrating multiple LLM calls within a single script. It provides five primitives — **fan-out**, **pipeline**, **validate**, **budget**, and **resume** — backed by a durable SQLite journal. Workflows are defined in plain Python, not YAML, so you get full control over branching, loops, and error handling.

The key differentiator from heavier frameworks (LangGraph, CrewAI, AutoGen) is minimalism: no server, no DAG DSL, no external state store. One `.py` file, one `owf run` command.

## Architecture

```
demo_workflow.py          # user-authored workflow script
  |
  v
Workflow                  # orchestrator: tracks steps, enforces budget
  |-- fan_out()           # creates N parallel Step objects
  |-- pipeline()          # chains steps sequentially
  |-- validate()          # attaches JSON-schema-style checks
  |-- run()               # executes all steps via an Adapter
        |
        v
  Adapter (pluggable)     # FakeAdapter | claude CLI | codex | custom
        |
        v
  Journal (SQLite)        # owf_journal.sqlite — durable run log
    |-- runs table        # run_id, workflow name, status, total_cost
    |-- steps table       # step_id, prompt, result, status, cost
```

### Key files

| File | Purpose |
|------|---------|
| `agent_workflows/core.py` | Workflow, Step, Adapter, FakeAdapter, Journal classes |
| `agent_workflows/__init__.py` | Public API re-exports |
| `demo_workflow.py` | End-to-end demo script |
| `run.sh` | One-command runner |
| `SKILL.md` | Claude Code skill definition |

### Data flow

1. User defines steps via `fan_out()` and `pipeline()`.
2. `run()` iterates through all steps, calling the adapter for each.
3. Each step result is logged to the SQLite journal.
4. Budget is checked before each step; workflow pauses if exceeded.
5. On resume, completed step IDs are read from the journal and skipped.

### Dependencies

- **Runtime**: Python 3.8+ stdlib only (`sqlite3`, `uuid`, `dataclasses`, `json`).
- **Real package**: `pip install agent-workflows` — also zero-dependency.
- **Adapters**: The `claude` adapter shells out to the `claude` CLI. The `fake` adapter needs nothing.

## Limitations

- **No true parallelism**: Fan-out steps run sequentially in the current implementation (the real package may add async/threading).
- **No streaming**: Results are returned as complete strings, not streamed.
- **Schema validation is basic**: Only checks `minLength` in this demo; the real package may support full JSON Schema.
- **No retry logic**: Failed steps stay failed — resume skips completed ones but doesn't retry failures.
- **Adapter ecosystem is small**: Only `claude`, `codex`, and `fake` ship built-in. Custom adapters are straightforward but undocumented.

## Why this matters for Claude-driven products

| Use case | How owf helps |
|----------|---------------|
| **Agent factories** | Define reusable workflow templates (fan-out research, pipeline summarization) that can be parameterized and re-run. |
| **Lead-gen / marketing** | Fan out across market segments, pipeline into a unified report, validate output quality before delivery. |
| **Ad creatives** | Generate multiple ad variants in parallel, rank/validate, stay within budget. |
| **Voice AI** | Chain transcription → analysis → response-generation steps with resume support for long-running calls. |
| **Cost control** | Budget caps prevent runaway API spend — critical for production agent loops. |
| **Auditability** | SQLite journal provides a complete, queryable history of every prompt and response for compliance. |
