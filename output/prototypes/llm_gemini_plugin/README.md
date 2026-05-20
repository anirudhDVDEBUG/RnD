# llm-gemini 0.32a0 — Streaming Reasoning Tokens from Gemini

The new alpha of Simon Willison's `llm-gemini` plugin adds **real-time reasoning-token streaming**: you can watch Gemini's chain-of-thought appear token-by-token in your terminal before the final answer lands. Pair it with `llm>=0.32a0` and any thinking-capable Gemini model.

**Headline result:** `llm -m gemini-2.0-flash-thinking "Prove there are infinitely many primes"` streams 8 visible reasoning steps, then delivers a polished proof — all from the CLI, no SDK boilerplate.

---

- **HOW_TO_USE.md** — Install steps, API key setup, Claude Skill config, first 60-second walkthrough.
- **TECH_DETAILS.md** — Architecture, data flow, limitations, and relevance to Claude-driven workflows.
- **run.sh** — `bash run.sh` for an end-to-end mock demo (no API key needed).
