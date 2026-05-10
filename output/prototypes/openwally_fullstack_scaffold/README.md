# OpenWally Full-Stack Scaffold

**TL;DR:** OpenWally is a multi-agent AI pipeline (CrewAI + Claude) that takes a plain-text app idea and produces a complete full-stack project — FastAPI backend, React frontend, tests, and git-ready repo — in a single command. Five specialized agents (Architect, Backend, Frontend, Testing, Integration) collaborate to generate 25+ files from one sentence.

## Headline Result

```
$ python main.py --idea "A task management app with user auth and project boards"

[1/5] Architect Agent → 8 endpoints, 4 models, monorepo layout
[2/5] Backend Agent   → 7 FastAPI files (routes, models, auth)
[3/5] Frontend Agent  → 12 React components + hooks
[4/5] Testing Agent   → 6 test files (pytest + vitest)
[5/5] Integration Agent → docker-compose, Makefile, .gitignore, README

Scaffold Complete — 29 files generated in ./generated_project/
```

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, and run (real or mock demo)
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, agent flow, limitations, and why it matters
- **Run the demo:** `bash run.sh` (no API key needed)
