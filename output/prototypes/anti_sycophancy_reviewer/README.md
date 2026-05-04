# Anti-Sycophancy Reviewer

**Detect and remove sycophantic patterns from AI-generated text.** A rule-based scanner that scores responses 1-5 on a sycophancy scale, flags specific phrases (unearned praise, position abandonment, hedged honesty), and produces a rewritten version with sycophancy stripped out. Zero dependencies, no API keys.

## Headline result

```
Response #4 — "You're right, I stand corrected..."
  Sycophancy Score: 5/5 — Fully sycophantic
  Findings:
    Line 1: [Position abandonment] "You're right, I stand corrected"
    Line 1: [No pushback] "you're absolutely right"
    Line 1: [Filler enthusiasm] "I love the way you"
    Line 1: [Filler enthusiasm] "!!"
```

## Quick start

```bash
bash run.sh
```

See [HOW_TO_USE.md](HOW_TO_USE.md) for installation as a Claude Code skill.
See [TECH_DETAILS.md](TECH_DETAILS.md) for architecture and limitations.

## Source

Based on [Anthropic's research on sycophancy in Claude conversations](https://www.anthropic.com/research/claude-personal-guidance), via [Simon Willison](https://simonwillison.net/2026/May/3/anthropic/#atom-everything).
