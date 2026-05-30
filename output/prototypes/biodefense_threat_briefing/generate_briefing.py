#!/usr/bin/env python3
"""
Biodefense Threat Briefing Generator

Generates structured, actionable biodefense and pandemic preparedness
threat briefings from threat data (real or mock).
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# Mock threat intelligence data
# ---------------------------------------------------------------------------

MOCK_THREATS = {
    "natural": [
        {
            "pathogen": "H5N1 Avian Influenza",
            "confidence": "high",
            "trend": "increasing",
            "detail": "Sustained mammal-to-mammal transmission confirmed in dairy cattle across 12 US states. Sporadic human cases linked to occupational exposure.",
            "source": "CDC FluView, WHO Disease Outbreak News",
        },
        {
            "pathogen": "Mpox (Clade Ib)",
            "confidence": "moderate",
            "trend": "stable",
            "detail": "Clade Ib continues circulating in Central/East Africa with limited exportation events. Vaccine uptake remains low in affected regions.",
            "source": "WHO AFRO Situation Reports",
        },
        {
            "pathogen": "Candida auris",
            "confidence": "high",
            "trend": "increasing",
            "detail": "Pan-resistant isolates detected in 3 additional US healthcare facilities. Antifungal pipeline insufficient for current resistance trajectory.",
            "source": "CDC AR Threats Report, hospital sentinel surveillance",
        },
    ],
    "engineered": [
        {
            "threat": "Dual-use gain-of-function research oversight gaps",
            "confidence": "moderate",
            "detail": "Updated US P3CO framework narrows oversight scope. Several international labs conducting enhanced pathogen research outside multilateral review.",
            "source": "NSABB meeting minutes, open-source policy tracking",
        },
        {
            "threat": "AI-assisted protein design risk",
            "confidence": "low",
            "detail": "Frontier protein-design models increasingly capable of de novo toxin design. No confirmed misuse incidents; guardrails vary across platforms.",
            "source": "Biosecurity academic literature, pre-print servers",
        },
    ],
    "surveillance": {
        "strengths": [
            "Wastewater genomic surveillance operational in 45 states",
            "Global GISAID submissions averaging 8,000 sequences/week",
            "Metagenomic sequencing pilots running at 6 international airports",
        ],
        "gaps": [
            "Sub-Saharan Africa sequencing capacity <2% of samples",
            "No integrated animal-human-environment dashboard (One Health)",
            "Syndromic surveillance latency averages 7-14 days in rural regions",
        ],
    },
    "preparedness": [
        {
            "domain": "Medical countermeasures",
            "status": "Partial",
            "gaps": "mRNA platform ready for known threats; no broad-spectrum antiviral stockpile for novel agents",
            "priority": "High",
        },
        {
            "domain": "Laboratory capacity",
            "status": "Adequate",
            "gaps": "BSL-4 surge capacity limited to 3 facilities; reagent supply chain single-sourced",
            "priority": "Medium",
        },
        {
            "domain": "Supply chain resilience",
            "status": "At Risk",
            "gaps": "PPE domestic manufacturing covers ~40% of surge demand; critical API sourced >80% overseas",
            "priority": "Critical",
        },
        {
            "domain": "Workforce readiness",
            "status": "Degraded",
            "gaps": "Epidemiology workforce down 15% since 2023; contact-tracing networks largely disbanded",
            "priority": "High",
        },
        {
            "domain": "Communications / public trust",
            "status": "Weak",
            "gaps": "Public confidence in health agencies at historic lows; misinformation response capacity fragmented",
            "priority": "High",
        },
    ],
}


def generate_briefing(
    scope: str = "National (United States)",
    audience: str = "Senior public health leadership",
    focus: str = "all",
    classification: str = "UNCLASSIFIED",
) -> str:
    """Generate a structured biodefense threat briefing."""

    today = datetime.now().strftime("%Y-%m-%d")

    # --- Executive Summary ---
    exec_summary = (
        "The biological threat landscape shows elevated risk driven by sustained "
        "H5N1 zoonotic transmission, expanding antifungal resistance, and persistent "
        "gaps in global biosurveillance coverage. Preparedness posture is mixed: "
        "platform vaccine technology provides rapid-response capability for known "
        "pathogens, but supply chain fragility, workforce attrition, and eroded public "
        "trust present systemic vulnerabilities requiring urgent attention."
    )

    # --- Natural threats section ---
    natural_lines = []
    for t in MOCK_THREATS["natural"]:
        natural_lines.append(
            f"- **{t['pathogen']}** (trend: {t['trend']}, confidence: {t['confidence']}): "
            f"{t['detail']}  \n  *Source: {t['source']}*"
        )

    # --- Engineered threats section ---
    engineered_lines = []
    for t in MOCK_THREATS["engineered"]:
        engineered_lines.append(
            f"- **{t['threat']}** (confidence: {t['confidence']}): "
            f"{t['detail']}  \n  *Source: {t['source']}*"
        )

    # --- Surveillance ---
    surv_strengths = "\n".join(f"- {s}" for s in MOCK_THREATS["surveillance"]["strengths"])
    surv_gaps = "\n".join(f"- {g}" for g in MOCK_THREATS["surveillance"]["gaps"])

    # --- Preparedness table ---
    prep_rows = []
    for p in MOCK_THREATS["preparedness"]:
        prep_rows.append(
            f"| {p['domain']} | {p['status']} | {p['gaps']} | **{p['priority']}** |"
        )
    prep_table = "\n".join(prep_rows)

    # --- Recommended actions ---
    actions = """1. **Immediate (0-30 days)**
   - Activate H5N1 pre-pandemic vaccine manufacturing lot release
   - Issue clinical guidance update for C. auris pan-resistant isolate management
   - Convene interagency tabletop exercise on zoonotic influenza scenario

2. **Short-term (30-90 days)**
   - Fund wastewater surveillance expansion to remaining 5 states
   - Launch One Health data integration pilot linking CDC, USDA, and EPA feeds
   - Re-establish regional contact-tracing rapid-deployment teams

3. **Long-term (6-18 months)**
   - Invest in domestic API manufacturing capacity for critical antimicrobials
   - Develop broad-spectrum antiviral stockpile strategy
   - Rebuild public health communications infrastructure with misinformation rapid-response units
   - Support international BSL-3/4 capacity building in underserved regions"""

    briefing = f"""# Biodefense Threat Briefing

**Date:** {today}
**Classification:** {classification}
**Scope:** {scope}
**Prepared for:** {audience}

---

## Executive Summary

{exec_summary}

---

## Current Threat Landscape

### Natural Biological Threats

{chr(10).join(natural_lines)}

### Deliberate / Engineered Threats

{chr(10).join(engineered_lines)}

---

## Surveillance & Detection Posture

### Active Capabilities
{surv_strengths}

### Gaps & Blind Spots
{surv_gaps}

---

## Preparedness Assessment

| Domain | Status | Key Gaps | Priority |
|--------|--------|----------|----------|
{prep_table}

---

## Recommended Actions

{actions}

---

## Intelligence Sources & Confidence

| Assessment | Confidence | Source Types |
|-----------|-----------|-------------|
| H5N1 zoonotic trajectory | High | CDC lab-confirmed cases, USDA herd testing |
| C. auris resistance expansion | High | Hospital sentinel surveillance, CDC AR network |
| Mpox Clade Ib exportation risk | Moderate | WHO sit-reps, limited genomic data from affected regions |
| Dual-use research oversight gaps | Moderate | Policy documents, open-source reporting |
| AI-enabled bioweapon risk | Low | Academic literature, no confirmed incidents |

---

*This briefing was generated for planning and preparedness purposes. Assessments reflect
open-source intelligence and publicly available data as of {today}. For operational
decision-making, validate against classified and agency-specific sources.*

*Reference: [Strengthening societal resilience with Rosalind Biodefense](https://openai.com/index/strengthening-societal-resilience-with-rosalind-biodefense)*
"""

    return briefing


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a structured biodefense threat briefing"
    )
    parser.add_argument(
        "--scope",
        default="National (United States)",
        help="Geographic scope (default: National (United States))",
    )
    parser.add_argument(
        "--audience",
        default="Senior public health leadership",
        help="Target audience (default: Senior public health leadership)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )

    args = parser.parse_args()

    briefing_md = generate_briefing(scope=args.scope, audience=args.audience)

    if args.format == "json":
        output = json.dumps(
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "scope": args.scope,
                "audience": args.audience,
                "threats": MOCK_THREATS,
                "briefing_markdown": briefing_md,
            },
            indent=2,
        )
    else:
        output = briefing_md

    if args.output:
        Path(args.output).write_text(output)
        print(f"Briefing written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
