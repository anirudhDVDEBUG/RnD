#!/usr/bin/env python3
"""
Vibe Coding vs Agentic Engineering Review Tool

Analyzes code diffs against Simon Willison's framework for responsible
AI-assisted programming. Flags anti-patterns common in AI-generated code
and rates changes on a vibe-coding-to-agentic-engineering spectrum.
"""

import re
import sys
import textwrap
from dataclasses import dataclass, field


@dataclass
class Finding:
    category: str
    severity: str  # "info", "warning", "critical"
    message: str
    line_hint: str = ""


@dataclass
class ReviewResult:
    name: str
    context: str
    classification: str  # "ship-it", "needs-revision", "start-over"
    score: int  # 0-100, 100 = perfect agentic engineering
    findings: list = field(default_factory=list)
    summary: str = ""


# --- Detectors ---

def detect_nested_try_except(diff_text: str) -> list[Finding]:
    """Flag cargo-culted nested try/except blocks."""
    findings = []
    lines = diff_text.split("\n")
    try_depth = 0
    for line in lines:
        stripped = line.lstrip("+").strip()
        if stripped.startswith("try:"):
            try_depth += 1
            if try_depth > 1:
                findings.append(Finding(
                    category="AI Anti-pattern",
                    severity="warning",
                    message="Nested try/except detected — likely cargo-culted error handling",
                    line_hint=line.strip(),
                ))
        elif stripped.startswith("except"):
            try_depth = max(0, try_depth - 1)
    return findings


def detect_broad_except(diff_text: str) -> list[Finding]:
    """Flag bare 'except Exception' that leaks debug info."""
    findings = []
    for line in diff_text.split("\n"):
        if not line.startswith("+"):
            continue
        stripped = line.lstrip("+").strip()
        if re.match(r"except\s+(Exception|BaseException)\s*(as\s+\w+)?:", stripped):
            findings.append(Finding(
                category="AI Anti-pattern",
                severity="warning",
                message="Broad except clause — consider catching specific exceptions",
                line_hint=stripped,
            ))
    return findings


def detect_security_issues(diff_text: str) -> list[Finding]:
    """Flag common security problems in AI-generated code."""
    findings = []
    for line in diff_text.split("\n"):
        if not line.startswith("+"):
            continue
        stripped = line.lstrip("+").strip()

        if "md5(" in stripped or "hashlib.md5" in stripped:
            findings.append(Finding(
                category="Security",
                severity="critical",
                message="MD5 used for hashing — insecure for passwords, use bcrypt/argon2",
                line_hint=stripped,
            ))

        if re.search(r"""['"]debug['"]\s*:\s*str\(""", stripped, re.IGNORECASE):
            findings.append(Finding(
                category="Security",
                severity="critical",
                message="Debug info leaked in error response — remove before production",
                line_hint=stripped,
            ))

        if re.search(r"""SECRET_KEY\s*=\s*['"](?!os\.getenv)""", stripped):
            findings.append(Finding(
                category="Security",
                severity="warning",
                message="Hardcoded secret key — use environment variable instead",
                line_hint=stripped,
            ))
    return findings


def detect_scope_creep(diff_text: str) -> list[Finding]:
    """Flag signs the AI went beyond what was asked."""
    findings = []
    added = [l for l in diff_text.split("\n") if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in diff_text.split("\n") if l.startswith("-") and not l.startswith("---")]

    # Large ratio of removed-to-added lines suggests rewrite
    if len(removed) > 5 and len(added) > len(removed) * 2:
        findings.append(Finding(
            category="Scope Creep",
            severity="warning",
            message=f"Significant rewrite detected ({len(removed)} lines removed, {len(added)} added) — verify all changes were requested",
        ))

    # Detect added docstrings/comments that weren't part of the ask
    docstring_additions = sum(1 for l in added if '"""' in l or "'''" in l)
    if docstring_additions >= 2:
        findings.append(Finding(
            category="Scope Creep",
            severity="info",
            message="Multiple docstrings added — check if documentation was part of the request",
        ))

    # Detect added type annotations
    type_hint_lines = sum(1 for l in added if re.search(r":\s*Final\[|:\s*Optional\[|:\s*List\[|:\s*Dict\[", l))
    if type_hint_lines >= 3:
        findings.append(Finding(
            category="Scope Creep",
            severity="info",
            message=f"Type annotations added to {type_hint_lines} lines — verify this was requested",
        ))

    return findings


def detect_missing_tests(diff_text: str) -> list[Finding]:
    """Check if the diff includes test changes alongside implementation."""
    findings = []
    has_impl = bool(re.search(r"^\+\+\+ b/(?!tests?/)", diff_text, re.MULTILINE))
    has_tests = bool(re.search(r"^\+\+\+ b/tests?/", diff_text, re.MULTILINE))

    if has_impl and not has_tests:
        findings.append(Finding(
            category="Test Coverage",
            severity="warning",
            message="Implementation changes with no corresponding test changes — agentic engineering requires tests",
        ))
    elif has_impl and has_tests:
        findings.append(Finding(
            category="Test Coverage",
            severity="info",
            message="Tests included alongside implementation — good agentic practice",
        ))
    return findings


def detect_hallucinated_imports(diff_text: str) -> list[Finding]:
    """Flag suspicious import patterns common in AI-generated code."""
    findings = []
    for line in diff_text.split("\n"):
        if not line.startswith("+"):
            continue
        stripped = line.lstrip("+").strip()

        # Flag imports from the same project that look auto-generated
        if re.match(r"from app\.\w+ import .+,.+,.+,.+", stripped):
            findings.append(Finding(
                category="AI Anti-pattern",
                severity="info",
                message="Many imports from single module — verify all are actually used",
                line_hint=stripped,
            ))
    return findings


def detect_over_abstraction(diff_text: str) -> list[Finding]:
    """Flag unnecessary helpers/utilities for one-time operations."""
    findings = []
    added = [l.lstrip("+") for l in diff_text.split("\n") if l.startswith("+")]
    new_functions = [l for l in added if re.match(r"\s*def \w+", l)]
    new_classes = [l for l in added if re.match(r"\s*class \w+", l)]

    if len(new_functions) > 4:
        findings.append(Finding(
            category="Over-abstraction",
            severity="info",
            message=f"{len(new_functions)} new functions added in one diff — check if all are necessary",
        ))
    if len(new_classes) > 2:
        findings.append(Finding(
            category="Over-abstraction",
            severity="warning",
            message=f"{len(new_classes)} new classes added — might be over-engineered for the task",
        ))
    return findings


# --- Scoring & Classification ---

SEVERITY_WEIGHTS = {"info": 3, "warning": 10, "critical": 25}

ALL_DETECTORS = [
    detect_nested_try_except,
    detect_broad_except,
    detect_security_issues,
    detect_scope_creep,
    detect_missing_tests,
    detect_hallucinated_imports,
    detect_over_abstraction,
]


def review_diff(name: str, diff_text: str, context: str = "production") -> ReviewResult:
    """Run all detectors on a diff and produce a scored review."""
    findings = []
    for detector in ALL_DETECTORS:
        findings.extend(detector(diff_text))

    # Calculate score (start at 100, subtract for issues)
    penalty = sum(SEVERITY_WEIGHTS[f.severity] for f in findings)
    score = max(0, 100 - penalty)

    # Throwaway context gets a bonus — we're more lenient
    if context == "throwaway":
        score = min(100, score + 30)

    # Classify
    if score >= 75:
        classification = "ship-it"
    elif score >= 40:
        classification = "needs-revision"
    else:
        classification = "start-over"

    # Build summary
    critical = [f for f in findings if f.severity == "critical"]
    warnings = [f for f in findings if f.severity == "warning"]
    infos = [f for f in findings if f.severity == "info"]

    if context == "throwaway" and score >= 60:
        summary = "Throwaway/prototype context — vibe coding acceptable. Ship if it works."
    elif not findings:
        summary = "Clean diff. Follows agentic engineering practices."
    elif critical:
        summary = f"Critical issues found. Do NOT merge without fixing: {critical[0].message}"
    elif warnings:
        summary = f"Review needed. Key concern: {warnings[0].message}"
    else:
        summary = "Minor observations only. Likely ready after quick check."

    return ReviewResult(
        name=name,
        context=context,
        classification=classification,
        score=score,
        findings=findings,
        summary=summary,
    )


# --- Output Formatting ---

SEVERITY_ICONS = {"info": "[.]", "warning": "[!]", "critical": "[X]"}
CLASS_LABELS = {
    "ship-it": "SHIP IT",
    "needs-revision": "NEEDS REVISION",
    "start-over": "START OVER",
}


def format_review(result: ReviewResult) -> str:
    """Format a ReviewResult as readable terminal output."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  REVIEW: {result.name}")
    lines.append(f"  Context: {result.context} | Score: {result.score}/100 | Verdict: {CLASS_LABELS[result.classification]}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Summary: {result.summary}")
    lines.append("")

    if result.findings:
        lines.append("  Findings:")
        lines.append("  " + "-" * 50)
        for f in result.findings:
            icon = SEVERITY_ICONS[f.severity]
            lines.append(f"  {icon} [{f.category}] {f.message}")
            if f.line_hint:
                hint = textwrap.shorten(f.line_hint, width=60, placeholder="...")
                lines.append(f"        -> {hint}")
        lines.append("")
    else:
        lines.append("  No issues found.")
        lines.append("")

    # Score bar
    filled = result.score // 5
    bar = "#" * filled + "." * (20 - filled)
    lines.append(f"  Quality: [{bar}] {result.score}/100")
    lines.append("")
    return "\n".join(lines)


def main():
    """Run the review tool on sample diffs."""
    from sample_diffs import SAMPLES

    print()
    print("  Vibe Coding vs Agentic Engineering — Code Review Tool")
    print("  Based on Simon Willison's framework (May 2026)")
    print()

    results = []
    for sample in SAMPLES:
        result = review_diff(
            name=sample["name"],
            diff_text=sample["diff"],
            context=sample.get("context", "production"),
        )
        results.append(result)
        print(format_review(result))

    # Summary table
    print("=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"  {'Diff':<35} {'Score':>6}  {'Verdict':<16} Context")
    print("  " + "-" * 66)
    for r in results:
        print(f"  {r.name:<35} {r.score:>4}/100  {CLASS_LABELS[r.classification]:<16} {r.context}")
    print()

    ship = sum(1 for r in results if r.classification == "ship-it")
    revise = sum(1 for r in results if r.classification == "needs-revision")
    block = sum(1 for r in results if r.classification == "start-over")
    print(f"  Totals: {ship} ship, {revise} need revision, {block} blocked")
    print()

    # Return non-zero if any production code is blocked
    prod_blocked = any(r.classification == "start-over" and r.context == "production" for r in results)
    sys.exit(1 if prod_blocked else 0)


if __name__ == "__main__":
    main()
