# Technical Details — AI Hype Audit

## What It Does

A regex-and-heuristic scoring engine that analyzes text for AI hype patterns. It counts buzzwords, measures specificity (numbers, metrics, timelines), checks feasibility of automation claims, verifies ROI grounding (cost mentions, success criteria), and assesses whether human workforce impact is handled responsibly. No LLM calls required — it runs entirely on pattern matching against curated phrase lists.

The tool is inspired by Mo Bitar's satirical "Unethical Guide to Surviving AI Layoffs" (cited by Simon Willison), which describes the "Ralph Loop" — a pattern where someone publicly announces AI will replace a colleague's role, creating pressure to either adopt vaporware or be seen as resistant to innovation. This skill catches that pattern and others before they erode team trust.

## Architecture

```
audit.py              — Core engine: scoring functions + CLI entrypoint
sample_proposals.py   — Two demo texts (hype vs. grounded) for testing
run.sh                — End-to-end demo script
SKILL.md              — Claude Code skill definition (drop into ~/.claude/skills/)
```

### Data Flow

1. Text input (stdin, file, or Claude skill context)
2. Five parallel scoring passes:
   - `score_buzzword_density()` — regex match against 35+ buzzword patterns
   - `score_specificity()` — regex match for numbers, metrics, timelines
   - `score_feasibility()` — detect infeasible automation claims
   - `score_roi_grounding()` — check for cost/budget/ROI mentions
   - `score_human_impact()` — detect displacement language vs. responsible transition
3. Weighted composite → substance score (1–10)
4. Verdict classification based on score thresholds
5. Structured output (formatted report + JSON)

### Dependencies

- Python 3.7+ standard library only (`re`, `json`, `sys`, `dataclasses`)
- No external packages, no API keys, no network access

### Model Calls

None. This is a deterministic heuristic tool. When used as a Claude Code skill, Claude applies the rubric from SKILL.md using its own reasoning — the skill file provides the scoring framework and Claude does the nuanced analysis that regex cannot (context-dependent claims, domain-specific feasibility, etc.).

## Limitations

- **No semantic understanding** — the standalone CLI uses pattern matching only. It cannot judge whether a specific claim is technically feasible in context (e.g., "automate invoice processing" is feasible; "automate strategic planning" is not). The Claude skill version handles this via LLM reasoning.
- **English only** — patterns are English-language buzzwords.
- **No PDF/slide parsing** — input must be plain text. Extract text from decks before piping in.
- **Threshold tuning** — the buzzword list and scoring weights reflect common patterns but may need tuning for specific industries (biotech, fintech jargon differs).
- **False positives** — legitimate use of words like "transform" in technical contexts (data transformation) may trigger buzzword flags.

## Why It Matters for Claude-Driven Products

| Use Case | Application |
|----------|-------------|
| **Agent factories** | Gate AI initiative proposals before allocating engineering time — only build agents for grounded use cases |
| **Lead-gen / marketing** | Audit your own outbound AI messaging — prospects are increasingly skeptical of AI hype |
| **Ad creatives** | Score ad copy for substance vs. empty claims before A/B testing |
| **Voice AI** | Validate that voice-agent pitch decks have real metrics before investing in integration |
| **Internal tooling** | Give engineering managers a quick filter for AI budget requests that lack success criteria |

The meta-insight: if you're building AI products, your credibility depends on not sounding like the proposals this tool flags. Use it on your own docs first.
