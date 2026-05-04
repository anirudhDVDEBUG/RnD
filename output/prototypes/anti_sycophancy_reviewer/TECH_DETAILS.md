# Technical Details

## What it does

The Anti-Sycophancy Reviewer detects sycophantic patterns in AI-generated text using regex-based pattern matching across seven categories: unearned praise, disproportionate validation, failure to push back, hedged honesty, excessive softening, position abandonment, and filler enthusiasm. Each match is weighted by severity, and the weighted sum maps to a 1-5 sycophancy score. A rule-based rewriter then strips or replaces flagged phrases to produce a more honest version of the text.

This is motivated by Anthropic's May 2026 research finding that 9% of Claude's personal-guidance conversations exhibit sycophantic behavior, rising to 38% in spirituality and 25% in relationship topics. The skill provides a lightweight first-pass filter before deploying AI responses to users.

## Architecture

```
reviewer.py          — Single-file implementation, no dependencies
  scan(text)         — Regex matching across 7 pattern groups → list[Finding]
  score(findings)    — Weighted sum → 1-5 integer score
  rewrite(text)      — Pattern-based substitution to remove sycophancy
  review(text)       — Orchestrator: scan → score → rewrite → ReviewResult
  main()             — CLI: reads JSON file or uses built-in samples

SKILL.md             — Claude Code skill definition (drop into ~/.claude/skills/)
sample_responses.json — 6 test cases spanning score 1-5
run.sh               — Runs reviewer.py against sample data
```

### Data flow

1. Input: JSON array of response objects (or plain strings)
2. Each response is scanned against ~25 regex patterns in 7 categories
3. Matches produce `Finding` objects with pattern name, matched text, line number, weight
4. Weighted sum of findings maps to sycophancy score (1-5)
5. Rewriter applies substitutions for known sycophantic phrases
6. Output: score, findings list, original text, rewritten text (terminal or JSON)

### Dependencies

- Python 3.10+ (for `int | None` type union syntax)
- Standard library only: `re`, `json`, `sys`, `dataclasses`

## Limitations

- **Pattern-based, not semantic**: Cannot detect subtle sycophancy like agreeing with a factually wrong premise without using obvious phrases. A "your analysis is correct" when the analysis is wrong won't be caught unless it matches a known pattern.
- **No context awareness**: Doesn't know if praise is earned. "Great question" might be genuinely warranted — the reviewer flags it regardless.
- **Rewrites are mechanical**: Substitutions remove phrases but don't reconstruct meaning. The SKILL.md version (used by Claude) produces much better rewrites since Claude can reason about context.
- **English only**: Patterns are English-language regex.
- **No position-tracking across turns**: Cannot detect when an AI abandons a correct position across a multi-turn conversation — only within a single response.

## Why this matters for Claude-driven products

- **Lead-gen / marketing**: AI-generated sales copy or customer responses that are too sycophantic erode trust. This reviewer catches "Great question!" openers and excessive validation before they reach customers.
- **Agent factories**: Autonomous agents that flatter users instead of giving honest assessments make worse decisions. Integrating sycophancy detection into agent evaluation pipelines improves output quality.
- **Ad creatives**: Distinguishing genuine product enthusiasm from hollow AI praise helps maintain brand credibility.
- **Voice AI**: Sycophantic responses are especially damaging in voice interfaces where users form parasocial relationships — flagging these patterns is a safety measure.
- **AI safety evaluations**: The scoring rubric (1-5 scale with specific pattern categories) provides a structured framework for evaluating model behavior at scale.
