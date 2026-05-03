"""
Design linting hooks for Claude Code.

These hooks check generated UI code for common design consistency issues:
  - Missing responsive breakpoints
  - Hardcoded colors (should use design tokens)
  - Accessibility issues (missing alt, aria-label)
  - Inconsistent spacing values
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class LintIssue:
    rule: str
    severity: str  # "error" | "warning" | "info"
    line: int
    message: str
    suggestion: str

    def __str__(self):
        icon = {"error": "X", "warning": "!", "info": "i"}[self.severity]
        return f"  [{icon}] L{self.line}: {self.message}\n      -> {self.suggestion}"


def lint_html(html: str) -> List[LintIssue]:
    """Run design consistency checks on HTML content."""
    issues: List[LintIssue] = []
    lines = html.split("\n")

    for i, line in enumerate(lines, 1):
        # Hardcoded hex colours in inline styles
        if re.search(r'style="[^"]*#[0-9a-fA-F]{3,8}', line):
            issues.append(LintIssue(
                rule="no-hardcoded-colors",
                severity="warning",
                line=i,
                message="Hardcoded color in inline style",
                suggestion="Use CSS variable (var(--color-primary-500)) or Tailwind class instead",
            ))

        # Images without alt attribute
        if re.search(r'<img\b', line) and not re.search(r'\balt=', line):
            issues.append(LintIssue(
                rule="img-alt",
                severity="error",
                line=i,
                message="<img> missing alt attribute",
                suggestion='Add alt="description" for accessibility',
            ))

        # Buttons / links without accessible text
        if re.search(r'<button[^>]*>\s*</button>', line):
            issues.append(LintIssue(
                rule="button-text",
                severity="error",
                line=i,
                message="Empty <button> element",
                suggestion="Add visible text or aria-label for screen readers",
            ))

        # Hardcoded pixel values for spacing (except in border/shadow contexts)
        px_matches = re.findall(r'(?:margin|padding|gap):\s*\d+px', line)
        for match in px_matches:
            issues.append(LintIssue(
                rule="no-hardcoded-spacing",
                severity="warning",
                line=i,
                message=f"Hardcoded pixel spacing: {match}",
                suggestion="Use spacing tokens (var(--spacing-md)) or Tailwind classes (p-4, gap-6)",
            ))

        # Missing responsive classes (check for bare grid/flex without breakpoint)
        if "grid-cols-" in line and "md:grid-cols" not in line and "lg:grid-cols" not in line:
            issues.append(LintIssue(
                rule="responsive-grid",
                severity="info",
                line=i,
                message="Grid without responsive breakpoints",
                suggestion="Add md: and lg: variants for responsive layouts (e.g., md:grid-cols-2 lg:grid-cols-3)",
            ))

    return issues


def lint_report(html: str, filename: str = "input.html") -> str:
    """Generate a human-readable lint report."""
    issues = lint_html(html)
    if not issues:
        return f"  {filename}: All checks passed (0 issues)"

    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        counts[issue.severity] += 1

    lines = [f"  {filename}: {len(issues)} issue(s) — {counts['error']} errors, {counts['warning']} warnings, {counts['info']} info"]
    for issue in issues:
        lines.append(str(issue))
    return "\n".join(lines)
