# Tech Details

## What It Does

This tool implements a lightweight AI maturity assessment engine based on the framework from [OpenAI's enterprise scaling guide](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai). It scores an organization across 6 dimensions (12 questions), computes an overall maturity score, determines the current scaling phase (1-5), and generates prioritized recommendations with 90-day milestones. No LLM calls required — the recommendation engine is rule-based and deterministic.

The skill version (SKILL.md) embeds the same 5-phase framework as structured guidance that Claude Code can deliver conversationally when users ask about scaling AI adoption.

## Architecture

```
assess.py          CLI entry point — interactive mode, demo mode, JSON export
playbook.py        Core engine — scoring, phase detection, recommendation generation
SKILL.md           Claude Code skill definition (conversational trigger)
run.sh             Demo runner (bash run.sh → visible output, no keys needed)
```

### Data Flow

```
User answers (or mock data)
    → AssessmentAnswer objects (question_id + score 1-5)
    → compute_dimension_scores() — averages per dimension
    → determine_phase() — maturity thresholds map to Phase 1-5
    → generate_recommendations() — template matching against weak dimensions
    → generate_milestones() — phase-appropriate 90-day targets
    → PlaybookReport.render_text() — formatted terminal output
```

### Scoring Model

- **6 dimensions**, 2 questions each, scored 1-5
- **Maturity score** = mean of dimension averages
- **Phase thresholds**: <1.8 → Phase 1, <2.6 → Phase 2, <3.4 → Phase 3, <4.2 → Phase 4, else Phase 5
- **Recommendation priority**: dimension score <2.5 → HIGH, <3.5 → MEDIUM, else LOW
- Recommendations are included if the dimension is weak OR the recommendation's phase is at/near the org's current phase

### Dependencies

None. Pure Python 3.10+ stdlib (dataclasses, enum, json, argparse).

## Limitations

- **No LLM calls** — recommendations come from a static template library (~20 templates), not generated dynamically. Good enough for quick triage; not a substitute for a consulting engagement.
- **12 questions only** — the assessment is deliberately shallow for speed. A real maturity model would have 50-100 questions with weighted scoring.
- **No persistence** — there's no database or state between runs. Use `--json` to save snapshots for trend tracking.
- **Single-org focus** — no multi-tenant or benchmarking features. You can compare profiles manually by running multiple mock profiles.
- **English only** — all templates and output are in English.

## Why It Matters for Claude-Driven Products

If you're building products with Claude (agent factories, lead-gen, marketing automation, voice AI), this framework applies directly to your customers:

- **Agent factories**: Enterprises evaluating your agentic platform need a governance story. This playbook gives them the vocabulary and phased plan to justify procurement. Embed the assessment as an onboarding flow.
- **Lead-gen / marketing**: Use the maturity assessment as a lead magnet — "Score your AI readiness in 60 seconds." The report becomes a natural handoff to sales.
- **Ad creatives**: The 5-phase framework provides messaging structure for enterprise campaigns (Phase 1 buyers need trust signals; Phase 4 buyers need quality/scale proof points).
- **Voice AI**: Call-center AI deployments face exactly the trust → governance → workflow → quality progression. The human-in-the-loop tier model (Tier 1/2/3) maps directly to call routing decisions.

The skill version means Claude Code users at enterprises can self-serve the framework without needing a separate tool — they just ask Claude.
