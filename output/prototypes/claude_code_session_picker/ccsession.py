#!/usr/bin/env python3
"""
ccsession — Claude Code Session Picker

Python reimplementation of github.com/sorafujitani/ccsession.
Scans ~/.claude/projects/ for past Claude Code sessions, renders them
in an interactive picker (or prints a table in non-interactive mode),
and can resume a selected session via `claude --resume <id>`.
"""

import json
import os
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

# ── Session discovery ──────────────────────────────────────────────

CLAUDE_DIR = Path.home() / ".claude" / "projects"

def find_sessions() -> list[dict]:
    """Walk ~/.claude/projects/ and collect session metadata."""
    sessions = []
    if not CLAUDE_DIR.exists():
        return sessions

    for project_dir in sorted(CLAUDE_DIR.iterdir()):
        if not project_dir.is_dir():
            continue
        # Decode project path from directory name
        # Claude Code encodes paths: e.g. "-home-user-myproject"
        project_path = "/" + project_dir.name.lstrip("-").replace("-", "/")

        for session_file in sorted(project_dir.glob("*.jsonl")):
            session_id = session_file.stem
            meta = _parse_session_file(session_file, project_path)
            if meta:
                meta["id"] = session_id
                sessions.append(meta)

    # Sort by most recent first
    sessions.sort(key=lambda s: s.get("timestamp", ""), reverse=True)
    return sessions


def _parse_session_file(path: Path, project_path: str) -> dict | None:
    """Extract metadata from a session .jsonl file."""
    try:
        first_line = None
        last_line = None
        message_count = 0

        with open(path, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                message_count += 1
                if first_line is None:
                    first_line = line
                last_line = line

        if not first_line:
            return None

        first_msg = json.loads(first_line)
        last_msg = json.loads(last_line) if last_line else first_msg

        # Extract timestamp
        timestamp = first_msg.get("timestamp", "")
        if not timestamp:
            # Fall back to file modification time
            mtime = path.stat().st_mtime
            timestamp = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

        # Extract a summary from the first user message
        summary = _extract_summary(first_msg)

        return {
            "project": project_path,
            "timestamp": timestamp,
            "messages": message_count,
            "summary": summary,
            "file": str(path),
        }
    except (json.JSONDecodeError, OSError):
        return None


def _extract_summary(msg: dict) -> str:
    """Pull a short summary from the first message in the session."""
    # Try message.content or message.message.content
    content = msg.get("message", {}).get("content", "")
    if isinstance(content, list):
        # Anthropic-style content blocks
        text_parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        content = " ".join(text_parts)
    if isinstance(content, str) and content.strip():
        # Take first line, truncate
        first_line = content.strip().split("\n")[0]
        return first_line[:80]
    return "(no summary)"


# ── Display ────────────────────────────────────────────────────────

def format_timestamp(ts: str) -> str:
    """Convert ISO timestamp to a human-friendly format."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return ts[:16] if ts else "unknown"


def print_sessions_table(sessions: list[dict]) -> None:
    """Print sessions in a tabular format."""
    if not sessions:
        print("No Claude Code sessions found.")
        print(f"  (looked in {CLAUDE_DIR})")
        return

    # Header
    print(f"\n{'#':>3}  {'Date':16}  {'Msgs':>5}  {'Project':30}  {'Summary'}")
    print(f"{'─'*3}  {'─'*16}  {'─'*5}  {'─'*30}  {'─'*40}")

    for i, s in enumerate(sessions, 1):
        ts = format_timestamp(s["timestamp"])
        project = s["project"][-30:]  # right-truncate long paths
        summary = s["summary"][:50]
        print(f"{i:>3}  {ts:16}  {s['messages']:>5}  {project:30}  {summary}")

    print(f"\n  Total: {len(sessions)} session(s)\n")


# ── Interactive picker (fzf or fallback) ───────────────────────────

def pick_with_fzf(sessions: list[dict]) -> dict | None:
    """Use fzf to interactively pick a session."""
    lines = []
    for i, s in enumerate(sessions):
        ts = format_timestamp(s["timestamp"])
        project = s["project"][-30:]
        summary = s["summary"][:50]
        lines.append(f"{i}|{ts}  {s['messages']:>4} msgs  {project}  {summary}")

    try:
        proc = subprocess.run(
            ["fzf", "--header=Pick a Claude Code session to resume",
             "--reverse", "--height=40%"],
            input="\n".join(lines),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return None
        chosen = proc.stdout.strip()
        idx = int(chosen.split("|")[0])
        return sessions[idx]
    except FileNotFoundError:
        return None


def pick_with_input(sessions: list[dict]) -> dict | None:
    """Fallback interactive picker without fzf."""
    print_sessions_table(sessions)
    try:
        choice = input("Enter session number to resume (or 'q' to quit): ").strip()
        if choice.lower() == "q":
            return None
        idx = int(choice) - 1
        if 0 <= idx < len(sessions):
            return sessions[idx]
        print("Invalid selection.")
        return None
    except (ValueError, EOFError, KeyboardInterrupt):
        return None


# ── Resume ─────────────────────────────────────────────────────────

def resume_session(session: dict, dry_run: bool = False) -> None:
    """Resume the selected Claude Code session from its original cwd."""
    sid = session["id"]
    cwd = session["project"]

    print(f"\n  Session:   {sid}")
    print(f"  Project:   {session['project']}")
    print(f"  Summary:   {session['summary']}")
    print(f"  Messages:  {session['messages']}")
    print(f"  Started:   {format_timestamp(session['timestamp'])}")

    if dry_run:
        print(f"\n  [dry-run] Would run: claude --resume {sid}")
        print(f"  [dry-run] From directory: {cwd}")
        return

    if not os.path.isdir(cwd):
        print(f"\n  Warning: directory {cwd} does not exist.")
        print(f"  Resuming from current directory instead.")
        cwd = os.getcwd()

    print(f"\n  Resuming session in {cwd} ...")
    os.chdir(cwd)
    os.execvp("claude", ["claude", "--resume", sid])


# ── Mock demo ──────────────────────────────────────────────────────

MOCK_SESSIONS = [
    {
        "id": "a1b2c3d4-session-001",
        "project": "/home/user/projects/web-app",
        "timestamp": "2026-05-29T14:30:00+00:00",
        "messages": 47,
        "summary": "Add dark mode toggle to settings page",
        "file": "(mock)",
    },
    {
        "id": "e5f6g7h8-session-002",
        "project": "/home/user/projects/api-server",
        "timestamp": "2026-05-29T10:15:00+00:00",
        "messages": 23,
        "summary": "Fix rate limiting middleware returning 500 instead of 429",
        "file": "(mock)",
    },
    {
        "id": "i9j0k1l2-session-003",
        "project": "/home/user/projects/ml-pipeline",
        "timestamp": "2026-05-28T18:45:00+00:00",
        "messages": 112,
        "summary": "Refactor data preprocessing to use Polars instead of Pandas",
        "file": "(mock)",
    },
    {
        "id": "m3n4o5p6-session-004",
        "project": "/home/user/projects/web-app",
        "timestamp": "2026-05-28T09:00:00+00:00",
        "messages": 8,
        "summary": "Debug CI pipeline failing on Node 22",
        "file": "(mock)",
    },
    {
        "id": "q7r8s9t0-session-005",
        "project": "/home/user/projects/mobile-app",
        "timestamp": "2026-05-27T16:20:00+00:00",
        "messages": 65,
        "summary": "Implement push notification service with Firebase",
        "file": "(mock)",
    },
    {
        "id": "u1v2w3x4-session-006",
        "project": "/home/user/projects/infra",
        "timestamp": "2026-05-27T08:10:00+00:00",
        "messages": 34,
        "summary": "Write Terraform modules for ECS Fargate deployment",
        "file": "(mock)",
    },
    {
        "id": "y5z6a7b8-session-007",
        "project": "/home/user/projects/docs-site",
        "timestamp": "2026-05-26T20:55:00+00:00",
        "messages": 19,
        "summary": "Generate API reference docs from OpenAPI spec",
        "file": "(mock)",
    },
]


# ── CLI ────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Pick and resume a past Claude Code session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              ccsession                  # interactive fzf picker
              ccsession --list           # print session table
              ccsession --demo           # run with mock data (no real sessions needed)
              ccsession --demo --pick 2  # pick mock session #2
        """),
    )
    parser.add_argument("--list", action="store_true", help="List sessions without picking")
    parser.add_argument("--demo", action="store_true", help="Use mock sessions for demo")
    parser.add_argument("--pick", type=int, metavar="N", help="Auto-pick session number N (1-based)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without resuming")
    parser.add_argument("--json", action="store_true", help="Output sessions as JSON")
    args = parser.parse_args()

    # Discover sessions
    if args.demo:
        sessions = MOCK_SESSIONS
        print("  [demo mode — using mock session data]\n")
    else:
        sessions = find_sessions()

    if args.json:
        print(json.dumps(sessions, indent=2))
        return

    if args.list or (not sessions and not args.demo):
        print_sessions_table(sessions)
        return

    # Pick a session
    if args.pick:
        idx = args.pick - 1
        if 0 <= idx < len(sessions):
            chosen = sessions[idx]
        else:
            print(f"Invalid pick: {args.pick} (have {len(sessions)} sessions)")
            sys.exit(1)
    else:
        # Try fzf, fall back to numbered input
        chosen = pick_with_fzf(sessions)
        if chosen is None and sys.stdin.isatty():
            chosen = pick_with_input(sessions)
        elif chosen is None:
            # Non-interactive, just list
            print_sessions_table(sessions)
            return

    if chosen:
        resume_session(chosen, dry_run=args.dry_run or args.demo)


if __name__ == "__main__":
    main()
