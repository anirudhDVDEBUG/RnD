#!/usr/bin/env python3
"""
Demo: Analyze the xAI/Anthropic Colossus data center deal.

Uses mock data derived from public reporting (Simon Willison's analysis,
May 2026) to demonstrate the deal analyst without requiring API keys.
"""

from analyzer import DealParameters, analyze_deal, to_json


def build_xai_anthropic_deal() -> tuple[DealParameters, dict]:
    """Mock data for the xAI Colossus / Anthropic deal."""
    deal = DealParameters(
        party_a="Anthropic",
        party_b="xAI (Colossus facility)",
        facility_name="Colossus Data Center",
        location="Memphis, Tennessee",
        capacity_mw=150,
        gpu_count=100_000,
        power_source="Natural gas turbines (bypass generators) + grid",
        duration_years=2,
        dedicated=False,
    )

    context = {
        # Environmental
        "env_risk_level": "CRITICAL",
        "power_gen": "Gas-fired turbine generators classified as 'temporary', bypassing standard emission controls",
        "emissions": "High NOx and particulate matter; turbines lack SCR catalytic controls required for permanent installations",
        "permit_status": "Operated under temporary 'construction' permits; reclassification to permanent source pending",
        "compliance_issues": [
            "Facility operated for months under temporary permits designed for short-term construction",
            "Shelby County Health Department issued violation notices for exceeding emission thresholds",
            "Tennessee DPHE documented elevated NOx levels in surrounding neighborhoods",
        ],
        "health_impacts": [
            "Residents in South Memphis reported increased respiratory symptoms",
            "Local hospital ER visits for asthma up 18% in zip codes adjacent to facility (per community health data)",
            "Environmental justice concerns — facility located in predominantly low-income area",
        ],
        "water_notes": "High water consumption for cooling; draws from Memphis Sand Aquifer, a sole-source aquifer",
        # Regulatory
        "reg_risk_level": "HIGH",
        "regulations": [
            "Clean Air Act — New Source Review (NSR)",
            "Tennessee Air Quality Act",
            "Shelby County Health Department air permits",
            "EPA environmental justice screening (EJScreen)",
        ],
        "violations": [
            "Operating generators without required permanent air quality permits",
            "Exceeding temporary permit emission limits on multiple occasions",
        ],
        "exemptions": [
            "'Temporary source' classification allowed bypass of New Source Review — legality contested",
        ],
        "pending_enforcement": [
            "Shelby County reviewing permit reclassification",
            "Community groups filed formal complaints with Tennessee DPHE",
        ],
        # Political
        "pol_risk_level": "HIGH",
        "public_sentiment": "Strong local opposition; community protests and city council hearings",
        "media_coverage": "Extensive investigative coverage (Reuters, local outlets, tech press); Simon Willison analysis widely shared",
        "controversial_associations": [
            "xAI owned by Elon Musk — polarizing figure in tech and politics",
            "Facility rushed to operational status; critics allege regulatory shortcuts",
            "Deal links Anthropic brand to facility with documented environmental violations",
        ],
        "brand_impact": "Risk of 'safety-washing' criticism — Anthropic's responsible-AI brand vs. partnering with a facility that harmed a vulnerable community",
        # Business
        "constraint_severity": "HIGH — GPU scarcity for frontier model training is acute; 6-12 month lead time for new capacity",
        "alternatives": [
            "AWS custom silicon (Trainium) — available but lower performance for some workloads",
            "Google Cloud TPU v5p — limited allocation, long waitlist",
            "CoreWeave — expanding but capacity committed through 2027",
            "Build own facility — 18-24 month timeline, $2B+ capex",
        ],
        "cost_advantage": "Colossus offers ~30% lower $/GPU-hour vs. hyperscaler on-demand pricing",
        "timeline_advantage": "Capacity available immediately vs. 6-18 months for alternatives",
        "lockin_risk": "MEDIUM — 2-year term with exit clauses, but migration cost is high for active training runs",
        # Overall
        "rationale": (
            "The facility's documented air quality violations and environmental justice "
            "concerns in South Memphis create critical reputational and regulatory risk. "
            "While compute scarcity is real, Anthropic's brand as a safety-focused AI lab "
            "is directly undermined by association with a facility that harmed a vulnerable "
            "community. Recommend seeking alternative capacity or requiring xAI to achieve "
            "full regulatory compliance (permanent permits with SCR controls) before proceeding."
        ),
    }
    return deal, context


def build_clean_deal() -> tuple[DealParameters, dict]:
    """Comparison: a hypothetical clean-energy deal."""
    deal = DealParameters(
        party_a="Anthropic",
        party_b="CleanCompute Co.",
        facility_name="Wind River Campus",
        location="Cheyenne, Wyoming",
        capacity_mw=80,
        gpu_count=40_000,
        power_source="Wind + solar PPA with battery backup",
        duration_years=3,
        dedicated=True,
    )

    context = {
        "env_risk_level": "LOW",
        "power_gen": "100% renewable PPA (wind + solar) with 4h battery storage",
        "emissions": "Near-zero operational emissions; embodied carbon from construction only",
        "permit_status": "All permits current; no violations on record",
        "compliance_issues": [],
        "health_impacts": [],
        "water_notes": "Air-cooled design; minimal water usage",
        "reg_risk_level": "LOW",
        "regulations": ["Wyoming DEQ air permits", "Federal NEPA review (completed)"],
        "violations": [],
        "exemptions": [],
        "pending_enforcement": [],
        "pol_risk_level": "LOW",
        "public_sentiment": "Positive; local job creation and tax revenue welcomed",
        "media_coverage": "Favorable coverage in regional press",
        "controversial_associations": [],
        "brand_impact": "Reinforces responsible-AI positioning and climate commitments",
        "constraint_severity": "HIGH — same GPU scarcity applies",
        "alternatives": [
            "Same alternatives as above, plus this option",
        ],
        "cost_advantage": "~10% premium over Colossus, but within budget",
        "timeline_advantage": "Available in 4 months (facility under construction, nearly complete)",
        "lockin_risk": "LOW — dedicated capacity with flexible scaling terms",
        "rationale": "Low risk across all categories. Slight cost premium and 4-month wait are acceptable given alignment with brand values and zero regulatory exposure.",
    }
    return deal, context


def main():
    print()
    print("=" * 70)
    print("  DATA CENTER DEAL ANALYST — DEMO")
    print("  Analyzing two deals for comparison")
    print("=" * 70)

    # Deal 1: xAI Colossus
    print("\n\n>>> DEAL 1: xAI Colossus (Memphis, TN)\n")
    deal1, ctx1 = build_xai_anthropic_deal()
    analysis1 = analyze_deal(deal1, ctx1)
    print(analysis1.render_report())

    # Deal 2: Clean alternative
    print("\n\n>>> DEAL 2: CleanCompute (Cheyenne, WY) — for comparison\n")
    deal2, ctx2 = build_clean_deal()
    analysis2 = analyze_deal(deal2, ctx2)
    print(analysis2.render_report())

    # Side-by-side summary
    print("\n")
    print("=" * 70)
    print("  SIDE-BY-SIDE COMPARISON")
    print("=" * 70)
    print(f"  {'':30s} {'Colossus':>16s}  {'Wind River':>16s}")
    print(f"  {'':30s} {'─' * 16}  {'─' * 16}")
    print(f"  {'Environmental Risk':30s} {analysis1.environmental.level.value:>16s}  {analysis2.environmental.level.value:>16s}")
    print(f"  {'Regulatory Risk':30s} {analysis1.regulatory.level.value:>16s}  {analysis2.regulatory.level.value:>16s}")
    print(f"  {'Political Risk':30s} {analysis1.political.level.value:>16s}  {analysis2.political.level.value:>16s}")
    print(f"  {'Overall Risk':30s} {analysis1.overall_risk().value:>16s}  {analysis2.overall_risk().value:>16s}")
    print(f"  {'Recommendation':30s} {analysis1.recommendation.value:>16s}  {analysis2.recommendation.value:>16s}")
    print()

    # JSON output
    print("\n--- JSON output (Deal 1) for programmatic use ---\n")
    print(to_json(analysis1))
    print()


if __name__ == "__main__":
    main()
