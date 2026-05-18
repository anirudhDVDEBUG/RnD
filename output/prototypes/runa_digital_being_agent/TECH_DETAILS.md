# Technical Details — Runa Digital Being Agent

## What It Does

Runa is a Python framework for building autonomous "digital being" agents that operate on a continuous loop rather than a request-response pattern. Each cycle the agent perceives its environment, reasons via an LLM call (or mock), selects and executes an action from a plugin registry, then reflects and updates persistent memory and goals. The architecture is inspired by [hrabanazviking/Runa-Agent-Digital-Being](https://github.com/hrabanazviking/Runa-Agent-Digital-Being), which was built as an alternative to Hermes/OpenClaw frameworks with emphasis on agent sovereignty and self-direction.

## Architecture

```
main.py                 Entry point — wires subsystems together, runs cycles
agent/
  core.py               RunaAgent class — the orchestrator loop
  identity.py           AgentIdentity — persona, values, boundaries → system prompt
  memory.py             PersistentMemory — JSON-file-backed recall + context window
  goals.py              GoalManager — hierarchical goal tree (aspiration/objective/task)
  actions.py            ActionRegistry — plugin system for executable capabilities
config/
  identity.yaml         Declarative agent persona config
  settings.yaml         Runtime settings (LLM provider, paths, log level)
logs/
  memory.json           Persisted memory entries (created at runtime)
  goals.json            Goal state (created at runtime)
  agent.log             Full decision audit log
```

### Data Flow (one cycle)

1. **Perceive** — gather timestamp, active goals summary, memory summary, optional external input
2. **Reason** — build messages array (system prompt from identity + context + perception), call LLM, parse JSON response with `{reasoning, action, action_args, reflection}`
3. **Act** — look up action in registry, inject dependencies (memory/goals), execute
4. **Reflect** — store outcome + reflection in memory, append to context window

### Dependencies

- Python 3.8+
- `pyyaml` (config parsing)
- No external API keys for demo (mock LLM included)

### Model Calls

The `llm_fn` callable is injected into `RunaAgent`. In demo mode it's a deterministic mock that returns structured JSON. In production you'd wire it to `anthropic.Anthropic().messages.create()` or any OpenAI-compatible endpoint.

## Limitations

- **No real LLM reasoning in demo** — the mock is deterministic and won't exhibit emergent behavior. Wire a real model for actual autonomy.
- **Keyword-only memory retrieval** — no embeddings or vector search; recall is naive substring matching.
- **No concurrency** — runs a single-threaded loop. Not designed for real-time multi-user scenarios.
- **No built-in tool use** — actions are Python callables you register. There's no MCP/function-calling integration out of the box.
- **No safety guardrails beyond boundaries** — the boundary system is prompt-based only; no runtime enforcement.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent Factories** | This is a scaffold for spinning up autonomous agents with distinct identities. Wrap it in a factory that generates identity configs per customer. |
| **Lead-Gen / Marketing** | An agent with persistent goals can autonomously run multi-step outreach campaigns (research → draft → follow-up) without babysitting. |
| **Voice AI** | The identity + memory system maps well to voice assistants that need continuity across calls. Plug the loop into a voice pipeline. |
| **Ad Creatives** | A goal-directed agent can iterate on creative variations, reflect on performance data, and self-improve copy. |

The key insight: traditional assistants are stateless and reactive. This pattern gives you a **stateful, proactive** agent that works toward goals between interactions — useful any time you need "agent that keeps working even when I'm not prompting it."
