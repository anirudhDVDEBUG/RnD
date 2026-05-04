#!/usr/bin/env python3
"""
Skill Validator — Audit any SKILL.md file against a 100-point rubric.
Produces a scored markdown report with critical issues, warnings, and exact fixes.
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    name: str
    category: str
    max_points: int
    points: int = 0
    passed: bool = False
    message: str = ""
    fix: str = ""
    severity: str = "warning"  # "critical" or "warning"


@dataclass
class AuditReport:
    file_path: str
    checks: list = field(default_factory=list)

    @property
    def total_score(self) -> int:
        return sum(c.points for c in self.checks)

    @property
    def max_score(self) -> int:
        return sum(c.max_points for c in self.checks)

    @property
    def grade(self) -> str:
        s = self.total_score
        if s >= 90:
            return "A"
        elif s >= 80:
            return "B"
        elif s >= 70:
            return "C"
        elif s >= 60:
            return "D"
        return "F"

    def category_score(self, category: str) -> tuple:
        earned = sum(c.points for c in self.checks if c.category == category)
        maximum = sum(c.max_points for c in self.checks if c.category == category)
        return earned, maximum


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    current_key = None
    current_value_lines = []
    for line in match.group(1).split("\n"):
        # Simple key: value
        kv = re.match(r"^(\w[\w_-]*):\s*(.*)", line)
        if kv:
            if current_key:
                fm[current_key] = "\n".join(current_value_lines).strip()
            current_key = kv.group(1)
            val = kv.group(2).strip()
            if val == "|" or val == ">":
                current_value_lines = []
            else:
                current_value_lines = [val]
        elif current_key and line.startswith("  "):
            current_value_lines.append(line.strip())
    if current_key:
        fm[current_key] = "\n".join(current_value_lines).strip()
    return fm


def find_section(content: str, heading: str) -> str:
    """Extract content under a specific markdown heading."""
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
    if not match:
        # Try partial match
        pattern = rf"^##\s+.*{re.escape(heading)}.*$"
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if not match:
            return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", content[start:], re.MULTILINE)
    if next_heading:
        return content[start : start + next_heading.start()].strip()
    return content[start:].strip()


def audit_skill(content: str, file_path: str) -> AuditReport:
    """Run the full audit checklist against a SKILL.md file."""
    report = AuditReport(file_path=file_path)
    fm = parse_frontmatter(content)

    # ── Structure (25 pts) ──

    # Check: valid frontmatter with name and description (10 pts)
    has_fm = bool(fm)
    has_name = "name" in fm and bool(fm["name"])
    has_desc = "description" in fm and bool(fm["description"])
    check = CheckResult(
        name="Valid YAML frontmatter with name and description",
        category="Structure",
        max_points=10,
    )
    if has_fm and has_name and has_desc:
        check.points = 10
        check.passed = True
    elif has_fm and (has_name or has_desc):
        missing = "description" if not has_desc else "name"
        check.points = 4
        check.message = f"Frontmatter missing `{missing}` field"
        check.fix = f"Add `{missing}: <value>` to the YAML frontmatter block"
        check.severity = "critical"
    else:
        check.message = "Missing or invalid YAML frontmatter"
        check.fix = 'Add frontmatter: ---\\nname: my_skill\\ndescription: |\\n  Description with TRIGGER clause\\n---'
        check.severity = "critical"
    report.checks.append(check)

    # Check: name is snake_case, <=60 chars (5 pts)
    check = CheckResult(
        name="Name is snake_case and <=60 characters",
        category="Structure",
        max_points=5,
    )
    if has_name:
        name_val = fm["name"]
        is_snake = bool(re.match(r"^[a-z][a-z0-9_]*$", name_val))
        is_short = len(name_val) <= 60
        if is_snake and is_short:
            check.points = 5
            check.passed = True
        elif not is_snake:
            check.message = f"Name `{name_val}` is not snake_case"
            snake = re.sub(r"[^a-z0-9]+", "_", name_val.lower()).strip("_")
            check.fix = f"Rename to `{snake}`"
            check.severity = "critical"
        else:
            check.points = 2
            check.message = f"Name is {len(name_val)} chars (max 60)"
            check.fix = "Shorten the name to 60 characters or fewer"
    else:
        check.message = "No name field found"
        check.fix = "Add a `name` field in snake_case to frontmatter"
        check.severity = "critical"
    report.checks.append(check)

    # Check: description includes TRIGGER clause (10 pts)
    check = CheckResult(
        name="Description includes a TRIGGER clause",
        category="Structure",
        max_points=10,
    )
    desc = fm.get("description", "")
    has_trigger = bool(re.search(r"TRIGGER", desc, re.IGNORECASE))
    if has_trigger:
        check.points = 10
        check.passed = True
    else:
        check.message = "Description lacks a TRIGGER clause"
        check.fix = 'Add "TRIGGER: user says ..." to the description field specifying when the skill activates'
        check.severity = "critical"
    report.checks.append(check)

    # ── Content Quality (35 pts) ──

    # Check: "When to use" section with 3-5 trigger phrases (10 pts)
    when_section = find_section(content, "When to use")
    check = CheckResult(
        name='"When to use" section with 3-5 trigger phrases',
        category="Content Quality",
        max_points=10,
    )
    if when_section:
        bullets = re.findall(r"^[-*]\s+.+", when_section, re.MULTILINE)
        if len(bullets) >= 3:
            check.points = 10
            check.passed = True
        elif len(bullets) >= 1:
            check.points = 5
            check.message = f"Only {len(bullets)} trigger phrase(s); aim for 3-5"
            check.fix = "Add more concrete trigger phrases (e.g., user utterances in quotes)"
        else:
            check.points = 3
            check.message = "Section exists but has no bullet-point trigger phrases"
            check.fix = 'Add 3-5 bullets starting with "-" showing example user phrases'
    else:
        check.message = 'Missing "When to use" section'
        check.fix = 'Add a "## When to use" section with 3-5 bullet-point trigger phrases'
        check.severity = "critical"
    report.checks.append(check)

    # Check: "How to use" section with numbered steps (10 pts)
    how_section = find_section(content, "How to use")
    check = CheckResult(
        name='"How to use" section with numbered steps',
        category="Content Quality",
        max_points=10,
    )
    if how_section:
        numbered = re.findall(r"^\d+\.\s+.+", how_section, re.MULTILINE)
        if len(numbered) >= 2:
            check.points = 10
            check.passed = True
        elif len(numbered) >= 1:
            check.points = 5
            check.message = "Only 1 numbered step; add more detail"
            check.fix = "Break the process into 2+ numbered, actionable steps"
        else:
            check.points = 3
            check.message = "Section exists but lacks numbered steps"
            check.fix = 'Use "1. Step one\\n2. Step two" format for actionable steps'
    else:
        check.message = 'Missing "How to use" section'
        check.fix = 'Add a "## How to use" section with numbered, actionable steps'
        check.severity = "critical"
    report.checks.append(check)

    # Check: Steps reference real tools/commands (5 pts)
    check = CheckResult(
        name="Steps reference real tools or commands",
        category="Content Quality",
        max_points=5,
    )
    tool_patterns = [
        r"`[^`]+`",  # inline code
        r"```",  # code blocks
        r"\b(Read|Write|Edit|Bash|Glob|Grep|Agent)\b",  # Claude tools
        r"\b(pip|npm|git|curl|docker)\b",
    ]
    if how_section:
        has_tools = any(re.search(p, how_section) for p in tool_patterns)
        if has_tools:
            check.points = 5
            check.passed = True
        else:
            check.message = "Steps don't reference specific tools or commands"
            check.fix = "Add inline code (`tool_name`) or code blocks showing exact commands"
    else:
        check.message = 'No "How to use" section to evaluate'
        check.fix = 'Add a "How to use" section with tool references'
    report.checks.append(check)

    # Check: "References" section (5 pts)
    ref_section = find_section(content, "References")
    check = CheckResult(
        name='"References" section with source links',
        category="Content Quality",
        max_points=5,
    )
    if ref_section:
        has_links = bool(re.search(r"\[.*?\]\(.*?\)|https?://", ref_section))
        if has_links:
            check.points = 5
            check.passed = True
        else:
            check.points = 2
            check.message = "References section exists but contains no links"
            check.fix = "Add markdown links [text](url) to source material"
    else:
        check.message = 'Missing "References" section'
        check.fix = 'Add a "## References" section with links to source repos or docs'
    report.checks.append(check)

    # Check: No placeholder/TODO content (5 pts)
    check = CheckResult(
        name="No placeholder or TODO content",
        category="Content Quality",
        max_points=5,
    )
    placeholders = re.findall(
        r"\bTODO\b|\bFIXME\b|\bXXX\b|\bplaceholder\b|\bTBD\b|\blorem ipsum\b",
        content,
        re.IGNORECASE,
    )
    if not placeholders:
        check.points = 5
        check.passed = True
    else:
        found = ", ".join(set(p.upper() for p in placeholders))
        check.message = f"Found placeholder markers: {found}"
        check.fix = "Replace all placeholder content with real information"
        check.severity = "critical"
    report.checks.append(check)

    # ── Best Practices (25 pts) ──

    # Check: Self-contained (10 pts)
    check = CheckResult(
        name="Self-contained (no unguarded external dependencies)",
        category="Best Practices",
        max_points=10,
    )
    ext_patterns = [
        r"requires?\s+(?:an?\s+)?API\s+key",
        r"must\s+(?:be\s+)?(?:running|installed|configured)",
        r"external\s+service",
        r"sign\s+up",
    ]
    has_ext = any(re.search(p, content, re.IGNORECASE) for p in ext_patterns)
    has_fallback = bool(
        re.search(r"fallback|mock|offline|optional|if\s+unavailable", content, re.IGNORECASE)
    )
    if not has_ext:
        check.points = 10
        check.passed = True
    elif has_fallback:
        check.points = 7
        check.message = "References external services but provides fallback"
        check.passed = True
    else:
        check.points = 3
        check.message = "Depends on external services without documented fallback"
        check.fix = "Add fallback behavior or note that external services are optional"
    report.checks.append(check)

    # Check: Follows Anthropic skill conventions (10 pts)
    check = CheckResult(
        name="Follows Anthropic skill conventions",
        category="Best Practices",
        max_points=10,
    )
    conventions_met = 0
    if has_fm:
        conventions_met += 1
    if has_name:
        conventions_met += 1
    if has_desc:
        conventions_met += 1
    if when_section:
        conventions_met += 1
    if how_section:
        conventions_met += 1
    score_map = {5: 10, 4: 8, 3: 6, 2: 4, 1: 2, 0: 0}
    check.points = score_map.get(conventions_met, 0)
    check.passed = conventions_met >= 4
    if conventions_met < 5:
        missing = []
        if not has_fm:
            missing.append("frontmatter")
        if not has_name:
            missing.append("name field")
        if not has_desc:
            missing.append("description field")
        if not when_section:
            missing.append('"When to use" section')
        if not how_section:
            missing.append('"How to use" section')
        check.message = f"Missing convention elements: {', '.join(missing)}"
        check.fix = "Add the missing sections to match the Anthropic skill template"
    report.checks.append(check)

    # Check: No security anti-patterns (5 pts)
    check = CheckResult(
        name="No security anti-patterns",
        category="Best Practices",
        max_points=5,
    )
    sec_issues = []
    if re.search(r"(?:sk-|key-|token=)[a-zA-Z0-9]{20,}", content):
        sec_issues.append("possible hardcoded API key/token")
    if re.search(r"rm\s+-rf\s+/|sudo\s+rm|chmod\s+777", content):
        sec_issues.append("dangerous shell command pattern")
    if re.search(r"eval\s*\(|exec\s*\(", content):
        sec_issues.append("eval/exec usage")
    if not sec_issues:
        check.points = 5
        check.passed = True
    else:
        check.message = f"Security concerns: {'; '.join(sec_issues)}"
        check.fix = "Remove hardcoded secrets, avoid dangerous shell patterns"
        check.severity = "critical"
    report.checks.append(check)

    # ── Trigger Reliability (15 pts) ──

    # Check: TRIGGER clause specific enough (8 pts)
    check = CheckResult(
        name="TRIGGER clause is specific (avoids false positives)",
        category="Trigger Reliability",
        max_points=8,
    )
    if has_trigger:
        trigger_match = re.search(r"TRIGGER[:\s]+(.*?)(?:\n|$)", desc, re.IGNORECASE)
        trigger_text = trigger_match.group(1) if trigger_match else ""
        has_quotes = bool(re.search(r'"[^"]+"|"[^"]+"|\'[^\']+\'', trigger_text))
        word_count = len(trigger_text.split())
        if has_quotes and word_count >= 5:
            check.points = 8
            check.passed = True
        elif word_count >= 5:
            check.points = 5
            check.message = "TRIGGER clause could be more specific with quoted phrases"
            check.fix = 'Add quoted example phrases: TRIGGER: user says "validate skill", "audit SKILL.md"'
        else:
            check.points = 3
            check.message = "TRIGGER clause is too brief to avoid false positives"
            check.fix = "Expand the TRIGGER clause with specific quoted phrases and contexts"
    else:
        check.message = "No TRIGGER clause found"
        check.fix = 'Add TRIGGER: user says "..." to the description'
        check.severity = "critical"
    report.checks.append(check)

    # Check: TRIGGER covers core use cases (7 pts)
    check = CheckResult(
        name="TRIGGER covers core use cases from When to use",
        category="Trigger Reliability",
        max_points=7,
    )
    if has_trigger and when_section:
        bullets = re.findall(r"^[-*]\s+(.+)", when_section, re.MULTILINE)
        # Extract key words from bullets
        bullet_keywords = set()
        for b in bullets:
            words = re.findall(r"[a-z]{4,}", b.lower())
            bullet_keywords.update(words)
        # Check overlap with trigger
        trigger_match = re.search(r"TRIGGER[:\s]+(.*?)(?:\n|$)", desc, re.IGNORECASE)
        trigger_text = (trigger_match.group(1) if trigger_match else "").lower()
        trigger_words = set(re.findall(r"[a-z]{4,}", trigger_text))
        overlap = bullet_keywords & trigger_words
        coverage = len(overlap) / max(len(bullet_keywords), 1)
        if coverage >= 0.3:
            check.points = 7
            check.passed = True
        elif coverage > 0:
            check.points = 4
            check.message = "TRIGGER partially covers use cases"
            check.fix = "Add more trigger keywords that match your 'When to use' examples"
        else:
            check.points = 1
            check.message = "TRIGGER keywords don't align with 'When to use' section"
            check.fix = "Ensure TRIGGER clause includes terms from your use-case examples"
    elif not has_trigger:
        check.message = "No TRIGGER clause to evaluate"
        check.fix = "Add a TRIGGER clause that covers the use cases in 'When to use'"
        check.severity = "critical"
    else:
        check.points = 3
        check.message = "Cannot cross-check: missing 'When to use' section"
        check.fix = 'Add a "When to use" section to enable cross-validation'
    report.checks.append(check)

    return report


def format_report(report: AuditReport) -> str:
    """Format the audit report as markdown."""
    lines = []
    lines.append("## SKILL.md Audit Report\n")
    lines.append(f"**File:** {report.file_path}")
    lines.append(f"**Score:** {report.total_score}/{report.max_score} ({report.grade})\n")

    # Critical issues
    criticals = [c for c in report.checks if not c.passed and c.severity == "critical"]
    if criticals:
        lines.append("### Critical Issues\n")
        for c in criticals:
            lines.append(f"- {c.message} → **Fix:** {c.fix}")
        lines.append("")

    # Warnings
    warnings = [
        c for c in report.checks if not c.passed and c.severity == "warning" and c.message
    ]
    if warnings:
        lines.append("### Warnings\n")
        for c in warnings:
            lines.append(f"- {c.message} → **Suggestion:** {c.fix}")
        lines.append("")

    # Passed
    passed = [c for c in report.checks if c.passed]
    if passed:
        lines.append("### Passed Checks\n")
        for c in passed:
            lines.append(f"- ✅ {c.name}")
        lines.append("")

    # Score breakdown
    categories = ["Structure", "Content Quality", "Best Practices", "Trigger Reliability"]
    lines.append("### Score Breakdown\n")
    lines.append("| Category            | Score | Max |")
    lines.append("|---------------------|-------|-----|")
    for cat in categories:
        earned, maximum = report.category_score(cat)
        lines.append(f"| {cat:<19} | {earned:<5} | {maximum:<3} |")
    lines.append(
        f"| **Total**           | **{report.total_score}** | **{report.max_score}** |"
    )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit a SKILL.md file for quality and best practices.")
    parser.add_argument("file", nargs="?", default="SKILL.md", help="Path to SKILL.md (default: ./SKILL.md)")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of markdown")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    report = audit_skill(content, str(path))

    if args.json:
        import json

        data = {
            "file": report.file_path,
            "score": report.total_score,
            "max_score": report.max_score,
            "grade": report.grade,
            "checks": [
                {
                    "name": c.name,
                    "category": c.category,
                    "points": c.points,
                    "max_points": c.max_points,
                    "passed": c.passed,
                    "message": c.message,
                    "fix": c.fix,
                    "severity": c.severity,
                }
                for c in report.checks
            ],
        }
        print(json.dumps(data, indent=2))
    else:
        print(format_report(report))

    sys.exit(0 if report.total_score >= 80 else 1)


if __name__ == "__main__":
    main()
