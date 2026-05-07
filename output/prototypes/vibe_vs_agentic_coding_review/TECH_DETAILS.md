# Technical Details

## What it does

This is a Claude Code skill (prompt template) plus a standalone Python reference implementation that reviews unified diffs for anti-patterns commonly introduced by AI coding assistants. It applies Simon Willison's framework distinguishing "vibe coding" (fast, uncritical acceptance of AI output) from "agentic engineering" (disciplined review where the human remains the accountable engineer).

The skill teaches Claude Code a structured 6-step review checklist. The Python tool demonstrates the same logic with concrete pattern-matching detectors that score diffs on a 0-100 scale.

## Architecture

```
SKILL.md                  — Claude Code skill (drop into ~/.claude/skills/)
review_diff.py            — Scoring engine: 7 detectors + classifier
sample_diffs.py           — 4 mock diffs covering the spectrum
run.sh                    — Demo runner
```

### Key files

- **`review_diff.py`** — Core module. Contains 7 detector functions, each returning `Finding` objects with category/severity/message. The `review_diff()` function runs all detectors, computes a weighted score, and classifies as ship-it / needs-revision / start-over. No external dependencies.

- **`sample_diffs.py`** — Four representative diffs: a vibe-coded auth endpoint (security issues, no tests), a clean utility function (tests included), a scope-creep refactor (AI rewrote more than asked), and a throwaway prototype (vibe coding is fine).

- **`SKILL.md`** — The actual skill definition. Frontmatter with name/description/trigger conditions, followed by the checklist Claude follows when the skill activates.

### Detectors

| Detector | What it catches | Severity |
|---|---|---|
| `detect_nested_try_except` | Cargo-culted nested error handling | warning |
| `detect_broad_except` | `except Exception` that swallows errors | warning |
| `detect_security_issues` | MD5 hashing, debug info leaks, hardcoded secrets | critical |
| `detect_scope_creep` | Rewrites larger than requested, added docstrings/type hints | info-warning |
| `detect_missing_tests` | Implementation without corresponding test changes | warning |
| `detect_hallucinated_imports` | Suspiciously many imports from one module | info |
| `detect_over_abstraction` | Too many new functions/classes for the task size | info-warning |

### Scoring

- Start at 100
- Subtract per finding: info=3, warning=10, critical=25
- Throwaway context gets +30 bonus (vibe coding is acceptable there)
- 75+ = ship it, 40-74 = needs revision, <40 = start over

### Data flow

```
Diff text → 7 detectors (parallel) → [Finding, ...] → score → classification → formatted output
```

No network calls, no model calls, no API keys. Pure pattern matching on diff text.

## Dependencies

None. Python 3.10+ standard library only (`re`, `dataclasses`, `textwrap`, `sys`).

## Limitations

- **Pattern matching, not semantic analysis**: The Python detectors use regex on diff text. They catch structural anti-patterns (nested try/except, MD5, etc.) but cannot understand intent or verify logical correctness. The Claude Code skill compensates — when Claude uses this skill, it applies full LLM reasoning to the diff.

- **No git integration**: The standalone tool works on raw diff text, not live repos. You must pipe or paste diffs in. The Claude Code skill, however, has full repo access.

- **Python-biased detectors**: The regex patterns target Python syntax (try/except, def, import). The skill itself is language-agnostic since Claude handles any language.

- **No persistent state**: Doesn't track review history or learn from past decisions. Each review is independent.

- **Heuristic thresholds**: The "too many functions" and "too many lines changed" thresholds are educated guesses, not empirically tuned.

## Why it matters for Claude-driven products

This skill addresses the central tension in AI-assisted development: **the better AI gets, the less people review its output**. For teams building:

- **Agent factories** — Agents that write code need a review layer. This skill provides a structured framework for that review, whether done by a human or by another Claude instance.

- **Lead-gen / marketing / ad creative tools** — These often start as vibe-coded prototypes ("just make it work") that gradually become production systems. The skill helps identify when code has crossed that line and needs proper engineering attention.

- **Voice AI and real-time systems** — Security anti-patterns (MD5 hashing, debug info leaks) are especially dangerous in user-facing products. The security detectors catch the most common AI-generated vulnerabilities.

- **Any team scaling AI-assisted development** — As Willison notes, the convergence of vibe coding and agentic engineering is inevitable. Having an explicit checklist and scoring system helps teams maintain standards as they adopt AI tools more heavily.
