#!/usr/bin/env python3
"""
GCC Market Intelligence — Demo CLI

Generates a market-entry briefing for a given GCC country and vertical.
Uses embedded reference data (no API keys needed).
"""

import argparse
import json
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Embedded reference data
# ---------------------------------------------------------------------------

COUNTRIES = {
    "saudi": {
        "name": "Saudi Arabia (KSA)",
        "gdp_approx": "$1.1T",
        "population": "36M",
        "vision": "Vision 2030",
        "regulatory_body": "MCIT / SDAIA / NCA",
        "procurement_portal": "Etimad (etimad.sa)",
        "data_residency": "PDPL — personal data of Saudi residents must be processed locally or under adequacy agreements",
        "labor_rules": "Saudization (Nitaqat) quotas apply; tech firms may need Saudi employees or a local partner",
        "entity_options": ["SAGIA 100% foreign-owned LLC", "Regional HQ program (mandatory for gov contracts by 2024+)"],
        "key_events": ["LEAP (Riyadh, Feb)", "Future Investment Initiative (Oct)"],
        "swf": {"name": "PIF", "aum": "$930B+", "focus": "NEOM, entertainment, tech, giga-projects"},
        "top_verticals": ["cybersecurity", "fintech", "healthtech", "edtech", "smart-city", "defense-tech"],
        "incentives": [
            "Saudi Venture Capital Company (SVC) — co-invests with VCs",
            "Monsha'at — SME grants, incubation, acceleration",
            "MCIT Cloud First policy — gov cloud migration spending",
        ],
    },
    "uae": {
        "name": "UAE",
        "gdp_approx": "$500B",
        "population": "10M",
        "vision": "We the UAE 2031",
        "regulatory_body": "TRA / Smart Dubai / ADDA",
        "procurement_portal": "TEJARI (tejari.com) / Abu Dhabi procurement portal",
        "data_residency": "Sector-specific; DIFC and ADGM have own data-protection frameworks",
        "labor_rules": "Emiratisation targets in private sector (2% annual increase). Free zones exempt from some quotas",
        "entity_options": ["DIFC (financial services)", "ADGM (fintech, digital)", "Mainland LLC", "DMCC / DAFZA free zones"],
        "key_events": ["GITEX Global (Dubai, Oct)", "Abu Dhabi Finance Week (Nov)"],
        "swf": {"name": "ADIA / Mubadala", "aum": "$990B+ / $300B+", "focus": "ADIA: global diversified; Mubadala: tech-forward, semiconductors to AI"},
        "top_verticals": ["fintech", "logistics-tech", "proptech", "AI/ML", "smart-city"],
        "incentives": [
            "Hub71 (Abu Dhabi) — housing, cloud credits, office space",
            "Dubai Future Accelerators — gov-backed pilots",
            "DIFC Innovation Hub — fintech sandbox",
        ],
    },
    "qatar": {
        "name": "Qatar",
        "gdp_approx": "$235B",
        "population": "3M",
        "vision": "National Vision 2030",
        "regulatory_body": "MCIT / Qatar Financial Centre (QFC)",
        "procurement_portal": "Daman portal",
        "data_residency": "Data Protection Law (Law No. 13 of 2016) — cross-border transfers need approval",
        "labor_rules": "Qatarisation targets in energy and finance sectors",
        "entity_options": ["QFC entity (100% foreign ownership)", "Mainland with local sponsor"],
        "key_events": ["Qatar Economic Forum (Doha, Jun)", "Web Summit Qatar (Feb)"],
        "swf": {"name": "QIA", "aum": "$500B+", "focus": "Strategic sectors, LNG-adjacent tech, real estate"},
        "top_verticals": ["LNG-tech", "sports-tech", "smart-city", "fintech"],
        "incentives": [
            "Qatar Development Bank — SME financing and startup support",
            "QFC tax benefits — 0% corporate tax for QFC entities",
        ],
    },
    "bahrain": {
        "name": "Bahrain",
        "gdp_approx": "$44B",
        "population": "1.5M",
        "vision": "Economic Vision 2030",
        "regulatory_body": "CBB (Central Bank) / EDB",
        "procurement_portal": "Tender Board (tenderboard.gov.bh)",
        "data_residency": "PDPL enacted 2019 — relatively flexible cross-border rules",
        "labor_rules": "Bahrainisation quotas; Tamkeen subsidies offset costs",
        "entity_options": ["Bahrain FinTech Bay", "Bahrain Investment Gateway (mainland)"],
        "key_events": ["Bahrain FinTech Forward (various)"],
        "swf": {"name": "Mumtalakat", "aum": "$18B+", "focus": "Diversified industrial and financial holdings"},
        "top_verticals": ["fintech", "insurtech", "Islamic finance tech"],
        "incentives": [
            "FinTech Bay / Tamkeen — workforce subsidies and training grants",
            "CBB regulatory sandbox — test financial products live",
        ],
    },
    "kuwait": {
        "name": "Kuwait",
        "gdp_approx": "$185B",
        "population": "4.3M",
        "vision": "New Kuwait 2035",
        "regulatory_body": "CAIT / CMA",
        "procurement_portal": "Central Agency for Public Tenders",
        "data_residency": "No comprehensive data-protection law yet; sector guidelines apply",
        "labor_rules": "Kuwaitisation quotas — strict in gov and oil sectors",
        "entity_options": ["KDIPA foreign investment license", "Local sponsor arrangement"],
        "key_events": ["Kuwait Tech Conference"],
        "swf": {"name": "KIA", "aum": "$900B+", "focus": "Conservative allocation, sovereign reserves"},
        "top_verticals": ["oil-gas-tech", "fintech", "e-government"],
        "incentives": [
            "KDIPA incentives — tax holidays for approved projects",
            "National Fund for SME Development",
        ],
    },
    "oman": {
        "name": "Oman",
        "gdp_approx": "$105B",
        "population": "5M",
        "vision": "Vision 2040",
        "regulatory_body": "ITA (Information Technology Authority)",
        "procurement_portal": "Tender Board (tender.gov.om)",
        "data_residency": "Evolving framework; e-transactions law applies",
        "labor_rules": "Omanisation quotas — significant in private sector",
        "entity_options": ["SAOC/SAOG company", "Free zone entity (Duqm, Sohar)"],
        "key_events": ["Comex Oman (Muscat)"],
        "swf": {"name": "OIA", "aum": "$17B+", "focus": "Diversification away from oil, logistics, tourism"},
        "top_verticals": ["logistics-tech", "tourism-tech", "mining-tech", "renewable energy"],
        "incentives": [
            "Oman Technology Fund — startup investment",
            "Duqm SEZ — tax-free zone with port access",
        ],
    },
}

FAMILY_OFFICES = [
    {"name": "Olayan Group", "hq": "Saudi", "sectors": ["industrial", "consumer", "tech"]},
    {"name": "Al Futtaim Group", "hq": "UAE", "sectors": ["retail", "real estate", "automotive"]},
    {"name": "Majid Al Futtaim", "hq": "UAE", "sectors": ["retail", "entertainment", "proptech"]},
    {"name": "Chalhoub Group", "hq": "UAE", "sectors": ["luxury", "retail", "e-commerce"]},
    {"name": "Al Ghurair Group", "hq": "UAE", "sectors": ["food", "construction", "energy"]},
    {"name": "Kanoo Group", "hq": "Bahrain/Saudi", "sectors": ["logistics", "industrial", "travel"]},
    {"name": "Al Habtoor Group", "hq": "UAE", "sectors": ["hospitality", "automotive", "real estate"]},
    {"name": "Dallah Albaraka", "hq": "Saudi", "sectors": ["healthcare", "finance", "real estate"]},
]

SOFT_LANDING_STEPS = [
    {
        "step": 1,
        "title": "Validate demand",
        "actions": [
            "Attend sector events (LEAP, GITEX, Qatar Economic Forum)",
            "Run 10-15 discovery calls with target buyers",
            "Map competitive landscape — who already has traction locally?",
        ],
    },
    {
        "step": 2,
        "title": "Find a local partner",
        "actions": [
            "Identify distributors, systems integrators, or sponsors",
            "Mandatory for many government tenders",
            "Look for partners already selling to your ICP",
        ],
    },
    {
        "step": 3,
        "title": "Set up legal entity",
        "actions": [
            "Choose jurisdiction: mainland vs. free zone",
            "Typical timeline: 2-6 weeks",
            "Consider regional HQ requirements (KSA mandate)",
        ],
    },
    {
        "step": 4,
        "title": "Hire local team",
        "actions": [
            "Country manager with government relationships",
            "Arabic-speaking BD — critical for B2G",
            "Ensure compliance with localization quotas",
        ],
    },
    {
        "step": 5,
        "title": "Land a pilot customer",
        "actions": [
            "Target semi-government entities as lighthouse accounts",
            "Use as reference case for wider rollout",
            "Aim for a signed POC within 3-6 months",
        ],
    },
    {
        "step": 6,
        "title": "Localize product",
        "actions": [
            "RTL Arabic UI",
            "Local payment methods (SADAD, Apple Pay MENA)",
            "Arabic support docs and onboarding",
        ],
    },
]


def generate_briefing(country_key: str, vertical: Optional[str] = None) -> dict:
    """Generate a market-entry briefing for a GCC country."""
    country = COUNTRIES.get(country_key)
    if not country:
        return {"error": f"Unknown country: {country_key}. Choose from: {', '.join(COUNTRIES.keys())}"}

    # Filter relevant family offices
    relevant_families = [
        f for f in FAMILY_OFFICES
        if country_key in f["hq"].lower() or (vertical and any(vertical.lower() in s for s in f["sectors"]))
    ]

    # Match verticals
    vertical_match = None
    if vertical:
        vl = vertical.lower()
        if vl in [v.lower() for v in country["top_verticals"]]:
            vertical_match = "strong"
        elif any(vl in v.lower() for v in country["top_verticals"]):
            vertical_match = "partial"
        else:
            vertical_match = "weak"

    briefing = {
        "country": country["name"],
        "macro": {
            "gdp": country["gdp_approx"],
            "population": country["population"],
            "national_vision": country["vision"],
        },
        "regulatory": {
            "authority": country["regulatory_body"],
            "procurement_portal": country["procurement_portal"],
            "data_residency": country["data_residency"],
            "labor_localization": country["labor_rules"],
            "entity_options": country["entity_options"],
        },
        "sovereign_wealth_fund": country["swf"],
        "top_verticals": country["top_verticals"],
        "vertical_fit": vertical_match,
        "relevant_family_offices": relevant_families[:4],
        "incentive_programs": country["incentives"],
        "key_events": country["key_events"],
        "soft_landing_playbook": SOFT_LANDING_STEPS,
    }
    return briefing


def print_briefing(briefing: dict) -> None:
    """Pretty-print a market-entry briefing."""
    if "error" in briefing:
        print(f"ERROR: {briefing['error']}")
        sys.exit(1)

    sep = "=" * 64
    print(sep)
    print(f"  GCC MARKET-ENTRY BRIEFING: {briefing['country']}")
    print(sep)

    # Macro
    m = briefing["macro"]
    print(f"\n{'MACRO OVERVIEW':^64}")
    print(f"  GDP (approx): {m['gdp']}")
    print(f"  Population:   {m['population']}")
    print(f"  Vision:       {m['national_vision']}")

    # SWF
    swf = briefing["sovereign_wealth_fund"]
    print(f"\n{'SOVEREIGN WEALTH FUND':^64}")
    print(f"  {swf['name']}  |  AUM: {swf['aum']}")
    print(f"  Focus: {swf['focus']}")

    # Regulatory
    r = briefing["regulatory"]
    print(f"\n{'REGULATORY & COMPLIANCE':^64}")
    print(f"  Authority:        {r['authority']}")
    print(f"  Procurement:      {r['procurement_portal']}")
    print(f"  Data residency:   {r['data_residency']}")
    print(f"  Labor rules:      {r['labor_localization']}")
    print(f"  Entity options:")
    for opt in r["entity_options"]:
        print(f"    - {opt}")

    # Verticals
    print(f"\n{'TOP VERTICALS':^64}")
    for v in briefing["top_verticals"]:
        print(f"    - {v}")
    if briefing["vertical_fit"]:
        label = {"strong": "STRONG FIT", "partial": "PARTIAL FIT", "weak": "WEAK FIT — consider pivoting GTM"}
        print(f"  >> Your vertical fit: {label[briefing['vertical_fit']]}")

    # Family offices
    if briefing["relevant_family_offices"]:
        print(f"\n{'RELEVANT FAMILY OFFICES':^64}")
        for fo in briefing["relevant_family_offices"]:
            print(f"    - {fo['name']} ({fo['hq']}) — {', '.join(fo['sectors'])}")

    # Incentives
    print(f"\n{'INCENTIVE PROGRAMS':^64}")
    for inc in briefing["incentive_programs"]:
        print(f"    - {inc}")

    # Events
    print(f"\n{'KEY EVENTS':^64}")
    for ev in briefing["key_events"]:
        print(f"    - {ev}")

    # Soft-landing
    print(f"\n{'SOFT-LANDING PLAYBOOK':^64}")
    for step in briefing["soft_landing_playbook"]:
        print(f"\n  Step {step['step']}: {step['title']}")
        for a in step["actions"]:
            print(f"      - {a}")

    print(f"\n{sep}")
    print("  Generated by gcc-market-intelligence skill (mock data)")
    print(sep)


def compare_countries(keys: list[str], vertical: Optional[str] = None) -> None:
    """Print a side-by-side comparison table for multiple countries."""
    countries = [COUNTRIES[k] for k in keys if k in COUNTRIES]
    if len(countries) < 2:
        print("Need at least 2 valid countries to compare.")
        return

    sep = "=" * 80
    print(sep)
    print(f"  GCC COUNTRY COMPARISON")
    if vertical:
        print(f"  Vertical: {vertical}")
    print(sep)

    headers = [c["name"] for c in countries]
    col_w = 24

    def row(label, getter):
        vals = [getter(c)[:col_w] for c in countries]
        print(f"  {label:<20}" + "".join(f"  {v:<{col_w}}" for v in vals))

    print(f"\n  {'':20}" + "".join(f"  {h:<{col_w}}" for h in headers))
    print("  " + "-" * (20 + (col_w + 2) * len(countries)))
    row("GDP", lambda c: c["gdp_approx"])
    row("Population", lambda c: c["population"])
    row("Vision", lambda c: c["vision"])
    row("SWF", lambda c: c["swf"]["name"])
    row("SWF AUM", lambda c: c["swf"]["aum"])

    if vertical:
        vl = vertical.lower()
        def fit(c):
            if vl in [v.lower() for v in c["top_verticals"]]:
                return "STRONG"
            elif any(vl in v.lower() for v in c["top_verticals"]):
                return "PARTIAL"
            return "WEAK"
        row(f"Fit: {vertical}", fit)

    print(f"\n{sep}")


def main():
    parser = argparse.ArgumentParser(
        description="GCC Market Intelligence — generate market-entry briefings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python gcc_intel.py --country saudi --vertical cybersecurity
              python gcc_intel.py --country uae --vertical fintech
              python gcc_intel.py --compare saudi uae qatar --vertical fintech
              python gcc_intel.py --all
        """),
    )
    parser.add_argument("--country", choices=list(COUNTRIES.keys()), help="Target GCC country")
    parser.add_argument("--vertical", help="Your product vertical (e.g., fintech, cybersecurity)")
    parser.add_argument("--compare", nargs="+", choices=list(COUNTRIES.keys()), help="Compare 2+ countries")
    parser.add_argument("--all", action="store_true", help="Brief all 6 GCC countries")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.compare:
        compare_countries(args.compare, args.vertical)
        return

    if args.all:
        for key in COUNTRIES:
            briefing = generate_briefing(key, args.vertical)
            if args.json:
                print(json.dumps(briefing, indent=2))
            else:
                print_briefing(briefing)
                print()
        return

    if not args.country:
        # Default demo: Saudi + cybersecurity
        args.country = "saudi"
        args.vertical = args.vertical or "cybersecurity"

    briefing = generate_briefing(args.country, args.vertical)
    if args.json:
        print(json.dumps(briefing, indent=2))
    else:
        print_briefing(briefing)


if __name__ == "__main__":
    main()
