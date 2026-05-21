# Zephyr Local AI Sidekick

**A local-first AI agent with a React control room, FastAPI bridge, RAG pipeline, MCP client, and self-healing workflows — running entirely on your machine with zero cloud dependencies.**

Zephyr demonstrates how to wire together a browser-based agent UI, a Python runtime with retrieval-augmented generation, and the Model Context Protocol for tool discovery — all locally. The self-healing engine automatically retries and patches failed workflow steps.

## Headline Result

```
$ bash run.sh
  5 subsystems exercised end-to-end:
    - Local LLM (mock-7b-q4): 3 prompts, 45 tokens
    - RAG: 4 docs indexed, top-2 retrieval, grounded answer
    - MCP: 3 servers connected, 2 tool invocations
    - Skills: 4 registered, query-matched execution
    - Self-heal: 4 steps with auto-retry on transient failures
  FastAPI bridge: /health, /chat, /skills, /mcp/tools, /self-heal/demo
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, run, integrate as a Claude skill
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, relevance

## Source

[nabcht/Zephyr](https://github.com/nabcht/Zephyr) — local-first AI sidekick with React control room + FastAPI bridge
