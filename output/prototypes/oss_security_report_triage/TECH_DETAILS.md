# Technical Details

## What it does

The OSS Security Report Triage engine is a rule-based pipeline that processes incoming security vulnerability reports and produces actionable triage decisions. It runs five stages per report: AI-detection scoring, CVSS severity estimation, reproducibility assessment, status determination, and response drafting. No LLM calls are needed for the core triage — it uses pattern matching and heuristics derived from real maintainer experience (particularly Daniel Stenberg's public writing about curl's security report flood).

The Claude Code skill wraps this logic into a structured prompt so Claude can apply the same methodology interactively when a maintainer pastes a report into their terminal.

## Architecture

```
mock_reports.json          Input: structured vulnerability reports
        |
        v
  triage.py                Core engine (pure Python, no deps)
  ├── detect_ai_signals()  NLP heuristics for AI-generated text
  ├── estimate_cvss()      Simplified CVSS scoring from keywords
  ├── assess_repro()       PoC quality / reproducibility check
  ├── determine_status()   Decision matrix → CONFIRMED/REJECTED/etc
  └── draft_response()     Template-based response generation
        |
        v
response_templates.json    Maintainer response templates
        |
        v
  Terminal output          Color-coded queue + detailed results
```

### Key files

| File | Purpose |
|------|---------|
| `triage.py` | Core triage engine, CLI entrypoint |
| `mock_reports.json` | 5 sample reports (2 AI-generated, 2 human, 1 borderline) |
| `response_templates.json` | Response templates for each triage outcome |
| `SKILL.md` | Claude Code skill definition |

### Data flow

1. Reports loaded from JSON (or pasted interactively via skill)
2. Each report passes through 4 scoring functions independently
3. Scores feed a decision matrix that assigns status
4. Status selects a response template, fills in specifics
5. Results rendered to terminal with severity coloring

### Dependencies

**None.** Pure Python 3.10+ standard library. No pip packages, no API keys, no network calls.

## AI-detection heuristics

The engine scores AI-generation likelihood using:

- **Phrase matching**: Checks for formulaic phrases common in LLM output ("could potentially be exploited", "classic use-after-free pattern", "remediation:")
- **Structural signals**: Report length, section count, placeholder CVE references (XXXXX)
- **Explicit indicators**: The `ai_indicators` field allows pre-labeled signals from intake
- **PoC quality**: AI reports frequently lack working PoCs or say "theoretical analysis"

Each signal adds ~12% to the AI confidence score (capped at 100%).

## Limitations

- **No actual code analysis.** The engine assesses reports textually — it does not parse C code, run static analysis, or execute PoCs. For real use, pair with a code review step.
- **CVSS is estimated, not calculated.** The scoring uses keyword matching against impact descriptions, not the full CVSS v3.1 vector string computation.
- **Heuristic AI detection.** The AI-detection is pattern-based, not ML-based. A well-written AI report could evade detection; a poorly-written human report could be mis-flagged.
- **No persistence.** Reports are processed from a JSON file per run. A production system would need a database, API intake, and notification pipeline.
- **English only.** The signal phrases and heuristics assume English-language reports.

## Why it matters

For teams building Claude-driven products:

- **Agent factories / agentic workflows**: This is a concrete example of encoding expert judgment (maintainer triage heuristics) into a reusable skill. The same pattern — intake → score → classify → respond — applies to any domain where AI agents face a flood of structured inputs (support tickets, lead qualification, content moderation).
- **Defensive AI tooling**: As AI makes it trivial to generate security reports at scale, projects need AI-assisted defenses. This skill demonstrates the "AI to fight AI" pattern.
- **Maintainer productivity**: Open-source maintainer burnout is a supply-chain risk. Tools that reduce triage burden directly protect the software ecosystem that commercial products depend on.
- **Claude Code skills as expert systems**: The SKILL.md format turns domain expertise into a portable, version-controlled artifact that any Claude Code user can install and benefit from immediately.
