#!/usr/bin/env python3
"""AI Maintenance Cost Auditor

Audits code for maintenance cost factors using James Shore's inverse-rate principle:
if AI doubles your code output, maintenance costs must halve — or you're accumulating
debt faster than you're shipping.

Usage:
    python auditor.py <file_or_directory> [--speed-multiplier N]
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# --------------------------------------------------------------------------- #
# Maintenance-cost heuristics (static analysis, no LLM needed)
# --------------------------------------------------------------------------- #

@dataclass
class Finding:
    factor: str
    severity: str  # low / medium / high
    file: str
    line: Optional[int]
    message: str
    suggestion: str


@dataclass
class AuditResult:
    file: str
    lines_total: int
    findings: list[Finding] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)


# ---- Individual checkers -------------------------------------------------- #

def check_readability(lines: list[str], filepath: str) -> list[Finding]:
    findings = []
    for i, line in enumerate(lines, 1):
        # Excessively long lines
        if len(line.rstrip()) > 120:
            findings.append(Finding(
                "Readability", "medium", filepath, i,
                f"Line is {len(line.rstrip())} chars — hard to scan.",
                "Break into shorter statements or extract a helper."
            ))
        # Single-char variable names in non-trivial context
        if re.search(r'\b([a-z])\s*=\s*(?!.*\bfor\b)', line) and len(line.strip()) > 20:
            match = re.search(r'\b([a-z])\s*=', line)
            if match and match.group(1) not in ('i', 'j', 'k', 'x', 'y', '_'):
                findings.append(Finding(
                    "Readability", "low", filepath, i,
                    f"Single-char variable '{match.group(1)}' — intent unclear.",
                    "Use a descriptive name."
                ))
    return findings


def check_duplication(lines: list[str], filepath: str) -> list[Finding]:
    findings = []
    # Detect near-duplicate consecutive blocks (>= 3 identical non-blank lines)
    stripped = [l.strip() for l in lines]
    window = 3
    seen_blocks: dict[str, int] = {}
    for i in range(len(stripped) - window + 1):
        block = "\n".join(stripped[i:i + window])
        if all(stripped[i + j] for j in range(window)):  # skip blank blocks
            if block in seen_blocks:
                findings.append(Finding(
                    "Duplication", "high", filepath, i + 1,
                    f"Lines {i+1}-{i+window} duplicate lines {seen_blocks[block]}-{seen_blocks[block]+window-1}.",
                    "Extract into a shared function or loop."
                ))
            else:
                seen_blocks[block] = i + 1
    return findings


def check_dead_code(lines: list[str], filepath: str) -> list[Finding]:
    findings = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Commented-out code (heuristic: comment containing code-like tokens)
        if stripped.startswith('#') and re.search(r'(def |class |import |return |=\s)', stripped):
            findings.append(Finding(
                "Dead code", "medium", filepath, i,
                "Commented-out code left behind.",
                "Delete it — version control remembers."
            ))
        # Unused imports (very rough heuristic for Python)
        if stripped.startswith('import ') or stripped.startswith('from '):
            module = stripped.split()[-1].rstrip(',')
            rest = "\n".join(lines[i:])  # everything after the import
            if module not in rest:
                findings.append(Finding(
                    "Dead code", "medium", filepath, i,
                    f"Import '{module}' may be unused.",
                    "Remove unused imports."
                ))
    return findings


def check_complexity(lines: list[str], filepath: str) -> list[Finding]:
    findings = []
    indent_stack = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        # Deep nesting
        if indent >= 20:  # 5 levels at 4-space indent
            findings.append(Finding(
                "Complexity", "high", filepath, i,
                f"Deeply nested code (indent level {indent // 4}).",
                "Extract inner logic into a function or use early returns."
            ))
        # Long functions (heuristic: def to next def)
    func_starts = [(i, line) for i, line in enumerate(lines, 1)
                   if line.strip().startswith('def ')]
    for idx, (start, _) in enumerate(func_starts):
        end = func_starts[idx + 1][0] if idx + 1 < len(func_starts) else len(lines)
        length = end - start
        if length > 60:
            findings.append(Finding(
                "Complexity", "medium", filepath, start,
                f"Function is {length} lines long.",
                "Break into smaller, focused functions."
            ))
    return findings


def check_error_handling(lines: list[str], filepath: str) -> list[Finding]:
    findings = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Bare except
        if stripped in ('except:', 'except Exception:'):
            findings.append(Finding(
                "Error handling", "high", filepath, i,
                "Bare or overly broad except clause.",
                "Catch specific exceptions and handle them explicitly."
            ))
        # Swallowed errors: except ... pass
        if stripped == 'pass' and i >= 2 and 'except' in lines[i - 2]:
            findings.append(Finding(
                "Error handling", "high", filepath, i,
                "Exception caught and silently swallowed with pass.",
                "Log the error or let it propagate."
            ))
    return findings


def check_consistency(lines: list[str], filepath: str) -> list[Finding]:
    findings = []
    has_snake = bool(re.search(r'\bdef [a-z]+_[a-z]', "\n".join(lines)))
    has_camel = bool(re.search(r'\bdef [a-z]+[A-Z]', "\n".join(lines)))
    if has_snake and has_camel:
        findings.append(Finding(
            "Consistency", "medium", filepath, None,
            "Mixed naming conventions (snake_case and camelCase).",
            "Pick one style and stick with it."
        ))
    return findings


CHECKERS = [
    check_readability,
    check_duplication,
    check_dead_code,
    check_complexity,
    check_error_handling,
    check_consistency,
]


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #

SEVERITY_WEIGHTS = {"low": 0.05, "medium": 0.15, "high": 0.30}


def compute_maintenance_multiplier(result: AuditResult) -> float:
    """Return estimated maintenance multiplier (1.0 = same as hand-written)."""
    penalty = sum(SEVERITY_WEIGHTS.get(f.severity, 0.1) for f in result.findings)
    # Normalize by file size — a 500-line file with 2 findings is fine
    density = penalty / max(result.lines_total / 100, 1)
    # Map to multiplier: 0 findings → 0.8x (AI code is at least searchable),
    # many findings push above 1.0
    multiplier = round(0.8 + density, 2)
    return multiplier


def rate_verdict(speed: float, maintenance: float) -> str:
    product = speed * maintenance
    if product <= 1.0:
        return "SUSTAINABLE"
    elif product <= 2.0:
        return "RISKY"
    else:
        return "UNSUSTAINABLE"


# --------------------------------------------------------------------------- #
# Main audit pipeline
# --------------------------------------------------------------------------- #

def audit_file(filepath: str) -> AuditResult:
    with open(filepath, "r", errors="replace") as f:
        lines = f.readlines()

    result = AuditResult(file=filepath, lines_total=len(lines))

    for checker in CHECKERS:
        result.findings.extend(checker(lines, filepath))

    result.scores["maintenance_multiplier"] = compute_maintenance_multiplier(result)
    return result


def audit_path(target: str) -> list[AuditResult]:
    results = []
    target_path = Path(target)

    if target_path.is_file():
        if target_path.suffix in ('.py', '.js', '.ts', '.jsx', '.tsx'):
            results.append(audit_file(str(target_path)))
    elif target_path.is_dir():
        for ext in ('*.py', '*.js', '*.ts', '*.jsx', '*.tsx'):
            for f in sorted(target_path.rglob(ext)):
                if '.venv' not in str(f) and 'node_modules' not in str(f):
                    results.append(audit_file(str(f)))
    else:
        print(f"Error: {target} not found", file=sys.stderr)
        sys.exit(1)

    return results


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

SEVERITY_COLORS = {"low": "\033[33m", "medium": "\033[93m", "high": "\033[91m"}
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def print_report(results: list[AuditResult], speed_multiplier: float, use_color: bool = True):
    if not use_color:
        # Strip color codes
        global RESET, BOLD, GREEN, YELLOW, RED
        RESET = BOLD = GREEN = YELLOW = RED = ""
        for k in SEVERITY_COLORS:
            SEVERITY_COLORS[k] = ""

    total_findings = sum(len(r.findings) for r in results)
    total_lines = sum(r.lines_total for r in results)

    print(f"\n{BOLD}{'='*70}")
    print(f"  AI MAINTENANCE COST AUDIT REPORT")
    print(f"{'='*70}{RESET}\n")

    print(f"  Files scanned:     {len(results)}")
    print(f"  Total lines:       {total_lines}")
    print(f"  Findings:          {total_findings}")
    print(f"  Speed multiplier:  {speed_multiplier}x (assumed AI coding speed gain)\n")

    for result in results:
        mm = result.scores.get("maintenance_multiplier", 1.0)
        verdict = rate_verdict(speed_multiplier, mm)
        verdict_color = {"SUSTAINABLE": GREEN, "RISKY": YELLOW, "UNSUSTAINABLE": RED}[verdict]

        print(f"{BOLD}  {result.file}{RESET}  ({result.lines_total} lines)")
        print(f"    Maintenance multiplier: {mm}x")
        print(f"    Speed x Maintenance:    {round(speed_multiplier * mm, 2)}x  "
              f"[{verdict_color}{verdict}{RESET}]")

        if result.findings:
            print(f"    Findings:")
            for f in result.findings:
                sev_color = SEVERITY_COLORS.get(f.severity, "")
                loc = f"L{f.line}" if f.line else "file"
                print(f"      {sev_color}[{f.severity.upper():6s}]{RESET} "
                      f"{f.factor} @ {loc}: {f.message}")
                print(f"               Fix: {f.suggestion}")
        print()

    # Overall summary
    if results:
        avg_mm = round(sum(r.scores.get("maintenance_multiplier", 1.0) for r in results) / len(results), 2)
    else:
        avg_mm = 1.0
    overall_product = round(speed_multiplier * avg_mm, 2)
    overall_verdict = rate_verdict(speed_multiplier, avg_mm)
    verdict_color = {"SUSTAINABLE": GREEN, "RISKY": YELLOW, "UNSUSTAINABLE": RED}[overall_verdict]

    print(f"{BOLD}{'='*70}")
    print(f"  OVERALL VERDICT")
    print(f"{'='*70}{RESET}")
    print(f"\n  Average maintenance multiplier:  {avg_mm}x")
    print(f"  Speed multiplier:               {speed_multiplier}x")
    print(f"  Product (speed x maintenance):  {overall_product}x")
    print()
    print(f"  Shore's Rule: speed x maintenance must be <= 1.0")
    print(f"  Result: {verdict_color}{BOLD}{overall_verdict}{RESET}")
    print()

    if overall_verdict == "SUSTAINABLE":
        print(f"  {GREEN}The AI-generated code meets the maintenance cost bar.{RESET}")
    elif overall_verdict == "RISKY":
        print(f"  {YELLOW}Address the findings above before merging — the speed gain")
        print(f"  is being eroded by maintenance overhead.{RESET}")
    else:
        print(f"  {RED}The speed boost is illusory. Significant rework needed.")
        print(f"  You're trading a temporary speed boost for permanent indenture.{RESET}")

    print()
    return {"verdict": overall_verdict, "product": overall_product, "avg_maintenance": avg_mm}


def print_json(results: list[AuditResult], speed_multiplier: float):
    output = {
        "speed_multiplier": speed_multiplier,
        "files": [],
    }
    for r in results:
        mm = r.scores.get("maintenance_multiplier", 1.0)
        output["files"].append({
            "file": r.file,
            "lines": r.lines_total,
            "maintenance_multiplier": mm,
            "product": round(speed_multiplier * mm, 2),
            "verdict": rate_verdict(speed_multiplier, mm),
            "findings": [asdict(f) for f in r.findings],
        })
    avg_mm = round(sum(f["maintenance_multiplier"] for f in output["files"]) / max(len(output["files"]), 1), 2)
    output["overall"] = {
        "avg_maintenance_multiplier": avg_mm,
        "product": round(speed_multiplier * avg_mm, 2),
        "verdict": rate_verdict(speed_multiplier, avg_mm),
    }
    print(json.dumps(output, indent=2))


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(
        description="Audit AI-generated code for maintenance cost impact."
    )
    parser.add_argument("target", help="File or directory to audit")
    parser.add_argument("--speed", type=float, default=3.0,
                        help="AI speed multiplier (default: 3.0)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable colored output")
    args = parser.parse_args()

    results = audit_path(args.target)

    if not results:
        print("No supported files found to audit.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print_json(results, args.speed)
    else:
        print_report(results, args.speed, use_color=not args.no_color)


if __name__ == "__main__":
    main()
