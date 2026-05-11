# Technical Details — CCGX Multi-Model Workflow

## What it does

CCGX (Claude Code Gemini/codeX) is a task-routing orchestrator for AI-assisted development. It takes natural-language task descriptions, classifies them as frontend or backend work using regex-based signal detection, and dispatches each task to the model best suited for it: Gemini for frontend/UI work, Codex for backend/infrastructure, and Claude as the general orchestrator and fallback. Quality tiers (draft, standard, production) control how many iterations, tests, and review passes each task receives.

The upstream TypeScript repo provides a CLI and programmatic API. This demo reimplements the core routing and orchestration logic in Python with mock model backends, so you can evaluate the concept without API keys.

## Architecture

```
demo.py                    Entry point — runs all demo steps
ccgx/
  router.py                Task classifier (regex signal matching)
  models.py                Mock model backends (simulated responses)
  orchestrator.py          Workflow engine (route → call → collect)
```

### Data flow

```
Task string
  → router.route_task()
      - count frontend signal matches (React, CSS, component, etc.)
      - count backend signal matches (API, database, Docker, etc.)
      - pick model with higher score; tie → Claude
      - compute confidence from score differential
  → models.call_model(model, task, tier)
      - simulate latency and token usage
      - return mock response text
  → orchestrator collects TaskResult[]
      - if production tier: extra Claude review pass
      - aggregate tokens, latency, model breakdown
```

### Key design choices

- **Regex signal detection** over LLM-based classification: zero latency, no API cost, deterministic. The upstream repo likely uses a similar heuristic with optional LLM refinement.
- **Quality tiers** map to concrete config: `max_iterations`, `run_tests`, `review`. Production tier adds a Claude review pass after each model response.
- **Autonomous mode**: when `autonomous=True`, the orchestrator runs all tasks without pausing for user confirmation — designed for overnight or CI-triggered runs.

### Dependencies

- **This demo**: Python 3.10+ standard library only (re, time, random, json, dataclasses).
- **Full repo**: Node.js 18+, TypeScript. Depends on model provider SDKs (Gemini API, OpenAI/Codex API, Anthropic API).

## Limitations

- **Regex routing is shallow.** "Fix the CSS bug in the payment API controller" has both frontend (CSS) and backend (API, controller) signals. The router picks whichever scores higher, but doesn't understand context or intent.
- **No actual model calls.** This demo uses mock responses. The upstream repo requires valid API keys for Gemini, Codex, and Claude.
- **No codebase awareness.** The router classifies task text only — it doesn't inspect your file tree, git history, or language breakdown to inform routing.
- **Single-pass classification.** Tasks aren't decomposed. A full-stack task like "Add user profiles end-to-end" gets routed to one model rather than split into frontend + backend subtasks.
- **No cost optimization.** No token budgets, rate limiting, or model-cost-aware routing.

## Why it matters

For teams building Claude-driven products:

- **Agent factories**: Multi-model routing is a core pattern. Rather than one model doing everything, you dispatch specialized work to specialized models — the same pattern behind agent swarms and tool-use orchestration.
- **Lead-gen / marketing**: Content generation pipelines can route copy-heavy tasks to one model and data/analytics tasks to another, improving both quality and cost.
- **Ad creatives**: Visual/layout tasks (Gemini) vs. copy/targeting logic (Claude) — same routing concept applied to creative production.
- **Voice AI**: Transcription → understanding → response generation can each target different models optimized for that stage.

The core insight: **model routing is becoming table stakes for production AI systems**, and CCGX provides a clean, configurable pattern for it within the Claude Code workflow.
