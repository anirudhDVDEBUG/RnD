# AI-Native Development Workflow (4-Phase Framework)

**Run multiple AI agents in parallel on one project without them stepping on each other.** The 4-Phase framework (Align > Design > Build > Integrate) generates shared contracts, scoped task boards, and per-agent CLAUDE.md files so each agent knows exactly what it owns, what interfaces to code against, and what not to touch.

## Headline Result

```
$ bash run.sh

[Phase 1: ALIGN]     4 modules defined, conventions established
[Phase 2: DESIGN]    4 contracts, 8 tasks created
[Phase 3: BUILD]     3 execution rounds — up to 4 agents in parallel
[Phase 4: INTEGRATE] 4 branches merged, ALL contract checks PASS
```

One command generates a complete artifact set: `ARCHITECTURE.md`, `CONVENTIONS.md`, `CLAUDE.md`, `TASK_BOARD.md`, `contracts.json`, and `INTEGRATION_REPORT.md`.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install as a Claude Skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, why this matters
