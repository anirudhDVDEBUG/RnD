#!/usr/bin/env python3
"""
Token Cost Lint — Static Audit Engine
Zero-LLM-call token waste detector for multi-agent Claude Code harnesses.

Usage:
    python audit.py --target /path/to/project [--format report|json] [--compare baseline.json]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

from taxonomy import TAXONOMY, SEVERITY, RESET_COLOR, get_all_sub_patterns


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".md", ".yaml", ".yml",
    ".json", ".toml", ".sh", ".bash", ".txt",
}

SKIP_DIRS = {
    "node_modules", "__pycache__", ".git", ".venv", "venv",
    "dist", "build", ".next", ".cache",
}


def collect_files(target: str) -> list[Path]:
    """Walk target directory and collect scannable files."""
    target_path = Path(target).resolve()
    files = []
    for root, dirs, filenames in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            fp = Path(root) / f
            if fp.suffix in SCAN_EXTENSIONS:
                files.append(fp)
    return sorted(files)


def read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Detection functions (zero-LLM, static rules)
# ---------------------------------------------------------------------------

class AuditEngine:
    def __init__(self, target: str):
        self.target = Path(target).resolve()
        self.files = collect_files(target)
        self.file_contents: dict[Path, str] = {}
        self.findings: list[dict] = []
        self.stats = {
            "files_scanned": 0,
            "total_lines": 0,
            "estimated_tokens": 0,
            "waste_tokens": 0,
        }

        # Pre-load all file contents
        for f in self.files:
            content = read_file_safe(f)
            self.file_contents[f] = content
            self.stats["files_scanned"] += 1
            self.stats["total_lines"] += content.count("\n") + 1
            # Rough token estimate: ~4 chars per token
            self.stats["estimated_tokens"] += len(content) // 4

    def run_audit(self) -> dict:
        """Run all detection passes and return results."""
        self._detect_redundant_context()
        self._detect_oversized_prompts()
        self._detect_unbounded_history()
        self._detect_duplicate_tool_results()
        self._detect_verbose_output()
        self._detect_unnecessary_rereads()
        self._detect_broad_file_inclusion()
        self._detect_uncompressed_examples()
        self._detect_idle_agent_overhead()
        self._detect_retry_amplification()

        # Calculate waste totals
        self.stats["waste_tokens"] = sum(f.get("estimated_waste_tokens", 0) for f in self.findings)
        if self.stats["estimated_tokens"] > 0:
            self.stats["waste_percentage"] = round(
                self.stats["waste_tokens"] / self.stats["estimated_tokens"] * 100, 1
            )
        else:
            self.stats["waste_percentage"] = 0

        return {
            "target": str(self.target),
            "stats": self.stats,
            "findings": self.findings,
            "summary": self._build_summary(),
        }

    def _add_finding(self, category_id: int, sub_pattern_id: str, file: Path,
                     line: int, message: str, waste_tokens: int, severity: str = "medium"):
        cat_key = [k for k, v in TAXONOMY.items() if v["id"] == category_id][0]
        self.findings.append({
            "category_id": category_id,
            "category": TAXONOMY[cat_key]["name"],
            "sub_pattern": sub_pattern_id,
            "file": str(file.relative_to(self.target)) if file != Path("-") else "-",
            "line": line,
            "message": message,
            "estimated_waste_tokens": waste_tokens,
            "severity": severity,
        })

    # --- Category 1: Redundant Context ---
    def _detect_redundant_context(self):
        file_read_map = defaultdict(list)
        read_patterns = [
            re.compile(r"""(?:read_file|Read|open)\s*\(\s*['"](.+?)['"]"""),
            re.compile(r"""(?:Read|cat)\s+(\S+\.\w+)"""),
        ]
        for fp, content in self.file_contents.items():
            for i, line in enumerate(content.splitlines(), 1):
                for pat in read_patterns:
                    for m in pat.finditer(line):
                        file_read_map[m.group(1)].append((fp, i))

        for read_target, locations in file_read_map.items():
            if len(locations) > 1:
                waste = 500 * (len(locations) - 1)
                self._add_finding(
                    1, "1a", locations[0][0], locations[0][1],
                    f"'{read_target}' read {len(locations)} times across files — "
                    f"consider caching",
                    waste, "high" if len(locations) > 2 else "medium",
                )

    # --- Category 2: Oversized Prompts ---
    def _detect_oversized_prompts(self):
        boilerplate = re.compile(
            r"(You are a helpful|Please be concise|Think step by step|"
            r"Answer carefully|Be thorough|Take a deep breath)",
            re.IGNORECASE,
        )
        role_def = re.compile(r"(You are |Your role is |Act as )", re.IGNORECASE)

        for fp, content in self.file_contents.items():
            lines = content.splitlines()
            # Detect boilerplate
            for i, line in enumerate(lines, 1):
                for m in boilerplate.finditer(line):
                    self._add_finding(
                        2, "2a", fp, i,
                        f"Boilerplate phrase '{m.group(0)}' — likely adds no value",
                        len(m.group(0)) // 4 + 10, "low",
                    )

            # Detect multiple role definitions
            role_lines = [(i, m.group(0)) for i, line in enumerate(lines, 1)
                          for m in role_def.finditer(line)]
            if len(role_lines) > 1:
                self._add_finding(
                    2, "2b", fp, role_lines[0][0],
                    f"Role defined {len(role_lines)} times in same file",
                    50 * (len(role_lines) - 1), "medium",
                )

            # Detect long prompt-like strings
            for i, line in enumerate(lines, 1):
                if len(line) > 500 and any(kw in line.lower() for kw in
                    ["system", "prompt", "instruction", "you are"]):
                    self._add_finding(
                        2, "2d", fp, i,
                        f"Line has {len(line)} chars — potential oversized prompt "
                        f"(~{len(line)//4} tokens)",
                        len(line) // 8, "high",
                    )

    # --- Category 3: Unbounded History ---
    def _detect_unbounded_history(self):
        append_pat = re.compile(r"messages\s*\.append\(|messages\s*\+=|messages\.extend\(")
        truncate_pat = re.compile(r"messages\s*=\s*messages\[|truncat|window|max_messages|slim")

        for fp, content in self.file_contents.items():
            appends = [(i, m) for i, line in enumerate(content.splitlines(), 1)
                       for m in append_pat.finditer(line)]
            has_truncation = bool(truncate_pat.search(content))

            if appends and not has_truncation:
                self._add_finding(
                    3, "3a", fp, appends[0][0],
                    f"Messages appended ({len(appends)}x) but no truncation/windowing found",
                    200 * len(appends), "critical",
                )

    # --- Category 4: Duplicate Tool Results ---
    def _detect_duplicate_tool_results(self):
        tool_pat = re.compile(r"(?:tool_call|function_call|tool_use)\s*\(")
        cache_pat = re.compile(r"cache|memoize|lru_cache|functools\.cache")

        for fp, content in self.file_contents.items():
            calls = tool_pat.findall(content)
            has_cache = bool(cache_pat.search(content))
            if len(calls) > 2 and not has_cache:
                self._add_finding(
                    4, "4b", fp, 1,
                    f"{len(calls)} tool calls without any caching mechanism",
                    100 * len(calls), "high",
                )

    # --- Category 5: Verbose Output ---
    def _detect_verbose_output(self):
        echo_pat = re.compile(r"(You asked|Your question|Let me repeat|As you mentioned)",
                              re.IGNORECASE)
        for fp, content in self.file_contents.items():
            for i, line in enumerate(content.splitlines(), 1):
                for m in echo_pat.finditer(line):
                    self._add_finding(
                        5, "5c", fp, i,
                        f"Input echo pattern: '{m.group(0)}' — wastes tokens repeating user input",
                        30, "low",
                    )

    # --- Category 6: Unnecessary Re-reads ---
    def _detect_unnecessary_rereads(self):
        read_pat = re.compile(r"(?:read_file|open)\s*\(\s*['\"](.+?)['\"]\s*\)")
        for fp, content in self.file_contents.items():
            reads = defaultdict(list)
            for i, line in enumerate(content.splitlines(), 1):
                for m in read_pat.finditer(line):
                    reads[m.group(1)].append(i)
            for target_file, lines in reads.items():
                if len(lines) > 1:
                    self._add_finding(
                        6, "6a", fp, lines[0],
                        f"'{target_file}' read {len(lines)} times in same file "
                        f"(lines {', '.join(map(str, lines))})",
                        300 * (len(lines) - 1), "high",
                    )

    # --- Category 7: Broad File Inclusion ---
    def _detect_broad_file_inclusion(self):
        broad_pat = re.compile(r"""(?:glob|Glob)\s*\.?\s*(?:glob\s*)?\(\s*['"](\*\*/\*|\*\.\*)['"]""")
        ignored_pat = re.compile(r"node_modules|__pycache__|\.git/|dist/")

        for fp, content in self.file_contents.items():
            for i, line in enumerate(content.splitlines(), 1):
                for m in broad_pat.finditer(line):
                    self._add_finding(
                        7, "7a", fp, i,
                        f"Broad glob '{m.group(1)}' — pulls in potentially irrelevant files",
                        500, "high",
                    )
                for m in ignored_pat.finditer(line):
                    if "skip" not in line.lower() and "ignore" not in line.lower() \
                            and "exclude" not in line.lower():
                        self._add_finding(
                            7, "7b", fp, i,
                            f"Reference to '{m.group(0)}' without exclusion",
                            200, "medium",
                        )

    # --- Category 8: Uncompressed Examples ---
    def _detect_uncompressed_examples(self):
        example_pat = re.compile(r"(Example \d|<example>|few.?shot|FEW_SHOT)", re.IGNORECASE)
        for fp, content in self.file_contents.items():
            matches = [(i, m) for i, line in enumerate(content.splitlines(), 1)
                       for m in example_pat.finditer(line)]
            if len(matches) > 3:
                self._add_finding(
                    8, "8a", fp, matches[0][0],
                    f"{len(matches)} example markers — consider compressing or deduplicating",
                    100 * (len(matches) - 2), "medium",
                )

    # --- Category 9: Idle Agent Overhead ---
    def _detect_idle_agent_overhead(self):
        spawn_pat = re.compile(r"(?:Agent|spawn_agent|delegate|subagent)\s*\(", re.IGNORECASE)
        for fp, content in self.file_contents.items():
            for i, line in enumerate(content.splitlines(), 1):
                for m in spawn_pat.finditer(line):
                    # Heuristic: if the task description is short, it might be trivial
                    if len(line.strip()) < 80:
                        self._add_finding(
                            9, "9a", fp, i,
                            "Short agent delegation — may be trivial enough to handle inline",
                            300, "medium",
                        )

    # --- Category 10: Retry Amplification ---
    def _detect_retry_amplification(self):
        retry_pat = re.compile(r"(retry|retries|max_retries|attempt)\s*[=<>:]")
        context_reduce_pat = re.compile(r"(truncat|trim|reduce|slim|shrink).*context",
                                         re.IGNORECASE)
        for fp, content in self.file_contents.items():
            retries = [(i, m) for i, line in enumerate(content.splitlines(), 1)
                       for m in retry_pat.finditer(line)]
            has_reduction = bool(context_reduce_pat.search(content))
            if retries and not has_reduction:
                self._add_finding(
                    10, "10a", fp, retries[0][0],
                    f"Retry logic found without context reduction strategy",
                    500, "high",
                )

    # --- Summary ---
    def _build_summary(self) -> dict:
        by_category = defaultdict(lambda: {"count": 0, "waste": 0})
        by_severity = defaultdict(int)
        for f in self.findings:
            by_category[f["category"]]["count"] += 1
            by_category[f["category"]]["waste"] += f["estimated_waste_tokens"]
            by_severity[f["severity"]] += 1

        return {
            "total_findings": len(self.findings),
            "by_category": dict(by_category),
            "by_severity": dict(by_severity),
        }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_report(results: dict) -> str:
    """Human-readable terminal report."""
    lines = []
    lines.append("")
    lines.append("=" * 68)
    lines.append("  TOKEN COST LINT — AUDIT REPORT")
    lines.append("=" * 68)
    lines.append("")

    stats = results["stats"]
    lines.append(f"  Target:           {results['target']}")
    lines.append(f"  Files scanned:    {stats['files_scanned']}")
    lines.append(f"  Total lines:      {stats['total_lines']:,}")
    lines.append(f"  Est. tokens:      {stats['estimated_tokens']:,}")
    lines.append(f"  Waste tokens:     {stats['waste_tokens']:,}")
    lines.append(f"  Waste %:          {stats.get('waste_percentage', 0)}%")
    lines.append("")
    lines.append("-" * 68)

    summary = results["summary"]
    lines.append(f"  Total findings:   {summary['total_findings']}")

    sev_order = ["critical", "high", "medium", "low"]
    sev_parts = []
    for s in sev_order:
        count = summary["by_severity"].get(s, 0)
        if count:
            color = SEVERITY[s]["color"]
            sev_parts.append(f"{color}{SEVERITY[s]['label']}: {count}{RESET_COLOR}")
    if sev_parts:
        lines.append(f"  Severity:         {' | '.join(sev_parts)}")

    lines.append("")
    lines.append("-" * 68)
    lines.append("  FINDINGS BY CATEGORY")
    lines.append("-" * 68)

    for cat_name, cat_stats in sorted(
        summary["by_category"].items(),
        key=lambda x: x[1]["waste"],
        reverse=True,
    ):
        lines.append(f"\n  [{cat_name}]")
        lines.append(f"    Findings: {cat_stats['count']}  |  Est. waste: ~{cat_stats['waste']:,} tokens")

    lines.append("")
    lines.append("-" * 68)
    lines.append("  DETAILED FINDINGS")
    lines.append("-" * 68)

    for f in sorted(self_findings_sort(results["findings"])):
        sev = f["severity"]
        color = SEVERITY.get(sev, SEVERITY["medium"])["color"]
        label = SEVERITY.get(sev, SEVERITY["medium"])["label"]
        lines.append(f"\n  {color}[{label}]{RESET_COLOR} {f['category']} > {f['sub_pattern']}")
        lines.append(f"    File: {f['file']}:{f['line']}")
        lines.append(f"    {f['message']}")
        lines.append(f"    Est. waste: ~{f['estimated_waste_tokens']} tokens")

    lines.append("")
    lines.append("=" * 68)

    # Recommendations
    if results["findings"]:
        lines.append("  TOP RECOMMENDATIONS")
        lines.append("=" * 68)
        recs = generate_recommendations(results)
        for i, rec in enumerate(recs[:5], 1):
            lines.append(f"  {i}. {rec}")
        lines.append("")

    lines.append("=" * 68)
    lines.append(f"  Audit complete. {summary['total_findings']} findings, "
                 f"~{stats['waste_tokens']:,} estimated waste tokens "
                 f"({stats.get('waste_percentage', 0)}% of total).")
    lines.append("=" * 68)
    lines.append("")
    return "\n".join(lines)


def self_findings_sort(findings):
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(findings, key=lambda f: (sev_order.get(f["severity"], 9),
                                           -f["estimated_waste_tokens"]))


def generate_recommendations(results: dict) -> list[str]:
    """Generate actionable recommendations from findings."""
    recs = []
    cats_found = {f["category_id"] for f in results["findings"]}

    if 3 in cats_found:
        recs.append("Add conversation history windowing — truncate or summarize beyond N turns.")
    if 1 in cats_found or 6 in cats_found:
        recs.append("Cache file contents and share between agents instead of re-reading.")
    if 4 in cats_found:
        recs.append("Add tool result caching (e.g., @lru_cache or dict-based memoization).")
    if 2 in cats_found:
        recs.append("Trim system prompts — remove boilerplate and duplicate role definitions.")
    if 10 in cats_found:
        recs.append("Reduce context on retries — don't resend full history on failures.")
    if 7 in cats_found:
        recs.append("Narrow glob patterns — filter by extension and exclude build artifacts.")
    if 9 in cats_found:
        recs.append("Consolidate trivial agent delegations — handle small tasks inline.")
    if 5 in cats_found:
        recs.append("Use structured JSON output for agent-to-agent communication.")
    if 8 in cats_found:
        recs.append("Compress few-shot examples — fewer, shorter examples often work as well.")

    return recs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Token Cost Lint — static token waste auditor"
    )
    parser.add_argument("--target", "-t", required=True,
                        help="Path to project directory to audit")
    parser.add_argument("--format", "-f", choices=["report", "json"],
                        default="report", help="Output format")
    parser.add_argument("--compare", "-c",
                        help="Path to baseline JSON for comparison")
    parser.add_argument("--output", "-o",
                        help="Write results to file (default: stdout)")
    args = parser.parse_args()

    if not os.path.isdir(args.target):
        print(f"Error: '{args.target}' is not a directory", file=sys.stderr)
        sys.exit(1)

    engine = AuditEngine(args.target)
    results = engine.run_audit()

    # Comparison mode
    if args.compare:
        try:
            with open(args.compare) as f:
                baseline = json.load(f)
            baseline_waste = baseline.get("stats", {}).get("waste_tokens", 0)
            current_waste = results["stats"]["waste_tokens"]
            delta = current_waste - baseline_waste
            pct = round(delta / baseline_waste * 100, 1) if baseline_waste else 0
            results["comparison"] = {
                "baseline_waste": baseline_waste,
                "current_waste": current_waste,
                "delta": delta,
                "delta_pct": pct,
                "improved": delta < 0,
            }
        except Exception as e:
            print(f"Warning: could not load baseline: {e}", file=sys.stderr)

    if args.format == "json":
        output = json.dumps(results, indent=2, default=str)
    else:
        output = format_report(results)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Results written to {args.output}")
    else:
        print(output)

    # Also save JSON for future comparisons
    json_out = Path(args.target) / ".token_lint_results.json"
    try:
        with open(json_out, "w") as f:
            json.dump(results, f, indent=2, default=str)
    except Exception:
        pass


if __name__ == "__main__":
    main()
