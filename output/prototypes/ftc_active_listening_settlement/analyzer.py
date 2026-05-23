#!/usr/bin/env python3
"""FTC 'Active Listening' Settlement Analyzer.

Loads structured case data and outputs a formatted analysis report.
No external dependencies -- uses Python standard library only.
"""

import argparse
import json
import os
import sys


def load_case_data():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case_data.json")
    with open(data_path) as f:
        return json.load(f)


def fmt_usd(amount):
    return f"${amount:,}"


def print_header(data):
    print()
    print("=" * 55)
    print('  FTC "Active Listening" Settlement Analysis')
    print("=" * 55)
    print()
    print(f"CASE: {data['case_name']} ({data['date']})")
    print(f"STATUTE: {data['statute']}")
    print()


def print_deception(data):
    print("--- What They Claimed ---")
    for claim in data["claims_made"]:
        print(f"  * {claim}")
    print()
    print("--- What Actually Happened ---")
    for fact in data["reality"]:
        print(f"  * {fact}")
    print()


def print_penalties(data):
    print("--- Penalties ---")
    for party in data["parties"]["respondents"]:
        name = party["name"]
        penalty = fmt_usd(party["penalty_usd"])
        print(f"  {name:<30s} {penalty:>12s}")
    print(f"  {'TOTAL':<30s} {fmt_usd(data['parties']['total_penalty_usd']):>12s}")
    print()


def print_lessons(data):
    print("--- Compliance Lessons ---")
    for i, lesson in enumerate(data["compliance_lessons"], 1):
        print(f"  {i}. {lesson}")
    print()


def print_timeline(data):
    print("--- Timeline ---")
    for entry in data["timeline"]:
        print(f"  {entry['date']:<14s} {entry['event']}")
    print()


def print_references(data):
    print("--- References ---")
    for ref in data["references"]:
        print(f"  {ref['title']}")
        print(f"    {ref['url']}")
    print()


SECTION_MAP = {
    "deception": print_deception,
    "penalties": print_penalties,
    "lessons": print_lessons,
    "timeline": print_timeline,
    "references": print_references,
}


def print_full_report(data):
    print_header(data)
    print_deception(data)
    print_penalties(data)
    print_lessons(data)
    print_timeline(data)
    print_references(data)
    print("Report complete.")
    print()


def output_json(data, section=None):
    if section:
        key_map = {
            "deception": lambda d: {"claims_made": d["claims_made"], "reality": d["reality"]},
            "penalties": lambda d: d["parties"],
            "lessons": lambda d: {"compliance_lessons": d["compliance_lessons"]},
            "timeline": lambda d: {"timeline": d["timeline"]},
            "references": lambda d: {"references": d["references"]},
        }
        output = key_map.get(section, lambda d: d)(data)
    else:
        output = data
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description='FTC "Active Listening" Settlement Analyzer')
    parser.add_argument(
        "--section",
        choices=list(SECTION_MAP.keys()),
        help="Show only a specific section of the analysis",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    data = load_case_data()

    if args.format == "json":
        output_json(data, args.section)
        return

    if args.section:
        print_header(data)
        SECTION_MAP[args.section](data)
    else:
        print_full_report(data)


if __name__ == "__main__":
    main()
