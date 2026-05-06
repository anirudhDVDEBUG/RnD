#!/usr/bin/env python3
"""
AI Dev Effectiveness Analyzer
Detects AI co-programming signatures in git history and calculates
productivity multipliers via top-down, bottom-up, and optional subagent methods.

Source: https://github.com/denn-gubsky/ai-dev-effectiveness
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# AI signature patterns
# ---------------------------------------------------------------------------

AI_SIGNATURES = {
    "Claude Code": {
        "co_author": [
            r"Co-authored-by:.*Claude",
            r"Co-authored-by:.*Anthropic",
            r"Co-Authored-By:.*Claude",
        ],
        "message": [
            r"^(?:feat|fix|refactor|docs|test|chore)\(.+\):",  # conventional commits (common with Claude)
        ],
        "trailer": [
            r"Generated.*Claude",
            r"claude-code",
        ],
    },
    "GitHub Copilot": {
        "co_author": [
            r"Co-authored-by:.*Copilot",
            r"Co-authored-by:.*GitHub Copilot",
        ],
        "message": [],
        "trailer": [
            r"copilot",
        ],
    },
    "Cursor": {
        "co_author": [
            r"Co-authored-by:.*Cursor",
        ],
        "message": [],
        "trailer": [
            r"cursor",
            r"Generated.*Cursor",
        ],
    },
    "OpenAI Codex": {
        "co_author": [
            r"Co-authored-by:.*Codex",
            r"Co-authored-by:.*OpenAI",
        ],
        "message": [],
        "trailer": [
            r"codex",
            r"Generated.*Codex",
        ],
    },
}


@dataclass
class CommitInfo:
    sha: str
    author: str
    date: str
    message: str
    insertions: int = 0
    deletions: int = 0
    files_changed: int = 0
    ai_tool: Optional[str] = None
    ai_confidence: float = 0.0


@dataclass
class AnalysisResult:
    repo_path: str
    total_commits: int = 0
    ai_assisted_commits: int = 0
    manual_commits: int = 0
    ai_tools_detected: dict = field(default_factory=dict)
    ai_loc_inserted: int = 0
    manual_loc_inserted: int = 0
    ai_loc_deleted: int = 0
    manual_loc_deleted: int = 0
    authors: dict = field(default_factory=dict)
    top_down_multiplier: float = 1.0
    bottom_up_multiplier: float = 1.0
    combined_multiplier: float = 1.0
    commits: list = field(default_factory=list)
    analysis_window: str = ""


# ---------------------------------------------------------------------------
# Git log parsing
# ---------------------------------------------------------------------------

def run_git_log(repo_path: str, since: Optional[str] = None,
                author: Optional[str] = None) -> list[CommitInfo]:
    """Parse git log with numstat into CommitInfo objects."""
    cmd = [
        "git", "-C", repo_path, "log",
        "--format=COMMIT_SEP%n%H%n%an%n%aI%n%B%nCOMMIT_END",
        "--numstat",
    ]
    if since:
        cmd.append(f"--since={since}")
    if author:
        cmd.append(f"--author={author}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"Error running git log: {result.stderr.strip()}", file=sys.stderr)
            return []
    except FileNotFoundError:
        print("git not found on PATH", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print("git log timed out", file=sys.stderr)
        return []

    commits = []
    raw_commits = result.stdout.split("COMMIT_SEP\n")

    for block in raw_commits:
        block = block.strip()
        if not block:
            continue

        parts = block.split("COMMIT_END")
        header = parts[0].strip() if parts else ""
        numstat = parts[1].strip() if len(parts) > 1 else ""

        lines = header.split("\n")
        if len(lines) < 4:
            continue

        sha = lines[0].strip()
        author_name = lines[1].strip()
        date = lines[2].strip()
        message = "\n".join(lines[3:]).strip()

        ins, dels, fchanged = 0, 0, 0
        if numstat:
            for stat_line in numstat.split("\n"):
                stat_line = stat_line.strip()
                if not stat_line:
                    continue
                stat_parts = stat_line.split("\t")
                if len(stat_parts) >= 2:
                    try:
                        ins += int(stat_parts[0])
                    except ValueError:
                        pass
                    try:
                        dels += int(stat_parts[1])
                    except ValueError:
                        pass
                    fchanged += 1

        commits.append(CommitInfo(
            sha=sha, author=author_name, date=date, message=message,
            insertions=ins, deletions=dels, files_changed=fchanged,
        ))

    return commits


# ---------------------------------------------------------------------------
# AI detection
# ---------------------------------------------------------------------------

def detect_ai_tool(commit: CommitInfo) -> tuple[Optional[str], float]:
    """Check commit message/trailers for AI tool signatures."""
    full_text = commit.message

    for tool_name, patterns in AI_SIGNATURES.items():
        # Co-author match (highest confidence)
        for pat in patterns["co_author"]:
            if re.search(pat, full_text, re.IGNORECASE):
                return tool_name, 0.95

        # Trailer match
        for pat in patterns["trailer"]:
            if re.search(pat, full_text, re.IGNORECASE):
                return tool_name, 0.80

        # Message pattern match (lower confidence)
        for pat in patterns["message"]:
            if re.search(pat, full_text, re.IGNORECASE):
                return tool_name, 0.40

    return None, 0.0


# ---------------------------------------------------------------------------
# Productivity multiplier calculations
# ---------------------------------------------------------------------------

def calc_top_down(ai_pct: float) -> float:
    """
    Top-down estimate: assumes AI-assisted work is 2-3x faster.
    Effective multiplier = 1 / (1 - ai_pct * (1 - 1/speedup))
    """
    if ai_pct <= 0:
        return 1.0
    assumed_speedup = 2.5
    return 1.0 / (1.0 - ai_pct * (1.0 - 1.0 / assumed_speedup))


def calc_bottom_up(ai_loc: int, manual_loc: int, ai_commits: int,
                    manual_commits: int) -> float:
    """
    Bottom-up: compare LOC-per-commit for AI vs manual commits.
    Multiplier = (ai_loc_per_commit) / (manual_loc_per_commit)
    """
    if manual_commits == 0 or ai_commits == 0:
        return 1.0
    ai_rate = ai_loc / ai_commits if ai_commits else 0
    manual_rate = manual_loc / manual_commits if manual_commits else 1
    if manual_rate == 0:
        return 1.0
    raw = ai_rate / manual_rate
    return max(1.0, min(raw, 10.0))  # clamp to reasonable range


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_report(result: AnalysisResult) -> str:
    """Produce a human-readable report."""
    lines = []
    lines.append("=" * 64)
    lines.append("  AI Dev Effectiveness Report")
    lines.append("=" * 64)
    lines.append(f"  Repository : {result.repo_path}")
    lines.append(f"  Window     : {result.analysis_window}")
    lines.append(f"  Total commits analyzed: {result.total_commits}")
    lines.append("")

    ai_pct = (result.ai_assisted_commits / result.total_commits * 100
              if result.total_commits else 0)
    lines.append(f"  AI-assisted commits : {result.ai_assisted_commits} "
                 f"({ai_pct:.1f}%)")
    lines.append(f"  Manual commits      : {result.manual_commits} "
                 f"({100 - ai_pct:.1f}%)")
    lines.append("")

    if result.ai_tools_detected:
        lines.append("  AI Tools Detected:")
        for tool, count in sorted(result.ai_tools_detected.items(),
                                   key=lambda x: -x[1]):
            lines.append(f"    - {tool}: {count} commits")
        lines.append("")

    lines.append("  Lines of Code Breakdown:")
    lines.append(f"    AI-assisted insertions : {result.ai_loc_inserted:,}")
    lines.append(f"    Manual insertions      : {result.manual_loc_inserted:,}")
    lines.append(f"    AI-assisted deletions  : {result.ai_loc_deleted:,}")
    lines.append(f"    Manual deletions       : {result.manual_loc_deleted:,}")
    lines.append("")

    lines.append("  Productivity Multiplier Estimates:")
    lines.append(f"    Top-down (role-based)  : {result.top_down_multiplier:.2f}x")
    lines.append(f"    Bottom-up (LOC-based)  : {result.bottom_up_multiplier:.2f}x")
    lines.append(f"    Combined estimate      : {result.combined_multiplier:.2f}x")
    lines.append("")

    if result.authors:
        lines.append("  Per-Author Breakdown:")
        for author, stats in sorted(result.authors.items()):
            ai_c = stats.get("ai_commits", 0)
            total_c = stats.get("total_commits", 0)
            pct = (ai_c / total_c * 100) if total_c else 0
            lines.append(f"    {author}: {total_c} commits, "
                         f"{ai_c} AI-assisted ({pct:.0f}%)")
        lines.append("")

    lines.append("=" * 64)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze_repo(repo_path: str, since: Optional[str] = None,
                 author: Optional[str] = None) -> AnalysisResult:
    """Run full analysis on a git repo."""
    result = AnalysisResult(repo_path=os.path.abspath(repo_path))
    result.analysis_window = f"since {since}" if since else "all history"

    commits = run_git_log(repo_path, since=since, author=author)
    result.total_commits = len(commits)

    tool_counts = defaultdict(int)
    author_stats = defaultdict(lambda: {"total_commits": 0, "ai_commits": 0})

    for commit in commits:
        tool, confidence = detect_ai_tool(commit)
        commit.ai_tool = tool
        commit.ai_confidence = confidence

        author_stats[commit.author]["total_commits"] += 1

        if tool and confidence >= 0.4:
            result.ai_assisted_commits += 1
            result.ai_loc_inserted += commit.insertions
            result.ai_loc_deleted += commit.deletions
            tool_counts[tool] += 1
            author_stats[commit.author]["ai_commits"] += 1
        else:
            result.manual_commits += 1
            result.manual_loc_inserted += commit.insertions
            result.manual_loc_deleted += commit.deletions

    result.ai_tools_detected = dict(tool_counts)
    result.authors = dict(author_stats)

    # Calculate multipliers
    ai_pct = (result.ai_assisted_commits / result.total_commits
              if result.total_commits else 0)
    result.top_down_multiplier = calc_top_down(ai_pct)
    result.bottom_up_multiplier = calc_bottom_up(
        result.ai_loc_inserted, result.manual_loc_inserted,
        result.ai_assisted_commits, result.manual_commits,
    )
    result.combined_multiplier = round(
        (result.top_down_multiplier + result.bottom_up_multiplier) / 2, 2
    )

    result.commits = [asdict(c) for c in commits[:50]]  # keep first 50 for JSON
    return result


# ---------------------------------------------------------------------------
# Mock / demo mode
# ---------------------------------------------------------------------------

def run_demo() -> AnalysisResult:
    """Generate a realistic demo report without needing a real repo."""
    result = AnalysisResult(repo_path="/demo/acme-saas-platform")
    result.analysis_window = "since 2025-01-01 (demo data)"
    result.total_commits = 347
    result.ai_assisted_commits = 142
    result.manual_commits = 205
    result.ai_tools_detected = {
        "Claude Code": 89,
        "GitHub Copilot": 41,
        "Cursor": 12,
    }
    result.ai_loc_inserted = 28_450
    result.manual_loc_inserted = 19_200
    result.ai_loc_deleted = 8_120
    result.manual_loc_deleted = 6_340
    result.authors = {
        "Alice Chen": {"total_commits": 124, "ai_commits": 78},
        "Bob Martinez": {"total_commits": 98, "ai_commits": 34},
        "Carol Nguyen": {"total_commits": 75, "ai_commits": 22},
        "Dave Kim": {"total_commits": 50, "ai_commits": 8},
    }

    ai_pct = result.ai_assisted_commits / result.total_commits
    result.top_down_multiplier = calc_top_down(ai_pct)
    result.bottom_up_multiplier = calc_bottom_up(
        result.ai_loc_inserted, result.manual_loc_inserted,
        result.ai_assisted_commits, result.manual_commits,
    )
    result.combined_multiplier = round(
        (result.top_down_multiplier + result.bottom_up_multiplier) / 2, 2
    )
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Measure AI co-programming effectiveness on a git repo"
    )
    parser.add_argument("--repo", type=str, default=None,
                        help="Path to the git repository to analyze")
    parser.add_argument("--since", type=str, default=None,
                        help="Limit analysis window (e.g. 2025-01-01)")
    parser.add_argument("--author", type=str, default=None,
                        help="Filter to a specific author")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--demo", action="store_true",
                        help="Run with mock data (no repo needed)")

    args = parser.parse_args()

    if args.demo or args.repo is None:
        if args.repo is None and not args.demo:
            print("No --repo specified, running in demo mode.\n", file=sys.stderr)
        result = run_demo()
    else:
        if not os.path.isdir(os.path.join(args.repo, ".git")):
            print(f"Error: {args.repo} is not a git repository", file=sys.stderr)
            sys.exit(1)
        result = analyze_repo(args.repo, since=args.since, author=args.author)

    if args.output == "json":
        print(json.dumps(asdict(result), indent=2, default=str))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
