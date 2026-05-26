# Technical Details

## What It Does

This prototype implements a framework for defining agent slash commands as structured markdown files, pairing each command with a YAML evaluation rubric, and running automated quality checks against agent outputs. The eval runner scores outputs on weighted criteria (format compliance, actionability, correctness) and a gate checker enforces minimum thresholds before code can ship. The pattern is adapted from [emaraschio/cursor-commands](https://github.com/emaraschio/cursor-commands), which targets Cursor IDE, recast here for Claude Code's skill system.

In production, the heuristic scorers would be replaced by LLM-as-judge calls (Claude evaluating Claude's outputs), but the demo uses deterministic regex/pattern checks so it runs instantly with no API keys.

## Architecture

```
commands/
  review.md             # Slash command definition (markdown)
  test-plan.md
  refactor.md
eval/
  rubrics/
    review.yaml         # Weighted criteria + thresholds (YAML)
    test-plan.yaml
    refactor.yaml
  mock_outputs/
    review.md           # Sample agent output to evaluate
    test-plan.md
    refactor.md
  run_evals.py          # Loads rubrics, scores outputs, writes JSON
  check_gate.py         # Reads JSON, prints report, exits non-zero on fail
.github/workflows/
  skill-eval.yml        # GitHub Actions CI pipeline
run.sh                  # One-command demo
```

### Data Flow

1. `run_evals.py` scans `eval/rubrics/*.yaml` to discover commands.
2. For each rubric, it loads the matching mock output from `eval/mock_outputs/`.
3. Each criterion in the rubric is scored by a heuristic function (regex checks for section headings, tables, code blocks, severity keywords).
4. Per-criterion scores are weighted and aggregated into an overall score.
5. Results are written to `eval-results.json`.
6. `check_gate.py` reads the JSON, renders a coloured terminal report, and exits 0 (pass) or 1 (fail).

### Dependencies

- **Python 3.9+**
- **PyYAML** — rubric parsing. No other runtime dependency.

### Key Design Decisions

- **Markdown for commands:** Human-readable, version-controllable, diffable. No custom DSL.
- **YAML for rubrics:** Supports weights, thresholds, and descriptions without code changes.
- **Heuristic scorers as stand-ins:** Each criterion maps to a Python function. Swapping in an LLM judge requires changing only the `HEURISTIC_MAP` dictionary.
- **JSON results file:** Machine-readable output for CI tooling, dashboards, or aggregation.

## Limitations

- **Heuristic scoring is shallow.** Pattern-matching for section headings can't assess semantic correctness. Production use needs LLM-as-judge (e.g., Claude grading Claude).
- **No actual agent invocation.** The demo evaluates pre-written mock outputs, not live agent responses. Integrating real agent calls requires an API key and prompt orchestration.
- **Single-output evaluation.** The framework evaluates one output per command. It does not yet support multi-turn conversations or stateful command sequences.
- **No automatic rubric generation.** Rubrics are hand-authored. An extension could generate rubrics from command definitions.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | Standardised command + rubric pattern makes agent skills composable and testable across a fleet of agents. |
| **Lead-gen / marketing** | Quality gates on agent-generated copy (e.g., `/write-ad`, `/seo-audit`) prevent low-quality outputs from reaching production. |
| **CI for AI-assisted dev** | Ship-gate checks catch regressions when prompt templates or model versions change — the same way unit tests catch code regressions. |
| **Prompt engineering** | Rubrics formalise what "good output" means, turning subjective prompt tuning into measurable optimisation. |
| **Ad creatives** | Eval rubrics can enforce brand guidelines, tone, and compliance criteria on generated creative copy before it ships. |
