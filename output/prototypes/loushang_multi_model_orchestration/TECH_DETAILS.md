# Technical Details: Loushang Multi-Model Orchestration

## What It Does

Loushang is a Python-based orchestration runtime that manages multiple LLM coding agents through a single interface. It provides stateful session management (context persists across model switches and restarts), a tool governance layer (policy-enforced access control for each agent's available tools), and full trace logging of every agent action, tool invocation, and output. The core value proposition is treating multi-model agentic coding like a pipeline: plan with one model, implement with another, review with a third — all within a single auditable session.

The platform abstracts provider differences behind a unified agent interface, so switching from Claude to DeepSeek mid-session requires no code changes. Sessions serialize to disk, enabling replay, forking, and audit workflows.

## Architecture

```
loushang/
  core/
    orchestrator.py    # Main workflow engine, routes tasks to agents
    session.py         # Stateful session management (create/fork/resume/serialize)
    registry.py        # Agent/model registry and provider abstraction
  agents/
    base.py            # Abstract agent interface
    anthropic.py       # Claude adapter
    deepseek.py        # DeepSeek adapter
    qwen.py            # Qwen adapter
    kimi.py            # Kimi adapter
    minimax.py         # Minimax adapter
  governance/
    policy.py          # Tool access policy engine
    audit.py           # Trace/audit logger
  workflows/
    pipeline.py        # Multi-step workflow definitions (plan/implement/review)
  tui/
    app.py             # Terminal UI (Textual-based)
  cli/
    main.py            # CLI entry point
```

### Data Flow

1. User defines a workflow (e.g., plan-implement-review) and submits a task
2. Orchestrator creates a session, assigns a unique ID, initializes state
3. For each pipeline step, orchestrator selects the configured model, checks governance policies, and dispatches the task
4. Agent adapter calls the provider API, streams results back
5. Governance layer validates tool calls against policy before execution
6. All actions logged to session trace (JSON)
7. Session state serialized to disk after each step

### Dependencies

- Python 3.10+
- `httpx` — async HTTP for provider APIs
- `pydantic` — data models and validation
- `textual` — TUI framework
- `click` — CLI framework
- `rich` — terminal formatting

### Model Calls

Each agent adapter implements a common interface:
- `plan(task: str) -> PlanResult`
- `implement(subtasks: list[Subtask]) -> ImplementResult`
- `review(artifacts: list[Artifact]) -> ReviewResult`

Calls are async, with configurable timeouts and retry logic per provider.

## Limitations

- **No built-in code execution sandbox** — tool calls that execute code rely on the host environment
- **Provider rate limits** — no built-in queuing; high-throughput workflows may hit limits
- **Session storage is local** — no built-in remote/cloud session sync
- **Limited streaming** — TUI shows streamed output, but CLI mode waits for full responses
- **Early-stage project** — API surface may change; limited test coverage upstream
- **No automatic model selection** — user must configure which model handles which step

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent Factories** | Loushang's workflow engine is a template for building multi-agent pipelines — plan/implement/review maps directly to agent factory patterns |
| **Lead-Gen / Marketing** | Orchestrate a research model (planning) + a copywriting model (implementation) + a quality model (review) in one auditable session |
| **Ad Creatives** | Chain models: one generates concepts, another produces copy, a third validates brand compliance |
| **Voice AI** | Session persistence pattern applies to voice agent state management across turns and model switches |
| **Tool Governance** | Critical for enterprise deployments where different agents need different permission levels — directly applicable to any production agent system |

The traceable delivery aspect is particularly valuable: every action is logged, making it possible to debug, audit, and reproduce agent behavior — essential for regulated industries and quality-sensitive workflows.
