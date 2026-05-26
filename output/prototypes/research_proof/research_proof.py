#!/usr/bin/env python3
"""
Research Proof — Pressure-test research claims with falsifiable evidence plans,
adversarial checks, frozen verifiers, and proof ledgers.

This module implements the full pipeline:
  1. Claim extraction (atomic propositions)
  2. Falsifiable evidence plans
  3. Adversarial checks (bias, fallacy, confound detection)
  4. Frozen verifiers (pre-registered acceptance criteria)
  5. Proof ledger (structured markdown table)
  6. Summary verdict
"""

import json
import textwrap
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Confidence(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Verdict(Enum):
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    INCONCLUSIVE = "INCONCLUSIVE"


class VerifierStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PENDING = "PENDING"


@dataclass
class EvidencePlan:
    confirming_evidence: list[str]
    falsifying_evidence: list[str]
    assumptions: list[str]
    data_sources: list[str]


@dataclass
class AdversarialFinding:
    fallacies: list[str]
    confounders: list[str]
    biases: list[str]
    steel_man_counter: str
    confidence: Confidence
    confidence_justification: str


@dataclass
class FrozenVerifier:
    criteria: list[str]
    threshold: str
    locked_before_evidence: bool = True


@dataclass
class ClaimResult:
    id: int
    claim: str
    falsifiable: bool
    evidence_plan: EvidencePlan
    adversarial: AdversarialFinding
    verifier: FrozenVerifier
    verifier_status: VerifierStatus
    verdict: Verdict


def extract_claims(text: str) -> list[str]:
    """Extract atomic, testable claims from research text."""
    claims = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Strip leading markers like "- ", "* ", "1. "
        for prefix in ["- ", "* "]:
            if line.startswith(prefix):
                line = line[len(prefix):]
                break
        if line[0].isdigit() and ". " in line:
            line = line.split(". ", 1)[1]
        claims.append(line)
    return claims


def build_evidence_plan(claim: str, mock_data: Optional[dict] = None) -> EvidencePlan:
    """Generate a falsifiable evidence plan for a single claim."""
    if mock_data:
        return EvidencePlan(**mock_data)
    # Default heuristic plan
    return EvidencePlan(
        confirming_evidence=[
            f"Peer-reviewed study replicating: '{claim}'",
            "Independent dataset showing consistent effect size",
        ],
        falsifying_evidence=[
            f"Study failing to replicate under same conditions",
            "Counter-example with larger sample size",
            "Meta-analysis showing null aggregate effect",
        ],
        assumptions=[
            "Original methodology is sound",
            "No undisclosed conflicts of interest",
            "Sample is representative of target population",
        ],
        data_sources=[
            "PubMed / Semantic Scholar",
            "Pre-registered replication databases",
            "Raw data repositories (OSF, Zenodo)",
        ],
    )


def run_adversarial_checks(claim: str, mock_data: Optional[dict] = None) -> AdversarialFinding:
    """Apply adversarial reasoning to a claim."""
    if mock_data:
        conf = mock_data.pop("confidence", "MEDIUM")
        return AdversarialFinding(
            confidence=Confidence[conf],
            **mock_data,
        )
    return AdversarialFinding(
        fallacies=["Possible post-hoc reasoning"],
        confounders=["Uncontrolled environmental variables"],
        biases=["Potential survivorship bias in sample selection"],
        steel_man_counter=(
            "Even if the claim is directionally correct, the effect size "
            "may be overstated due to publication bias."
        ),
        confidence=Confidence.MEDIUM,
        confidence_justification=(
            "Claim is plausible but lacks independent replication."
        ),
    )


def freeze_verifiers(claim: str, mock_data: Optional[dict] = None) -> FrozenVerifier:
    """Define immutable verification criteria BEFORE examining evidence."""
    if mock_data:
        return FrozenVerifier(**mock_data)
    return FrozenVerifier(
        criteria=[
            "Effect size >= original study's reported Cohen's d",
            "p-value < 0.05 with Bonferroni correction",
            "At least 2 independent replications",
        ],
        threshold="All 3 criteria must be met for PASS",
        locked_before_evidence=True,
    )


def evaluate_claim(
    claim_id: int,
    claim: str,
    evidence_mock: Optional[dict] = None,
    adversarial_mock: Optional[dict] = None,
    verifier_mock: Optional[dict] = None,
    status_override: Optional[str] = None,
    verdict_override: Optional[str] = None,
) -> ClaimResult:
    """Run the full pipeline on a single claim."""
    plan = build_evidence_plan(claim, evidence_mock)
    adversarial = run_adversarial_checks(claim, adversarial_mock)
    verifier = freeze_verifiers(claim, verifier_mock)

    # Determine verifier status
    if status_override:
        v_status = VerifierStatus[status_override]
    else:
        v_status = VerifierStatus.PENDING

    # Determine verdict
    if verdict_override:
        verdict = Verdict[verdict_override]
    elif v_status == VerifierStatus.PASS:
        verdict = Verdict.SUPPORTED
    elif v_status == VerifierStatus.FAIL:
        verdict = Verdict.REFUTED
    else:
        verdict = Verdict.INCONCLUSIVE

    return ClaimResult(
        id=claim_id,
        claim=claim,
        falsifiable=True,
        evidence_plan=plan,
        adversarial=adversarial,
        verifier=verifier,
        verifier_status=v_status,
        verdict=verdict,
    )


def render_proof_ledger(results: list[ClaimResult]) -> str:
    """Render the proof ledger as a markdown table."""
    lines = [
        "| # | Claim | Falsifiable? | Evidence Plan | Adversarial Finding | Verifier Status | Verdict |",
        "|---|-------|-------------|---------------|---------------------|-----------------|---------|",
    ]
    for r in results:
        plan_summary = f"{len(r.evidence_plan.falsifying_evidence)} falsifiers defined"
        adv_summary = f"{len(r.adversarial.fallacies)} fallacies, {len(r.adversarial.confounders)} confounders"
        lines.append(
            f"| {r.id} | {r.claim[:60]}{'...' if len(r.claim)>60 else ''} "
            f"| {'Yes' if r.falsifiable else 'No'} "
            f"| {plan_summary} "
            f"| {adv_summary} "
            f"| {r.verifier_status.value} "
            f"| {r.verdict.value} |"
        )
    return "\n".join(lines)


def render_full_report(results: list[ClaimResult]) -> str:
    """Render the complete Research Proof report."""
    sections = []

    # Header
    sections.append("# Research Proof Report\n")

    # 1. Claim List
    sections.append("## 1. Claim List\n")
    for r in results:
        sections.append(f"  {r.id}. {r.claim}")
    sections.append("")

    # 2. Evidence Plans
    sections.append("## 2. Falsifiable Evidence Plans\n")
    for r in results:
        sections.append(f"### Claim {r.id}: {r.claim}\n")
        sections.append("**Confirming evidence needed:**")
        for e in r.evidence_plan.confirming_evidence:
            sections.append(f"  - {e}")
        sections.append("\n**Falsifying evidence (what would disprove this):**")
        for e in r.evidence_plan.falsifying_evidence:
            sections.append(f"  - {e}")
        sections.append("\n**Assumptions that must hold:**")
        for a in r.evidence_plan.assumptions:
            sections.append(f"  - {a}")
        sections.append("\n**Data sources:**")
        for d in r.evidence_plan.data_sources:
            sections.append(f"  - {d}")
        sections.append("")

    # 3. Adversarial Report
    sections.append("## 3. Adversarial Report\n")
    for r in results:
        sections.append(f"### Claim {r.id}: {r.claim}\n")
        sections.append(f"**Confidence: {r.adversarial.confidence.value}** — {r.adversarial.confidence_justification}\n")
        if r.adversarial.fallacies:
            sections.append("**Logical fallacies / reasoning gaps:**")
            for f in r.adversarial.fallacies:
                sections.append(f"  - {f}")
        if r.adversarial.confounders:
            sections.append("\n**Confounding variables:**")
            for c in r.adversarial.confounders:
                sections.append(f"  - {c}")
        if r.adversarial.biases:
            sections.append("\n**Biases detected:**")
            for b in r.adversarial.biases:
                sections.append(f"  - {b}")
        sections.append(f"\n**Steel-man counter-argument:** {r.adversarial.steel_man_counter}")
        sections.append("")

    # 4. Frozen Verifiers
    sections.append("## 4. Frozen Verifiers\n")
    for r in results:
        sections.append(f"### Claim {r.id}\n")
        sections.append(f"**Locked before evidence review:** {'Yes' if r.verifier.locked_before_evidence else 'No'}\n")
        sections.append("**Criteria:**")
        for c in r.verifier.criteria:
            sections.append(f"  - {c}")
        sections.append(f"\n**Threshold:** {r.verifier.threshold}")
        sections.append("")

    # 5. Proof Ledger
    sections.append("## 5. Proof Ledger\n")
    sections.append(render_proof_ledger(results))
    sections.append("")

    # 6. Summary Verdict
    total = len(results)
    passed = sum(1 for r in results if r.verdict == Verdict.SUPPORTED)
    failed = sum(1 for r in results if r.verdict == Verdict.REFUTED)
    inconclusive = sum(1 for r in results if r.verdict == Verdict.INCONCLUSIVE)

    sections.append("## 6. Summary Verdict\n")
    sections.append(f"- **Claims tested:** {total}")
    sections.append(f"- **Supported:** {passed}")
    sections.append(f"- **Refuted:** {failed}")
    sections.append(f"- **Inconclusive:** {inconclusive}")
    sections.append(f"- **Pass rate:** {passed}/{total} ({100*passed//total if total else 0}%)")

    # Overall confidence
    if passed > failed and inconclusive == 0:
        overall = "HIGH"
    elif passed >= failed:
        overall = "MEDIUM"
    else:
        overall = "LOW"
    sections.append(f"- **Overall confidence:** {overall}")

    vulnerabilities = set()
    for r in results:
        vulnerabilities.update(r.adversarial.fallacies)
        vulnerabilities.update(r.adversarial.biases)
    if vulnerabilities:
        sections.append("\n**Key vulnerabilities:**")
        for v in sorted(vulnerabilities):
            sections.append(f"  - {v}")

    sections.append("\n**Recommended next steps:**")
    if inconclusive > 0:
        sections.append(f"  - Gather additional data for {inconclusive} inconclusive claim(s)")
    if failed > 0:
        sections.append(f"  - Investigate {failed} refuted claim(s) for methodology issues")
    sections.append("  - Seek independent replication of supported claims")
    sections.append("  - Consider pre-registering follow-up studies")

    return "\n".join(sections)


def run_demo():
    """Run with mock research claims to demonstrate the pipeline."""

    print("=" * 70)
    print("  RESEARCH PROOF — Demo Run (mock data)")
    print("=" * 70)
    print()

    # Simulated research claims
    research_text = textwrap.dedent("""\
        LLM-generated code has 40% fewer bugs than human-written code
        Fine-tuned models outperform few-shot prompting on domain-specific tasks
        AI pair programming increases developer productivity by 55%
        Retrieval-augmented generation eliminates hallucinations in production
    """)

    claims = extract_claims(research_text)
    print(f"Extracted {len(claims)} claims from research input.\n")

    # Mock scenario data for realistic demo output
    mock_scenarios = [
        {
            "evidence": {
                "confirming_evidence": [
                    "Controlled study comparing LLM vs human code on identical tasks",
                    "Bug density analysis across 10k+ commits in matched repositories",
                ],
                "falsifying_evidence": [
                    "Study showing no bug-rate difference with rigorous code review",
                    "Analysis where LLM code has higher defect rate on complex logic",
                    "Evidence that bug metrics used don't capture semantic errors",
                ],
                "assumptions": [
                    "Bug definition is consistent across human and LLM code",
                    "Complexity of tasks is comparable",
                    "LLM code was not cherry-picked for the comparison",
                ],
                "data_sources": [
                    "GitHub Copilot usage studies",
                    "Internal A/B test data from IDE providers",
                ],
            },
            "adversarial": {
                "fallacies": ["Overgeneralization from narrow benchmark tasks"],
                "confounders": [
                    "Task complexity not controlled",
                    "Developer experience level varies",
                ],
                "biases": ["Survivorship bias — only successful LLM outputs compared"],
                "steel_man_counter": (
                    "LLM code may have fewer syntactic bugs but more subtle "
                    "logic errors that automated tests miss."
                ),
                "confidence": "LOW",
                "confidence_justification": (
                    "40% is a specific quantitative claim with no cited source or "
                    "controlled methodology."
                ),
            },
            "status": "FAIL",
            "verdict": "REFUTED",
        },
        {
            "status": "PASS",
            "verdict": "SUPPORTED",
            "adversarial": {
                "fallacies": [],
                "confounders": ["Domain specificity varies widely"],
                "biases": ["Benchmark selection bias"],
                "steel_man_counter": (
                    "Few-shot prompting may close the gap as base models improve, "
                    "making fine-tuning ROI questionable."
                ),
                "confidence": "HIGH",
                "confidence_justification": (
                    "Well-established in NLP literature with multiple replications."
                ),
            },
        },
        {
            "status": "PENDING",
            "verdict": "INCONCLUSIVE",
            "adversarial": {
                "fallacies": ["Correlation treated as causation"],
                "confounders": [
                    "Novelty effect on productivity metrics",
                    "Self-selection of tech-savvy developers",
                ],
                "biases": ["Hawthorne effect in measured productivity studies"],
                "steel_man_counter": (
                    "Even if 55% is inflated, directional productivity gains from "
                    "AI pair programming are consistently reported."
                ),
                "confidence": "MEDIUM",
                "confidence_justification": (
                    "Directionally supported but specific percentage is unverified."
                ),
            },
        },
        {
            "status": "FAIL",
            "verdict": "REFUTED",
            "adversarial": {
                "fallacies": ["Absolute claim ('eliminates') is unfalsifiable in practice"],
                "confounders": ["RAG retrieval quality depends on corpus coverage"],
                "biases": ["Cherry-picked examples in RAG demos"],
                "steel_man_counter": (
                    "RAG significantly reduces hallucination rates compared to "
                    "pure generation, even if it cannot eliminate them entirely."
                ),
                "confidence": "LOW",
                "confidence_justification": (
                    "'Eliminates' is too strong — no production system achieves "
                    "zero hallucinations."
                ),
            },
        },
    ]

    results = []
    for i, claim in enumerate(claims, 1):
        scenario = mock_scenarios[i - 1] if i <= len(mock_scenarios) else {}
        result = evaluate_claim(
            claim_id=i,
            claim=claim,
            evidence_mock=scenario.get("evidence"),
            adversarial_mock=scenario.get("adversarial"),
            verifier_mock=scenario.get("verifier"),
            status_override=scenario.get("status"),
            verdict_override=scenario.get("verdict"),
        )
        results.append(result)

    report = render_full_report(results)
    print(report)

    # Also dump structured JSON
    json_path = "proof_ledger.json"
    ledger_data = []
    for r in results:
        entry = {
            "id": r.id,
            "claim": r.claim,
            "falsifiable": r.falsifiable,
            "verifier_status": r.verifier_status.value,
            "verdict": r.verdict.value,
            "adversarial_confidence": r.adversarial.confidence.value,
        }
        ledger_data.append(entry)

    with open(json_path, "w") as f:
        json.dump(ledger_data, f, indent=2)

    print(f"\nStructured ledger written to {json_path}")
    print()
    print("=" * 70)
    print("  Demo complete. In production, an LLM fills each stage above.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
