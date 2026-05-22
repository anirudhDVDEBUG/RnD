#!/usr/bin/env python3
"""Query the TrustGraph JSONL ledger and display aggregate trust scores."""

import json
import sys
import os
from collections import defaultdict
from pathlib import Path


def load_ledger(path: str) -> list[dict]:
    """Load JSONL ledger, skipping malformed lines."""
    records = []
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"  [warn] skipping malformed line {lineno}", file=sys.stderr)
    return records


def aggregate(records: list[dict]) -> dict[str, dict]:
    """Return per-domain aggregated stats."""
    buckets: dict[str, list] = defaultdict(list)
    tools_seen: dict[str, set] = defaultdict(set)
    for r in records:
        domain = r.get("domain", "unknown")
        rating = r.get("rating", {})
        score = rating.get("score") if isinstance(rating, dict) else None
        if score is not None:
            buckets[domain].append(score)
        tools_seen[domain].add(r.get("tool", "?"))
    result = {}
    for domain, scores in buckets.items():
        result[domain] = {
            "avg": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores),
            "count": len(scores),
            "tools": sorted(tools_seen[domain]),
        }
    return result


def print_report(agg: dict[str, dict]):
    """Pretty-print the trust report sorted by average score."""
    if not agg:
        print("No scored domains found.")
        return
    print(f"\n{'Domain':<35} {'Avg':>5} {'Min':>4} {'Max':>4} {'#':>3}  Tools")
    print("-" * 80)
    for domain, stats in sorted(agg.items(), key=lambda x: x[1]["avg"]):
        tools_str = ", ".join(stats["tools"])
        print(
            f"{domain:<35} {stats['avg']:5.1f} {stats['min']:4} {stats['max']:4} "
            f"{stats['count']:3}  {tools_str}"
        )


def main():
    ledger_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        os.environ.get("TRUSTGRAPH_LEDGER", "~/.claude/trustgraph_ledger.jsonl")
    )
    if not Path(ledger_path).exists():
        print(f"Ledger not found: {ledger_path}")
        sys.exit(1)

    records = load_ledger(ledger_path)
    print(f"Loaded {len(records)} records from {ledger_path}")
    agg = aggregate(records)
    print_report(agg)


if __name__ == "__main__":
    main()
