# Maestro Agent Orchestrator

**Route coding tasks to the right AI agent automatically.** Define profiles for Claude, Codex, Cursor, Gemini, and Windsurf, set up pattern-based routing rules, and chain agents into multi-step workflows with shared hooks and context handoffs.

> **Headline result:** Given 6 different coding tasks, the orchestrator correctly routes each to the best-suited agent (architecture to Claude, scaffolding to Codex, UI work to Cursor, research to Gemini) in under a second.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** - Install, configure, and run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** - Architecture, data flow, limitations

## Run It

```bash
bash run.sh
```

No API keys required - uses mock agent responses to demonstrate the routing, hooks, and workflow pipeline.

## Source

Based on [FernandoBolzan/Orquestrador-Maestro](https://github.com/FernandoBolzan/Orquestrador-Maestro).
