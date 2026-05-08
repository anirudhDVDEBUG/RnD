"""
Data Center Deal Analyst — evaluates infrastructure deals for environmental,
political, and business risk.
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Recommendation(str, Enum):
    PROCEED = "Proceed"
    PROCEED_WITH_MITIGATIONS = "Proceed with mitigations"
    SEEK_ALTERNATIVES = "Seek alternatives"


@dataclass
class DealParameters:
    party_a: str
    party_b: str
    facility_name: str
    location: str
    capacity_mw: float
    gpu_count: Optional[int] = None
    power_source: str = "grid"
    duration_years: int = 1
    cost_per_mw_month: Optional[float] = None
    dedicated: bool = False


@dataclass
class EnvironmentalRisk:
    level: RiskLevel
    power_generation_method: str
    emissions_profile: str
    permit_status: str
    compliance_history: list[str] = field(default_factory=list)
    health_impacts: list[str] = field(default_factory=list)
    water_usage_notes: str = ""

    def summary(self) -> str:
        lines = [
            f"  Power generation: {self.power_generation_method}",
            f"  Emissions profile: {self.emissions_profile}",
            f"  Permit status: {self.permit_status}",
        ]
        if self.compliance_history:
            lines.append("  Compliance issues:")
            for item in self.compliance_history:
                lines.append(f"    - {item}")
        if self.health_impacts:
            lines.append("  Health impacts:")
            for item in self.health_impacts:
                lines.append(f"    - {item}")
        if self.water_usage_notes:
            lines.append(f"  Water usage: {self.water_usage_notes}")
        return "\n".join(lines)


@dataclass
class RegulatoryRisk:
    level: RiskLevel
    applicable_regulations: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    exemptions: list[str] = field(default_factory=list)
    pending_enforcement: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = []
        if self.applicable_regulations:
            lines.append("  Applicable regulations:")
            for r in self.applicable_regulations:
                lines.append(f"    - {r}")
        if self.violations:
            lines.append("  Violations:")
            for v in self.violations:
                lines.append(f"    - {v}")
        if self.exemptions:
            lines.append("  Exemptions / temporary permits:")
            for e in self.exemptions:
                lines.append(f"    - {e}")
        if self.pending_enforcement:
            lines.append("  Pending enforcement:")
            for p in self.pending_enforcement:
                lines.append(f"    - {p}")
        return "\n".join(lines)


@dataclass
class PoliticalRisk:
    level: RiskLevel
    public_sentiment: str = ""
    media_coverage: str = ""
    controversial_associations: list[str] = field(default_factory=list)
    brand_impact: str = ""

    def summary(self) -> str:
        lines = [
            f"  Public sentiment: {self.public_sentiment}",
            f"  Media coverage: {self.media_coverage}",
        ]
        if self.controversial_associations:
            lines.append("  Controversial associations:")
            for a in self.controversial_associations:
                lines.append(f"    - {a}")
        if self.brand_impact:
            lines.append(f"  Brand impact: {self.brand_impact}")
        return "\n".join(lines)


@dataclass
class BusinessTradeoffs:
    compute_constraint_severity: str
    alternative_options: list[str] = field(default_factory=list)
    cost_advantage: str = ""
    timeline_advantage: str = ""
    lockin_risk: str = ""

    def summary(self) -> str:
        lines = [
            f"  Compute constraint: {self.compute_constraint_severity}",
            f"  Cost advantage: {self.cost_advantage}",
            f"  Timeline advantage: {self.timeline_advantage}",
            f"  Lock-in risk: {self.lockin_risk}",
        ]
        if self.alternative_options:
            lines.append("  Alternatives:")
            for a in self.alternative_options:
                lines.append(f"    - {a}")
        return "\n".join(lines)


@dataclass
class DealAnalysis:
    deal: DealParameters
    environmental: EnvironmentalRisk
    regulatory: RegulatoryRisk
    political: PoliticalRisk
    business: BusinessTradeoffs
    recommendation: Recommendation
    recommendation_rationale: str

    def overall_risk(self) -> RiskLevel:
        levels = [self.environmental.level, self.regulatory.level, self.political.level]
        if RiskLevel.CRITICAL in levels:
            return RiskLevel.CRITICAL
        if RiskLevel.HIGH in levels:
            return RiskLevel.HIGH
        if RiskLevel.MEDIUM in levels:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def render_report(self) -> str:
        d = self.deal
        gpu_line = f", {d.gpu_count:,} GPUs" if d.gpu_count else ""
        sections = [
            "=" * 70,
            "DATA CENTER DEAL ANALYSIS REPORT",
            "=" * 70,
            "",
            "## Deal Summary",
            f"  Parties: {d.party_a} leasing capacity from {d.party_b}",
            f"  Facility: {d.facility_name}, {d.location}",
            f"  Capacity: {d.capacity_mw} MW{gpu_line}",
            f"  Power source: {d.power_source}",
            f"  Duration: {d.duration_years} year(s)",
            f"  Capacity type: {'Dedicated' if d.dedicated else 'Shared'}",
            "",
            f"## Environmental Risk  [{self.environmental.level.value}]",
            self.environmental.summary(),
            "",
            f"## Regulatory / Compliance Status  [{self.regulatory.level.value}]",
            self.regulatory.summary(),
            "",
            f"## Political / Reputational Risk  [{self.political.level.value}]",
            self.political.summary(),
            "",
            "## Business Trade-offs",
            self.business.summary(),
            "",
            f"## Overall Risk: {self.overall_risk().value}",
            "",
            f"## Recommendation: {self.recommendation.value}",
            f"  {self.recommendation_rationale}",
            "",
            "=" * 70,
        ]
        return "\n".join(sections)


def analyze_deal(deal: DealParameters, context: dict) -> DealAnalysis:
    """Analyze a deal given parameters and contextual intelligence."""

    env = EnvironmentalRisk(
        level=RiskLevel(context.get("env_risk_level", "MEDIUM")),
        power_generation_method=context.get("power_gen", "Unknown"),
        emissions_profile=context.get("emissions", "Unknown"),
        permit_status=context.get("permit_status", "Unknown"),
        compliance_history=context.get("compliance_issues", []),
        health_impacts=context.get("health_impacts", []),
        water_usage_notes=context.get("water_notes", ""),
    )

    reg = RegulatoryRisk(
        level=RiskLevel(context.get("reg_risk_level", "MEDIUM")),
        applicable_regulations=context.get("regulations", []),
        violations=context.get("violations", []),
        exemptions=context.get("exemptions", []),
        pending_enforcement=context.get("pending_enforcement", []),
    )

    pol = PoliticalRisk(
        level=RiskLevel(context.get("pol_risk_level", "MEDIUM")),
        public_sentiment=context.get("public_sentiment", "Unknown"),
        media_coverage=context.get("media_coverage", "Unknown"),
        controversial_associations=context.get("controversial_associations", []),
        brand_impact=context.get("brand_impact", ""),
    )

    biz = BusinessTradeoffs(
        compute_constraint_severity=context.get("constraint_severity", "Unknown"),
        alternative_options=context.get("alternatives", []),
        cost_advantage=context.get("cost_advantage", ""),
        timeline_advantage=context.get("timeline_advantage", ""),
        lockin_risk=context.get("lockin_risk", ""),
    )

    # Determine recommendation based on risk levels
    overall = max(
        [env.level, reg.level, pol.level],
        key=lambda x: list(RiskLevel).index(x),
    )
    if overall == RiskLevel.CRITICAL:
        rec = Recommendation.SEEK_ALTERNATIVES
        rationale = context.get(
            "rationale",
            "Critical-level risks in one or more categories make this deal inadvisable without fundamental changes.",
        )
    elif overall == RiskLevel.HIGH:
        rec = Recommendation.PROCEED_WITH_MITIGATIONS
        rationale = context.get(
            "rationale",
            "High risks exist but may be manageable with contractual protections and public transparency.",
        )
    else:
        rec = Recommendation.PROCEED
        rationale = context.get("rationale", "Risks are within acceptable bounds.")

    return DealAnalysis(
        deal=deal,
        environmental=env,
        regulatory=reg,
        political=pol,
        business=biz,
        recommendation=rec,
        recommendation_rationale=rationale,
    )


def to_json(analysis: DealAnalysis) -> str:
    """Serialize analysis to JSON for programmatic consumption."""
    data = {
        "deal": asdict(analysis.deal),
        "environmental_risk": {
            "level": analysis.environmental.level.value,
            "power_generation": analysis.environmental.power_generation_method,
            "emissions": analysis.environmental.emissions_profile,
            "permit_status": analysis.environmental.permit_status,
            "compliance_issues": analysis.environmental.compliance_history,
            "health_impacts": analysis.environmental.health_impacts,
        },
        "regulatory_risk": {
            "level": analysis.regulatory.level.value,
            "regulations": analysis.regulatory.applicable_regulations,
            "violations": analysis.regulatory.violations,
            "exemptions": analysis.regulatory.exemptions,
        },
        "political_risk": {
            "level": analysis.political.level.value,
            "sentiment": analysis.political.public_sentiment,
            "controversial_associations": analysis.political.controversial_associations,
        },
        "business_tradeoffs": {
            "constraint_severity": analysis.business.compute_constraint_severity,
            "alternatives": analysis.business.alternative_options,
            "lockin_risk": analysis.business.lockin_risk,
        },
        "overall_risk": analysis.overall_risk().value,
        "recommendation": analysis.recommendation.value,
        "rationale": analysis.recommendation_rationale,
    }
    return json.dumps(data, indent=2)
