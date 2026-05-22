#!/usr/bin/env python3
"""
TrustGraph Resource Rater — Demo with mock data.
Generates a synthetic JSONL ledger and prints the trust report.
No API keys required.
"""

import json
import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# Deterministic for reproducible demo output
random.seed(42)

MOCK_ENTRIES = [
    # (domain, tool, score_range, reason)
    ("docs.python.org", "WebFetch", (8, 10), "Official Python documentation, highly authoritative"),
    ("docs.python.org", "WebSearch", (8, 10), "Well-maintained official docs"),
    ("stackoverflow.com", "WebSearch", (6, 9), "Community answers vary in quality but generally reliable"),
    ("stackoverflow.com", "WebFetch", (5, 8), "Answers can be outdated; check dates"),
    ("github.com", "WebFetch", (7, 9), "Major open-source platform, repos vary in quality"),
    ("github.com", "Bash", (7, 9), "GitHub API via curl, well-documented"),
    ("arxiv.org", "WebFetch", (8, 10), "Peer-adjacent research preprints"),
    ("medium.com", "WebSearch", (3, 7), "Blog platform, quality varies widely by author"),
    ("medium.com", "WebFetch", (3, 6), "Some posts are marketing disguised as tutorials"),
    ("random-seo-blog.xyz", "WebSearch", (1, 3), "Low-quality SEO content farm"),
    ("random-seo-blog.xyz", "WebFetch", (1, 4), "Thin content, keyword-stuffed articles"),
    ("news.ycombinator.com", "WebSearch", (6, 8), "Tech community aggregator, links to varied sources"),
    ("npmjs.com", "WebFetch", (6, 8), "Official npm registry, package quality varies"),
    ("pypi.org", "WebFetch", (7, 9), "Official Python package index"),
    ("sketchy-download.io", "Bash", (1, 2), "Unknown download site, potential security risk"),
    ("developer.mozilla.org", "WebFetch", (9, 10), "MDN Web Docs, gold standard for web references"),
    ("developer.mozilla.org", "WebSearch", (9, 10), "Authoritative web documentation"),
    ("api.example-mcp.com", "mcp__example", (5, 7), "Third-party MCP server, moderate trust"),
]


def generate_ledger(output_path: str, num_entries: int = 50) -> list[dict]:
    """Generate mock ledger entries."""
    records = []
    base_time = datetime.utcnow() - timedelta(days=7)

    for i in range(num_entries):
        entry = random.choice(MOCK_ENTRIES)
        domain, tool, (lo, hi), reason = entry
        score = random.randint(lo, hi)
        ts = base_time + timedelta(
            hours=random.randint(0, 168),
            minutes=random.randint(0, 59),
        )
        record = {
            "ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tool": tool,
            "domain": domain,
            "rating": {
                "domain": domain,
                "score": score,
                "reason": reason,
            },
        }
        records.append(record)

    # Sort by timestamp
    records.sort(key=lambda r: r["ts"])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    return records


def print_banner():
    print("=" * 60)
    print("  TrustGraph Resource Rater — Demo")
    print("=" * 60)
    print()


def print_sample_entries(records: list[dict], n: int = 5):
    print(f"Sample ledger entries ({n} of {len(records)}):")
    print("-" * 60)
    for r in records[:n]:
        rating = r["rating"]
        print(
            f"  [{r['ts']}] {r['tool']:<12} {r['domain']:<30} "
            f"score={rating['score']}"
        )
    print(f"  ... and {len(records) - n} more entries")
    print()


def main():
    ledger_path = os.path.join(os.path.dirname(__file__), "demo_ledger.jsonl")

    print_banner()

    # Step 1: Generate mock data
    print("1. Generating mock trust ledger...")
    records = generate_ledger(ledger_path, num_entries=50)
    print(f"   Written {len(records)} entries to {ledger_path}")
    print()

    # Step 2: Show sample entries
    print("2. Sample raw entries:")
    print_sample_entries(records)

    # Step 3: Run the query tool
    print("3. Aggregate trust report (sorted by score, lowest first):")
    print("-" * 60)

    # Import and run the query module directly
    sys.path.insert(0, os.path.dirname(__file__))
    import query_ledger
    agg_records = query_ledger.load_ledger(ledger_path)
    agg = query_ledger.aggregate(agg_records)
    query_ledger.print_report(agg)
    print()

    # Step 4: Highlight key findings
    print()
    print("4. Key findings:")
    print("-" * 60)
    sorted_domains = sorted(agg.items(), key=lambda x: x[1]["avg"])
    worst = sorted_domains[:2]
    best = sorted_domains[-2:]
    print("   LEAST TRUSTED:")
    for domain, stats in worst:
        print(f"     {domain}: avg {stats['avg']:.1f}/10 ({stats['count']} ratings)")
    print("   MOST TRUSTED:")
    for domain, stats in best:
        print(f"     {domain}: avg {stats['avg']:.1f}/10 ({stats['count']} ratings)")
    print()
    print("In production, these scores accumulate silently via PostToolUse")
    print("hooks — every WebFetch, WebSearch, curl, and MCP call is rated.")
    print()
    print("=" * 60)
    print("  Demo complete. See HOW_TO_USE.md to install the live skill.")
    print("=" * 60)


if __name__ == "__main__":
    main()
