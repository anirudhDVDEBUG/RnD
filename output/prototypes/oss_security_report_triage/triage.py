#!/usr/bin/env python3
"""
OSS Security Report Triage Engine

Triages incoming security vulnerability reports for open-source projects.
Scores severity (CVSS-inspired), detects likely AI-generated reports,
assesses reproducibility, and drafts maintainer responses.
"""

import json
import sys
import os
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────────

SEVERITY_LABELS = {
    (9.0, 10.0): "CRITICAL",
    (7.0, 8.9):  "HIGH",
    (4.0, 6.9):  "MEDIUM",
    (0.1, 3.9):  "LOW",
    (0.0, 0.0):  "INFORMATIONAL",
}

RESPONSE_SLAS = {
    "CRITICAL": "24 hours",
    "HIGH": "72 hours",
    "MEDIUM": "1 week",
    "LOW": "2 weeks",
    "INFORMATIONAL": "best-effort",
}

# Phrases that frequently appear in AI-generated security reports
AI_SIGNAL_PHRASES = [
    "could potentially be exploited",
    "classic use-after-free pattern",
    "remediation:",
    "this vulnerability pattern is similar to",
    "cwe-",
    "all versions since commit",
    "severity: critical",
    "cvss score:",
    "note: this vulnerability",
    "the vulnerable code path is:",
]

ATTACK_VECTOR_SCORES = {
    "network": 0.85, "adjacent": 0.62, "local": 0.55, "physical": 0.20
}

IMPACT_KEYWORDS = {
    "remote code execution": 1.0, "rce": 1.0,
    "request smuggling": 0.8, "response splitting": 0.7,
    "header injection": 0.65, "crlf injection": 0.65,
    "use-after-free": 0.9, "buffer overflow": 0.9, "heap overflow": 0.9,
    "denial of service": 0.5, "dos": 0.5, "crash": 0.4,
    "information disclosure": 0.5, "info leak": 0.5,
    "integer overflow": 0.6, "null pointer": 0.4,
}


class Status(str, Enum):
    NEW = "NEW"
    ANALYZING = "ANALYZING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    NEEDS_INFO = "NEEDS_INFO"


@dataclass
class TriageResult:
    report_id: str
    title: str
    severity_label: str
    cvss_estimate: float
    ai_confidence: float          # 0.0 = definitely human, 1.0 = definitely AI
    ai_signals: list[str]
    reproducibility: str          # "confirmed", "plausible", "unlikely", "not_provided"
    status: Status
    response_draft: str
    sla: str
    flags: list[str] = field(default_factory=list)


def detect_ai_signals(report: dict) -> tuple[float, list[str]]:
    """Score how likely a report is AI-generated based on textual signals."""
    text = (report.get("description", "") + " " + report.get("poc", "")).lower()
    explicit = report.get("ai_indicators", [])

    signals = list(explicit)

    # Check for AI signal phrases in text
    for phrase in AI_SIGNAL_PHRASES:
        if phrase in text:
            signals.append(f"contains phrase: '{phrase}'")

    # Heuristics
    desc = report.get("description", "")
    if len(desc) > 800:
        signals.append(f"very long description ({len(desc)} chars)")
    if desc.count("\n") > 10:
        signals.append("highly structured with many sections")
    if "XXXXX" in desc or "YYYYY" in desc:
        signals.append("placeholder CVE references")
    if "no working poc" in text or "theoretical" in text:
        signals.append("no working proof of concept")

    # Score: each signal contributes diminishing returns
    if not signals:
        return 0.0, signals
    score = min(1.0, len(signals) * 0.12)
    return round(score, 2), signals


def estimate_cvss(report: dict) -> float:
    """Rough CVSS estimate based on attack vector + claimed impact."""
    av = report.get("attack_vector", "network").lower()
    av_score = ATTACK_VECTOR_SCORES.get(av, 0.5)

    # Find highest-matching impact keyword
    desc = (report.get("claimed_impact", "") + " " + report.get("description", "")).lower()
    impact_score = 0.3  # baseline
    for keyword, score in IMPACT_KEYWORDS.items():
        if keyword in desc:
            impact_score = max(impact_score, score)

    raw = (av_score * 0.4 + impact_score * 0.6) * 10
    return round(min(10.0, raw), 1)


def get_severity_label(cvss: float) -> str:
    for (lo, hi), label in SEVERITY_LABELS.items():
        if lo <= cvss <= hi:
            return label
    return "INFORMATIONAL"


def assess_reproducibility(report: dict) -> str:
    """Assess whether the PoC is likely reproducible."""
    poc = report.get("poc", "").lower()
    desc = report.get("description", "").lower()

    if not poc or poc == "none" or "no working poc" in poc or "theoretical" in poc:
        return "not_provided"

    # Check for concrete artifacts
    has_concrete = any(w in poc for w in ["curl ", "python ", "gcc ", "attached", "capture", "log"])
    has_env = any(w in desc for w in ["tested on", "confirmed", "reproduced", "build log", "tcpdump"])

    if has_concrete and has_env:
        return "confirmed"
    elif has_concrete:
        return "plausible"
    else:
        return "unlikely"


def determine_status(ai_conf: float, repro: str, cvss: float) -> Status:
    """Decide initial triage status."""
    if ai_conf >= 0.6 and repro in ("not_provided", "unlikely"):
        return Status.REJECTED
    if repro == "not_provided":
        return Status.NEEDS_INFO
    if repro in ("confirmed", "plausible") and cvss >= 4.0:
        return Status.CONFIRMED
    return Status.ANALYZING


def draft_response(report: dict, result: "TriageResult", templates: dict) -> str:
    """Generate a response draft using templates."""
    if result.status == Status.REJECTED:
        tmpl = templates.get("false_positive_ai", "")
        explanation = "Our analysis indicates the described code path is not reachable under the conditions stated."
        if result.reproducibility == "not_provided":
            reachability = "is theoretical and no proof of concept was provided"
        else:
            reachability = "does not lead to the claimed impact based on our review"
        return tmpl.format(
            explanation=explanation,
            reachability_note=reachability,
        )

    if result.status == Status.NEEDS_INFO:
        return templates.get("needs_more_info", "").format(
            questions="- A working proof of concept demonstrating the vulnerability\n"
                      "- The exact version/commit tested\n"
                      "- Build configuration and platform details"
        )

    if result.status == Status.CONFIRMED:
        if result.severity_label in ("CRITICAL", "HIGH"):
            return templates.get("valid_critical", "").format(
                severity=result.severity_label,
                sla=result.sla,
            )
        return templates.get("valid_standard", "").format(
            severity=result.severity_label,
            additional_notes=f"Estimated response timeline: {result.sla}.",
        )

    # ANALYZING
    return f"Report {result.report_id} is under active analysis. Estimated triage completion: {result.sla}."


def triage_report(report: dict, templates: dict) -> TriageResult:
    """Run the full triage pipeline on a single report."""
    ai_conf, ai_signals = detect_ai_signals(report)
    cvss = estimate_cvss(report)
    severity = get_severity_label(cvss)
    repro = assess_reproducibility(report)
    status = determine_status(ai_conf, repro, cvss)
    sla = RESPONSE_SLAS.get(severity, "best-effort")

    flags = []
    if ai_conf >= 0.4:
        flags.append("LIKELY_AI_GENERATED")
    if repro == "not_provided":
        flags.append("NO_POC")
    if cvss >= 9.0 and repro != "confirmed":
        flags.append("HIGH_SEVERITY_UNVERIFIED")

    result = TriageResult(
        report_id=report["id"],
        title=report["title"],
        severity_label=severity,
        cvss_estimate=cvss,
        ai_confidence=ai_conf,
        ai_signals=ai_signals,
        reproducibility=repro,
        status=status,
        response_draft="",  # filled below
        sla=sla,
        flags=flags,
    )
    result.response_draft = draft_response(report, result, templates)
    return result


# ── Display ────────────────────────────────────────────────────────────────

SEVERITY_COLORS = {
    "CRITICAL": "\033[91m",  # red
    "HIGH":     "\033[93m",  # yellow
    "MEDIUM":   "\033[33m",  # orange-ish
    "LOW":      "\033[92m",  # green
    "INFORMATIONAL": "\033[90m",  # gray
}
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

STATUS_ICONS = {
    Status.NEW: "  ",
    Status.ANALYZING: "  ",
    Status.CONFIRMED: "  ",
    Status.REJECTED: "  ",
    Status.NEEDS_INFO: "  ",
}


def print_header():
    print(f"\n{BOLD}{'='*78}")
    print(f"  OSS SECURITY REPORT TRIAGE ENGINE")
    print(f"  Helping maintainers survive the AI-generated report flood")
    print(f"{'='*78}{RESET}\n")


def print_queue_summary(results: list[TriageResult]):
    print(f"{BOLD}TRIAGE QUEUE SUMMARY{RESET}")
    print(f"{'-'*78}")

    by_status = {}
    for r in results:
        by_status.setdefault(r.status.value, []).append(r)

    for status_name in ["CONFIRMED", "ANALYZING", "NEEDS_INFO", "REJECTED"]:
        items = by_status.get(status_name, [])
        if items:
            print(f"\n  {BOLD}{status_name}{RESET} ({len(items)})")
            for r in items:
                color = SEVERITY_COLORS.get(r.severity_label, "")
                ai_tag = f" {DIM}[AI?]{RESET}" if r.ai_confidence >= 0.4 else ""
                print(f"    {color}[{r.severity_label:>13}]{RESET} {r.report_id} {r.title[:45]}{ai_tag}")

    print(f"\n{'-'*78}")
    total = len(results)
    rejected = len(by_status.get("REJECTED", []))
    confirmed = len(by_status.get("CONFIRMED", []))
    ai_flagged = sum(1 for r in results if r.ai_confidence >= 0.4)
    print(f"  Total: {total}  |  Confirmed: {confirmed}  |  Rejected: {rejected}  |  AI-flagged: {ai_flagged}")
    print()


def print_report_detail(r: TriageResult):
    color = SEVERITY_COLORS.get(r.severity_label, "")
    icon = STATUS_ICONS.get(r.status, "")

    print(f"{BOLD}{'- '*39}{RESET}")
    print(f"{BOLD}{r.report_id}: {r.title}{RESET}")
    print(f"  Severity:       {color}{r.severity_label} (CVSS ~{r.cvss_estimate}){RESET}")
    print(f"  Status:         {icon}{r.status.value}")
    print(f"  Reproducibility:{' ' + r.reproducibility}")
    print(f"  Response SLA:   {r.sla}")

    if r.ai_confidence >= 0.4:
        pct = int(r.ai_confidence * 100)
        print(f"  AI-generated:   {BOLD}{pct}% confidence{RESET}")
        for sig in r.ai_signals[:4]:
            print(f"    - {DIM}{sig}{RESET}")
        if len(r.ai_signals) > 4:
            print(f"    {DIM}  ...and {len(r.ai_signals)-4} more signals{RESET}")

    if r.flags:
        print(f"  Flags:          {', '.join(r.flags)}")

    print(f"\n  {DIM}--- Draft Response ---{RESET}")
    for line in r.response_draft.split("\n"):
        print(f"  {DIM}{line}{RESET}")
    print()


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    reports_path = os.path.join(script_dir, "mock_reports.json")
    templates_path = os.path.join(script_dir, "response_templates.json")

    with open(reports_path) as f:
        reports = json.load(f)
    with open(templates_path) as f:
        templates = json.load(f)

    print_header()

    # If a specific report ID is given as argument, triage just that one
    target_id = sys.argv[1] if len(sys.argv) > 1 else None

    results = []
    for report in reports:
        if target_id and report["id"] != target_id:
            continue
        result = triage_report(report, templates)
        results.append(result)

    if not results:
        print(f"No reports found{f' matching {target_id}' if target_id else ''}.")
        sys.exit(1)

    # Show queue overview first
    print_queue_summary(results)

    # Then show details for each report
    print(f"{BOLD}DETAILED TRIAGE RESULTS{RESET}\n")
    for r in results:
        print_report_detail(r)

    # Summary stats
    ai_count = sum(1 for r in results if r.ai_confidence >= 0.4)
    rejected = sum(1 for r in results if r.status == Status.REJECTED)
    print(f"{BOLD}MAINTAINER INSIGHT{RESET}")
    print(f"  {ai_count}/{len(results)} reports flagged as likely AI-generated")
    print(f"  {rejected}/{len(results)} reports auto-rejected (no PoC + high AI confidence)")
    actual = sum(1 for r in results if r.status in (Status.CONFIRMED, Status.ANALYZING))
    print(f"  {actual}/{len(results)} reports need human attention")
    saved_min = rejected * 30  # rough estimate: 30 min per manual review
    print(f"  Estimated time saved: ~{saved_min} minutes of manual review")
    print(f"\n  As Daniel Stenberg notes: report length != severity.")
    print(f"  Don't let a wall of text bias your assessment upward.\n")


if __name__ == "__main__":
    main()
