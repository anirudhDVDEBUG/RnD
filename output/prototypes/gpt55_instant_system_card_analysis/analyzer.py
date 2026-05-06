#!/usr/bin/env python3
"""
GPT-5.5 Instant System Card Analyzer

Parses, analyzes, and summarizes the GPT-5.5 Instant System Card data,
producing structured reports on safety evaluations, benchmarks, risk
assessments, and deployment mitigations.
"""

import json
import sys
from pathlib import Path

# Risk level display config
RISK_COLORS = {
    "low": "\033[92m",       # green
    "medium": "\033[93m",    # yellow
    "high": "\033[91m",      # red
    "critical": "\033[95m",  # magenta
}
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def load_system_card(path: str = "system_card_data.json") -> dict:
    """Load system card data from JSON file."""
    p = Path(path)
    if not p.exists():
        print(f"Error: {path} not found. Run from the project directory.")
        sys.exit(1)
    with open(p) as f:
        return json.load(f)


def print_header(title: str) -> None:
    width = 60
    print(f"\n{BOLD}{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}{RESET}")


def print_section(title: str) -> None:
    print(f"\n{BOLD}--- {title} ---{RESET}")


def analyze_overview(data: dict) -> None:
    print_header("GPT-5.5 INSTANT SYSTEM CARD ANALYSIS")
    ov = data["overview"]
    print(f"\n{BOLD}Model:{RESET} {data['model']}")
    print(f"{BOLD}Publisher:{RESET} {data['publisher']}")
    print(f"{BOLD}Release:{RESET} {data['release_date']}")
    print(f"{BOLD}Context Window:{RESET} {ov['context_window']:,} tokens")
    print(f"{BOLD}Training Cutoff:{RESET} {ov['training_data_cutoff']}")
    print(f"{BOLD}Modalities:{RESET} {', '.join(ov['modalities'])}")
    print(f"\n{DIM}{ov['description']}{RESET}")


def analyze_preparedness(data: dict) -> dict[str, str]:
    """Analyze Preparedness Framework ratings. Returns category->rating map."""
    print_header("PREPAREDNESS FRAMEWORK RISK ASSESSMENT")
    pf = data["preparedness_framework"]
    print(f"\n{DIM}{pf['description']}{RESET}\n")

    ratings = {}
    for cat_key, cat in pf["evaluation_categories"].items():
        rating = cat["risk_rating"]
        ratings[cat_key] = rating
        color = RISK_COLORS.get(rating, "")
        print(f"  {BOLD}{cat['full_name']:<45}{RESET} {color}[{rating.upper()}]{RESET}")
        print(f"    {DIM}{cat['details']}{RESET}")
        for finding in cat["key_findings"]:
            print(f"    - {finding}")
        print()

    return ratings


def analyze_safety_benchmarks(data: dict) -> list[dict]:
    """Analyze safety benchmarks and return comparison data."""
    print_header("SAFETY BENCHMARK RESULTS")
    results = []
    for key, bench in data["safety_benchmarks"].items():
        comp = bench.get("comparison", {})
        gpt4o = comp.get("gpt4o")
        gpt5 = comp.get("gpt5")

        # Determine if higher or lower is better
        lower_better = "toxicity" in key.lower()
        if lower_better:
            vs_4o = "better" if bench["score"] < gpt4o else "worse"
            vs_5 = "better" if bench["score"] < gpt5 else "worse"
        else:
            vs_4o = "better" if bench["score"] > gpt4o else "worse"
            vs_5 = "better" if bench["score"] > gpt5 else "worse"

        result = {
            "name": bench["name"],
            "score": bench["score"],
            "metric": bench["metric"],
            "vs_gpt4o": vs_4o,
            "vs_gpt5": vs_5,
        }
        results.append(result)

        arrow_4o = "\033[92m^" if vs_4o == "better" else "\033[91mv"
        arrow_5 = "\033[92m^" if vs_5 == "better" else "\033[91mv"

        print(f"\n  {BOLD}{bench['name']}{RESET} ({bench['metric']})")
        print(f"    GPT-5.5 Instant: {BOLD}{bench['score']:.3f}{RESET}")
        if gpt4o is not None:
            print(f"    vs GPT-4o:        {gpt4o:.3f}  {arrow_4o} {vs_4o}{RESET}")
        if gpt5 is not None:
            print(f"    vs GPT-5:         {gpt5:.3f}  {arrow_5} {vs_5}{RESET}")
        print(f"    {DIM}{bench['notes']}{RESET}")

    return results


def analyze_capability_benchmarks(data: dict) -> None:
    print_header("CAPABILITY BENCHMARK RESULTS")
    print(f"\n  {'Benchmark':<20} {'GPT-5.5i':>10} {'GPT-4o':>10} {'GPT-5':>10} {'Gap vs 5':>10}")
    print(f"  {'-'*60}")
    for key, bench in data["capability_benchmarks"].items():
        comp = bench.get("comparison", {})
        gap = bench["score"] - comp.get("gpt5", 0)
        color = "\033[92m" if gap >= 0 else "\033[91m"
        print(
            f"  {bench['name']:<20} {bench['score']:>10.3f} "
            f"{comp.get('gpt4o', 0):>10.3f} {comp.get('gpt5', 0):>10.3f} "
            f"{color}{gap:>+10.3f}{RESET}"
        )


def analyze_red_teaming(data: dict) -> None:
    print_header("RED TEAMING SUMMARY")
    rt = data["red_teaming"]
    print(f"\n  Internal teams: {'Yes' if rt['internal_teams'] else 'No'}")
    print(f"  External red teamers: {'Yes' if rt['external_red_teamers'] else 'No'}")
    print_section("Categories Tested")
    for cat in rt["categories_tested"]:
        print(f"    - {cat}")
    print_section("Key Findings")
    for finding in rt["key_findings"]:
        print(f"    - {finding}")


def analyze_mitigations(data: dict) -> None:
    print_header("DEPLOYMENT MITIGATIONS")
    for key, desc in data["deployment_mitigations"].items():
        label = key.replace("_", " ").title()
        print(f"\n  {BOLD}{label}{RESET}")
        print(f"    {desc}")


def analyze_limitations(data: dict) -> None:
    print_header("KNOWN LIMITATIONS")
    for i, lim in enumerate(data["known_limitations"], 1):
        print(f"  {i}. {lim}")


def generate_executive_summary(data: dict, ratings: dict, safety_results: list) -> None:
    print_header("EXECUTIVE SUMMARY")

    # Overall risk
    all_low = all(r == "low" for r in ratings.values())
    if all_low:
        print(f"\n  {RISK_COLORS['low']}{BOLD}Overall Risk: LOW across all Preparedness categories{RESET}")
    else:
        max_risk = max(ratings.values(), key=lambda r: ["low", "medium", "high", "critical"].index(r))
        color = RISK_COLORS.get(max_risk, "")
        print(f"\n  {color}{BOLD}Highest Risk Level: {max_risk.upper()}{RESET}")

    # Safety vs capability tradeoff
    better_than_4o = sum(1 for r in safety_results if r["vs_gpt4o"] == "better")
    total = len(safety_results)
    print(f"\n  Safety vs GPT-4o: {better_than_4o}/{total} benchmarks improved")

    worse_than_5 = sum(1 for r in safety_results if r["vs_gpt5"] == "worse")
    print(f"  Safety vs GPT-5:  {total - worse_than_5}/{total} benchmarks on par or better")

    # Key takeaway
    print(f"\n  {BOLD}Key Takeaway:{RESET}")
    print(f"  GPT-5.5 Instant achieves near-GPT-5 safety properties at")
    print(f"  significantly lower latency and cost, making it suitable for")
    print(f"  high-throughput production deployments with strong safety")
    print(f"  requirements.")

    # Builder implications
    print(f"\n  {BOLD}Implications for Builders:{RESET}")
    print(f"  - Drop-in replacement for GPT-4o with better safety profile")
    print(f"  - Suitable for customer-facing applications (chatbots, agents)")
    print(f"  - Still requires application-level guardrails for sensitive domains")
    print(f"  - Cost-efficiency enables safety-first approaches at scale")


def main() -> None:
    card_path = sys.argv[1] if len(sys.argv) > 1 else "system_card_data.json"
    data = load_system_card(card_path)

    analyze_overview(data)
    ratings = analyze_preparedness(data)
    safety_results = analyze_safety_benchmarks(data)
    analyze_capability_benchmarks(data)
    analyze_red_teaming(data)
    analyze_mitigations(data)
    analyze_limitations(data)
    generate_executive_summary(data, ratings, safety_results)

    print(f"\n{DIM}Source: {data['source_url']}{RESET}")
    print(f"{DIM}Analysis generated from system card data.{RESET}\n")


if __name__ == "__main__":
    main()
