# Technical Details: Gemini 3.5 Flash Guide

## What this does

This is a Claude Code **skill** — a structured markdown file (`SKILL.md`) that Claude Code loads into its context when the user's message matches predefined trigger phrases about Google's Gemini 3.5 Flash model. It gives Claude instant, accurate reference data (model ID, token limits, pricing, API examples, migration steps) so it can answer Gemini 3.5 Flash questions without hallucinating or requiring the user to paste documentation.

The companion `demo.py` script validates the skill's content by simulating four real-world query scenarios and printing formatted responses built from the same data the skill contains.

## Architecture

```
User message
    │
    ▼
Claude Code trigger matcher
    │  matches: "gemini 3.5 flash", "gemini-3.5-flash",
    │           "google i/o 2026", "gemini flash pricing",
    │           "migrating from gemini 3 flash preview"
    ▼
SKILL.md loaded into context
    │
    ▼
Claude answers using skill data
    (model specs, pricing table, code snippets, migration checklist)
```

**Key files:**

| File | Role |
|---|---|
| `SKILL.md` | The skill itself — YAML frontmatter (name + trigger description) followed by markdown sections. Claude Code parses the frontmatter to decide when to inject this into context. |
| `demo.py` | Standalone Python script (stdlib only). Loads `SKILL.md`, defines mock pricing data, implements trigger regex matching, and runs four demo scenarios. |
| `run.sh` | Shell wrapper — runs `demo.py` with Python 3. |

**Dependencies:** None at runtime. The demo uses only Python standard library (`re`, `json`, `textwrap`, `pathlib`). To actually call the Gemini API you would install `google-generativeai>=0.8.0`.

## Data sources

- Model specs and pricing: sourced from Simon Willison's analysis and Google's official announcements at Google I/O 2026.
- Pricing figures in `demo.py` are illustrative mock data based on publicly discussed ranges — verify against the live Google AI pricing page before production use.

## Limitations

- **No live API calls.** The skill is reference documentation, not an API wrapper. It tells Claude *how* to call Gemini 3.5 Flash but does not call it.
- **Pricing may drift.** The mock pricing data is a snapshot. Google may adjust pricing; the skill does not auto-update.
- **No computer-use coverage.** Gemini 3.5 Flash does not support computer use, so the skill explicitly excludes that topic.
- **Single-model scope.** Covers only Gemini 3.5 Flash. Other Gemini models (Pro, Ultra, Nano) are out of scope.
- **Interactions API is beta.** The skill references Google's new Interactions API, which is in beta and may change.

## Why this matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Agent factories** | If your agents route between Claude and Gemini models, this skill ensures Claude has accurate Gemini 3.5 Flash specs without an extra lookup tool. |
| **Lead-gen / marketing** | Cost comparisons between model families help agents recommend the right model for budget-sensitive batch workloads. |
| **Ad creatives** | Flash models are often used for high-volume, low-latency creative generation — knowing the pricing delta matters for ROI calculations. |
| **Multi-model orchestration** | Migration checklist and API snippets reduce friction when adding Gemini 3.5 Flash as a new backend in a multi-provider pipeline. |
