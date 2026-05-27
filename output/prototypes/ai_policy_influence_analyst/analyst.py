"""AI Policy Influence Analyst — standalone demo implementation."""

import json
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from mock_data import (
    POLICY_DOCUMENTS,
    STRATEGY_DEFINITIONS,
    TERM_VENDOR_MAP,
    VENDOR_PROFILES,
    PolicyDocument,
    VendorProfile,
)


@dataclass
class InfluenceMapping:
    principle: str
    vendor: str
    technical_reality: str
    confidence: float


@dataclass
class AnalysisResult:
    document_title: str
    institution: str
    primary_beneficiary: str
    strategy_type: str
    strategy_secondary: str
    influence_mappings: List[InfluenceMapping]
    channels: List[str]
    effectiveness_score: float
    assessment: str


class InfluenceAnalyzer:
    """Analyzes policy documents for vendor influence patterns."""

    def __init__(self):
        self.vendor_profiles = {v.name: v for v in VENDOR_PROFILES}
        self.term_map = TERM_VENDOR_MAP

    def analyze(self, doc: PolicyDocument) -> AnalysisResult:
        """Run full influence analysis on a policy document."""
        # Step 1: Map vendor interests in each excerpt
        mappings = self._map_vendor_interests(doc)

        # Step 2: Identify primary beneficiary
        vendor_counts: Dict[str, int] = {}
        for m in mappings:
            vendor_counts[m.vendor] = vendor_counts.get(m.vendor, 0) + 1
        primary = max(vendor_counts, key=vendor_counts.get) if vendor_counts else "Unknown"

        # Step 3: Classify strategy
        strategy, secondary = self._classify_strategy(doc, primary)

        # Step 4: Identify channels
        channels = self._trace_channels(doc, primary)

        # Step 5: Score effectiveness
        score = self._score_effectiveness(doc, primary, mappings)

        # Step 6: Generate assessment
        assessment = self._generate_assessment(doc, primary, strategy, score)

        return AnalysisResult(
            document_title=doc.title,
            institution=doc.institution,
            primary_beneficiary=primary,
            strategy_type=strategy,
            strategy_secondary=secondary,
            influence_mappings=mappings,
            channels=channels,
            effectiveness_score=score,
            assessment=assessment,
        )

    def _map_vendor_interests(self, doc: PolicyDocument) -> List[InfluenceMapping]:
        mappings = []
        for excerpt in doc.excerpts:
            lower = excerpt.lower()
            for term, vendor in self.term_map.items():
                if term in lower:
                    profile = self.vendor_profiles[vendor]
                    # Find matching constraint
                    tech_reality = next(
                        (c for c in profile.key_constraints if any(w in c for w in term.split())),
                        profile.architecture,
                    )
                    mappings.append(
                        InfluenceMapping(
                            principle=excerpt[:80] + ("..." if len(excerpt) > 80 else ""),
                            vendor=vendor,
                            technical_reality=tech_reality,
                            confidence=0.85 if vendor in str(doc.known_advisors) else 0.6,
                        )
                    )
                    break  # one match per excerpt
        return mappings

    def _classify_strategy(self, doc: PolicyDocument, primary: str) -> Tuple[str, str]:
        institution = doc.institution.lower()
        if "vatican" in institution or "pope" in institution:
            return "Institutional Blessing", "Limitation Laundering"
        elif "parliament" in institution or "congress" in institution:
            return "Standards Setting", "Safety Capture"
        elif "nist" in institution or "iso" in institution:
            return "Standards Setting", "Safety Capture"
        else:
            return "Safety Capture", "Limitation Laundering"

    def _trace_channels(self, doc: PolicyDocument, primary: str) -> List[str]:
        channels = []
        if doc.known_advisors:
            channels.append(f"Direct advisory: {', '.join(doc.known_advisors)}")
        profile = self.vendor_profiles.get(primary)
        if profile:
            channels.extend(profile.lobbying_channels[:2])
        return channels

    def _score_effectiveness(
        self, doc: PolicyDocument, primary: str, mappings: List[InfluenceMapping]
    ) -> float:
        base = 5.0
        # More mappings = more influence embedded
        base += min(len(mappings) * 0.8, 3.0)
        # Known advisors = confirmed channel
        if any(primary.lower() in a.lower() for a in doc.known_advisors):
            base += 1.5
        # Institutional prestige multiplier
        institution = doc.institution.lower()
        if "vatican" in institution or "pope" in institution:
            base += 1.0  # unprecedented institutional authority
        return min(base, 10.0)

    def _generate_assessment(
        self, doc: PolicyDocument, primary: str, strategy: str, score: float
    ) -> str:
        profile = self.vendor_profiles.get(primary)
        arch = profile.architecture if profile else "unknown architecture"

        if score >= 9.0:
            impact = "This represents an unprecedented level of vendor influence on institutional policy."
        elif score >= 7.0:
            impact = "This demonstrates significant vendor capture of the regulatory framework."
        else:
            impact = "This shows moderate vendor influence embedded in policy language."

        return (
            f"{primary}'s {arch} is reflected in the core principles of {doc.title}. "
            f"The {strategy} strategy operates by elevating technical constraints to "
            f"universal ethical imperatives. {impact}"
        )


def print_analysis(result: AnalysisResult) -> None:
    """Pretty-print an analysis result."""
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  POLICY INFLUENCE ANALYSIS")
    print(f"{sep}\n")
    print(f"  Document:    {result.document_title}")
    print(f"  Institution: {result.institution}")
    print(f"  Beneficiary: {result.primary_beneficiary}")
    print(f"  Strategy:    {result.strategy_type}")
    print(f"               ({STRATEGY_DEFINITIONS[result.strategy_type]})")
    print(f"  Secondary:   {result.strategy_secondary}")
    print(f"  Effectiveness: {result.effectiveness_score:.1f}/10")
    print()

    print("  INFLUENCE CHANNELS:")
    for ch in result.channels:
        print(f"    - {ch}")
    print()

    print("  VENDOR INTEREST MAPPINGS:")
    print(f"  {'Principle':<45} {'Vendor':<15} {'Technical Reality'}")
    print(f"  {'-'*45} {'-'*15} {'-'*30}")
    for m in result.influence_mappings:
        principle = m.principle[:43] + ".." if len(m.principle) > 45 else m.principle
        tech = m.technical_reality[:28] + ".." if len(m.technical_reality) > 30 else m.technical_reality
        print(f"  {principle:<45} {m.vendor:<15} {tech}")
    print()

    print("  ASSESSMENT:")
    for line in textwrap.wrap(result.assessment, width=66):
        print(f"    {line}")
    print(f"\n{sep}\n")


def main():
    print("\n" + "+" * 70)
    print("+  AI POLICY INFLUENCE ANALYST — Demo Analysis")
    print("+  Analyzing", len(POLICY_DOCUMENTS), "policy documents for vendor influence")
    print("+" * 70)

    analyzer = InfluenceAnalyzer()

    for doc in POLICY_DOCUMENTS:
        result = analyzer.analyze(doc)
        print_analysis(result)

    # Summary
    print("=" * 70)
    print("  SUMMARY: STRATEGY TAXONOMY")
    print("=" * 70)
    for strategy, definition in STRATEGY_DEFINITIONS.items():
        print(f"\n  {strategy}:")
        print(f"    {definition}")
    print()
    print("  Source: Corey Quinn via Simon Willison (2026-05-26)")
    print("  \"Getting the literal Pope to canonize your product's specific")
    print("  technical limitations as a spiritual treatise is the single")
    print("  greatest act of vendor lobbying I have ever seen.\"")
    print()


if __name__ == "__main__":
    main()
