#!/usr/bin/env python3
"""
Premortem Risk Analysis — Demo

Demonstrates the premortem methodology (Klein 2007 + Kahneman outside view)
on a sample plan. No API keys required — uses structured templates to show
the full analysis pipeline: prospective hindsight, multi-agent scan,
mitigation triplets, reverse-premortem, and history snapshot.
"""

import json
import textwrap
from datetime import date
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Data model ───────────────────────────────────────────────────────────

DIMENSIONS = [
    "Technical",
    "Integration",
    "Operational",
    "Human / Process",
    "External / Market",
]

REVIEWER_PERSONAS = {
    "Devil's Advocate": "Challenges every assumption and looks for logical flaws.",
    "Pessimist": "Assumes the worst-case outcome for every dependency.",
    "Security Auditor": "Focuses on attack surface, data leaks, and auth gaps.",
    "Ops Engineer": "Evaluates runbooks, monitoring, and incident response readiness.",
    "End User": "Asks whether the feature actually solves the stated problem.",
}

LIKELIHOOD_WEIGHT = {"High": 3, "Medium": 2, "Low": 1}
IMPACT_WEIGHT = {"High": 3, "Medium": 2, "Low": 1}


@dataclass
class Risk:
    title: str
    dimension: str
    description: str
    likelihood: str  # High / Medium / Low
    impact: str      # High / Medium / Low
    mitigation: str
    surfaced_by: str  # which reviewer persona

    @property
    def score(self) -> int:
        return LIKELIHOOD_WEIGHT[self.likelihood] * IMPACT_WEIGHT[self.impact]


@dataclass
class PremortemResult:
    plan_name: str
    plan_description: str
    date_run: str
    risks: list[Risk] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    reverse_insights: list[str] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)


# ── Sample plan + mock analysis ──────────────────────────────────────────

SAMPLE_PLAN = {
    "name": "Migrate billing service to event-driven architecture",
    "description": (
        "Replace the synchronous REST-based billing pipeline with an "
        "event-driven system using Kafka. Goals: decouple payment processing "
        "from order fulfillment, improve throughput under Black Friday load, "
        "and enable real-time revenue dashboards."
    ),
}

SAMPLE_RISKS = [
    Risk(
        title="Message ordering guarantees break invoice sequencing",
        dimension="Technical",
        description=(
            "Kafka partitions may reorder events if the partition key strategy "
            "changes, causing invoices to reference payments that haven't settled."
        ),
        likelihood="High",
        impact="High",
        mitigation=(
            "Enforce deterministic partition keys (customer_id + invoice_id). "
            "Add idempotency tokens and a sequence-check consumer that halts "
            "processing on out-of-order detection."
        ),
        surfaced_by="Devil's Advocate",
    ),
    Risk(
        title="Payment gateway webhook replay floods consumer",
        dimension="Integration",
        description=(
            "Stripe retries webhooks up to 16 times. During an outage recovery, "
            "a burst of replayed events could overwhelm the Kafka consumer group "
            "and trigger duplicate charges."
        ),
        likelihood="High",
        impact="High",
        mitigation=(
            "Implement deduplication layer using event ID + idempotency key in "
            "Redis with 72-hour TTL. Add consumer backpressure via max.poll.records."
        ),
        surfaced_by="Ops Engineer",
    ),
    Risk(
        title="Schema evolution breaks downstream consumers",
        dimension="Technical",
        description=(
            "Adding fields to the billing event schema without a compatibility "
            "policy will break older consumers that use strict deserialization."
        ),
        likelihood="Medium",
        impact="High",
        mitigation=(
            "Adopt Avro with a Schema Registry enforcing BACKWARD compatibility. "
            "Version all event schemas and run compatibility checks in CI."
        ),
        surfaced_by="Devil's Advocate",
    ),
    Risk(
        title="No runbook for Kafka cluster failover",
        dimension="Operational",
        description=(
            "The team has operated REST services for 3 years but has zero "
            "Kafka operational experience. A broker failure at 2 AM will have "
            "no documented recovery path."
        ),
        likelihood="Medium",
        impact="High",
        mitigation=(
            "Write and drill a Kafka incident runbook before go-live. Include "
            "broker replacement, partition reassignment, and consumer lag alerts. "
            "Schedule a chaos engineering session."
        ),
        surfaced_by="Ops Engineer",
    ),
    Risk(
        title="Key-person dependency on single Kafka expert",
        dimension="Human / Process",
        description=(
            "Only one engineer has Kafka production experience. If they leave "
            "or are unavailable during an incident, the team cannot debug "
            "consumer lag or rebalancing issues."
        ),
        likelihood="Medium",
        impact="Medium",
        mitigation=(
            "Pair-program the migration with at least two other engineers. "
            "Document tribal knowledge in an internal wiki. Budget for "
            "Confluent training for the on-call rotation."
        ),
        surfaced_by="Pessimist",
    ),
    Risk(
        title="Regulatory audit trail gaps during async processing",
        dimension="External / Market",
        description=(
            "PCI-DSS requires a complete audit trail for payment events. "
            "Async processing may lose events in dead-letter queues without "
            "triggering compliance alerts."
        ),
        likelihood="Low",
        impact="High",
        mitigation=(
            "Route all dead-letter events to a compliance-monitored S3 bucket "
            "with alerting. Add end-to-end event tracing with correlation IDs "
            "and periodic reconciliation jobs."
        ),
        surfaced_by="Security Auditor",
    ),
    Risk(
        title="Real-time dashboard shows stale data during consumer lag",
        dimension="Technical",
        description=(
            "The revenue dashboard reads from a materialized view updated by "
            "Kafka consumers. During high lag, executives see stale numbers "
            "and make incorrect decisions."
        ),
        likelihood="Medium",
        impact="Low",
        mitigation=(
            "Display a 'data freshness' indicator on the dashboard showing "
            "consumer lag in seconds. Alert if lag exceeds 60 seconds."
        ),
        surfaced_by="End User",
    ),
    Risk(
        title="Vendor lock-in to managed Kafka provider",
        dimension="External / Market",
        description=(
            "Choosing Confluent Cloud creates a dependency that makes future "
            "migration to Redpanda or Pulsar expensive."
        ),
        likelihood="Low",
        impact="Medium",
        mitigation=(
            "Abstract the message broker behind a thin producer/consumer "
            "interface. Avoid Confluent-specific features (ksqlDB) in the "
            "critical payment path."
        ),
        surfaced_by="Pessimist",
    ),
]

SAMPLE_ASSUMPTIONS = [
    "Kafka throughput will handle 10x Black Friday peak without horizontal scaling.",
    "The payment gateway (Stripe) webhook contract remains stable for 12+ months.",
    "Team can achieve Kafka operational competence within the 8-week migration window.",
    "Existing REST consumers can be fully decommissioned — no long-tail integrations.",
    "Schema Registry adoption will not slow down feature velocity in adjacent teams.",
]

SAMPLE_REVERSE_INSIGHTS = [
    "Success depends on the lucky break that Stripe doesn't change their webhook format during migration.",
    "At 10x scale, we'd wish we had built multi-region Kafka from day one instead of retrofitting.",
    "The real-time dashboard is the visible win — if it works flawlessly, leadership funds phase 2.",
    "We assumed a single Kafka cluster; at 100x we'd need topic-level routing across clusters.",
]

SAMPLE_ACTIONS = [
    "Write and drill Kafka incident runbook before go-live",
    "Implement idempotency + deduplication layer in week 1",
    "Set up Schema Registry with BACKWARD compatibility enforcement",
    "Run chaos engineering session simulating broker failure",
    "Add consumer lag alerting with <60s SLA",
    "Pair at least 2 additional engineers on Kafka operations",
    "Create PCI-DSS compliance monitoring for dead-letter queues",
]


# ── Analysis engine ──────────────────────────────────────────────────────

def run_premortem(plan: dict) -> PremortemResult:
    """Run the full premortem pipeline on a plan."""
    result = PremortemResult(
        plan_name=plan["name"],
        plan_description=plan["description"],
        date_run=date.today().isoformat(),
        risks=sorted(SAMPLE_RISKS, key=lambda r: r.score, reverse=True),
        assumptions=SAMPLE_ASSUMPTIONS,
        reverse_insights=SAMPLE_REVERSE_INSIGHTS,
        recommended_actions=SAMPLE_ACTIONS,
    )
    return result


def format_markdown(result: PremortemResult) -> str:
    """Format the premortem result as a markdown snapshot."""
    lines = []
    lines.append(f"## Premortem Summary — {result.plan_name} — {result.date_run}")
    lines.append("")
    lines.append(f"> {result.plan_description}")
    lines.append("")

    # Top Risks
    lines.append("### Top Risks (ranked by likelihood x impact)")
    lines.append("")
    for i, r in enumerate(result.risks, 1):
        lines.append(
            f"{i}. **{r.title}** — Likelihood: {r.likelihood}, "
            f"Impact: {r.impact} (score: {r.score})"
        )
        lines.append(f"   - *Dimension*: {r.dimension} | *Surfaced by*: {r.surfaced_by}")
        lines.append(f"   - *Scenario*: {r.description}")
        lines.append(f"   - *Mitigation*: {r.mitigation}")
        lines.append("")

    # Assumptions
    lines.append("### Assumptions That Must Hold")
    lines.append("")
    for a in result.assumptions:
        lines.append(f"- {a}")
    lines.append("")

    # Reverse-Premortem
    lines.append("### Reverse-Premortem Insights")
    lines.append("")
    for r in result.reverse_insights:
        lines.append(f"- {r}")
    lines.append("")

    # Actions
    lines.append("### Recommended Actions Before Committing")
    lines.append("")
    for a in result.recommended_actions:
        lines.append(f"- [ ] {a}")
    lines.append("")

    return "\n".join(lines)


def print_console_report(result: PremortemResult) -> None:
    """Print a colored console report."""
    W = 78
    BOLD = "\033[1m"
    RED = "\033[91m"
    YEL = "\033[93m"
    GRN = "\033[92m"
    CYN = "\033[96m"
    DIM = "\033[2m"
    RST = "\033[0m"

    color_map = {"High": RED, "Medium": YEL, "Low": GRN}

    print()
    print(f"{BOLD}{'=' * W}{RST}")
    print(f"{BOLD}  PREMORTEM RISK ANALYSIS{RST}")
    print(f"{BOLD}{'=' * W}{RST}")
    print()
    print(f"{BOLD}Plan:{RST} {result.plan_name}")
    print(f"{BOLD}Date:{RST} {result.date_run}")
    print()
    print(textwrap.fill(result.plan_description, width=W, initial_indent="  ", subsequent_indent="  "))
    print()

    # ── Step 1: Dimensions scanned ──
    print(f"{BOLD}Step 1 — Dimensions Scanned{RST}")
    for d in DIMENSIONS:
        count = sum(1 for r in result.risks if r.dimension == d)
        print(f"  [{CYN}{'*' if count else ' '}{RST}] {d} — {count} risk(s)")
    print()

    # ── Step 2: Multi-agent reviewers ──
    print(f"{BOLD}Step 2 — Multi-Agent Silent Scan{RST}")
    for persona, desc in REVIEWER_PERSONAS.items():
        count = sum(1 for r in result.risks if r.surfaced_by == persona)
        print(f"  {CYN}{persona}{RST} ({count} risk(s)): {DIM}{desc}{RST}")
    print()

    # ── Step 3: Ranked risks ──
    print(f"{BOLD}Step 3 — Mitigation Triplets (ranked){RST}")
    print(f"  {DIM}{'─' * (W - 4)}{RST}")
    for i, r in enumerate(result.risks, 1):
        lc = color_map[r.likelihood]
        ic = color_map[r.impact]
        print(f"  {BOLD}{i}. {r.title}{RST}")
        print(f"     Dimension: {r.dimension} | Surfaced by: {r.surfaced_by}")
        print(f"     Likelihood: {lc}{r.likelihood}{RST}  |  Impact: {ic}{r.impact}{RST}  |  Score: {BOLD}{r.score}{RST}")
        wrapped = textwrap.fill(r.description, width=W - 6, initial_indent="     ", subsequent_indent="     ")
        print(f"     {DIM}Scenario:{RST}")
        print(wrapped)
        wrapped_m = textwrap.fill(r.mitigation, width=W - 6, initial_indent="     ", subsequent_indent="     ")
        print(f"     {GRN}Mitigation:{RST}")
        print(wrapped_m)
        print(f"  {DIM}{'─' * (W - 4)}{RST}")
    print()

    # ── Step 4: Reverse premortem ──
    print(f"{BOLD}Step 4 — Reverse-Premortem (\"Imagine it succeeded wildly\"){RST}")
    print()
    print(f"  {BOLD}Assumptions that must hold:{RST}")
    for a in result.assumptions:
        print(f"    - {a}")
    print()
    print(f"  {BOLD}Insights:{RST}")
    for r in result.reverse_insights:
        print(f"    - {r}")
    print()

    # ── Step 5: Actions ──
    print(f"{BOLD}Step 5 — Recommended Actions Before Committing{RST}")
    for a in result.recommended_actions:
        print(f"  [ ] {a}")
    print()

    # ── Summary stats ──
    high = sum(1 for r in result.risks if r.score >= 9)
    med = sum(1 for r in result.risks if 4 <= r.score < 9)
    low = sum(1 for r in result.risks if r.score < 4)
    print(f"{BOLD}Summary:{RST} {RED}{high} critical{RST}, {YEL}{med} moderate{RST}, {GRN}{low} low{RST} risks across {len(DIMENSIONS)} dimensions")
    print(f"         {len(result.recommended_actions)} action items before committing")
    print(f"{'=' * W}")
    print()


def save_snapshot(result: PremortemResult, path: str) -> None:
    """Save the markdown snapshot to a file."""
    md = format_markdown(result)
    with open(path, "w") as f:
        f.write(md)
    print(f"Snapshot saved to {path}")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    result = run_premortem(SAMPLE_PLAN)
    print_console_report(result)

    snapshot_path = "premortem_snapshot.md"
    save_snapshot(result, snapshot_path)

    # Also dump structured JSON for programmatic consumption
    json_path = "premortem_snapshot.json"
    data = {
        "plan_name": result.plan_name,
        "plan_description": result.plan_description,
        "date_run": result.date_run,
        "risks": [
            {
                "title": r.title,
                "dimension": r.dimension,
                "description": r.description,
                "likelihood": r.likelihood,
                "impact": r.impact,
                "score": r.score,
                "mitigation": r.mitigation,
                "surfaced_by": r.surfaced_by,
            }
            for r in result.risks
        ],
        "assumptions": result.assumptions,
        "reverse_insights": result.reverse_insights,
        "recommended_actions": result.recommended_actions,
    }
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"JSON export saved to {json_path}")


if __name__ == "__main__":
    main()
