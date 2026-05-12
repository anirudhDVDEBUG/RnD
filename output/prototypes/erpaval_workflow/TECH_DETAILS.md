# Technical Details

## What it does

ERPAVal is a structured workflow that wraps Claude Code's autonomous development in a six-phase loop: **Explore, Research, Plan, Act, Validate, Compound**. Instead of letting the agent jump straight to writing code, it forces a disciplined sequence — understand first, research second, plan third, then act, validate, and capture lessons. A keyword-based classifier inspects each incoming task to determine the task type (bug fix, feature, refactor, simple change, or unknown) and adjusts which phases get extra emphasis.

The compounding lessons store is the key differentiator: every completed cycle writes a structured lesson (category, insight, tags) to a persistent file. On future tasks, the Research phase queries this store, so the agent gets smarter over time without retraining.

## Architecture

```
User prompt
    |
    v
[Classifier]  -- keyword scoring -> TaskType + entry_phase + emphasized_phases
    |
    v
[ERPAValWorkflow.run()]
    |
    +---> Explore   (scan codebase, map dependencies)
    +---> Research  (query lessons store, find patterns)
    +---> Plan      (define steps, validation criteria, rollback)
    +---> Act       (execute plan, minimal changes)
    +---> Validate  (run tests, review diff, check regressions)
    +---> Compound  (write lesson to store)
    |
    v
WorkflowRun (results + lessons added)
```

### Key files

| File | Purpose |
|---|---|
| `SKILL.md` | The Claude Code skill definition — drop into `~/.claude/skills/erpaval_workflow/` |
| `erpaval.py` | Workflow engine: phase orchestration, pluggable handlers, display |
| `classifier.py` | Task classifier: keyword scoring, routing rules, Classification dataclass |
| `lessons_store.py` | Lessons CRUD: load/save/add/search over a JSON file |
| `demo.py` | Runs three demo tasks through the engine with mock data |
| `run.sh` | One-command demo entry point |

### Data flow

1. Task string enters the classifier, which scores it against keyword lists for each TaskType.
2. The classifier returns a `Classification` with the best-match type, confidence, entry phase, and which phases to emphasize.
3. `ERPAValWorkflow.run()` iterates through all six phases in order, calling the handler for each.
4. Handlers are pluggable — the demo uses built-in mock handlers; in production use, the SKILL.md instructs Claude Code to perform each phase using its native capabilities (file reading, search, editing, test running).
5. The Compound phase writes a `Lesson` to the JSON store. Future Research phases query it.

### Dependencies

- **Python 3.8+** (stdlib only — no external packages)
- No API keys, no network calls, no database

## Limitations

- **The skill is prompt-driven, not enforced.** Claude Code follows the SKILL.md instructions by convention. There is no runtime that blocks Claude from skipping phases — it relies on the model's instruction-following.
- **Classifier is keyword-based.** The demo classifier uses simple keyword scoring. In production, Claude's own judgment replaces this; the SKILL.md routing instructions serve as the real classifier.
- **Lessons store is local.** Lessons are stored per-project in a single JSON/Markdown file. There is no cross-project sharing, deduplication, or relevance ranking beyond substring match.
- **No real code execution in demo.** The mock handlers simulate file reads, test runs, and code changes. The actual value comes from the SKILL.md guiding Claude Code's real tool calls.
- **No multi-agent orchestration.** This is a single-agent workflow. It does not spawn sub-agents or parallelize phases.

## Why it matters

For teams building Claude-driven products (lead-gen pipelines, marketing automation, agent factories, voice AI systems):

- **Reliability over speed.** Autonomous agents that skip planning produce fragile code. ERPAVal forces the agent to understand before it acts, reducing rework cycles.
- **Institutional memory.** The compounding lessons store means the agent learns project-specific patterns — API quirks, testing conventions, architecture constraints — without retraining the model.
- **Auditability.** Each phase produces a structured result. You can inspect what the agent explored, what it planned, and what it validated — critical for production systems where you need to trust the output.
- **Transferable pattern.** The six-phase loop is not specific to any domain. It works for ad-creative generators, CRM integrations, voice-AI pipelines, or any codebase where you want disciplined autonomous development.

## Source

[theagenticguy/erpaval](https://github.com/theagenticguy/erpaval) — ERPAVal autonomous software development workflow with classifier-driven routing and compounding lessons store.
