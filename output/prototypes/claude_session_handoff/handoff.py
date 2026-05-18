#!/usr/bin/env python3
"""
Claude Session Handoff — generates structured STATUS.md documents
that capture project state for seamless agent-to-agent transitions.

Works standalone (mock mode) or inside a real git repo.
"""

import subprocess
import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path


def run_cmd(cmd: list[str], default: str = "") -> str:
    """Run a shell command and return stripped stdout, or default on failure."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else default
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return default


def detect_git_state(repo_path: str = ".") -> dict:
    """Gather current git repo metadata."""
    cwd = os.path.abspath(repo_path)
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}

    def git(*args):
        return run_cmd(["git", "-C", cwd] + list(args))

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    last_hash = git("log", "-1", "--format=%h")
    last_msg = git("log", "-1", "--format=%s")
    status_raw = git("status", "--porcelain")
    recent_log = git("log", "--oneline", "-10")
    diff_stat = git("diff", "--stat")

    changed_files = []
    for line in status_raw.splitlines():
        if len(line) >= 3:
            changed_files.append({"status": line[:2].strip(), "file": line[3:]})

    return {
        "branch": branch or "(detached)",
        "last_commit_hash": last_hash or "none",
        "last_commit_msg": last_msg or "no commits yet",
        "changed_files": changed_files,
        "recent_log": recent_log,
        "diff_stat": diff_stat,
        "is_git": bool(branch),
    }


def mock_git_state() -> dict:
    """Generate a realistic mock git state for demo purposes."""
    return {
        "branch": "feature/user-dashboard",
        "last_commit_hash": "a3f7c21",
        "last_commit_msg": "Add dashboard layout and sidebar navigation",
        "changed_files": [
            {"status": "M", "file": "src/components/Dashboard.tsx"},
            {"status": "M", "file": "src/api/analytics.ts"},
            {"status": "??", "file": "src/components/Charts.tsx"},
            {"status": "A", "file": "src/hooks/useMetrics.ts"},
        ],
        "recent_log": "\n".join([
            "a3f7c21 Add dashboard layout and sidebar navigation",
            "b8e4d12 Set up analytics API client",
            "c91a0f3 Create useMetrics hook for data fetching",
            "d2b5e67 Initial project scaffolding",
            "e4c8f90 Initialize repo with README",
        ]),
        "diff_stat": (
            " src/components/Dashboard.tsx | 42 ++++++++++----\n"
            " src/api/analytics.ts        | 18 +++--\n"
            " 2 files changed, 45 insertions(+), 15 deletions(-)"
        ),
        "is_git": True,
    }


def generate_status_md(
    git_state: dict,
    completed_tasks: list[str] | None = None,
    blockers: list[str] | None = None,
    next_steps: list[str] | None = None,
    context_notes: list[str] | None = None,
) -> str:
    """Generate a STATUS.md handoff document from git state + annotations."""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    completed_tasks = completed_tasks or [
        "Built responsive dashboard layout with sidebar",
        "Integrated analytics API for metrics fetching",
        "Created useMetrics hook with caching support",
    ]
    blockers = blockers or [
        "Charts.tsx needs a charting library — recharts vs visx TBD",
        "Analytics API rate-limits to 100 req/min; may need caching layer",
    ]
    next_steps = next_steps or [
        "Choose and install charting library (recommend recharts for simplicity)",
        "Implement Charts.tsx with line/bar chart components",
        "Add error boundaries around dashboard widgets",
        "Write unit tests for useMetrics hook",
        "Connect real-time WebSocket feed for live metrics",
    ]
    context_notes = context_notes or [
        "Dashboard uses CSS Grid (not flexbox) — see Dashboard.tsx:15-42",
        "Analytics client is a thin wrapper over fetch — src/api/analytics.ts",
        "Auth token is read from env var ANALYTICS_TOKEN at runtime",
        "Design mockups are in docs/figma-export.png",
    ]

    # Build changed files section
    changes_lines = []
    for f in git_state["changed_files"]:
        status_label = {"M": "Modified", "A": "Added", "??": "Untracked", "D": "Deleted"}.get(
            f["status"], f["status"]
        )
        changes_lines.append(f"- `{f['file']}` ({status_label})")

    doc = f"""# STATUS.md — Session Handoff

## Project Status
- **Branch**: `{git_state['branch']}`
- **Last Commit**: `{git_state['last_commit_hash']}` — {git_state['last_commit_msg']}
- **Handoff Date**: {now}

## What Was Done
{chr(10).join('- ' + t for t in completed_tasks)}

## Current State
### Uncommitted Changes
{chr(10).join(changes_lines) if changes_lines else '- (clean working tree)'}

### Diff Summary
```
{git_state['diff_stat'] or '(no changes)'}
```

## Blockers / Issues
{chr(10).join('- ' + b for b in blockers) if blockers else '- None'}

## Next Steps
{chr(10).join('- [ ] ' + s for s in next_steps)}

## Key Context
{chr(10).join('- ' + c for c in context_notes)}

## Recent Commits
```
{git_state['recent_log'] or '(no commits)'}
```

---
*Generated by Claude Session Handoff*
"""
    return doc


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a STATUS.md handoff document for Claude session transitions"
    )
    parser.add_argument(
        "--mock", action="store_true",
        help="Use mock data instead of reading real git state"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output file path (default: stdout; use 'STATUS.md' to write file)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw git state as JSON instead of STATUS.md"
    )
    args = parser.parse_args()

    # Gather state
    if args.mock:
        state = mock_git_state()
        print("[handoff] Using mock git state for demo", file=sys.stderr)
    else:
        state = detect_git_state(args.repo)
        if not state["is_git"]:
            print("[handoff] Not a git repo — falling back to mock data", file=sys.stderr)
            state = mock_git_state()
        else:
            print(f"[handoff] Reading git state from {os.path.abspath(args.repo)}", file=sys.stderr)

    # Output
    if args.json:
        output = json.dumps(state, indent=2)
    else:
        output = generate_status_md(state)

    if args.output:
        Path(args.output).write_text(output)
        print(f"[handoff] Wrote {args.output} ({len(output)} bytes)", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
