# Technical Details

## What it does

This is a **Claude Code skill** (a `SKILL.md` file) plus a standalone Python demo. The skill injects curated facts and analysis points about Y Combinator's ~0.6% stake in OpenAI into Claude's context when triggered by relevant user queries. The Python demo independently computes stake valuations, return multiples, comparables, and sensitivity tables using embedded data — no LLM calls or API keys required.

The data comes from John Gruber's Daring Fireball post on YC's stake, quoted by Simon Willison, cross-referenced with OpenAI's announced $852B valuation.

## Architecture

```
yc_openai_stake_analysis/
├── SKILL.md               # Claude Code skill definition (trigger phrases + knowledge)
├── yc_openai_analysis.py  # Standalone analysis script
├── run.sh                 # Entry point — runs the Python script
├── requirements.txt       # No external deps (stdlib only)
└── output.json            # Generated structured output
```

**Data flow:** Embedded dataclasses → computed properties (stake value, multiples) → formatted terminal output + JSON file.

**Dependencies:** Python 3.10+ standard library only (`json`, `textwrap`, `dataclasses`).

**Model calls:** None. The skill file is consumed by Claude Code at session start; the Python demo is purely computational.

## Limitations

- **Static data:** The 0.6% stake figure and $852B valuation are point-in-time (May 2026). OpenAI's valuation and YC's diluted stake will change with future funding rounds.
- **Estimated initial investment:** The ~$150K figure is inferred from YC's historical deal terms circa 2005; the actual amount for OpenAI may differ given its atypical structure.
- **No live data:** The demo does not fetch real-time valuations or SEC filings. To keep it API-key-free, all data is hardcoded.
- **Comparables are approximate:** Stake percentages for Airbnb, Stripe, and DoorDash are public estimates, not audited figures.

## Why it matters for Claude-driven product builders

- **Market signal:** $852B valuations and 34,000x returns mean capital is flooding into AI infrastructure. Teams building on Claude (lead-gen agents, ad-creative pipelines, voice AI) operate in a rapidly capitalizing ecosystem — more customers, more competition.
- **Skill pattern:** This repo demonstrates how to package domain-specific knowledge as a Claude Code skill: curated facts, trigger phrases, and structured references that make Claude immediately useful for a niche topic without fine-tuning.
- **Downstream integration:** The `output.json` format is designed to feed into dashboards, newsletters, or agent pipelines that track AI-sector financials.
