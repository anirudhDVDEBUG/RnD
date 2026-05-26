#!/usr/bin/env python3
"""
CI ship-gate checker.

Reads eval-results.json and exits non-zero if any command fails its
quality threshold. Designed to run as a GitHub Actions step.
"""

import argparse
import json
import sys
from pathlib import Path


PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
WARN = "\033[93mWARN\033[0m"


def print_report(results: list[dict]) -> bool:
    """Pretty-print results and return True if all gates pass."""
    all_passed = True

    print("\n" + "=" * 64)
    print("  SHIP-GATE QUALITY REPORT")
    print("=" * 64)

    for r in results:
        cmd = r["command"]
        score = r["overall_score"]
        threshold = r["overall_pass_threshold"]
        passed = r["passed"]
        status = PASS if passed else FAIL

        print(f"\n  {status}  {cmd}  (score: {score:.1%}  threshold: {threshold:.0%})")
        print(f"  {'─' * 56}")

        for c in r["criteria"]:
            c_status = PASS if c["passed"] else FAIL
            bar_len = int(c["score"] * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"    {c_status}  {c['criterion']:<28s} [{bar}] {c['score']:.0%}")

        if not passed:
            all_passed = False

    print("\n" + "=" * 64)
    overall = PASS if all_passed else FAIL
    print(f"  OVERALL: {overall}")
    print("=" * 64 + "\n")

    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Check ship-gate results")
    parser.add_argument("--results", default="eval-results.json", help="Path to eval results JSON")
    args = parser.parse_args()

    results_path = Path(args.results)
    if not results_path.exists():
        print(f"ERROR: Results file not found: {results_path}", file=sys.stderr)
        sys.exit(1)

    with open(results_path) as f:
        results = json.load(f)

    if not results:
        print(f"{WARN}  No eval results found — nothing to gate.")
        sys.exit(0)

    all_passed = print_report(results)

    if not all_passed:
        print("Ship-gate FAILED. Fix failing criteria before merging.")
        sys.exit(1)
    else:
        print("Ship-gate PASSED. Safe to merge.")
        sys.exit(0)


if __name__ == "__main__":
    main()
