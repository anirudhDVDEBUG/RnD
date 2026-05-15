# Technical Details

## What it does

This skill provides a structured methodology for AI-agent-driven codebase migrations between programming languages or frameworks. The standalone demo implements the full 5-step workflow (audit → plan → migrate → validate → report) using Python's AST module for analysis and rule-based code generation for the TypeScript output.

In production use as a Claude Code skill, the AST analysis is replaced by Claude's own code understanding — it reads source modules, reasons about behavioral contracts, and writes idiomatic target-language code directly. The skill's SKILL.md file encodes the migration methodology so Claude follows a disciplined, module-by-module approach rather than attempting an error-prone big-bang rewrite.

## Architecture

```
migrate.py              — Single-file orchestrator (all 5 steps)
sample_project/         — Source Python codebase (the migration input)
  models.py             — Data models: Task, Priority, Status (dataclass + enum)
  queue.py              — TaskQueue with priority sorting
  worker.py             — Worker with handler registry and error handling
  tests/test_taskflow.py — 10 unit tests (the behavioral contract)
migration_output/       — Generated after run (TypeScript + plan JSON)
SKILL.md                — Claude Code skill definition (drop into ~/.claude/skills/)
```

### Data flow

```
Source .py files
    ↓ ast.parse()
ModuleInfo (classes, functions, imports, LOC)
    ↓ build_dependency_graph() + topological_sort()
MigrationPlan (ordered modules, type/lib mappings)
    ↓ generate_ts_for_module()
Target .ts files + test scaffold
    ↓ print_report()
Structured migration report (stdout + JSON)
```

### Key implementation details

- **Dependency ordering** uses Kahn's algorithm (topological sort) — leaf modules with no internal imports are migrated first, ensuring each module's dependencies are already ported when it's translated.
- **Type mapping** converts Python types to TypeScript equivalents (`str→string`, `dict→Record`, `Optional→| null`, etc.).
- **Library mapping** identifies stdlib replacements (`dataclasses→plain TS class`, `enum→native TS enum`, `uuid→crypto.randomUUID()`, `unittest→Vitest`).
- **AST-based generation** walks the Python AST to produce TypeScript interfaces, classes, enums, and method stubs — not string substitution.

### Dependencies

None beyond Python 3.10+ stdlib. The demo uses: `ast`, `dataclasses`, `enum`, `json`, `pathlib`, `typing`, `uuid`, `time`, `unittest`.

## Limitations

- **The demo uses rule-based generation, not LLM.** Complex logic inside function bodies gets placeholder stubs. Real migrations use Claude to translate method bodies with full semantic understanding.
- **No incremental/mixed-language execution.** The demo generates all TypeScript at once. A real migration might use FFI shims or a dual-runtime strategy to migrate incrementally.
- **No runtime validation of generated TypeScript.** The demo produces `.ts` files but doesn't compile or run them (would require Node.js + TypeScript toolchain). The test scaffold needs manual completion.
- **Single source language.** The analyzer only handles Python source. The skill methodology itself is language-agnostic, but the demo's AST parser is Python-specific.
- **No handling of framework-specific patterns** (Django ORM, Flask routes, async/await concurrency models). These require the LLM's reasoning, not rule-based translation.

## Why this matters for Claude-driven products

**Agent factories / automation platforms:** Migration skills let you offer "modernize your stack" as a productized service — scan a client's legacy codebase, generate a migration plan, and execute it with Claude agents. The reversibility angle ("we can always port back") is a strong sales argument.

**Lead generation / consulting:** The audit step alone (dependency graph, LOC analysis, library mapping) produces a valuable deliverable — a migration feasibility report — that can serve as a lead magnet or paid assessment.

**Marketing / content:** "We migrated 50k lines of Python to TypeScript in a weekend" is a compelling case study. The structured methodology makes these stories reproducible and credible.

**Reducing platform risk:** If you're building on a framework that might lose support, the confidence that you can migrate away in days rather than months changes your risk calculus entirely. As Simon Willison noted, "Programming languages used to be LOCK IN, and they're increasingly not so."

## References

- [Quoting Mitchell Hashimoto — Simon Willison](https://simonwillison.net/2026/May/14/mitchell-hashimoto/#atom-everything)
- Mitchell Hashimoto on Bun's Zig→Rust migration
- Native iOS/Android → React Native agent-driven rewrite (cited in source article)
