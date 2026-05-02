# Technical Details

## What It Does

The AI-Native 4-Phase Framework is a methodology (not a runtime) for coordinating multiple AI coding agents on the same project. The workflow engine in this repo is a concrete implementation that takes a project specification (name, modules, dependencies) and generates the full set of coordination artifacts: architecture docs, interface contracts, parallelized task boards, per-agent context files (CLAUDE.md), and integration reports.

The core insight: AI agents working in parallel need the same thing human teams need — shared contracts. The 4-Phase structure (Align > Design > Build > Integrate) enforces that contracts are defined *before* agents start coding, and frozen during the build phase so no agent's in-progress work gets invalidated.

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `workflow_engine.py` | Core engine — data models, 4-phase functions, artifact generators |
| `demo.py` | Two demo scenarios (greenfield e-commerce, existing Django monolith) |
| `run.sh` | Entry point — cleans output, runs demo |

### Data Flow

```
Project Spec (name, modules, deps, tech stack)
    |
    v
Phase 1: Align    --> Module[], Conventions{}
    |
    v
Phase 2: Design   --> Contract[], Task[]
    |
    v
Phase 3: Build    --> Task[] (with status), ExecutionRounds[]
    |
    v
Phase 4: Integrate --> IntegrationReport{}
    |
    v
Artifact Files:
  ARCHITECTURE.md, CONVENTIONS.md, CLAUDE.md,
  TASK_BOARD.md, contracts.json, INTEGRATION_REPORT.md
```

### Dependencies

**Zero external dependencies.** Uses only Python 3.10+ stdlib: `dataclasses`, `json`, `os`, `typing`.

### No Model Calls

This is a pure logic engine — it does not call any LLM API. It generates the *structure* that agents need. The actual AI agents (Claude Code instances, etc.) consume the generated artifacts as context.

## Limitations

- **Simulation only**: Phase 3 (Build) simulates parallel execution by resolving dependency graphs. It does not actually spawn agents or run code.
- **No conflict detection**: The integration phase assumes contract compliance. Real projects need actual test runners.
- **Static contracts**: The engine generates contracts from module dependency declarations. In practice, contracts need domain-specific refinement (OpenAPI schemas, protobuf definitions, etc.).
- **No dynamic re-planning**: If an agent gets stuck, the framework has no mechanism to reassign tasks. That requires an orchestrator layer on top.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|---|---|
| **Agent factories** | The contract + task-board pattern is the scaffolding for any multi-agent system. Use this to generate the coordination layer before letting agents loose. |
| **Lead-gen / marketing automation** | Complex pipelines (scrape > enrich > score > email) map naturally to 4 modules with contracts. Each step can be built and tested independently. |
| **Ad creative generation** | Separate agents for copy, image prompts, A/B variants, and compliance checks — each with clear interfaces. |
| **Voice AI / conversational agents** | Intent router, dialog manager, tool caller, response formatter — the 4-module pattern fits directly. Contracts define what each component sends/receives. |
| **Existing codebase modernization** | The "existing codebase" scenario shows how to audit an existing project, document implicit conventions, and split work across agents without breaking things. |

The framework is methodology-agnostic — it works whether your agents are Claude Code sessions, LangChain chains, or custom scripts. The value is in the contract-first coordination pattern.

## Source

- [tianji-qingtian/AI-Native](https://github.com/tianji-qingtian/AI-Native) — Original methodology docs (Chinese + English), anti-pattern catalog, scenario guides.
