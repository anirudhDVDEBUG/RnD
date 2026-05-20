#!/usr/bin/env python3
"""
LLM Landscape Briefing Generator

Generates a structured briefing on the current LLM landscape using
curated data from Simon Willison's PyCon US 2026 lightning talk and
publicly known model release timelines.

No API keys required — all data is embedded.
"""

import json
import sys
from datetime import date

# --- Embedded knowledge base (no API calls needed) ---

MODEL_TIERS = {
    "Frontier": [
        {"name": "Claude Opus 4.6", "vendor": "Anthropic", "released": "2026-05"},
        {"name": "GPT-5", "vendor": "OpenAI", "released": "2026-03"},
        {"name": "Gemini 2.5 Pro", "vendor": "Google", "released": "2026-03"},
    ],
    "Balanced": [
        {"name": "Claude Sonnet 4.6", "vendor": "Anthropic", "released": "2026-05"},
        {"name": "GPT-4.1", "vendor": "OpenAI", "released": "2025-04"},
        {"name": "Gemini 2.5 Flash", "vendor": "Google", "released": "2025-04"},
    ],
    "Fast / Cheap": [
        {"name": "Claude Haiku 4.5", "vendor": "Anthropic", "released": "2025-10"},
        {"name": "GPT-4.1 mini", "vendor": "OpenAI", "released": "2025-04"},
        {"name": "Gemini 2.5 Flash-Lite", "vendor": "Google", "released": "2025-04"},
    ],
}

LEADERSHIP_TIMELINE = [
    {"period": "Nov 2025", "leader": "Claude 3.5 Sonnet (new)", "vendor": "Anthropic", "note": "Coding inflection point"},
    {"period": "Dec 2025", "leader": "Gemini 2.0 Flash", "vendor": "Google", "note": "Speed + quality leap"},
    {"period": "Jan 2026", "leader": "o3-mini", "vendor": "OpenAI", "note": "Reasoning benchmark sweep"},
    {"period": "Feb 2026", "leader": "Claude 3.5 Opus", "vendor": "Anthropic", "note": "Agentic coding dominance"},
    {"period": "Mar 2026", "leader": "GPT-5", "vendor": "OpenAI", "note": "Broad capability jump"},
]

KEY_INSIGHTS = [
    "The 'best' model changed hands 5 times in 6 months — vendor lock-in is risky.",
    "Nov 2025 was the inflection point: coding agents went from 'neat trick' to 'daily driver'.",
    "Evaluate on YOUR tasks, not leaderboards. Rankings vary wildly by domain.",
    "Recommendations expire in ~3 months. Build for model-switching.",
    "Cost/speed/quality tradeoffs matter more than raw capability for production.",
]

RECOMMENDATIONS = {
    "coding": "Test Claude Opus 4.6, GPT-5, and Gemini 2.5 Pro on real tasks from your codebase. Coding saw the biggest gains.",
    "general": "Claude Sonnet 4.6 or GPT-4.1 offer the best quality/cost ratio for most production workloads.",
    "cost_sensitive": "Haiku 4.5, GPT-4.1 mini, and Flash-Lite are surprisingly capable for structured tasks.",
    "multi_provider": "Use LiteLLM or Simon Willison's `llm` CLI to abstract the provider layer. Switch without rewriting.",
}


def generate_briefing(focus: str = "general", output_format: str = "text") -> str:
    """Generate a structured LLM landscape briefing."""

    today = date.today().isoformat()

    if output_format == "json":
        return json.dumps({
            "generated": today,
            "focus": focus,
            "model_tiers": MODEL_TIERS,
            "leadership_timeline": LEADERSHIP_TIMELINE,
            "key_insights": KEY_INSIGHTS,
            "recommendation": RECOMMENDATIONS.get(focus, RECOMMENDATIONS["general"]),
            "source": "Simon Willison, PyCon US 2026 — 'The last six months in LLMs in five minutes'",
        }, indent=2)

    # --- Text output ---
    lines = []
    lines.append("=" * 64)
    lines.append("  LLM LANDSCAPE BRIEFING")
    lines.append(f"  Generated: {today} | Focus: {focus}")
    lines.append("=" * 64)

    # Leadership timeline
    lines.append("\n## Model Leadership Timeline (Nov 2025 – Mar 2026)\n")
    for entry in LEADERSHIP_TIMELINE:
        marker = "*" if entry["vendor"] == "Anthropic" else " "
        lines.append(f"  {marker} {entry['period']:>8}  {entry['leader']:<28} [{entry['vendor']}]")
        lines.append(f"             {entry['note']}")
    lines.append(f"\n  -> Leadership changed 5 times across 3 vendors in 6 months.")

    # Current model tiers
    lines.append("\n## Current Model Tiers (mid-2026)\n")
    for tier, models in MODEL_TIERS.items():
        lines.append(f"  [{tier}]")
        for m in models:
            lines.append(f"    - {m['name']:<24} ({m['vendor']}, {m['released']})")
        lines.append("")

    # Key insights
    lines.append("## Key Insights\n")
    for i, insight in enumerate(KEY_INSIGHTS, 1):
        lines.append(f"  {i}. {insight}")

    # Recommendation
    rec = RECOMMENDATIONS.get(focus, RECOMMENDATIONS["general"])
    lines.append(f"\n## Recommendation ({focus})\n")
    lines.append(f"  {rec}")

    # Source
    lines.append("\n" + "-" * 64)
    lines.append("  Source: Simon Willison, PyCon US 2026 Lightning Talk")
    lines.append("  https://simonwillison.net/2026/May/19/5-minute-llms/")
    lines.append("-" * 64)

    return "\n".join(lines)


def main():
    focus = sys.argv[1] if len(sys.argv) > 1 else "general"
    fmt = sys.argv[2] if len(sys.argv) > 2 else "text"

    valid_focuses = list(RECOMMENDATIONS.keys())
    if focus not in valid_focuses:
        print(f"Unknown focus '{focus}'. Choose from: {', '.join(valid_focuses)}")
        sys.exit(1)

    print(generate_briefing(focus=focus, output_format=fmt))


if __name__ == "__main__":
    main()
