# Technical Details

## What It Does

The AI Maintenance Cost Auditor performs static analysis on source files to estimate their long-term maintenance cost, then applies James Shore's inverse-rate formula: **speed_multiplier x maintenance_multiplier must be <= 1.0**. If your AI writes code 3x faster but that code costs 1.5x more to maintain, the product is 4.5x — you're losing, not winning.

The tool runs six checker passes over each file (readability, duplication, dead code, complexity, error handling, consistency), produces per-finding actionable suggestions, and rolls up a per-file and overall maintenance multiplier. No LLM calls, no API keys, no network access — it's a pure Python linter with an opinionated scoring model.

## Architecture

```
auditor.py          CLI entry point + all logic (single file, ~280 lines)
  |
  +-- audit_path()      Walks files, filters by extension
  +-- audit_file()      Reads file, runs all checkers
  |     +-- check_readability()    Line length, variable naming
  |     +-- check_duplication()    Sliding-window near-duplicate detection
  |     +-- check_dead_code()      Commented-out code, unused imports
  |     +-- check_complexity()     Nesting depth, function length
  |     +-- check_error_handling() Bare excepts, swallowed errors
  |     +-- check_consistency()    Mixed naming conventions
  +-- compute_maintenance_multiplier()   Weighted severity scoring
  +-- print_report() / print_json()      Output formatting

samples/
  good_code.py      Clean example — few/no findings
  bad_code.py       Deliberately messy — triggers most checkers

SKILL.md            Claude Code skill definition (drop into ~/.claude/skills/)
```

**Dependencies:** None. Python 3.10+ stdlib only (`pathlib`, `re`, `json`, `dataclasses`, `argparse`).

**No model calls.** The auditor is deterministic static analysis. The SKILL.md file is what gives Claude the framework to do the *qualitative* assessment (coupling, test coverage, architectural fit) that static analysis can't cover.

## Scoring Model

Each finding has a severity (low/medium/high) with weights 0.05/0.15/0.30. The weighted sum is normalized by file size (per 100 lines), then added to a baseline of 0.8x (well-structured code starts below 1.0).

```
maintenance_multiplier = 0.8 + (weighted_severity_sum / (lines / 100))
```

This means:
- A clean 100-line file with zero findings: **0.8x** (good)
- A 100-line file with 2 high-severity findings: **0.8 + 0.60 = 1.4x** (risky)
- A 100-line file with 5 high + 3 medium findings: **0.8 + 1.95 = 2.75x** (unsustainable)

The final verdict multiplies this by the assumed AI speed gain:
- **Sustainable**: product <= 1.0
- **Risky**: product 1.0-2.0
- **Unsustainable**: product > 2.0

## Limitations

- **Heuristic, not semantic.** The checkers use regex and line-counting, not ASTs. They catch common patterns but miss context (e.g., a long function might be a state machine that's genuinely complex).
- **Python-biased.** The dead-code and consistency checks assume Python conventions. JS/TS files get readability, duplication, and complexity checks but less coverage.
- **No test-coverage analysis.** The tool can't tell if tests exist for the audited code. The SKILL.md fills this gap when used with Claude.
- **Speed multiplier is self-reported.** The tool has no way to measure how fast code was actually written. It trusts the `--speed` input.
- **No diff-mode yet.** It audits whole files, not just the AI-generated delta within a file.

## Why This Matters for Claude-Driven Products

If you're building agent factories, marketing automation, or any product where Claude generates customer-facing code:

1. **Quality gates for agent output.** Run this auditor on code your agents produce before shipping it. An "UNSUSTAINABLE" verdict means your agent is creating support tickets, not solving them.
2. **Quantified tradeoffs.** Instead of vague "code quality" discussions, you get a number: "this agent output has a 2.1x maintenance multiplier at 4x speed — product is 8.4x, we're losing."
3. **Skill-augmented review.** The SKILL.md gives Claude itself the framework to audit its own output. Use it as a post-generation review step in your agent pipeline.
4. **CI integration.** The `--json` flag makes it pipeline-friendly. Fail builds when AI-generated code exceeds your maintenance budget.

Shore's insight is simple but powerful: the speed of AI code generation is irrelevant if maintenance costs eat the gains. This tool makes that tradeoff visible.
