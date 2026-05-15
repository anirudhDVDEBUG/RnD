# Codebase Language Migration

**AI agents have made programming languages fungible.** This Claude Code skill + demo tool migrates codebases between languages using a structured 5-phase workflow: audit the dependency graph, plan module-by-module migration order, translate with idiomatic target-language code, validate against the original test suite, and document everything.

**Headline result:** A 150-line Python task-queue library is analyzed, dependency-sorted, and translated to TypeScript in under 2 seconds — with interfaces, enums, classes, and a test scaffold — all offline, no API keys.

| | |
|---|---|
| **How to install & use** | [HOW_TO_USE.md](HOW_TO_USE.md) |
| **Architecture & limitations** | [TECH_DETAILS.md](TECH_DETAILS.md) |
| **Run the demo** | `bash run.sh` |

## Quick start

```bash
bash run.sh
```

This runs the Python test suite (the behavioral contract), then performs a full Python-to-TypeScript migration producing `migration_output/` with `.ts` files and a `migration_plan.json`.

## Context

Inspired by Mitchell Hashimoto's observation (via [Simon Willison](https://simonwillison.net/2026/May/14/mitchell-hashimoto/#atom-everything)) that Bun's Zig-to-Rust rewrite demonstrates how AI agents make language lock-in obsolete. The same agent-driven approach that migrates forward can migrate back — reversibility is built in.
