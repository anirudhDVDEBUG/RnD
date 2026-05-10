# Technical Details: OpenWally Full-Stack Scaffold

## What It Does

OpenWally is a Python-based multi-agent pipeline built on CrewAI that decomposes full-stack code generation into five specialized roles. Given a plain-text project idea, it runs a sequential crew of AI agents — each backed by Anthropic Claude — where each agent's output feeds the next. The Architect designs the structure; Backend and Frontend agents generate code; Testing produces test suites; Integration wires it all into a deployable repo. The result is a complete, opinionated project scaffold (FastAPI + React + SQLAlchemy) generated in one pass.

The pipeline also integrates Inspect AI for evaluation: after generation, Inspect can score the output against quality rubrics (code correctness, completeness, adherence to the spec), giving a quantitative measure of how well the agents performed.

## Architecture

### Key Files (in the real repo)

| File | Purpose |
|---|---|
| `main.py` | CLI entry point — parses `--idea` arg, kicks off crew |
| `crew.py` | CrewAI crew definition — agent roles, task chaining |
| `agents/architect.py` | Architect agent — prompt for structure/endpoints/models |
| `agents/backend.py` | Backend agent — FastAPI code generation |
| `agents/frontend.py` | Frontend agent — React component generation |
| `agents/testing.py` | Testing agent — pytest + vitest generation |
| `agents/integration.py` | Integration agent — docker-compose, Makefile, git init |
| `evaluation/` | Inspect AI evals for output quality scoring |

### Data Flow

```
User idea (string)
  |
  v
Architect Agent --> project spec (JSON: endpoints, models, stack)
  |
  v
Backend Agent --> backend/ files (FastAPI routes, models, auth)
  |
  v
Frontend Agent --> frontend/ files (React components, hooks, pages)
  |
  v
Testing Agent --> test files (pytest for backend, vitest for frontend)
  |
  v
Integration Agent --> config files (docker-compose, Makefile, .gitignore, README)
  |
  v
Output directory (git-ready scaffold)
```

### Dependencies

- **CrewAI** — Agent orchestration framework; manages role assignment, task sequencing, and inter-agent communication
- **Anthropic Claude** — LLM backend for all agents (also supports Ollama for local models)
- **Inspect AI** — Evaluation framework for scoring generated code quality
- **FastAPI** — The generated backend framework (not a runtime dep of OpenWally itself)

### Model Calls

Each agent makes 1-3 Claude API calls (depending on complexity). A typical run for a mid-complexity idea uses ~5-15 API calls total, consuming roughly 50-100K tokens. Cost per scaffold: approximately $0.50-$2.00 with Claude Sonnet.

## Limitations

- **Opinionated stack only:** Always generates FastAPI + React + SQLAlchemy. No Django, Next.js, or other framework options.
- **Scaffold, not production code:** Generated code is structurally correct but needs review, error handling, and security hardening before deployment.
- **No incremental updates:** Each run generates from scratch. There's no "add a feature to existing project" mode.
- **Sequential pipeline:** Agents run one after another; no parallelism. A full run takes 30-60 seconds.
- **Limited customization:** You can't easily swap agent prompts or add new agents without modifying source.
- **No database migrations:** Generates models but not Alembic migrations.
- **Test stubs only:** Test files contain structure and assertions but may need manual completion for edge cases.

## Why It Matters

For teams building Claude-driven products:

- **Agent factory pattern:** OpenWally is a concrete example of multi-agent orchestration via CrewAI. The crew → agent → task decomposition pattern is directly reusable for building agent factories that generate marketing copy, ad creatives, or lead-gen funnels.
- **Code generation as a service:** The pipeline can be wrapped as an API endpoint — accept an idea, return a repo. This is the backbone of "vibe coding" platforms and internal tooling scaffolders.
- **Eval integration:** The Inspect AI integration shows how to add quality gates to agentic pipelines — critical for any production agent system where output must meet a bar before shipping.
- **Prompt engineering reference:** Each agent's system prompt is a well-structured example of role-specialized prompting for code generation, useful as a template for other domains (voice AI scripts, marketing email generators, etc.).
