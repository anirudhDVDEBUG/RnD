#!/usr/bin/env python3
"""
Anthropic Grade Optimizer — Audit Claude-directing artifacts against
189 cited Anthropic rules across 11 dimensions.
"""

import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field

from rules import RULES, DIMENSIONS


@dataclass
class Finding:
    dimension: str
    severity: str  # PASS, WARN, FAIL
    line_num: int
    line_text: str
    rule_id: str
    rule_desc: str
    suggestion: str = ""


@dataclass
class AuditReport:
    artifact_name: str
    artifact_type: str
    findings: list = field(default_factory=list)
    voice_drift: bool = False
    dimension_results: dict = field(default_factory=dict)


def detect_artifact_type(filepath: str, content: str) -> str:
    name = Path(filepath).name.upper()
    if "CLAUDE.MD" in name:
        return "CLAUDE.md"
    if "SKILL.MD" in name:
        return "SKILL.md"
    if "settings.json" in filepath:
        return "Hook/Config"
    if "mcp" in filepath.lower():
        return "MCP Config"
    if content.strip().startswith("{") or content.strip().startswith("["):
        return "JSON Config"
    return "Prompt File"


def check_voice_drift(lines: list) -> list:
    """Detect tone shifts between imperative and conversational registers."""
    findings = []
    imperative_markers = re.compile(
        r"^[-*]?\s*(Always|Never|Do not|Don't|Use|Avoid|Keep|Ensure|Provide|Include)\b",
        re.IGNORECASE
    )
    conversational_markers = re.compile(
        r"\b(you might|you could|feel free|you may want|don't worry|it's okay|keep it casual)\b",
        re.IGNORECASE
    )

    tone_sequence = []
    for i, line in enumerate(lines):
        if imperative_markers.search(line):
            tone_sequence.append(("imperative", i + 1, line.strip()))
        elif conversational_markers.search(line):
            tone_sequence.append(("conversational", i + 1, line.strip()))

    # Detect drift: any switch from one tone to another
    for idx in range(1, len(tone_sequence)):
        prev_tone, _, _ = tone_sequence[idx - 1]
        curr_tone, line_num, line_text = tone_sequence[idx]
        if prev_tone != curr_tone:
            findings.append(Finding(
                dimension="Voice Alignment",
                severity="FAIL",
                line_num=line_num,
                line_text=line_text,
                rule_id="§4.2",
                rule_desc="No mixing imperative and conversational tone",
                suggestion=f"Rewrite in uniform imperative tone to match surrounding directives"
            ))
            break  # Report first drift point

    return findings


def check_completeness(content: str, artifact_type: str) -> list:
    """Check for required sections based on artifact type."""
    findings = []
    content_lower = content.lower()

    if artifact_type == "CLAUDE.md":
        required = {
            "role": "§5.1",
            "error": "§5.3",
            "constraint": "§5.2",
        }
        for section, rule_id in required.items():
            # Check for section header or keyword presence
            if f"## {section}" not in content_lower and section not in content_lower:
                rule = next((r for r in RULES if r["id"] == rule_id), None)
                findings.append(Finding(
                    dimension="Completeness",
                    severity="WARN",
                    line_num=0,
                    line_text="(missing section)",
                    rule_id=rule_id,
                    rule_desc=rule["desc"] if rule else "",
                    suggestion=f"Add a section addressing: {section}"
                ))

    return findings


def check_structure(lines: list) -> list:
    """Verify markdown structure and hierarchy."""
    findings = []
    has_headers = any(line.startswith("#") for line in lines)
    if not has_headers:
        findings.append(Finding(
            dimension="Structure",
            severity="WARN",
            line_num=1,
            line_text="(entire file)",
            rule_id="§2.1",
            rule_desc="Use markdown headers for section organization",
            suggestion="Add markdown headers to organize content into sections"
        ))
    return findings


def check_pattern_rules(lines: list) -> list:
    """Run regex-based rule checks against all lines."""
    findings = []
    for i, line in enumerate(lines):
        for rule in RULES:
            if not rule.get("patterns"):
                continue
            for pattern in rule["patterns"]:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(Finding(
                        dimension=rule["dim"],
                        severity="WARN" if rule["dim"] != "Voice Alignment" else "FAIL",
                        line_num=i + 1,
                        line_text=line.strip(),
                        rule_id=rule["id"],
                        rule_desc=rule["desc"],
                        suggestion=f"Revise to comply with {rule['id']}: {rule['desc']}"
                    ))
                    break  # One finding per rule per line
    return findings


def check_tool_vagueness(lines: list) -> list:
    """Check for vague tool-use instructions."""
    findings = []
    for i, line in enumerate(lines):
        if re.search(r"\b(when appropriate|when needed|as necessary)\b", line, re.IGNORECASE):
            if any(kw in line.lower() for kw in ["tool", "use them", "use it"]):
                findings.append(Finding(
                    dimension="Tool Use",
                    severity="WARN",
                    line_num=i + 1,
                    line_text=line.strip(),
                    rule_id="§8.2",
                    rule_desc="Define when to use each tool",
                    suggestion="Replace vague trigger with specific conditions for tool invocation"
                ))
    return findings


def compute_grade(findings: list) -> str:
    """Compute letter grade from findings."""
    fail_count = sum(1 for f in findings if f.severity == "FAIL")
    warn_count = sum(1 for f in findings if f.severity == "WARN")

    score = 100 - (fail_count * 15) - (warn_count * 5)
    if score >= 93:
        return "A"
    elif score >= 90:
        return "A-"
    elif score >= 87:
        return "B+"
    elif score >= 83:
        return "B"
    elif score >= 80:
        return "B-"
    elif score >= 77:
        return "C+"
    elif score >= 73:
        return "C"
    elif score >= 70:
        return "C-"
    elif score >= 60:
        return "D"
    else:
        return "F"


def compute_dimension_results(findings: list) -> dict:
    """Determine PASS/WARN/FAIL per dimension."""
    results = {}
    for dim in DIMENSIONS:
        dim_findings = [f for f in findings if f.dimension == dim]
        if any(f.severity == "FAIL" for f in dim_findings):
            results[dim] = "FAIL"
        elif any(f.severity == "WARN" for f in dim_findings):
            results[dim] = "WARN"
        else:
            results[dim] = "PASS"
    return results


def audit_file(filepath: str) -> AuditReport:
    """Run full audit on a file."""
    path = Path(filepath)
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    artifact_type = detect_artifact_type(filepath, content)
    report = AuditReport(
        artifact_name=path.name,
        artifact_type=artifact_type,
    )

    # Run all checks
    report.findings.extend(check_pattern_rules(lines))
    report.findings.extend(check_voice_drift(lines))
    report.findings.extend(check_completeness(content, artifact_type))
    report.findings.extend(check_structure(lines))
    report.findings.extend(check_tool_vagueness(lines))

    # Determine voice drift
    report.voice_drift = any(
        f.dimension == "Voice Alignment" and f.severity == "FAIL"
        for f in report.findings
    )

    # Compute dimension results
    report.dimension_results = compute_dimension_results(report.findings)

    return report


def format_report(report: AuditReport, as_json: bool = False) -> str:
    """Format audit report for display."""
    if as_json:
        return json.dumps({
            "artifact": report.artifact_name,
            "type": report.artifact_type,
            "grade": compute_grade(report.findings),
            "voice_drift": report.voice_drift,
            "dimensions": report.dimension_results,
            "findings": [
                {
                    "dimension": f.dimension,
                    "severity": f.severity,
                    "line": f.line_num,
                    "rule": f.rule_id,
                    "description": f.rule_desc,
                    "text": f.line_text,
                    "suggestion": f.suggestion,
                }
                for f in report.findings
            ],
        }, indent=2)

    grade = compute_grade(report.findings)
    passing = sum(1 for v in report.dimension_results.values() if v == "PASS")
    critical = sum(1 for f in report.findings if f.severity == "FAIL")

    lines = []
    lines.append("=" * 60)
    lines.append("ANTHROPIC GRADE OPTIMIZER — Audit Report")
    lines.append("=" * 60)
    lines.append(f"Artifact: {report.artifact_name}")
    lines.append(f"Artifact type: {report.artifact_type}")
    lines.append("")
    lines.append("SUMMARY")
    lines.append(f"  Overall grade: {grade}")
    lines.append(f"  Dimensions passing: {passing}/11")
    lines.append(f"  Critical findings: {critical}")
    lines.append(f"  Voice drift detected: {'Yes' if report.voice_drift else 'No'}")
    lines.append("")
    lines.append("FINDINGS BY DIMENSION")
    lines.append("")

    for i, dim in enumerate(DIMENSIONS, 1):
        result = report.dimension_results.get(dim, "PASS")
        dim_findings = [f for f in report.findings if f.dimension == dim]

        marker = ""
        if result == "FAIL":
            marker = " *** CRITICAL ***"

        lines.append(f"  {i}. {dim} [{result}]{marker}")

        if dim_findings:
            for f in dim_findings:
                if f.line_num > 0:
                    lines.append(f"     Line {f.line_num}: \"{f.line_text}\"")
                else:
                    lines.append(f"     {f.line_text}")
                lines.append(f"     Rule: {f.rule_id} — {f.rule_desc}")
                if f.suggestion:
                    lines.append(f"     Fix: {f.suggestion}")
                lines.append("")
        else:
            lines.append(f"     No issues found.")
            lines.append("")

    # Recommended fixes (priority: FAIL first, then WARN)
    sorted_findings = sorted(report.findings, key=lambda f: (0 if f.severity == "FAIL" else 1, f.line_num))
    if sorted_findings:
        lines.append("RECOMMENDED FIXES (priority order)")
        lines.append("")
        for i, f in enumerate(sorted_findings[:5], 1):
            loc = f"Line {f.line_num}" if f.line_num > 0 else "Global"
            lines.append(f"  {i}. [{f.dimension}] {loc}: {f.suggestion}")
            lines.append(f"     Rule: {f.rule_id}")
            lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit.py <file> [--json]")
        sys.exit(1)

    filepath = sys.argv[1]
    as_json = "--json" in sys.argv

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    report = audit_file(filepath)
    print(format_report(report, as_json=as_json))


if __name__ == "__main__":
    main()
