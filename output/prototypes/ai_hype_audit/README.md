# AI Hype Audit

**TL;DR:** A Claude Code skill (and standalone CLI tool) that scores AI proposals on a 1–10 substance scale, flags buzzword inflation, and delivers a verdict: *Ship It*, *Needs Work*, or *Career Theater*.

## Headline Result

```
  SUBSTANCE SCORE: 2/10
  VERDICT: Career Theater

  [1] (BUZZWORD) "revolutionary AI-first strategy"
      -> "revolutionary" is a buzzword that adds no technical specificity.
  [2] (VAGUE_CLAIM) "fully automate all... no human intervention needed"
      -> Full automation claims are unrealistic — specify expected error rates.
```

A hype-laden "AI Transformation" memo scores 2/10. A scoped pilot proposal with metrics, costs, and fallbacks scores 8/10. The tool tells you which is which — and why.

## Quick Start

```bash
bash run.sh          # runs both sample audits, no API keys needed
echo "your text" | python3 audit.py   # audit any text from stdin
```

See [HOW_TO_USE.md](HOW_TO_USE.md) for Claude Code skill installation and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture.
