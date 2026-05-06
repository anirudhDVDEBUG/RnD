"""
Autonomous Agent Risk Audit Tool

Analyzes an autonomous AI agent design specification and produces a risk report
covering: unintended external actions, resource waste, consent violations,
ethical boundary violations, and missing guardrails.

Inspired by the AI cafe in Stockholm that ordered 120 eggs with no stove,
6,000 napkins, and applied for government permits with AI-generated sketches.
"""

import json
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RiskCategory(str, Enum):
    CONSENT_VIOLATION = "Consent Violation"
    RESOURCE_WASTE = "Resource Waste"
    EXTERNAL_COMMS = "Uncontrolled External Communications"
    IRREVERSIBLE_ACTION = "Irreversible Real-World Action"
    LEGAL_REGULATORY = "Legal/Regulatory Risk"
    ETHICAL_BOUNDARY = "Ethical Boundary Violation"
    MISSING_GUARDRAIL = "Missing Guardrail"


@dataclass
class Finding:
    category: RiskCategory
    severity: Severity
    title: str
    description: str
    recommendation: str
    affected_capability: str


@dataclass
class AgentSpec:
    """Describes an autonomous agent's capabilities and constraints."""
    name: str
    description: str
    capabilities: list  # what the agent can do
    external_touchpoints: list  # external systems it interacts with
    has_human_approval: dict = field(default_factory=dict)  # capability -> bool
    quantity_limits: dict = field(default_factory=dict)  # capability -> limit info
    logging_enabled: bool = False
    override_log: bool = False  # "hall of shame" log


@dataclass
class AuditReport:
    agent_name: str
    findings: list = field(default_factory=list)
    checklist: dict = field(default_factory=dict)
    risk_score: int = 0
    summary: str = ""


# --- Risk detection rules ---

DANGEROUS_KEYWORDS = {
    "emergency": Severity.CRITICAL,
    "urgent": Severity.HIGH,
    "asap": Severity.HIGH,
    "immediately": Severity.MEDIUM,
}

GOVERNMENT_KEYWORDS = ["permit", "license", "application", "filing", "registration",
                       "tax", "compliance", "regulatory", "government", "legal"]

COMMS_KEYWORDS = ["email", "sms", "message", "notify", "contact", "call", "slack",
                  "whatsapp", "letter", "fax"]

ORDERING_KEYWORDS = ["order", "purchase", "buy", "procure", "acquire", "subscribe",
                     "rent", "lease", "hire"]

IRREVERSIBLE_KEYWORDS = ["delete", "cancel", "terminate", "fire", "dismiss",
                         "sign contract", "submit", "publish", "broadcast",
                         "transfer funds", "wire", "payment"]


def check_consent_boundary(spec: AgentSpec) -> list:
    """Check if external interactions respect consent boundaries."""
    findings = []
    for tp in spec.external_touchpoints:
        tp_lower = tp.lower()
        # Check if this touchpoint involves contacting people
        if any(kw in tp_lower for kw in COMMS_KEYWORDS):
            has_approval = spec.has_human_approval.get(tp, False)
            if not has_approval:
                findings.append(Finding(
                    category=RiskCategory.CONSENT_VIOLATION,
                    severity=Severity.CRITICAL,
                    title=f"No consent gate on external comms: '{tp}'",
                    description=(
                        f"The agent can use '{tp}' to contact external parties "
                        f"without verifying they've opted into AI interaction. "
                        f"This wastes real people's time and attention."
                    ),
                    recommendation=(
                        "Add human-in-the-loop approval before any outbound "
                        "communication. Ensure recipients have consented to AI contact."
                    ),
                    affected_capability=tp,
                ))
    return findings


def check_urgency_escalation(spec: AgentSpec) -> list:
    """Check if agent can artificially escalate urgency."""
    findings = []
    for cap in spec.capabilities:
        cap_lower = cap.lower()
        for keyword, severity in DANGEROUS_KEYWORDS.items():
            if keyword in cap_lower:
                has_approval = spec.has_human_approval.get(cap, False)
                if not has_approval:
                    findings.append(Finding(
                        category=RiskCategory.ETHICAL_BOUNDARY,
                        severity=severity,
                        title=f"Urgency escalation risk: '{cap}'",
                        description=(
                            f"Capability '{cap}' involves urgency language ('{keyword}'). "
                            f"AI agents should never artificially escalate urgency to "
                            f"override normal human processes."
                        ),
                        recommendation=(
                            "Require human approval for any communication or action "
                            "marked as urgent/emergency. Add rate limits on escalations."
                        ),
                        affected_capability=cap,
                    ))
    return findings


def check_quantity_guardrails(spec: AgentSpec) -> list:
    """Check for missing quantity/frequency limits on ordering."""
    findings = []
    for cap in spec.capabilities:
        cap_lower = cap.lower()
        if any(kw in cap_lower for kw in ORDERING_KEYWORDS):
            limit = spec.quantity_limits.get(cap)
            if not limit:
                findings.append(Finding(
                    category=RiskCategory.RESOURCE_WASTE,
                    severity=Severity.HIGH,
                    title=f"No quantity limits on: '{cap}'",
                    description=(
                        f"Capability '{cap}' has no quantity or frequency guardrails. "
                        f"Without limits, an AI cafe manager ordered 120 eggs (no stove), "
                        f"6,000 napkins, and 22.5kg of canned tomatoes for fresh sandwiches."
                    ),
                    recommendation=(
                        "Cap order quantities relative to historical usage (e.g., no "
                        "single order > 3x average). Require human sign-off for "
                        "first-time items or bulk orders."
                    ),
                    affected_capability=cap,
                ))
    return findings


def check_irreversible_actions(spec: AgentSpec) -> list:
    """Flag capabilities that involve irreversible real-world decisions."""
    findings = []
    for cap in spec.capabilities:
        cap_lower = cap.lower()
        if any(kw in cap_lower for kw in IRREVERSIBLE_KEYWORDS):
            has_approval = spec.has_human_approval.get(cap, False)
            if not has_approval:
                findings.append(Finding(
                    category=RiskCategory.IRREVERSIBLE_ACTION,
                    severity=Severity.CRITICAL,
                    title=f"Irreversible action without approval: '{cap}'",
                    description=(
                        f"Capability '{cap}' can trigger irreversible real-world "
                        f"consequences without human confirmation."
                    ),
                    recommendation=(
                        "Add mandatory human-in-the-loop confirmation for all "
                        "irreversible actions. Log the decision chain for audit."
                    ),
                    affected_capability=cap,
                ))
    return findings


def check_legal_regulatory(spec: AgentSpec) -> list:
    """Check for autonomous interactions with government/legal systems."""
    findings = []
    all_items = spec.capabilities + spec.external_touchpoints
    for item in all_items:
        item_lower = item.lower()
        if any(kw in item_lower for kw in GOVERNMENT_KEYWORDS):
            has_approval = spec.has_human_approval.get(item, False)
            if not has_approval:
                findings.append(Finding(
                    category=RiskCategory.LEGAL_REGULATORY,
                    severity=Severity.CRITICAL,
                    title=f"Autonomous legal/regulatory action: '{item}'",
                    description=(
                        f"'{item}' involves government or legal interaction without "
                        f"human oversight. An AI agent once applied for government "
                        f"permits with AI-generated floor plans."
                    ),
                    recommendation=(
                        "Never allow autonomous submission to government or legal "
                        "systems. Require human review and explicit sign-off. "
                        "Disclose AI involvement in all filings."
                    ),
                    affected_capability=item,
                ))
    return findings


def check_missing_guardrails(spec: AgentSpec) -> list:
    """Check for systemic missing guardrails."""
    findings = []
    if not spec.logging_enabled:
        findings.append(Finding(
            category=RiskCategory.MISSING_GUARDRAIL,
            severity=Severity.HIGH,
            title="No action logging enabled",
            description="Agent decisions are not being logged, making post-hoc audit impossible.",
            recommendation="Enable comprehensive logging of all agent decisions and actions.",
            affected_capability="system-wide",
        ))
    if not spec.override_log:
        findings.append(Finding(
            category=RiskCategory.MISSING_GUARDRAIL,
            severity=Severity.MEDIUM,
            title="No 'Hall of Shame' override log",
            description=(
                "There is no record of agent decisions that were overridden or flagged "
                "by humans. This feedback loop is essential for tightening constraints."
            ),
            recommendation=(
                "Implement a log that records all overridden agent decisions. "
                "Review weekly and update agent constraints accordingly."
            ),
            affected_capability="system-wide",
        ))

    # Check what fraction of capabilities have human approval
    caps_with_approval = sum(1 for c in spec.capabilities
                            if spec.has_human_approval.get(c, False))
    if len(spec.capabilities) > 0 and caps_with_approval == 0:
        findings.append(Finding(
            category=RiskCategory.MISSING_GUARDRAIL,
            severity=Severity.CRITICAL,
            title="No capabilities have human-in-the-loop",
            description=(
                "None of the agent's capabilities require human approval. "
                "Fully autonomous agents in physical/business environments are high-risk."
            ),
            recommendation=(
                "Add human-in-the-loop approval for at minimum: first-time actions, "
                "high-value transactions, external communications, and irreversible decisions."
            ),
            affected_capability="all capabilities",
        ))

    return findings


def build_checklist(spec: AgentSpec, findings: list) -> dict:
    """Build the standard audit checklist with pass/fail status."""
    categories_found = {f.category for f in findings}
    severity_found = {f.severity for f in findings}

    checklist = {
        "No EMERGENCY emails without human approval": (
            not any(f.category == RiskCategory.ETHICAL_BOUNDARY
                    and "emergency" in f.title.lower() for f in findings)
        ),
        "No autonomous government/legal submissions": (
            RiskCategory.LEGAL_REGULATORY not in categories_found
        ),
        "Quantity limits on all ordering capabilities": (
            not any(f.category == RiskCategory.RESOURCE_WASTE for f in findings)
        ),
        "All external comms have human-in-the-loop": (
            not any(f.category == RiskCategory.CONSENT_VIOLATION for f in findings)
        ),
        "Irreversible actions require confirmation": (
            not any(f.category == RiskCategory.IRREVERSIBLE_ACTION for f in findings)
        ),
        "Action logging enabled": spec.logging_enabled,
        "Override/escalation log ('Hall of Shame') active": spec.override_log,
    }
    return checklist


def calculate_risk_score(findings: list) -> int:
    """Calculate overall risk score (0-100, higher = more risky)."""
    weights = {
        Severity.CRITICAL: 25,
        Severity.HIGH: 15,
        Severity.MEDIUM: 8,
        Severity.LOW: 3,
    }
    score = sum(weights.get(f.severity, 0) for f in findings)
    return min(score, 100)


def run_audit(spec: AgentSpec) -> AuditReport:
    """Run the full audit against an agent specification."""
    findings = []
    findings.extend(check_consent_boundary(spec))
    findings.extend(check_urgency_escalation(spec))
    findings.extend(check_quantity_guardrails(spec))
    findings.extend(check_irreversible_actions(spec))
    findings.extend(check_legal_regulatory(spec))
    findings.extend(check_missing_guardrails(spec))

    checklist = build_checklist(spec, findings)
    risk_score = calculate_risk_score(findings)

    passed = sum(1 for v in checklist.values() if v)
    total = len(checklist)

    if risk_score >= 75:
        grade = "F - DO NOT DEPLOY"
    elif risk_score >= 50:
        grade = "D - Major risks, needs significant work"
    elif risk_score >= 25:
        grade = "C - Moderate risks, address before production"
    elif risk_score >= 10:
        grade = "B - Minor risks, acceptable with monitoring"
    else:
        grade = "A - Low risk"

    summary = (
        f"Risk Score: {risk_score}/100 | Grade: {grade} | "
        f"Findings: {len(findings)} | Checklist: {passed}/{total} passed"
    )

    return AuditReport(
        agent_name=spec.name,
        findings=findings,
        checklist=checklist,
        risk_score=risk_score,
        summary=summary,
    )


def format_report(report: AuditReport) -> str:
    """Format audit report as human-readable text."""
    lines = []
    w = 70

    lines.append("=" * w)
    lines.append(f"  AUTONOMOUS AGENT RISK AUDIT REPORT")
    lines.append(f"  Agent: {report.agent_name}")
    lines.append("=" * w)
    lines.append("")
    lines.append(f"  {report.summary}")
    lines.append("")

    # Risk score bar
    filled = int(report.risk_score / 100 * 40)
    bar = "#" * filled + "-" * (40 - filled)
    lines.append(f"  Risk: [{bar}] {report.risk_score}/100")
    lines.append("")

    # Checklist
    lines.append("-" * w)
    lines.append("  AUDIT CHECKLIST")
    lines.append("-" * w)
    for item, passed in report.checklist.items():
        icon = "[PASS]" if passed else "[FAIL]"
        lines.append(f"  {icon} {item}")
    lines.append("")

    # Findings by severity
    lines.append("-" * w)
    lines.append("  FINDINGS")
    lines.append("-" * w)

    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        sev_findings = [f for f in report.findings if f.severity == sev]
        if not sev_findings:
            continue
        lines.append(f"\n  --- {sev.value} ({len(sev_findings)}) ---")
        for i, f in enumerate(sev_findings, 1):
            lines.append(f"")
            lines.append(f"  [{sev.value}] {f.title}")
            lines.append(f"  Category: {f.category.value}")
            for desc_line in textwrap.wrap(f.description, width=w - 4):
                lines.append(f"    {desc_line}")
            lines.append(f"  Recommendation:")
            for rec_line in textwrap.wrap(f.recommendation, width=w - 6):
                lines.append(f"    {rec_line}")
    lines.append("")

    # Ethical red lines reminder
    lines.append("-" * w)
    lines.append("  ETHICAL RED LINES (must never be crossed)")
    lines.append("-" * w)
    red_lines = [
        "Contact individuals who haven't opted in to AI interaction",
        "Submit fraudulent/AI-generated documents to authorities without disclosure",
        "Escalate urgency artificially to override normal human processes",
        "Make irreversible physical-world decisions without confirmation",
    ]
    for rl in red_lines:
        lines.append(f"  X  {rl}")
    lines.append("")
    lines.append("=" * w)

    return "\n".join(lines)


def load_spec_from_json(path: str) -> AgentSpec:
    """Load agent spec from a JSON file."""
    with open(path) as f:
        data = json.load(f)
    return AgentSpec(**data)


# --- Built-in demo scenarios ---

def get_demo_cafe_agent() -> AgentSpec:
    """The AI cafe in Stockholm scenario - a deliberately risky agent."""
    return AgentSpec(
        name="AI Cafe Manager (Stockholm)",
        description=(
            "Autonomous AI agent managing a pop-up cafe: ordering supplies, "
            "contacting suppliers, applying for permits, managing inventory, "
            "and handling customer communications."
        ),
        capabilities=[
            "Order food supplies from wholesalers",
            "Order equipment and furniture",
            "Send emergency emails to suppliers",
            "Apply for government permits and licenses",
            "Contact potential customers via email",
            "Purchase advertising",
            "Sign contracts with delivery services",
            "Set menu prices",
            "Manage staff scheduling",
            "Submit regulatory compliance documents",
        ],
        external_touchpoints=[
            "Wholesale supplier email/ordering system",
            "Government permit portal",
            "Customer email list",
            "Payment processing (Stripe)",
            "Delivery service APIs",
            "Social media accounts",
            "Slack channel for supplier communication",
        ],
        has_human_approval={},  # No human approval on anything!
        quantity_limits={},     # No limits!
        logging_enabled=False,
        override_log=False,
    )


def get_demo_safe_agent() -> AgentSpec:
    """A well-designed agent with proper guardrails."""
    return AgentSpec(
        name="Inventory Assistant (with guardrails)",
        description=(
            "AI assistant for inventory management with human-in-the-loop "
            "for all external actions and quantity limits based on history."
        ),
        capabilities=[
            "Order restocking supplies (capped at 2x weekly average)",
            "Draft emails to suppliers (human sends)",
            "Generate inventory reports",
            "Flag low-stock items",
            "Suggest menu adjustments",
        ],
        external_touchpoints=[
            "Internal inventory database",
            "Draft email queue (human-reviewed)",
        ],
        has_human_approval={
            "Order restocking supplies (capped at 2x weekly average)": True,
            "Draft emails to suppliers (human sends)": True,
        },
        quantity_limits={
            "Order restocking supplies (capped at 2x weekly average)": "2x weekly average",
        },
        logging_enabled=True,
        override_log=True,
    )


def main():
    print("\n" + "=" * 70)
    print("  AUTONOMOUS AGENT RISK AUDIT TOOL")
    print("  Inspired by: 'Our AI started a cafe in Stockholm'")
    print("=" * 70)

    # Scenario 1: The dangerous cafe agent
    print("\n>>> SCENARIO 1: AI Cafe Manager (no guardrails)")
    print("    Based on the real AI cafe experiment in Stockholm\n")
    spec1 = get_demo_cafe_agent()
    report1 = run_audit(spec1)
    print(format_report(report1))

    # Scenario 2: A safer agent
    print("\n>>> SCENARIO 2: Inventory Assistant (with guardrails)")
    print("    Same domain, but designed with safety in mind\n")
    spec2 = get_demo_safe_agent()
    report2 = run_audit(spec2)
    print(format_report(report2))

    # Comparison
    print("\n" + "=" * 70)
    print("  COMPARISON SUMMARY")
    print("=" * 70)
    print(f"  {'Agent':<45} {'Score':>8} {'Findings':>10}")
    print(f"  {'-'*45} {'-'*8} {'-'*10}")
    print(f"  {report1.agent_name:<45} {report1.risk_score:>5}/100 {len(report1.findings):>10}")
    print(f"  {report2.agent_name:<45} {report2.risk_score:>5}/100 {len(report2.findings):>10}")
    print()

    # If a custom spec file is provided
    if len(sys.argv) > 1:
        print(f"\n>>> CUSTOM AGENT: Loading from {sys.argv[1]}\n")
        custom_spec = load_spec_from_json(sys.argv[1])
        custom_report = run_audit(custom_spec)
        print(format_report(custom_report))

    # JSON output option
    if "--json" in sys.argv:
        output = {
            "scenario_1": {
                "agent": spec1.name,
                "risk_score": report1.risk_score,
                "findings_count": len(report1.findings),
                "checklist": report1.checklist,
                "findings": [asdict(f) for f in report1.findings],
            },
            "scenario_2": {
                "agent": spec2.name,
                "risk_score": report2.risk_score,
                "findings_count": len(report2.findings),
                "checklist": report2.checklist,
                "findings": [asdict(f) for f in report2.findings],
            },
        }
        with open("audit_results.json", "w") as f:
            json.dump(output, f, indent=2, default=str)
        print("  JSON results written to audit_results.json")


if __name__ == "__main__":
    main()
