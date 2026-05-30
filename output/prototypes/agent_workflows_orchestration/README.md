# Agent Workflows Orchestration

**Provider-agnostic, zero-dependency Python runtime for multi-step agent workflows.** Fan-out, pipeline, validate, budget-cap, and resume many LLM calls from a single script — with a durable SQLite journal that survives crashes.

## Headline result

```
$ bash run.sh

--- Executing workflow ---

  Run ID : a3f1c8e20b91
  Steps  : 4
  Budget : $0.50

  [run]  fan-out:AI safety
  [run]  fan-out:agent architectures
  [run]  fan-out:tool use in LLMs
  [run]  pipeline:aggregator
  [pass] validation (len=218 >= 50)

  Total cost: $0.0080
```

Four steps, validated output, journal on disk — zero API keys needed.

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install, configure the Claude Code skill, run in 60 seconds.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, data flow, limitations, and why this matters.
