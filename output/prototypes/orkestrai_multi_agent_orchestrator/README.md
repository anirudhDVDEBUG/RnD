# Orkestrai Multi-Agent Orchestrator

**Autonomous multi-agent orchestration platform** that decomposes complex tasks into subtasks and delegates them to specialized LLM-powered agents (Planner, Researcher, Coder, Reviewer) — coordinated by a central Orchestrator via FastAPI.

**Headline result:** Submit a single prompt like "Build a landing page for a SaaS product" and watch 4 agents collaborate in sequence — planning, researching, coding, and reviewing — returning a structured, reviewed output in under 10 seconds (mock mode).

```
bash run.sh
```

---

- [HOW_TO_USE.md](./HOW_TO_USE.md) — Installation, skill setup, trigger phrases
- [TECH_DETAILS.md](./TECH_DETAILS.md) — Architecture, data flow, limitations
