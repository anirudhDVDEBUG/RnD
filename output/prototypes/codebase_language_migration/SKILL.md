---
name: codebase_language_migration
description: |
  Plan and execute large-scale codebase migrations between programming languages or frameworks using AI coding agents.
  TRIGGER when: user wants to port/migrate/rewrite code from one language or framework to another, convert a codebase, or evaluate feasibility of a language/platform switch.
  DO NOT TRIGGER when: user is writing new code from scratch, doing minor refactors within the same language, or translating a single small snippet.
---

# Codebase Language / Framework Migration

AI coding agents have made programming language and framework migrations dramatically more feasible. As Simon Willison noted (citing Mitchell Hashimoto on Bun's Zig-to-Rust migration): "Programming languages used to be LOCK IN, and they're increasingly not so." Companies are now completing full rewrites—such as native iOS/Android apps to React Native—using agent-driven workflows, with confidence they can port back if needed.

## When to use

- "Migrate this Python project to TypeScript"
- "Port our iOS and Android apps to React Native"
- "Rewrite this legacy Java service in Go"
- "Convert this Zig codebase to Rust"
- "Evaluate whether we should switch from X framework to Y"

## How to use

### Step 1: Audit the source codebase

- Map out the full directory structure, entry points, and dependency graph.
- Identify language-specific idioms, platform APIs, and third-party libraries that need target-language equivalents.
- List external integrations (databases, APIs, file formats) that must be preserved.
- Note test coverage—existing tests become the migration's acceptance criteria.

### Step 2: Build a migration plan

- Create a module-by-module migration order, starting with leaf dependencies (no internal imports) and working inward.
- For each module, identify:
  - The target-language equivalent of every dependency and API call.
  - Behavioral contracts (inputs, outputs, side effects) that must be preserved.
  - Any idiom translations (e.g., error handling patterns, concurrency models).
- Define a "shim" strategy for incremental migration if the project can run mixed-language during transition.

### Step 3: Migrate module by module

For each module in dependency order:

1. **Read** the source module thoroughly.
2. **Write** the target-language equivalent, preserving the public API contract.
3. **Translate tests** to the target language's test framework.
4. **Run tests** to verify behavioral equivalence.
5. **Document** any intentional deviations or improvements made during translation.

### Step 4: Integration and validation

- Wire all migrated modules together and run the full test suite.
- Perform integration testing against real external services where possible.
- Compare build artifacts, binary sizes, startup times, and performance benchmarks against the original.
- If the project has UI, do a side-by-side visual/functional comparison.

### Step 5: Document the migration

- Record the mapping of old modules → new modules for future reference.
- Note any libraries that were swapped and why.
- Keep the original codebase archived—if the migration turns out wrong, you can port back.

## Key principles

- **Preserve behavior, not syntax.** The goal is functional equivalence, not line-by-line translation. Use target-language idioms.
- **Tests are the contract.** If the original has tests, they define correctness. If it doesn't, write characterization tests before migrating.
- **Migrate incrementally.** Don't attempt a big-bang rewrite. Module-by-module migration lets you validate continuously.
- **Reversibility is a feature.** The same agent-driven approach that makes migration feasible also makes reverting feasible. This lowers the stakes of the decision.

## References

- [Quoting Mitchell Hashimoto – Simon Willison](https://simonwillison.net/2026/May/14/mitchell-hashimoto/#atom-everything)
