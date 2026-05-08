#!/usr/bin/env python3
"""
Report generator for the LLM Vulnerability Research Harness.

Outputs findings in a clear, actionable format modeled on real security
advisory reports. Supports text (terminal) and JSON output.
"""

from vuln_harness import Finding

# ANSI color codes for terminal output
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

SEVERITY_COLOR = {
    "Critical": RED,
    "High": YELLOW,
    "Medium": CYAN,
    "Low": GREEN,
}

SEVERITY_ICON = {
    "Critical": "[!!]",
    "High": "[!] ",
    "Medium": "[~] ",
    "Low": "[.] ",
}


def severity_badge(severity: str) -> str:
    color = SEVERITY_COLOR.get(severity, RESET)
    icon = SEVERITY_ICON.get(severity, "    ")
    return f"{color}{BOLD}{icon} {severity}{RESET}"


def print_finding(idx: int, f: Finding) -> None:
    print(f"\n{'='*72}")
    print(f"  {severity_badge(f.severity)}  {BOLD}{f.vuln_class}{RESET}")
    print(f"{'='*72}")
    print(f"  {DIM}Location:{RESET}  {f.file}:{f.line}  in  {BOLD}{f.function}(){RESET}")
    print(f"  {DIM}Pass:{RESET}      {f.pass_number}  |  Validated: {'Yes' if f.validated else 'No'}")
    print()
    print(f"  {BOLD}Description{RESET}")
    _wrap_print(f.description, indent=4)
    print()
    print(f"  {BOLD}Root Cause{RESET}")
    _wrap_print(f.root_cause, indent=4)
    print()
    print(f"  {BOLD}Trigger Scenario{RESET}")
    _wrap_print(f.trigger, indent=4)
    print()
    print(f"  {BOLD}Suggested Fix{RESET}")
    _wrap_print(f.suggested_fix, indent=4)

    if f.mitigations:
        print()
        print(f"  {BOLD}Existing Mitigations{RESET}")
        for m in f.mitigations:
            print(f"    - {m}")


def _wrap_print(text: str, indent: int = 4, width: int = 68) -> None:
    prefix = " " * indent
    words = text.split()
    line = prefix
    for word in words:
        if len(line) + len(word) + 1 > width:
            print(line)
            line = prefix + word
        else:
            line = line + " " + word if line.strip() else prefix + word
    if line.strip():
        print(line)


def print_summary(findings: list[Finding]) -> None:
    counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    print(f"\n{'='*72}")
    print(f"  {BOLD}SCAN SUMMARY{RESET}")
    print(f"{'='*72}")
    print(f"  Total validated findings: {BOLD}{len(findings)}{RESET}")
    for sev in ["Critical", "High", "Medium", "Low"]:
        if sev in counts:
            print(f"    {severity_badge(sev)}: {counts[sev]}")

    files = set(f.file for f in findings)
    print(f"\n  Files scanned with findings: {len(files)}")
    for fp in sorted(files):
        n = sum(1 for f in findings if f.file == fp)
        print(f"    {fp}  ({n} finding{'s' if n != 1 else ''})")

    vuln_classes = set(f.vuln_class for f in findings)
    print(f"\n  Vulnerability classes detected: {len(vuln_classes)}")
    for vc in sorted(vuln_classes):
        n = sum(1 for f in findings if f.vuln_class == vc)
        print(f"    {vc}  ({n})")


def print_methodology_note() -> None:
    print(f"\n{DIM}{'─'*72}")
    print(f"  Methodology: Steer / Scale / Stack  (Mozilla Firefox approach)")
    print(f"  Pass 1 — Broad pattern scan across all files")
    print(f"  Pass 2 — Validate reachability and exploitability")
    print(f"  Pass 3 — Generate actionable reports (this output)")
    print(f"{'─'*72}{RESET}")


def print_report(findings: list[Finding]) -> None:
    print(f"\n{BOLD}{'#'*72}")
    print(f"  LLM VULNERABILITY RESEARCH HARNESS — SCAN REPORT")
    print(f"{'#'*72}{RESET}")

    print_methodology_note()

    if not findings:
        print(f"\n  {GREEN}No validated findings.{RESET}")
        return

    for i, f in enumerate(findings, 1):
        print_finding(i, f)

    print_summary(findings)

    print(f"\n{DIM}  Note: In production, each pass is an LLM call with focused prompts.")
    print(f"  This demo uses pattern-matching heuristics to illustrate the pipeline.{RESET}\n")
