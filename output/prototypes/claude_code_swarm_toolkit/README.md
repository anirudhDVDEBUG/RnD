# Claude Code Swarm Toolkit

**TL;DR:** Orchestrate multiple Claude Code subagents in parallel swarm patterns (fan-out/fan-in, map-reduce, pipeline) to divide and conquer complex tasks 3-5x faster than sequential execution.

**Headline result:** A single prompt like "refactor auth, payments, and notifications" spawns 3 parallel agents that each handle one module independently, then merges results — turning a 15-minute sequential task into a 5-minute parallel one.

---

- [HOW_TO_USE.md](./HOW_TO_USE.md) — Installation, setup, trigger phrases
- [TECH_DETAILS.md](./TECH_DETAILS.md) — Architecture, patterns, limitations
- [run.sh](./run.sh) — Live demo (no API keys needed)
