# Technical Details — TDM Messaging Audit

## What it does

The TDM Messaging Audit evaluates product copy against the mental model of a **Technical Decision Maker** — the majority of enterprise buyers who rely on analyst reports (Gartner, Forrester, McKinsey) and secular trends to make defensible purchasing decisions. It scores messaging on 5 dimensions, flags weak areas, and generates concrete rewrites that shift copy from developer-culture language to analyst-aligned, career-safe positioning.

The core insight comes from Mitchell Hashimoto (co-founder of HashiCorp): 90% of TDMs are motivated primarily by *not getting fired*. They need copy that maps to recognized categories, references trusted proof points, and can be pasted into a procurement justification without embarrassment.

## Architecture

### Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Claude Code skill definition — the prompt Claude follows when triggered |
| `tdm_audit.py` | Standalone Python scorer — keyword-based heuristic audit (no LLM needed) |
| `sample_copies.py` | Three sample landing pages: weak, mixed, strong |
| `run.sh` | Runs the demo end-to-end |

### Scoring dimensions

1. **Analyst Alignment** — Matches copy against ~25 analyst-recognized terms (e.g., "composable architecture", "AI governance", "platform engineering"). Higher term density = higher score.
2. **Career-Safety Signaling** — Detects trust signals: compliance badges (SOC 2, HIPAA), analyst mentions, enterprise social proof, customer logos.
3. **Trend Anchoring** — Checks whether the product positions itself within a recognized secular trend (AI, cloud-native, zero trust).
4. **Jargon Calibration** — Penalizes developer-culture jargon ("blazingly fast", "yak shaving", "Hacker News") that a 9-to-5 TDM wouldn't recognize or trust.
5. **Defensibility Framing** — Composite score: can a TDM point to this page and justify the purchase to leadership?

### Data flow

```
Copy text ──→ Keyword matching against 4 term sets
           ──→ Score (1-5) per dimension
           ──→ Rewrite suggestions for scores < 3
           ──→ Formatted report with summary table
```

### When used as a Claude Code Skill

Claude reads the SKILL.md instructions and applies the 5-dimension framework using its own judgment — no keyword matching needed. The LLM evaluates semantic meaning, not just term presence, making it far more nuanced than the standalone Python demo. The Python version exists as a runnable proof-of-concept.

## Dependencies

- **Python 3.10+** (stdlib only, no pip packages)
- **No API keys required** — the standalone demo uses heuristic keyword matching
- When used as a Claude Code skill, Claude itself is the "engine"

## Limitations

- The Python scorer uses keyword matching, not semantic understanding. It will miss synonyms and context. The Claude Code skill version is much more capable.
- Term lists are opinionated and US-enterprise-centric. EMEA/APAC analyst vocabulary may differ.
- Does not evaluate visual design, layout, or above-the-fold placement — text only.
- Does not fetch URLs directly — you must provide copy as text (the Claude skill can fetch URLs via tools).
- Rewrite suggestions are templates, not polished final copy. The Claude skill generates context-aware rewrites.

## Why this matters for Claude-driven products

- **Lead-gen / marketing teams**: Audit landing pages before launch. Catch "developer brain" copy that repels enterprise buyers.
- **Agent factories**: Embed TDM scoring as a step in content-generation pipelines — every AI-generated landing page gets an automatic enterprise-readiness check.
- **Ad creatives**: Score ad copy variants for TDM resonance before A/B testing. Filter out variants that only appeal to the developer 10%.
- **Sales enablement**: Audit pitch decks and one-pagers against the same framework procurement teams use internally.
