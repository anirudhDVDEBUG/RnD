# Technical Details

## What it does

The GenAI Consulting Methodology Toolkit implements a structured consulting framework for diagnosing enterprise AI readiness and planning transformation. It evaluates organizations across five dimensions (Strategy, Data, Talent, Governance, Use Cases) on an L1-L5 maturity scale, then generates gap analyses, prioritized use-case matrices, and phased roadmaps. The upstream repo also includes n8n workflow templates and Open WebUI integration for operationalizing assessments.

The core logic is deterministic and rule-based — no LLM calls are needed to produce the scorecard and roadmap. This makes it fast, reproducible, and auditable, which matters in consulting contexts where clients want to understand exactly how their score was derived.

## Architecture

```
mock_company.json          assess.py                   Terminal + JSON
┌──────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│ Company name │────►│ DimensionScore      │────►│ Maturity card    │
│ Dimensions[] │     │ analyze_gaps()      │     │ Gap analysis     │
│ Use cases[]  │     │ generate_roadmap()  │     │ Recommendations  │
│              │     │ prioritize_cases()  │     │ Use-case matrix  │
│              │     │ determine_stage()   │     │ Roadmap (3 tier) │
└──────────────┘     └─────────────────────┘     │ Stage indicator  │
                                                  └──────────────────┘
                                                  assessment_output.json
```

### Key files

| File | Purpose |
|------|---------|
| `assess.py` | All logic: data structures, gap analysis rules, roadmap generator, use-case scorer, CLI entry point, report printer |
| `mock_company.json` | Example input: a mid-size manufacturer at L1-L2 maturity |
| `SKILL.md` | Claude Code skill definition with trigger phrases and methodology reference |
| `run.sh` | One-command demo runner |

### Data flow

1. **Input**: JSON company profile with dimension scores (1-5), evidence strings, and candidate use cases with impact/feasibility/fit ratings.
2. **Gap analysis**: For each dimension, the `GAP_RECOMMENDATIONS` lookup table maps `(current_level, target_level)` step pairs to concrete recommendations. Every level gap produces specific, actionable items.
3. **Roadmap**: Recommendations are bucketed into 90-day (first priority per dimension), 6-month, and 12-month horizons automatically.
4. **Use-case scoring**: Weighted formula: `impact×0.4 + feasibility×0.35 + strategic_fit×0.25`. Cases scoring >=4.0 get starred as top picks.
5. **Stage mapping**: Overall maturity average maps to one of the eight consulting stages, telling the consultant where to focus next.
6. **Output**: Rich terminal report + `assessment_output.json` for downstream tooling.

### Dependencies

None beyond Python 3.8+ stdlib (`json`, `dataclasses`, `sys`).

The upstream repo optionally uses:
- **n8n** for workflow automation of the assessment pipeline
- **Open WebUI** for interactive questionnaire UI
- **Claude / LLM APIs** for generating narrative summaries (not required for core scoring)

## Limitations

- **No interactive questionnaire**: This prototype takes pre-scored dimensions. The upstream repo's Open WebUI integration handles guided discovery, but that requires a running Open WebUI instance.
- **Static recommendation bank**: Gap recommendations are hard-coded per level transition. They cover common scenarios well but aren't industry-specific. A production deployment would want to fine-tune these per vertical.
- **No persistence**: Each run is stateless. Tracking maturity progress over time would require wrapping this in a database-backed application.
- **Scoring is manual input, not automated**: The tool doesn't crawl your infrastructure or interview stakeholders — a human consultant provides the dimension scores based on their assessment.
- **English/bilingual**: The SKILL.md references APAC/Taiwan market contexts, but the prototype output is English-only. The upstream repo includes Traditional Chinese documentation.

## Why it matters for Claude-driven products

**Consulting-as-code pattern**: This is a template for encoding domain expertise into structured, repeatable workflows. The same pattern applies to:

- **Lead-gen / marketing**: Replace maturity dimensions with marketing readiness dimensions (content strategy, analytics maturity, channel coverage) to score and qualify enterprise leads.
- **Agent factories**: The eight-stage framework maps naturally to an agentic workflow — each stage becomes a sub-agent that gathers data, scores, and generates recommendations.
- **Ad creatives**: Use-case prioritization matrix logic (impact × feasibility × fit) is directly reusable for creative campaign prioritization.
- **Voice AI**: The structured questionnaire format (assess 5 dimensions, score 1-5) is ideal for voice-driven intake — a voice agent walks the client through scoring.

The skill format means Claude Code can run this methodology conversationally — a consultant using Claude Code gets an AI copilot that knows the framework and produces deliverables on the fly.
