# OpenClaw Orchestra — Multi-Agent Orchestration

**TL;DR:** Spawn isolated specialist agents (backend, frontend, reviewer) that each get their own workspace, memory, and tools. A central orchestrator decomposes tasks, delegates to agents, and tracks progress via Linear tickets. Claude-powered autonomous workflows out of the box.

## Headline Result

```
Task: "Implement user authentication flow"
  -> 3 specialist agents spawned
  -> 3 subtasks auto-decomposed and assigned
  -> 3 Linear tickets created & tracked
  -> Artifacts written to isolated workspaces
  -> Review agent approves with minor suggestions
  All done in < 1 second (mock mode)
```

## Quick Start

```bash
bash run.sh
```

No API keys needed — runs in mock mode with simulated agent reasoning.

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, trigger phrases for the Claude skill
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why it matters
