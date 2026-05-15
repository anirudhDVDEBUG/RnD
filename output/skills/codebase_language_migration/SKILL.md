---
name: codebase_language_migration
description: |
  Migrate or port a codebase (or significant module) from one programming language to another using agentic, incremental translation strategies.
  TRIGGER when: user asks to rewrite/port/migrate code from one language to another, convert a project between languages, or evaluate feasibility of a language switch.
  DO NOT TRIGGER when: user is refactoring within the same language, or asking general questions about programming languages.
---

# Codebase Language Migration

Agentic skill for porting codebases between programming languages — inspired by the observation that AI agents have made programming languages increasingly fungible. As Mitchell Hashimoto noted regarding Bun's Zig-to-Rust rewrite: languages are no longer lock-in; a codebase can move to a new language in days rather than months.

## When to use

- "Port this Python project to Rust"
- "Rewrite this module from JavaScript to TypeScript"
- "Migrate our Go service to Zig"
- "Convert this C++ library to Rust"
- "Evaluate whether we should switch languages for this codebase"

## How to use

### Phase 1: Audit & Plan

1. **Map the source codebase** — Identify all modules, entry points, dependencies, FFI boundaries, build scripts, and tests.
2. **Catalog external dependencies** — For each dependency in the source language, find the equivalent library in the target language. Flag any with no equivalent (these need custom implementation or a thin FFI bridge).
3. **Identify translation risk zones** — Language-specific idioms that don't map cleanly (e.g., Go goroutines → Rust async, Python dynamic typing → typed language, C++ templates → Rust generics). Rank modules by migration difficulty.
4. **Define the migration order** — Start with leaf modules (no internal dependencies), move toward the core. Prefer modules with good test coverage first.
5. **Write a migration plan document** listing each module, its target-language equivalent structure, dependency mappings, and estimated complexity (low / medium / high).

### Phase 2: Incremental Translation

6. **Translate module-by-module** — For each module in the planned order:
   - Read the entire source module.
   - Write the target-language equivalent, preserving the same public API surface and semantics.
   - Translate or recreate unit tests for the module.
   - Run the tests and fix any failures.
7. **Preserve interop during migration** — If the project must remain functional during migration, use FFI bindings (e.g., `pyo3`, `napi-rs`, `cgo`) so translated modules can coexist with untranslated ones.
8. **Handle idiom translation** — Don't write "Language A code in Language B syntax." Adopt target-language idioms:
   - Error handling: exceptions → Result types, or vice versa.
   - Concurrency: map threading/async models appropriately.
   - Memory management: GC → ownership, or vice versa.
   - Type system: add/remove type annotations as the target requires.

### Phase 3: Validate & Ship

9. **Run the full test suite** in the target language. Ensure parity with the original.
10. **Benchmark critical paths** — Compare performance between source and target. Flag any regressions.
11. **Update build system & CI** — Replace build configs (Makefile, package.json, Cargo.toml, go.mod, etc.) and CI pipelines.
12. **Remove the source language code** once all modules are translated and validated. Clean up any FFI bridge code.
13. **Document the migration** — Note any behavioral differences, dependency changes, or API adjustments.

### Key principles

- **Test-driven migration**: Never translate a module without also translating (or writing) its tests. Tests are your proof of correctness.
- **Semantic fidelity over syntactic mirroring**: The goal is identical behavior, not line-for-line translation.
- **Incremental over big-bang**: A working hybrid codebase is better than a broken fully-translated one.
- **Leverage AI for bulk translation, human review for correctness**: Use agentic translation for the mechanical work, but review idiom choices and edge cases carefully.

## References

- [Quoting Mitchell Hashimoto — Simon Willison](https://simonwillison.net/2026/May/14/mitchell-hashimoto/#atom-everything) — On how AI agents make programming languages fungible, referencing Bun's Zig-to-Rust migration.
- Mitchell Hashimoto's original post on the fungibility of programming languages in the age of AI-assisted development.
