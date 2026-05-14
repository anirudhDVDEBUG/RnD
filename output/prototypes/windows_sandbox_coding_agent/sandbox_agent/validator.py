"""Validates agent-produced file changes against safety rules."""

import fnmatch
from pathlib import Path
from dataclasses import dataclass

from .config import SafetyRules


@dataclass
class ValidationResult:
    passed: bool
    violations: list[str]

    def __str__(self):
        if self.passed:
            return "PASS: All changes within safety bounds."
        return "FAIL:\n" + "\n".join(f"  - {v}" for v in self.violations)


def validate_changes(changed_files: list[dict], rules: SafetyRules) -> ValidationResult:
    """
    Validate a list of file changes against safety rules.

    Each entry in changed_files: {"path": str, "size_bytes": int, "action": "add"|"modify"|"delete"}
    """
    violations = []

    # Check total file count
    if len(changed_files) > rules.max_files_changed:
        violations.append(
            f"Too many files changed: {len(changed_files)} > {rules.max_files_changed}"
        )

    for f in changed_files:
        path = f["path"]
        size = f.get("size_bytes", 0)
        ext = Path(path).suffix

        # Check extension
        if ext and ext not in rules.allowed_extensions:
            violations.append(f"Disallowed extension '{ext}' in: {path}")

        # Check blocked patterns
        for pattern in rules.blocked_patterns:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(Path(path).name, pattern):
                violations.append(f"Blocked path pattern '{pattern}' matched: {path}")

        # Check file size
        if size > rules.max_file_size_bytes:
            violations.append(
                f"File too large ({size:,} bytes > {rules.max_file_size_bytes:,}): {path}"
            )

    return ValidationResult(passed=len(violations) == 0, violations=violations)
