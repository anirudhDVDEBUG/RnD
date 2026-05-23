"""Keyword research module — expands seed keywords with volume, competition, and relevance."""

import argparse
import sys

from . import mock_data

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def research_keywords(seed: str) -> None:
    keywords = mock_data.KEYWORDS.get(seed)
    if not keywords:
        print(f"No keyword data for seed '{seed}'. Available seeds: {', '.join(mock_data.KEYWORDS.keys())}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  KEYWORD RESEARCH")
    print(f"{'='*60}")
    print(f"\n  Seed keyword: \"{seed}\"")
    print(f"  Results: {len(keywords)} keywords found")

    sorted_kw = sorted(keywords, key=lambda k: k["volume"], reverse=True)

    if tabulate:
        table = []
        for i, kw in enumerate(sorted_kw, 1):
            table.append([
                i,
                kw["keyword"],
                f"{kw['volume']:,}",
                kw["competition"].upper(),
                f"{kw['relevance']:.0%}",
                priority_label(kw),
            ])
        print()
        print(tabulate(table,
                       headers=["#", "Keyword", "Est. Volume", "Competition", "Relevance", "Priority"],
                       tablefmt="simple"))
    else:
        print(f"\n  {'#':<4} {'Keyword':<35} {'Volume':>10} {'Comp':>8} {'Rel':>6} {'Priority':<10}")
        print(f"  {'-'*4} {'-'*35} {'-'*10} {'-'*8} {'-'*6} {'-'*10}")
        for i, kw in enumerate(sorted_kw, 1):
            print(f"  {i:<4} {kw['keyword']:<35} {kw['volume']:>10,} {kw['competition']:>8} {kw['relevance']:>5.0%} {priority_label(kw):<10}")

    # Summary
    high_priority = [kw for kw in sorted_kw if priority_label(kw) == "HIGH"]
    print(f"\n--- RECOMMENDATIONS ---")
    print(f"  High-priority keywords to target: {len(high_priority)}")
    if high_priority:
        print(f"  Top picks: {', '.join(kw['keyword'] for kw in high_priority[:5])}")
    print(f"  Total addressable search volume: {sum(kw['volume'] for kw in sorted_kw):,}")
    print()


def priority_label(kw: dict) -> str:
    if kw["relevance"] >= 0.90 and kw["competition"] != "high":
        return "HIGH"
    elif kw["relevance"] >= 0.85:
        return "MEDIUM"
    else:
        return "LOW"


def main():
    parser = argparse.ArgumentParser(description="Amazon Keyword Researcher")
    parser.add_argument("--seed", default="insulated water bottle", help="Seed keyword")
    args = parser.parse_args()
    research_keywords(args.seed)


if __name__ == "__main__":
    main()
