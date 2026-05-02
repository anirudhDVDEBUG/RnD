# Technical Details — PRTS Agent Terminal Service

## What it does

PRTS (Rebuild Terminal Service) is a terminal-first framework for orchestrating multiple AI agents from a single REPL. Each agent has a lifecycle (idle / running / completed / failed / rebuilding) managed by a central dispatcher. The key feature is **hot rebuild**: an agent can be restarted mid-session — clearing its internal state without removing it from the registry or restarting the whole service. This makes it practical for long-running terminal sessions where you iterate on agent behavior.

The original [zayokami/PRTS](https://github.com/zayokami/PRTS) is a TypeScript/Cloudflare Worker project themed around Arknights' in-game AI system. This prototype extracts the architectural pattern — agent registry + dispatch + rebuild — and reimplements it in Python as a local, zero-dependency orchestration layer.

## Architecture

```
main.py
  └── Dispatcher (orchestrator/dispatcher.py)
        ├── ResearchAgent  ─┐
        ├── CodeAgent       ├── agents/worker.py (all extend agents/base.py)
        └── SummaryAgent   ─┘
  └── TerminalService (terminal/interface.py)
        └── cmd.Cmd REPL → calls Dispatcher methods
```

**Data flow:**

1. User types `dispatch <type> <payload>` in the REPL.
2. `TerminalService.do_dispatch()` calls `Dispatcher.dispatch(type, payload)`.
3. Dispatcher resolves which agent handles `type` by checking each agent's `task_types` list.
4. Agent's `run()` sets state to RUNNING, calls `execute()`, captures result or error.
5. On failure, dispatcher auto-rebuilds the agent and retries once.
6. Result JSON is printed to the terminal.

**Key files:**

| File | Lines | Role |
|------|-------|------|
| `agents/base.py` | ~85 | Abstract `Agent` ABC with state machine, lifecycle hooks, status reporting |
| `agents/worker.py` | ~70 | Three mock agents (research, code, summary) |
| `orchestrator/dispatcher.py` | ~65 | Agent registry, task routing, retry + rebuild logic |
| `terminal/interface.py` | ~90 | `cmd.Cmd` subclass — REPL commands, batch mode |
| `main.py` | ~30 | Wires components, `--demo` flag for non-interactive run |

**Dependencies:** Only `pyyaml` (for config parsing). The core framework uses only the Python stdlib (`cmd`, `abc`, `enum`, `json`, `time`).

## Limitations

- **No real LLM calls.** Agents return mock/template data. Swap `execute()` implementations to call OpenAI, Anthropic, or local models.
- **Single-process, synchronous.** No async dispatch, no parallel agent execution. Works fine for sequential terminal use; not suited for high-throughput server scenarios.
- **No persistence.** Agent state lives in memory. Restarting the process loses all history.
- **No auth or multi-user.** It's a local terminal tool, not a network service.
- **Config file is read but not wired** to dynamically load agents (agents are registered in `main.py`). Extending to YAML-driven registration is straightforward.

## Why it matters for Claude-driven products

**Agent factories / orchestration layers:** If you're building a system where Claude (or another LLM) spawns and manages sub-agents — research, code generation, summarization — this pattern gives you a clean registry + dispatch + lifecycle layer. The rebuild mechanism is especially relevant for long-running agent sessions where you want to reset a misbehaving agent without tearing down the whole system.

**Terminal-first prototyping:** Before building a web UI, you can iterate on agent behavior from a REPL. The `cmd.Cmd` interface is trivial to extend and works over SSH, in CI pipelines, and in Docker containers.

**Pluggable architecture:** Swap mock agents for real LLM-backed ones by changing `execute()`. The orchestration layer doesn't care what the agent does internally — it manages lifecycle, routing, and error recovery. This makes it a good skeleton for multi-agent demos, internal tools, or Claude-powered automation pipelines.
