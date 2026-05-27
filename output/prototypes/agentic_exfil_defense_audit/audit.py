#!/usr/bin/env python3
"""
Agentic Exfiltration Defense Audit

Scans agentic AI system configurations and code for data exfiltration
vulnerabilities — the "lethal trifecta" pattern where an agent has:
  1. Access to untrusted input (prompt injection vector)
  2. Access to sensitive data (files, credentials, tokens)
  3. An exfiltration channel (email, rendered images, API calls)

Inspired by the Microsoft Copilot Cowork vulnerability disclosure.
"""

import json
import re
import sys
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pathlib import Path


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Finding:
    title: str
    severity: Severity
    category: str
    description: str
    location: str
    recommendation: str
    trifecta_leg: Optional[str] = None  # "input", "data", "channel"


@dataclass
class AuditReport:
    target: str
    findings: list = field(default_factory=list)
    trifecta_inputs: list = field(default_factory=list)
    trifecta_data: list = field(default_factory=list)
    trifecta_channels: list = field(default_factory=list)

    @property
    def has_lethal_trifecta(self) -> bool:
        return bool(self.trifecta_inputs and self.trifecta_data and self.trifecta_channels)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.HIGH)


# --- Pattern Definitions ---

UNTRUSTED_INPUT_PATTERNS = [
    (r'(?i)(process|read|parse|handle).*?(email|mail|message|inbox)', 'Email processing'),
    (r'(?i)(fetch|load|read|parse).*?(document|file|attachment|upload)', 'Document ingestion'),
    (r'(?i)(scrape|crawl|fetch).*?(web|url|page|site)', 'Web content fetching'),
    (r'(?i)(user|external).*?(input|query|prompt|message)', 'User/external input'),
    (r'(?i)untrusted|user.provided|external.content', 'Untrusted content marker'),
    (r'(?i)(slack|discord|teams).*?(message|channel|webhook)', 'Chat platform input'),
]

SENSITIVE_DATA_PATTERNS = [
    (r'(?i)(onedrive|sharepoint|gdrive|dropbox).*?(file|link|url|download)', 'Cloud storage access'),
    (r'(?i)(pre.?auth|signed.?url|sas.?token|presigned)', 'Pre-authenticated URL generation'),
    (r'(?i)(credential|password|secret|token|api.?key)', 'Credential access'),
    (r'(?i)(database|db|sql).*?(query|read|select|connect)', 'Database access'),
    (r'(?i)(file|fs|path).*?(read|open|access|list)', 'File system access'),
    (r'(?i)(env|environment).*?(var|variable|secret)', 'Environment variable access'),
    (r'(?i)(private|internal|confidential|sensitive)', 'Sensitive data marker'),
]

EXFIL_CHANNEL_PATTERNS = [
    (r'(?i)(send|compose|draft|reply).*?(email|mail|smtp)', 'Email sending'),
    (r'(?i)(render|display).*?(html|markdown|image|img)', 'HTML/Markdown rendering'),
    (r'(?i)<img\s+src\s*=', 'Image tag rendering'),
    (r'(?i)!\[.*?\]\(https?://', 'Markdown image with external URL'),
    (r'(?i)(fetch|request|call|post|get).*?(api|endpoint|url|webhook)', 'External API calls'),
    (r'(?i)(slack|discord|teams).*?(send|post|webhook)', 'Chat platform output'),
    (r'(?i)(log|write).*?(external|remote|cloud)', 'Remote logging'),
    (r'(?i)window\.location|document\.cookie|navigator\.sendBeacon', 'Browser exfiltration'),
    (r'(?i)(iframe|script|link\s+rel.*?prefetch)', 'Resource loading tags'),
    (r'(?i)url\s*\(', 'CSS url() reference'),
]

AUTO_ACTION_PATTERNS = [
    (r'(?i)auto.?(send|reply|forward|respond)', 'Auto-send action'),
    (r'(?i)without.?(approval|confirmation|review|consent)', 'No-approval action'),
    (r'(?i)(skip|bypass|disable).*?(confirm|approval|review)', 'Approval bypass'),
    (r'(?i)auto.?(create|generate).*?(link|url|share)', 'Auto link creation'),
    (r'(?i)(background|async|cron|schedule).*?(send|post|upload)', 'Background action'),
]

MISSING_MITIGATION_CHECKS = [
    ('content.security.policy|CSP', 'Content Security Policy'),
    ('sanitize|escape|strip.*?tag|bleach|DOMPurify', 'Output sanitization'),
    ('allowlist|whitelist|approved.?domain', 'Domain allowlisting'),
    ('rate.?limit|throttle', 'Rate limiting on output'),
    ('approval|confirm|human.?in.?loop|HITL', 'Human approval gate'),
    ('sandbox|iframe.*?sandbox', 'Output sandboxing'),
]


def scan_content(content: str, filename: str, report: AuditReport):
    """Scan a single file's content for exfiltration patterns."""
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        loc = f"{filename}:{line_num}"

        # Check untrusted inputs
        for pattern, label in UNTRUSTED_INPUT_PATTERNS:
            if re.search(pattern, line):
                report.trifecta_inputs.append(label)
                report.findings.append(Finding(
                    title=f"Untrusted input: {label}",
                    severity=Severity.MEDIUM,
                    category="Untrusted Input Vector",
                    description=f"Agent processes untrusted input via {label.lower()}.",
                    location=loc,
                    recommendation="Isolate untrusted input processing from sensitive data context.",
                    trifecta_leg="input",
                ))

        # Check sensitive data access
        for pattern, label in SENSITIVE_DATA_PATTERNS:
            if re.search(pattern, line):
                report.trifecta_data.append(label)
                sev = Severity.HIGH if 'pre' in label.lower() or 'credential' in label.lower() else Severity.MEDIUM
                report.findings.append(Finding(
                    title=f"Sensitive data access: {label}",
                    severity=sev,
                    category="Sensitive Data Exposure",
                    description=f"Agent has access to {label.lower()} in same context as untrusted input.",
                    location=loc,
                    recommendation="Minimize data access scope; avoid pre-authenticated URLs in agent context.",
                    trifecta_leg="data",
                ))

        # Check exfiltration channels
        for pattern, label in EXFIL_CHANNEL_PATTERNS:
            if re.search(pattern, line):
                report.trifecta_channels.append(label)
                report.findings.append(Finding(
                    title=f"Exfiltration channel: {label}",
                    severity=Severity.HIGH,
                    category="Exfiltration Channel",
                    description=f"Agent output includes {label.lower()}, which could leak embedded data.",
                    location=loc,
                    recommendation="Block external resource loading in agent output rendering.",
                    trifecta_leg="channel",
                ))

        # Check auto-actions (escalates severity)
        for pattern, label in AUTO_ACTION_PATTERNS:
            if re.search(pattern, line):
                report.findings.append(Finding(
                    title=f"Unsupervised action: {label}",
                    severity=Severity.CRITICAL,
                    category="Auto-Action Without Approval",
                    description=f"Agent can {label.lower()} without human approval — critical exfil enabler.",
                    location=loc,
                    recommendation="Require explicit user approval for ALL external-facing actions.",
                    trifecta_leg="channel",
                ))

    # Check for missing mitigations
    full_text = content.lower()
    for pattern, label in MISSING_MITIGATION_CHECKS:
        if not re.search(pattern, full_text, re.IGNORECASE):
            report.findings.append(Finding(
                title=f"Missing mitigation: {label}",
                severity=Severity.LOW,
                category="Missing Defense",
                description=f"No evidence of {label.lower()} in {filename}.",
                location=filename,
                recommendation=f"Implement {label.lower()} to reduce exfiltration risk.",
            ))


def scan_json_config(config: dict, filename: str, report: AuditReport):
    """Scan a JSON config for dangerous agent permissions."""
    config_str = json.dumps(config, indent=2).lower()

    dangerous_perms = {
        'send_email': 'Email sending permission',
        'send_mail': 'Email sending permission',
        'file_read': 'File read permission',
        'file_access': 'File access permission',
        'web_request': 'Web request permission',
        'external_api': 'External API permission',
        'create_link': 'Link creation permission',
        'share_file': 'File sharing permission',
    }

    for perm, label in dangerous_perms.items():
        if perm in config_str:
            sev = Severity.CRITICAL if 'email' in perm or 'share' in perm else Severity.HIGH
            report.findings.append(Finding(
                title=f"Dangerous agent permission: {label}",
                severity=sev,
                category="Excessive Permission",
                description=f"Agent config grants {label.lower()} — potential exfiltration enabler.",
                location=filename,
                recommendation="Remove or gate this permission behind human approval.",
            ))

    # Check for approval_required flags
    if 'approval_required' in config_str and '"false"' in config_str:
        report.findings.append(Finding(
            title="Approval explicitly disabled",
            severity=Severity.CRITICAL,
            category="Auto-Action Without Approval",
            description="Agent config explicitly disables approval for actions.",
            location=filename,
            recommendation="Set approval_required to true for all external-facing actions.",
        ))

    # Check rendering config
    if any(k in config_str for k in ['render_html', 'render_markdown', 'allow_images']):
        if 'external' in config_str or 'allow_images' in config_str:
            report.findings.append(Finding(
                title="External content rendering enabled",
                severity=Severity.HIGH,
                category="Exfiltration Channel",
                description="Agent output renders external images/HTML — classic exfil vector.",
                location=filename,
                recommendation="Disable external image loading; use CSP to restrict resource origins.",
                trifecta_leg="channel",
            ))


def scan_directory(path: str) -> AuditReport:
    """Scan a directory of files for exfiltration risks."""
    report = AuditReport(target=path)
    scan_extensions = {'.py', '.js', '.ts', '.yaml', '.yml', '.json', '.toml', '.md', '.txt', '.cfg', '.ini', '.conf'}

    target = Path(path)
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = [f for f in target.rglob('*') if f.suffix in scan_extensions and f.is_file()]
    else:
        print(f"Error: {path} not found")
        sys.exit(1)

    for filepath in sorted(files):
        rel_path = str(filepath)
        try:
            content = filepath.read_text(errors='replace')
        except Exception:
            continue

        scan_content(content, rel_path, report)

        if filepath.suffix == '.json':
            try:
                config = json.loads(content)
                scan_json_config(config, rel_path, report)
            except json.JSONDecodeError:
                pass

    return report


def render_report(report: AuditReport) -> str:
    """Render the audit report as formatted text."""
    lines = []
    lines.append("=" * 70)
    lines.append("  AGENTIC EXFILTRATION DEFENSE AUDIT REPORT")
    lines.append("=" * 70)
    lines.append(f"  Target: {report.target}")
    lines.append(f"  Findings: {len(report.findings)}")
    lines.append(f"  Critical: {report.critical_count}  |  High: {report.high_count}")
    lines.append("")

    # Lethal trifecta assessment
    lines.append("-" * 70)
    if report.has_lethal_trifecta:
        lines.append("  !! LETHAL TRIFECTA DETECTED !!")
        lines.append("")
        lines.append("  All three conditions for data exfiltration are present:")
    else:
        missing = []
        if not report.trifecta_inputs:
            missing.append("untrusted input processing")
        if not report.trifecta_data:
            missing.append("sensitive data access")
        if not report.trifecta_channels:
            missing.append("exfiltration channel")
        lines.append("  Lethal trifecta: INCOMPLETE (missing: " + ", ".join(missing) + ")")
        lines.append("")
        lines.append("  Trifecta status:")

    inputs_uniq = sorted(set(report.trifecta_inputs))
    data_uniq = sorted(set(report.trifecta_data))
    channels_uniq = sorted(set(report.trifecta_channels))

    mark = lambda items: "[X]" if items else "[ ]"
    lines.append(f"  {mark(inputs_uniq)} Untrusted Input:      {', '.join(inputs_uniq[:3]) or 'none detected'}")
    lines.append(f"  {mark(data_uniq)} Sensitive Data:       {', '.join(data_uniq[:3]) or 'none detected'}")
    lines.append(f"  {mark(channels_uniq)} Exfiltration Channel: {', '.join(channels_uniq[:3]) or 'none detected'}")
    lines.append("")

    # Findings by severity
    for sev in Severity:
        sev_findings = [f for f in report.findings if f.severity == sev]
        if not sev_findings:
            continue
        lines.append("-" * 70)
        lines.append(f"  [{sev.value}] ({len(sev_findings)} findings)")
        lines.append("-" * 70)
        # Deduplicate by title
        seen = set()
        for f in sev_findings:
            if f.title in seen:
                continue
            seen.add(f.title)
            lines.append(f"  * {f.title}")
            lines.append(f"    Category: {f.category}")
            lines.append(f"    Location: {f.location}")
            lines.append(f"    {f.description}")
            lines.append(f"    -> {f.recommendation}")
            lines.append("")

    # Mitigation checklist
    lines.append("=" * 70)
    lines.append("  MITIGATION CHECKLIST")
    lines.append("=" * 70)
    mitigations = [
        "Require explicit user approval for ALL external-facing actions",
        "Strip or sandbox external resource references in agent output",
        "Use Content Security Policy to block image/resource exfiltration",
        "Never render agent output with external image loading enabled",
        "Avoid generating pre-authenticated URLs in agent context",
        "Separate untrusted input processing from sensitive data access",
        "Log and monitor all outbound requests from agent output rendering",
        "Apply output filtering to detect encoded data in URLs",
    ]
    for m in mitigations:
        lines.append(f"  [ ] {m}")

    lines.append("")
    lines.append("=" * 70)
    lines.append(f"  Scan complete. {report.critical_count} critical, {report.high_count} high severity findings.")
    if report.has_lethal_trifecta:
        lines.append("  ACTION REQUIRED: Lethal trifecta present — exfiltration is possible.")
    lines.append("=" * 70)
    return "\n".join(lines)


def render_json_report(report: AuditReport) -> str:
    """Render as JSON for programmatic consumption."""
    return json.dumps({
        "target": report.target,
        "lethal_trifecta": report.has_lethal_trifecta,
        "trifecta": {
            "untrusted_inputs": sorted(set(report.trifecta_inputs)),
            "sensitive_data": sorted(set(report.trifecta_data)),
            "exfil_channels": sorted(set(report.trifecta_channels)),
        },
        "summary": {
            "total": len(report.findings),
            "critical": report.critical_count,
            "high": report.high_count,
        },
        "findings": [
            {
                "title": f.title,
                "severity": f.severity.value,
                "category": f.category,
                "description": f.description,
                "location": f.location,
                "recommendation": f.recommendation,
            }
            for f in report.findings
        ],
    }, indent=2)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Audit agentic AI systems for data exfiltration vulnerabilities"
    )
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--output", "-o", help="Write report to file")
    args = parser.parse_args()

    report = scan_directory(args.target)

    if args.json:
        output = render_json_report(report)
    else:
        output = render_report(report)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Report written to {args.output}")
    else:
        print(output)

    # Exit code: 2 if trifecta, 1 if critical findings, 0 otherwise
    if report.has_lethal_trifecta:
        sys.exit(2)
    elif report.critical_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
