# How to Use

## This is a Claude Code Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/codebase_language_migration
cp SKILL.md ~/.claude/skills/codebase_language_migration/SKILL.md
```

### Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "Migrate this Python project to TypeScript"
- "Port our iOS and Android apps to React Native"
- "Rewrite this legacy Java service in Go"
- "Convert this Zig codebase to Rust"
- "Evaluate whether we should switch from Django to FastAPI"

It will NOT activate for new code, single-snippet translations, or same-language refactors.

### What Claude does when the skill triggers

1. **Audits** your source codebase — maps directory structure, dependency graph, external integrations
2. **Builds a migration plan** — module-by-module order starting from leaf dependencies
3. **Migrates module by module** — writes target-language code preserving the public API contract
4. **Translates tests** — converts your test suite to the target framework
5. **Documents the migration** — records module mappings, library swaps, and deviations

---

## Run the standalone demo

No API keys or external services needed. Requires Python 3.10+.

```bash
git clone <this-repo>
cd codebase_language_migration
bash run.sh
```

### First 60 seconds

**Input:** A sample Python task-queue library (`sample_project/`) with 3 modules and a test suite.

**What happens:**
```
$ bash run.sh

[pre] Running source Python tests (the behavioral contract)...
test_default_status ... ok
test_is_terminal ... ok
test_priority_ordering ... ok
test_process_one ... ok
...
Ran 10 tests in 0.001s — OK

[1/5] Auditing source codebase...
       Found 3 modules
[2/5] Building migration plan...
       Migration order: models → queue → worker
[3/5] Generating TypeScript code...
       ✓ models.ts
       ✓ queue.ts
       ✓ worker.ts
       ✓ tests/taskflow.test.ts
[4/5] Validating migration...
[5/5] Generating report...

======================================================================
  CODEBASE MIGRATION REPORT: Python → TypeScript
======================================================================
  ...full dependency graph, type mappings, generated code...
```

**Output:** `migration_output/` directory containing:
- `models.ts` — TypeScript enums + class with interfaces
- `queue.ts` — generic task queue
- `worker.ts` — task processor with handler registry
- `tests/taskflow.test.ts` — Vitest test scaffold
- `migration_plan.json` — machine-readable plan

### Using the skill on your own codebase

Point Claude Code at your project and use a trigger phrase:

```
> Migrate this Flask API to FastAPI

Claude will:
1. Scan your project structure
2. Present the migration plan for your approval
3. Migrate module by module, running tests after each
4. Show you a diff of behavioral changes
```

The skill follows a strict "preserve behavior, not syntax" principle — it uses target-language idioms rather than line-by-line translation.
