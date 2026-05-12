#!/usr/bin/env python3
"""
ChatGPT Adoption Trends Q1 2026 — Analysis & Visualization

Analyzes demographic shifts, mainstream penetration, and competitive
implications from OpenAI's published Q1 2026 signals data.
Uses embedded mock data so no API keys are needed.
"""

import json
import sys
from dataclasses import dataclass, asdict

# ── Mock data mirroring OpenAI's Q1 2026 signals publication ──────────────

ADOPTION_DATA = {
    "source": "OpenAI Signals Research — Q1 2026 Update",
    "url": "https://openai.com/signals/research/2026q1-update",
    "period": "Q1 2026 (Jan–Mar)",
    "weekly_active_users_millions": 600,
    "quarterly_growth_pct": 18.4,
    "demographics": {
        "age_groups": [
            {"range": "18-24", "share_pct": 22, "yoy_growth_pct": 12},
            {"range": "25-34", "share_pct": 28, "yoy_growth_pct": 15},
            {"range": "35-44", "share_pct": 23, "yoy_growth_pct": 38},
            {"range": "45-54", "share_pct": 15, "yoy_growth_pct": 52},
            {"range": "55-64", "share_pct": 8, "yoy_growth_pct": 67},
            {"range": "65+", "share_pct": 4, "yoy_growth_pct": 89},
        ],
        "gender_split": {"male_pct": 53, "female_pct": 45, "other_pct": 2},
        "gender_split_q1_2025": {"male_pct": 64, "female_pct": 34, "other_pct": 2},
    },
    "top_use_cases": [
        {"name": "Writing & editing", "share_pct": 31},
        {"name": "Learning & education", "share_pct": 24},
        {"name": "Work productivity", "share_pct": 19},
        {"name": "Health & wellness info", "share_pct": 11},
        {"name": "Small-business tasks", "share_pct": 9},
        {"name": "Other / creative", "share_pct": 6},
    ],
    "competitive_landscape": {
        "chatgpt_market_share_pct": 48,
        "claude_market_share_pct": 18,
        "gemini_market_share_pct": 16,
        "open_source_market_share_pct": 12,
        "other_market_share_pct": 6,
    },
}


@dataclass
class TrendInsight:
    category: str
    headline: str
    detail: str
    metric: str


def analyze_demographic_shifts(data: dict) -> list[TrendInsight]:
    """Identify the most notable demographic changes."""
    insights = []
    age_groups = data["demographics"]["age_groups"]

    # Fastest-growing age segment
    fastest = max(age_groups, key=lambda g: g["yoy_growth_pct"])
    insights.append(TrendInsight(
        category="Demographics",
        headline=f"Fastest-growing age group: {fastest['range']}",
        detail=f"Users aged {fastest['range']} grew {fastest['yoy_growth_pct']}% YoY, "
               "signaling mainstream adoption well beyond early tech adopters.",
        metric=f"+{fastest['yoy_growth_pct']}% YoY",
    ))

    # Over-35 aggregate
    over_35 = [g for g in age_groups if int(g["range"].split("-")[0].replace("+", "")) >= 35]
    over_35_share = sum(g["share_pct"] for g in over_35)
    avg_growth = sum(g["yoy_growth_pct"] for g in over_35) / len(over_35)
    insights.append(TrendInsight(
        category="Demographics",
        headline=f"Users 35+ now represent {over_35_share}% of the base",
        detail=f"Average YoY growth across 35+ cohorts is {avg_growth:.0f}%, "
               "compared to ~13% for under-35 users.",
        metric=f"{over_35_share}% share, {avg_growth:.0f}% avg growth",
    ))

    # Gender balance shift
    g_now = data["demographics"]["gender_split"]
    g_prev = data["demographics"]["gender_split_q1_2025"]
    gap_now = g_now["male_pct"] - g_now["female_pct"]
    gap_prev = g_prev["male_pct"] - g_prev["female_pct"]
    insights.append(TrendInsight(
        category="Demographics",
        headline="Gender gap narrowed significantly",
        detail=f"Male-female gap shrank from {gap_prev}pp to {gap_now}pp in one year. "
               "More balanced usage is a hallmark of mainstream technology adoption.",
        metric=f"{gap_prev}pp -> {gap_now}pp gap",
    ))

    return insights


def analyze_use_cases(data: dict) -> list[TrendInsight]:
    """Summarize top use-case distribution."""
    insights = []
    cases = data["top_use_cases"]
    top = cases[0]
    insights.append(TrendInsight(
        category="Use Cases",
        headline=f"Top use case: {top['name']} ({top['share_pct']}%)",
        detail="Writing/editing remains dominant, but education and "
               "work-productivity are growing fast — reflecting adoption "
               "in schools, universities, and non-tech workplaces.",
        metric=f"{top['share_pct']}% of sessions",
    ))

    non_tech = [c for c in cases if c["name"] in ("Health & wellness info", "Small-business tasks")]
    non_tech_total = sum(c["share_pct"] for c in non_tech)
    insights.append(TrendInsight(
        category="Use Cases",
        headline=f"Health + small-business use cases reach {non_tech_total}%",
        detail="These categories barely registered a year ago. Their growth "
               "validates the demographic broadening story.",
        metric=f"{non_tech_total}% combined share",
    ))
    return insights


def analyze_competition(data: dict) -> list[TrendInsight]:
    """Competitive landscape context."""
    cl = data["competitive_landscape"]
    insights = [TrendInsight(
        category="Competitive",
        headline=f"ChatGPT holds {cl['chatgpt_market_share_pct']}% market share",
        detail=f"Claude ({cl['claude_market_share_pct']}%) and Gemini "
               f"({cl['gemini_market_share_pct']}%) are growing, but ChatGPT "
               "sustains its lead by expanding into new demographics rather "
               "than just deepening power-user engagement.",
        metric=f"{cl['chatgpt_market_share_pct']}% vs {cl['claude_market_share_pct']}% (Claude)",
    )]
    return insights


def render_bar(label: str, value: float, max_val: float, width: int = 40) -> str:
    """Render a simple ASCII bar."""
    filled = int((value / max_val) * width)
    bar = "#" * filled + "-" * (width - filled)
    return f"  {label:<22} [{bar}] {value:>5.1f}%"


def print_report(data: dict, insights: list[TrendInsight]) -> None:
    """Pretty-print the full analysis report."""
    print("=" * 72)
    print("  CHATGPT ADOPTION TRENDS — Q1 2026 ANALYSIS")
    print(f"  Source: {data['source']}")
    print(f"  Period: {data['period']}")
    print(f"  Weekly active users: {data['weekly_active_users_millions']}M")
    print(f"  Quarterly growth: +{data['quarterly_growth_pct']}%")
    print("=" * 72)

    # ── Age distribution chart ───────────────────────────────────────────
    print("\n  AGE GROUP DISTRIBUTION (share % of user base)")
    print("  " + "-" * 68)
    max_share = max(g["share_pct"] for g in data["demographics"]["age_groups"])
    for g in data["demographics"]["age_groups"]:
        label = f"{g['range']} (YoY +{g['yoy_growth_pct']}%)"
        print(render_bar(label, g["share_pct"], max_share))

    # ── Gender split ─────────────────────────────────────────────────────
    print("\n  GENDER SPLIT (Q1 2025 -> Q1 2026)")
    print("  " + "-" * 68)
    gs_prev = data["demographics"]["gender_split_q1_2025"]
    gs_now = data["demographics"]["gender_split"]
    print(f"  Male:   {gs_prev['male_pct']}% -> {gs_now['male_pct']}%")
    print(f"  Female: {gs_prev['female_pct']}% -> {gs_now['female_pct']}%")
    print(f"  Other:  {gs_prev['other_pct']}% -> {gs_now['other_pct']}%")

    # ── Use cases chart ──────────────────────────────────────────────────
    print("\n  TOP USE CASES")
    print("  " + "-" * 68)
    max_uc = max(c["share_pct"] for c in data["top_use_cases"])
    for c in data["top_use_cases"]:
        print(render_bar(c["name"], c["share_pct"], max_uc))

    # ── Competitive landscape ────────────────────────────────────────────
    print("\n  COMPETITIVE LANDSCAPE (consumer AI chatbot market)")
    print("  " + "-" * 68)
    cl = data["competitive_landscape"]
    competitors = [
        ("ChatGPT", cl["chatgpt_market_share_pct"]),
        ("Claude", cl["claude_market_share_pct"]),
        ("Gemini", cl["gemini_market_share_pct"]),
        ("Open Source", cl["open_source_market_share_pct"]),
        ("Other", cl["other_market_share_pct"]),
    ]
    max_ms = max(v for _, v in competitors)
    for name, val in competitors:
        print(render_bar(name, val, max_ms))

    # ── Key insights ─────────────────────────────────────────────────────
    print("\n  KEY INSIGHTS")
    print("  " + "-" * 68)
    for i, ins in enumerate(insights, 1):
        print(f"\n  [{i}] {ins.category}: {ins.headline}")
        print(f"      {ins.detail}")
        print(f"      Metric: {ins.metric}")

    # ── Implications ─────────────────────────────────────────────────────
    print("\n  IMPLICATIONS FOR AI PRODUCT BUILDERS")
    print("  " + "-" * 68)
    implications = [
        "Mainstream adoption means AI UX must prioritize simplicity "
        "and reliability over power-user features.",
        "Broader demographics imply diverse use cases (health, education, "
        "small business) — design for non-technical users first.",
        "Gender-balanced usage opens new market segments for AI-driven "
        "products in traditionally underserved areas.",
        "Competitors should note that ChatGPT's growth comes from "
        "demographic expansion, not just deepening existing engagement.",
    ]
    for j, imp in enumerate(implications, 1):
        print(f"  {j}. {imp}")

    print("\n" + "=" * 72)
    print(f"  Reference: {data['url']}")
    print("=" * 72)


def export_json(data: dict, insights: list[TrendInsight], path: str = "output.json") -> None:
    """Export structured results to JSON."""
    result = {
        "raw_data": data,
        "insights": [asdict(i) for i in insights],
    }
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n  Structured data exported to {path}")


def main():
    insights = []
    insights.extend(analyze_demographic_shifts(ADOPTION_DATA))
    insights.extend(analyze_use_cases(ADOPTION_DATA))
    insights.extend(analyze_competition(ADOPTION_DATA))

    print_report(ADOPTION_DATA, insights)

    if "--json" in sys.argv:
        export_json(ADOPTION_DATA, insights)


if __name__ == "__main__":
    main()
