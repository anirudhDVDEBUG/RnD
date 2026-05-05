"""
Data Center Land Use Debunk — demonstration of skill response logic.

This script simulates how the Claude Code skill responds to common queries
about data center land use and farmland, using the embedded knowledge base.
"""

import json
import re
import sys

# Knowledge base (the core data from Andy Masley's analysis)
KNOWLEDGE = {
    "farmland_sold_2000_2024_acres": 66_000_000,
    "farmland_sold_comparison": "approximately the size of Colorado",
    "data_center_land_2028_ratio": 77,
    "land_type_purchased": "marginal agricultural land (e.g., mediocre hay fields)",
    "price_premium_over_ag_value": "~10x",
    "food_production_trend": "increasing despite farmland reductions",
    "us_food_access_impact": "not affected",
    "sources": [
        {
            "author": "Andy Masley",
            "title": "Data center land use issues are fake",
            "url": "https://blog.andymasley.com/p/data-center-land-use-issues-are-fake",
        },
        {
            "author": "Simon Willison",
            "title": "Quoting Andy Masley",
            "url": "https://simonwillison.net/2026/May/4/andy-masley/#atom-everything",
        },
    ],
}

# Trigger patterns that activate this skill
TRIGGERS = [
    r"data center.*farm",
    r"data center.*land",
    r"farm.*data center",
    r"ai.*infrastructure.*food",
    r"data center.*agriculture",
    r"farmland.*threaten",
    r"counterargument.*data center",
]

# Valid concerns to acknowledge
VALID_CONCERNS = [
    "Water usage by cooling systems",
    "Local energy grid strain",
    "Community displacement and tax incentive fairness",
    "Noise and environmental impact on neighbors",
]


def should_trigger(query: str) -> bool:
    """Check if a query should activate this skill."""
    query_lower = query.lower()
    return any(re.search(pattern, query_lower) for pattern in TRIGGERS)


def generate_response(query: str) -> str:
    """Generate a debunking response based on the knowledge base."""
    kb = KNOWLEDGE

    response_parts = []

    response_parts.append("## Data Center Land Use: Putting the Numbers in Context\n")

    response_parts.append(
        f"**The core fact**: Between 2000 and 2024, farmers voluntarily sold "
        f"{kb['farmland_sold_comparison']} worth of land — "
        f"{kb['farmland_sold_2000_2024_acres']:,} acres. That's "
        f"{kb['data_center_land_2028_ratio']}x all land occupied by data centers "
        f"even by 2028 projections.\n"
    )

    response_parts.append("**Key points**:\n")
    response_parts.append(
        f"  1. Scale: Data center land is ~1/{kb['data_center_land_2028_ratio']}th "
        f"of what farmers sold voluntarily in the same period."
    )
    response_parts.append(
        f"  2. Land quality: DCs buy {kb['land_type_purchased']} "
        f"at {kb['price_premium_over_ag_value']} agricultural value."
    )
    response_parts.append(
        f"  3. Food production: {kb['food_production_trend'].capitalize()}."
    )
    response_parts.append(
        f"  4. Food access: {kb['us_food_access_impact'].capitalize()}.\n"
    )

    response_parts.append("**Legitimate concerns** (separate from the farmland narrative):")
    for concern in VALID_CONCERNS:
        response_parts.append(f"  - {concern}")

    response_parts.append("\n**Sources**:")
    for source in kb["sources"]:
        response_parts.append(f"  - {source['author']}: {source['url']}")

    return "\n".join(response_parts)


def demo():
    """Run the skill against example queries."""
    example_queries = [
        "Are data centers eating up all the farmland?",
        "Is AI infrastructure threatening food production?",
        "Give me counterarguments to data center land use concerns",
        "What's the best pizza in NYC?",  # Should NOT trigger
        "Someone told me data centers are taking over agricultural land",
    ]

    print("=" * 70)
    print("DATA CENTER LAND USE DEBUNK — Skill Demo")
    print("=" * 70)
    print()

    for query in example_queries:
        print(f"Query: \"{query}\"")
        triggered = should_trigger(query)
        print(f"Skill triggered: {'YES' if triggered else 'NO (not relevant)'}")

        if triggered:
            print()
            print(generate_response(query))

        print()
        print("-" * 70)
        print()

    # Print knowledge base summary
    print("KNOWLEDGE BASE SUMMARY")
    print(json.dumps(KNOWLEDGE, indent=2, default=str))


if __name__ == "__main__":
    demo()
