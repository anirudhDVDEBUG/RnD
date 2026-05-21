#!/usr/bin/env python3
"""Standalone analyzer for the Anthropic x xAI COLOSSUS cloud compute deal.

All data sourced from SpaceX S-1 filing (SEC Archives, May 2026).
No API keys or external services required.
"""

DEAL = {
    "parties": ("xAI Corp", "Anthropic PBC"),
    "agreement_type": "Cloud Services Agreements",
    "facilities": ["COLOSSUS", "COLOSSUS II"],
    "monthly_fee_usd": 1_250_000_000,
    "term_months": 36,
    "term_end": "May 2029",
    "ramp_months": ["May 2026", "June 2026"],
    "termination_notice_days": 90,
    "signing_date": "May 2026",
    "source_filing": "SpaceX S-1 (SEC EDGAR)",
    "source_url": "https://simonwillison.net/2026/May/20/spacex-s1/#atom-everything",
}


def fmt_usd(amount: int) -> str:
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.0f}M"
    return f"${amount:,}"


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_summary() -> None:
    print_section("Anthropic x xAI COLOSSUS Deal -- Quick Analysis")
    total = DEAL["monthly_fee_usd"] * DEAL["term_months"]
    rows = [
        ("Monthly fee", fmt_usd(DEAL["monthly_fee_usd"])),
        ("Term", f"{DEAL['term_months']} months (through {DEAL['term_end']})"),
        ("Total value", f"~{fmt_usd(total)}"),
        ("Facilities", " + ".join(DEAL["facilities"])),
        ("Termination", f"{DEAL['termination_notice_days']} days notice by either party"),
        ("Signing", DEAL["signing_date"]),
    ]
    for label, value in rows:
        print(f"  {label:<20s} {value}")


def print_financial_breakdown() -> None:
    print_section("Financial Breakdown")
    monthly = DEAL["monthly_fee_usd"]
    print(f"  Per month:          {fmt_usd(monthly)}")
    print(f"  Per quarter:        {fmt_usd(monthly * 3)}")
    print(f"  Per year:           {fmt_usd(monthly * 12)}")
    print(f"  Full term (36 mo):  {fmt_usd(monthly * 36)}")
    print()
    print("  For comparison:")
    print(f"    - Annual run-rate ({fmt_usd(monthly * 12)}) exceeds the")
    print("      entire annual revenue of most cloud providers' AI divisions.")
    print(f"    - Monthly fee ({fmt_usd(monthly)}) is roughly 2x what most")
    print("      frontier labs spend on compute per month with traditional")
    print("      cloud providers.")


def print_strategic_analysis() -> None:
    print_section("Strategic Analysis")
    points = [
        (
            "Compute diversification",
            "Anthropic supplements its AWS/GCP partnerships with xAI capacity,\n"
            "    signaling that no single cloud provider can meet frontier lab demand.",
        ),
        (
            "xAI as cloud vendor",
            "xAI monetizes spare COLOSSUS GPU capacity by selling to a direct\n"
            "    competitor -- a novel dynamic in the AI industry.",
        ),
        (
            "Flexible commitment",
            "90-day termination clause makes this more like a capacity reservation\n"
            "    than a locked-in contract, reducing risk for both parties.",
        ),
        (
            "COLOSSUS II dual use",
            "xAI trains Grok models on COLOSSUS II while leasing capacity to\n"
            "    Anthropic simultaneously, implying massive total cluster size.",
        ),
        (
            "Market signal",
            "At $1.25B/month, this is the largest publicly disclosed cloud\n"
            "    compute contract in AI history. It resets expectations for\n"
            "    infrastructure spend at frontier labs.",
        ),
    ]
    for i, (title, detail) in enumerate(points, 1):
        print(f"\n  {i}. {title}")
        print(f"    {detail}")


def print_source() -> None:
    print_section("Source")
    print(f"  Filing:  {DEAL['source_filing']}")
    print(f"  Via:     {DEAL['source_url']}")
    print()


def main() -> None:
    print_summary()
    print_financial_breakdown()
    print_strategic_analysis()
    print_source()


if __name__ == "__main__":
    main()
