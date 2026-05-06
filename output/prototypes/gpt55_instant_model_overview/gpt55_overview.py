#!/usr/bin/env python3
"""
GPT-5.5 Instant Model Overview — Claude Skill Demo

Demonstrates the knowledge a Claude skill would surface when users ask
about OpenAI's GPT-5.5 Instant release.  No API keys required; all data
is embedded from the official OpenAI blog post.
"""

import json
import textwrap
from datetime import date

# ── Embedded knowledge base (mirrors SKILL.md) ──────────────────────────

MODEL_INFO = {
    "name": "GPT-5.5 Instant",
    "vendor": "OpenAI",
    "announced": "May 2026",
    "blog_url": "https://openai.com/index/gpt-5-5-instant",
    "role": "New default model for ChatGPT",
    "replaces": "Previous ChatGPT default (GPT-4o tier)",
    "key_improvements": [
        "Smarter, more accurate responses",
        "Clearer, more natural communication style",
        "Reduced hallucinations via architectural + training changes",
        "Enhanced personalization controls (tone, detail, interaction style)",
        "Optimized latency — the 'Instant' designation",
    ],
    "hallucination_reduction": {
        "approach": "Architectural and training-pipeline improvements targeting factual accuracy",
        "goal": "Reduce confabulation — model declines rather than fabricates when uncertain",
    },
    "personalization": {
        "features": [
            "Adjustable response tone (formal ↔ casual)",
            "Configurable detail level (concise ↔ comprehensive)",
            "Customizable interaction style preferences",
        ],
        "mechanism": "User-facing controls stored in ChatGPT profile, applied at inference time",
    },
    "lineup_position": {
        "tier": "Default / everyday",
        "speed": "Fast (optimized latency)",
        "comparison": "Heavier reasoning models (o-series) handle complex multi-step tasks",
    },
}

COMPETITOR_COMPARISON = [
    {
        "model": "GPT-5.5 Instant",
        "vendor": "OpenAI",
        "tier": "Default fast",
        "hallucination_focus": "Yes — core selling point",
        "personalization": "Built-in user controls",
    },
    {
        "model": "Claude Opus 4.6",
        "vendor": "Anthropic",
        "tier": "Flagship reasoning",
        "hallucination_focus": "Yes — constitutional AI + citations",
        "personalization": "System prompts / skills",
    },
    {
        "model": "Claude Sonnet 4.6",
        "vendor": "Anthropic",
        "tier": "Balanced speed/quality",
        "hallucination_focus": "Yes — same family",
        "personalization": "System prompts / skills",
    },
    {
        "model": "Claude Haiku 4.5",
        "vendor": "Anthropic",
        "tier": "Fast / cost-efficient",
        "hallucination_focus": "Moderate",
        "personalization": "System prompts / skills",
    },
]

# ── Query handlers ───────────────────────────────────────────────────────

QUERIES = {
    "overview": {
        "question": "What is GPT-5.5 Instant?",
        "handler": "_answer_overview",
    },
    "hallucinations": {
        "question": "How does GPT-5.5 Instant reduce hallucinations?",
        "handler": "_answer_hallucinations",
    },
    "personalization": {
        "question": "What personalization features does GPT-5.5 Instant have?",
        "handler": "_answer_personalization",
    },
    "comparison": {
        "question": "How does GPT-5.5 Instant compare to Claude models?",
        "handler": "_answer_comparison",
    },
    "implications": {
        "question": "Why does this matter for Claude-based product builders?",
        "handler": "_answer_implications",
    },
}


def _answer_overview() -> str:
    m = MODEL_INFO
    improvements = "\n".join(f"  - {i}" for i in m["key_improvements"])
    return textwrap.dedent(f"""\
    # {m['name']}

    **Vendor:** {m['vendor']}  |  **Announced:** {m['announced']}
    **Role:** {m['role']}  |  **Replaces:** {m['replaces']}

    ## Key improvements
    {improvements}

    **Lineup position:** {m['lineup_position']['tier']} tier, optimized for
    speed.  Complex reasoning tasks still route to OpenAI's o-series models.

    Source: {m['blog_url']}
    """)


def _answer_hallucinations() -> str:
    h = MODEL_INFO["hallucination_reduction"]
    return textwrap.dedent(f"""\
    # Hallucination Reduction in GPT-5.5 Instant

    **Approach:** {h['approach']}

    **Goal:** {h['goal']}

    This is a direct response to user-trust concerns that have plagued all
    large language models.  OpenAI is positioning factual accuracy as a
    first-class product feature rather than a research afterthought.
    """)


def _answer_personalization() -> str:
    p = MODEL_INFO["personalization"]
    features = "\n".join(f"  - {f}" for f in p["features"])
    return textwrap.dedent(f"""\
    # Personalization in GPT-5.5 Instant

    ## Available controls
    {features}

    **How it works:** {p['mechanism']}

    This moves personalization from prompt-engineering hacks into a
    first-party UX — lowering the bar for non-technical users.
    """)


def _answer_comparison() -> str:
    header = f"{'Model':<22} {'Vendor':<12} {'Tier':<22} {'Halluc. Focus':<28} {'Personalization'}"
    sep = "-" * len(header)
    rows = [header, sep]
    for c in COMPETITOR_COMPARISON:
        rows.append(
            f"{c['model']:<22} {c['vendor']:<12} {c['tier']:<22} "
            f"{c['hallucination_focus']:<28} {c['personalization']}"
        )
    return "# GPT-5.5 Instant vs Claude Model Family\n\n" + "\n".join(rows) + "\n"


def _answer_implications() -> str:
    return textwrap.dedent("""\
    # Implications for Claude-Based Product Builders

    1. **Competitive pressure on hallucination metrics** — If GPT-5.5 Instant
       delivers measurably fewer hallucinations, Claude-powered products need
       to emphasize citations, source grounding, and constitutional-AI
       safeguards as differentiators.

    2. **Personalization as table stakes** — Built-in tone/detail controls
       raise user expectations.  Claude skills and system prompts already
       enable this, but the UX gap matters for end-user products.

    3. **Speed tier alignment** — "Instant" signals that OpenAI's default is
       latency-optimized.  For agent factories and voice-AI pipelines,
       Claude Haiku 4.5 / Sonnet 4.6 remain competitive on speed.

    4. **Marketing angle** — Competitors highlighting "fewer hallucinations"
       gives Claude products an opening to counter with verifiable citations
       and tool-use transparency.

    5. **Lead-gen / ad-creative workflows** — Personalization controls could
       let ChatGPT users self-serve brand-voice tuning, a feature Claude
       skill authors should consider replicating.
    """)


# ── Main demo loop ───────────────────────────────────────────────────────

HANDLERS = {
    "overview": _answer_overview,
    "hallucinations": _answer_hallucinations,
    "personalization": _answer_personalization,
    "comparison": _answer_comparison,
    "implications": _answer_implications,
}


def run_demo():
    print("=" * 70)
    print(" GPT-5.5 Instant — Claude Skill Demo")
    print(f" Generated: {date.today().isoformat()}")
    print("=" * 70)

    for key, meta in QUERIES.items():
        print(f"\n{'─' * 70}")
        print(f"  Q: {meta['question']}")
        print(f"{'─' * 70}\n")
        print(HANDLERS[key]())

    # Also dump structured JSON for downstream tooling
    print("=" * 70)
    print(" Structured data (JSON)")
    print("=" * 70)
    print(json.dumps(MODEL_INFO, indent=2))


if __name__ == "__main__":
    run_demo()
