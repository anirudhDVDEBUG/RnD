# Technical Details

## What It Does

Maestro is a configuration-driven orchestration layer that sits above multiple AI coding agents (Claude, Codex, Cursor, Gemini, Windsurf). Given a task description, it pattern-matches against routing rules to select the best agent, runs pre/post hooks to maintain project state, and supports multi-step workflows that chain agents together with context handoffs. The original project targets Windows but the pattern is fully cross-platform.

This prototype implements the core routing engine, config loading, and workflow executor with mock agent responses, demonstrating the orchestration logic without requiring actual API keys or agent installations.

## Architecture

```
demo.py                     # Entry point - runs all demos
maestro/
├── __init__.py
├── models.py               # Dataclasses: AgentProfile, RoutingRule, Workflow, etc.
├── loader.py               # YAML config -> model objects
├── router.py               # Pattern-matching router with priority weights
└── orchestrator.py          # Core engine: route->hook->execute->hook pipeline
.maestro/
├── profiles/*.yaml          # Agent capability definitions
├── routing.yaml             # Pattern->agent rules with priorities
├── hooks.yaml               # Pre/post/handoff shell commands
└── workflows/*.yaml         # Multi-step agent pipelines
```

### Data Flow

1. **Task arrives** - Router scans routing rules for regex pattern matches
2. **Priority weighting** - Each match scored by `priority_weight * matched_count`
3. **Fallback** - If no rule matches, profiles are scored by strength/task overlap
4. **Pre-hooks fire** - Simulated shell commands (git diff, state sync)
5. **Agent executes** - MockAgentExecutor returns canned response (swap for real API)
6. **Post-hooks fire** - Validation, logging
7. **Handoff** (workflows only) - Context exported from source to target agent

### Key Design Decisions

- **Regex routing** over LLM-based routing: deterministic, fast, auditable. No token cost for the routing decision itself.
- **YAML config** over code: non-developers can add agents and rules without touching Python.
- **Mock executor** pattern: swap `MockAgentExecutor` for a real implementation that calls Claude API, Codex CLI, etc. The orchestration layer stays the same.

## Dependencies

- `pyyaml` - YAML config parsing
- Python 3.10+ (uses `dict[str, str]` type hints)

No API keys, no network calls, no database.

## Limitations

- **No real agent execution.** This is a routing and orchestration skeleton. You must implement `AgentExecutor` subclasses that actually call each agent's API/CLI.
- **No context window management.** Profiles declare `context_window: large/medium` but the orchestrator doesn't truncate or chunk input to fit.
- **No state persistence.** Workflow state is in-memory only. A production version would need a SQLite/Redis store for resumable workflows.
- **Hooks are simulated.** The hook commands are logged but not executed. Wire them to `subprocess.run()` for real use.
- **No authentication or access control.** Any caller can route to any agent.
- **Simple regex routing.** Complex routing (e.g., "this file is React so use Cursor") would need AST-aware or embedding-based matching.

## Why This Matters for Claude-Driven Products

**Agent factories / multi-agent systems:** This is a lightweight alternative to frameworks like CrewAI or AutoGen for teams that want deterministic routing without the overhead. The YAML-first config makes it easy to version-control and audit agent assignments.

**Lead-gen / marketing automation:** Workflows that chain research (Gemini) -> content generation (Claude) -> formatting (Cursor) map directly to content pipelines. Swap "code tasks" for "marketing tasks" and the routing logic transfers.

**Ad creative pipelines:** Route brief analysis to Claude, visual layout to Cursor, copy variants to Codex - same pattern, different domain.

**Voice AI / conversational agents:** The hook system (pre/post/handoff) is the same pattern needed for managing context between turns in a multi-agent conversation system.

The core value proposition: **you don't need a framework - a config file and 200 lines of Python give you auditable, deterministic multi-agent orchestration.**
