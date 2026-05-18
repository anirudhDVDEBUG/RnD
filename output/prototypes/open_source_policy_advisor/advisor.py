#!/usr/bin/env python3
"""
Open Source Policy Advisor — CLI demo.

Evaluates a public-sector open source scenario and produces a structured
policy recommendation based on the GDS "open by default" framework and
Project Glasswing context (AI-driven vulnerability scanning).

No API keys required — runs entirely with local logic and mock scenarios.
"""

import json
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List


# ── Domain types ─────────────────────────────────────────────────────────

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RepoAction(Enum):
    STAY_OPEN = "stay_open"
    TEMPORARY_CLOSURE = "temporary_closure"
    PERMANENT_CLOSURE = "permanent_closure"


@dataclass
class Vulnerability:
    name: str
    severity: Severity
    exploited_in_wild: bool = False
    patch_available: bool = False


@dataclass
class Scenario:
    org_name: str
    repo_count: int
    description: str
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    ai_scanning_reported: bool = False
    public_pressure: bool = False


@dataclass
class Recommendation:
    action: RepoAction
    rationale: str
    immediate_steps: List[str]
    policy_clauses: List[str]
    risk_score: float  # 0-10


# ── Advisory engine ──────────────────────────────────────────────────────

def assess(scenario: Scenario) -> Recommendation:
    """Core advisory logic: score the risk and recommend an action."""

    # Calculate risk score
    risk = 0.0
    critical_exploited = []

    for v in scenario.vulnerabilities:
        severity_weight = {
            Severity.LOW: 1, Severity.MEDIUM: 2,
            Severity.HIGH: 4, Severity.CRITICAL: 7,
        }[v.severity]
        risk += severity_weight
        if v.exploited_in_wild:
            risk += 5
            critical_exploited.append(v.name)
        if not v.patch_available:
            risk += 2

    if scenario.ai_scanning_reported:
        risk += 1  # raises awareness but is NOT a reason to close
    if scenario.public_pressure:
        risk += 1

    risk = min(risk, 10.0)

    # Decide action
    if critical_exploited:
        action = RepoAction.TEMPORARY_CLOSURE
        rationale = (
            f"Temporary closure recommended ONLY for repos containing "
            f"actively exploited vulnerabilities ({', '.join(critical_exploited)}). "
            f"Reopen once patches are deployed. All other repos should stay open."
        )
    else:
        action = RepoAction.STAY_OPEN
        rationale = (
            "No actively exploited vulnerabilities found. The GDS principle "
            "applies: remain open by default, fix vulnerabilities in place, "
            "and invest in security practices rather than obscurity."
        )

    # Build immediate steps
    steps = []
    unpatched = [v for v in scenario.vulnerabilities if not v.patch_available]
    patched = [v for v in scenario.vulnerabilities if v.patch_available]

    if patched:
        steps.append(f"Deploy existing patches for: {', '.join(v.name for v in patched)}")
    if unpatched:
        steps.append(f"Prioritize developing patches for: {', '.join(v.name for v in unpatched)}")
    if critical_exploited:
        steps.append("Temporarily restrict access to affected repos during remediation (max 30 days)")
    steps.append("Run automated security scanning across all repositories")
    steps.append("Establish or update responsible disclosure policy")
    if scenario.ai_scanning_reported:
        steps.append("Acknowledge AI scanning as a reality; focus on fixing, not hiding")

    # Policy clauses
    clauses = [
        "All source code SHALL be open by default, in line with GDS Service Standard.",
        "Repositories MAY be temporarily closed (max 30 days) only when an actively "
        "exploited critical vulnerability has no available patch.",
        "A vulnerability response team SHALL triage, patch, and disclose all reported "
        "vulnerabilities within published SLA timelines.",
        "Security audits SHALL be conducted quarterly regardless of repository visibility.",
        "AI-assisted vulnerability scanning SHALL be treated as equivalent to manual "
        "security research under the organisation's responsible disclosure policy.",
        "Closure decisions SHALL be reviewed fortnightly and reopened at the earliest "
        "safe opportunity.",
    ]

    return Recommendation(
        action=action,
        rationale=rationale,
        immediate_steps=steps,
        policy_clauses=clauses,
        risk_score=round(risk, 1),
    )


# ── Mock scenarios ───────────────────────────────────────────────────────

SCENARIOS = [
    Scenario(
        org_name="NHS Digital",
        repo_count=157,
        description=(
            "AI scanning tool (Project Glasswing) reported multiple vulnerabilities "
            "in public NHS repos. Political pressure to close all repositories."
        ),
        vulnerabilities=[
            Vulnerability("SQL injection in patient lookup API", Severity.CRITICAL,
                          exploited_in_wild=False, patch_available=True),
            Vulnerability("XSS in appointment booking form", Severity.HIGH,
                          exploited_in_wild=False, patch_available=True),
            Vulnerability("Hardcoded test credentials in CI config", Severity.MEDIUM,
                          exploited_in_wild=False, patch_available=False),
            Vulnerability("Outdated dependency with known CVE", Severity.LOW,
                          exploited_in_wild=False, patch_available=True),
        ],
        ai_scanning_reported=True,
        public_pressure=True,
    ),
    Scenario(
        org_name="HMRC Tax Platform",
        repo_count=83,
        description=(
            "A critical auth bypass in the tax submission API is being actively "
            "exploited. Media coverage is intense."
        ),
        vulnerabilities=[
            Vulnerability("Auth bypass in submission endpoint", Severity.CRITICAL,
                          exploited_in_wild=True, patch_available=False),
            Vulnerability("Rate limiting missing on login", Severity.MEDIUM,
                          exploited_in_wild=False, patch_available=True),
        ],
        ai_scanning_reported=False,
        public_pressure=True,
    ),
    Scenario(
        org_name="Local Council Digital Services",
        repo_count=12,
        description=(
            "Council received a responsible disclosure email about a minor "
            "info-leak. No exploitation. Board wants to 'go private' out of caution."
        ),
        vulnerabilities=[
            Vulnerability("Server version header disclosure", Severity.LOW,
                          exploited_in_wild=False, patch_available=True),
        ],
        ai_scanning_reported=False,
        public_pressure=False,
    ),
]


# ── Output formatting ───────────────────────────────────────────────────

def hr():
    print("=" * 72)


def print_report(scenario: Scenario, rec: Recommendation):
    hr()
    print(f"  OPEN SOURCE POLICY ADVISORY REPORT")
    print(f"  Organisation: {scenario.org_name}")
    print(f"  Repositories: {scenario.repo_count} public repos")
    hr()

    print(f"\n  Situation")
    print(f"  {'-' * 40}")
    for line in textwrap.wrap(scenario.description, width=66):
        print(f"    {line}")

    print(f"\n  Vulnerabilities Assessed: {len(scenario.vulnerabilities)}")
    for v in scenario.vulnerabilities:
        status = "PATCHED" if v.patch_available else "UNPATCHED"
        exploited = " [ACTIVELY EXPLOITED]" if v.exploited_in_wild else ""
        print(f"    [{v.severity.value.upper():8s}] {v.name}")
        print(f"             {status}{exploited}")

    print(f"\n  AI Scanning Reported: {'Yes' if scenario.ai_scanning_reported else 'No'}")
    print(f"  Public/Political Pressure: {'Yes' if scenario.public_pressure else 'No'}")

    print(f"\n  Risk Score: {rec.risk_score}/10")

    action_labels = {
        RepoAction.STAY_OPEN: "STAY OPEN (recommended)",
        RepoAction.TEMPORARY_CLOSURE: "TEMPORARY CLOSURE (affected repos only)",
        RepoAction.PERMANENT_CLOSURE: "PERMANENT CLOSURE (not recommended)",
    }
    print(f"\n  Recommendation: {action_labels[rec.action]}")
    print(f"  {'-' * 40}")
    for line in textwrap.wrap(rec.rationale, width=66):
        print(f"    {line}")

    print(f"\n  Immediate Steps")
    print(f"  {'-' * 40}")
    for i, step in enumerate(rec.immediate_steps, 1):
        for j, line in enumerate(textwrap.wrap(step, width=62)):
            if j == 0:
                print(f"    {i}. {line}")
            else:
                print(f"       {line}")

    print(f"\n  Suggested Policy Clauses")
    print(f"  {'-' * 40}")
    for i, clause in enumerate(rec.policy_clauses, 1):
        for j, line in enumerate(textwrap.wrap(clause, width=62)):
            if j == 0:
                print(f"    {i}. {line}")
            else:
                print(f"       {line}")

    print()
    hr()


def print_json_report(scenario: Scenario, rec: Recommendation):
    output = {
        "organisation": scenario.org_name,
        "repo_count": scenario.repo_count,
        "risk_score": rec.risk_score,
        "action": rec.action.value,
        "rationale": rec.rationale,
        "immediate_steps": rec.immediate_steps,
        "policy_clauses": rec.policy_clauses,
    }
    print(json.dumps(output, indent=2))


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    output_json = "--json" in sys.argv
    single = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            single = int(arg) - 1

    scenarios = [SCENARIOS[single]] if single is not None and 0 <= single < len(SCENARIOS) else SCENARIOS

    if not output_json:
        print()
        print("  Open Source Policy Advisor")
        print("  Based on GDS guidance (May 2026) and Project Glasswing context")
        print()

    for scenario in scenarios:
        rec = assess(scenario)
        if output_json:
            print_json_report(scenario, rec)
        else:
            print_report(scenario, rec)

    if not output_json:
        print("  Key Principle: \"Open by default. Fix vulnerabilities, don't hide code.\"")
        print("  Source: GDS - AI, open code and vulnerability risk in the public sector")
        print()


if __name__ == "__main__":
    main()
