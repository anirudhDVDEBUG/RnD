#!/usr/bin/env python3
"""
Demo of the doc-audit pipeline running against a mock repo.
Shows all 7 phases with simulated output — no API keys needed.
"""

import os
import time
import json
import sys

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

MOCK_REPO = {
    "README.md": {
        "content": """# MyApp
Uses Express 4.x for the API server.
Run `npm test` to execute tests.
Auth module: `src/auth.ts` exports `validateToken(jwt)`.
Config lives in `config/defaults.yaml`.
""",
    },
    "CLAUDE.md": {
        "content": """# CLAUDE.md
- Always run `npm run lint` before committing
- The database is PostgreSQL 13
- Use `src/helpers/format.ts` for string formatting
- Never modify `legacy/` directory — it's frozen
- The app uses React 17 for the frontend
- Always check `docs/API.md` for endpoint specs
""",
    },
    "CONTRIBUTING.md": {
        "content": """# Contributing
1. Fork the repo
2. Run `npm install` to set up
3. Tests use Jest — run `npm test`
4. Linting: `npm run lint` (ESLint + Prettier)
""",
    },
}

# Simulated actual state of the codebase
ACTUAL_STATE = {
    "src/auth.ts": {"exports": ["validateToken(token: string, opts?: ValidateOpts)"]},
    "config/defaults.json": {"exists": True, "note": "YAML was migrated to JSON"},
    "config/defaults.yaml": {"exists": False},
    "package.json": {
        "scripts": {"test": "jest", "lint": "eslint ."},
        "dependencies": {"express": "^5.0.0"},
    },
    "src/helpers/format.ts": {"exists": False, "note": "moved to src/utils/format.ts"},
    "legacy/": {"exists": False, "note": "directory was removed in v3.0"},
    "docs/API.md": {"exists": True},
    "database": "PostgreSQL 16",
    "frontend": "React 19",
}


def phase_header(num, name):
    print(f"\n{BOLD}{CYAN}{'='*60}")
    print(f"  Phase {num} — {name}")
    print(f"{'='*60}{RESET}\n")
    time.sleep(0.3)


def spinner(msg, duration=0.5):
    print(f"  {DIM}{msg}...{RESET}")
    time.sleep(duration)


def run_demo():
    print(f"\n{BOLD}Doc Audit — 7-Phase Pipeline Demo{RESET}")
    print(f"{DIM}Running against mock repo with 3 doc files{RESET}\n")
    time.sleep(0.5)

    # Phase 1 — Discovery
    phase_header(1, "Discovery")
    spinner("Scanning repo for documentation files")
    docs_found = list(MOCK_REPO.keys())
    print(f"  Found {len(docs_found)} documentation files:")
    for doc in docs_found:
        print(f"    - {doc}")
    time.sleep(0.3)

    # Phase 2 — Claim Extraction
    phase_header(2, "Claim Extraction")
    claims = [
        {"file": "README.md", "line": 2, "claim": "Uses Express 4.x", "type": "dependency"},
        {"file": "README.md", "line": 3, "claim": "`npm test` executes tests", "type": "command"},
        {"file": "README.md", "line": 4, "claim": "`src/auth.ts` exports `validateToken(jwt)`", "type": "signature"},
        {"file": "README.md", "line": 5, "claim": "Config in `config/defaults.yaml`", "type": "file_path"},
        {"file": "CLAUDE.md", "line": 2, "claim": "`npm run lint` before committing", "type": "command"},
        {"file": "CLAUDE.md", "line": 3, "claim": "Database is PostgreSQL 13", "type": "version"},
        {"file": "CLAUDE.md", "line": 4, "claim": "`src/helpers/format.ts` for formatting", "type": "file_path"},
        {"file": "CLAUDE.md", "line": 5, "claim": "Never modify `legacy/` directory", "type": "constraint"},
        {"file": "CLAUDE.md", "line": 6, "claim": "App uses React 17", "type": "version"},
        {"file": "CLAUDE.md", "line": 7, "claim": "Check `docs/API.md` for specs", "type": "file_path"},
        {"file": "CONTRIBUTING.md", "line": 3, "claim": "`npm test` runs Jest", "type": "command"},
        {"file": "CONTRIBUTING.md", "line": 4, "claim": "`npm run lint` uses ESLint + Prettier", "type": "command"},
    ]
    spinner("Parsing documents and extracting verifiable claims")
    print(f"  Extracted {len(claims)} verifiable claims:")
    for c in claims[:5]:
        print(f"    [{c['type']:10}] {c['file']}:{c['line']} — {c['claim']}")
    print(f"    ... and {len(claims)-5} more")
    time.sleep(0.3)

    # Phase 3 — Cross-Reference
    phase_header(3, "Cross-Reference")
    spinner("Checking each claim against actual codebase")

    results = [
        {"claim": claims[0], "status": "CRITICAL", "detail": "Express is now 5.x (^5.0.0 in package.json)"},
        {"claim": claims[1], "status": "OK", "detail": "npm test script exists and runs jest"},
        {"claim": claims[2], "status": "CRITICAL", "detail": "Actual signature: validateToken(token: string, opts?: ValidateOpts)"},
        {"claim": claims[3], "status": "CRITICAL", "detail": "config/defaults.yaml doesn't exist — migrated to config/defaults.json"},
        {"claim": claims[4], "status": "OK", "detail": "npm run lint script exists"},
        {"claim": claims[5], "status": "STALE", "detail": "Database is now PostgreSQL 16"},
        {"claim": claims[6], "status": "CRITICAL", "detail": "src/helpers/format.ts doesn't exist — moved to src/utils/format.ts"},
        {"claim": claims[7], "status": "STALE", "detail": "legacy/ directory no longer exists (removed in v3.0)"},
        {"claim": claims[8], "status": "STALE", "detail": "Frontend is now React 19"},
        {"claim": claims[9], "status": "OK", "detail": "docs/API.md exists"},
        {"claim": claims[10], "status": "OK", "detail": "test script runs jest"},
        {"claim": claims[11], "status": "MINOR", "detail": "Prettier config not found — may only be ESLint"},
    ]

    for r in results:
        time.sleep(0.1)
        color = {"CRITICAL": RED, "STALE": YELLOW, "MINOR": DIM, "OK": GREEN}[r["status"]]
        print(f"  {color}[{r['status']:8}]{RESET} {r['claim']['file']}:{r['claim']['line']} — {r['claim']['claim']}")
    time.sleep(0.3)

    # Phase 4 — Triage
    phase_header(4, "Triage")
    counts = {"CRITICAL": 0, "STALE": 0, "MINOR": 0, "OK": 0}
    for r in results:
        counts[r["status"]] += 1

    print(f"  {BOLD}Summary:{RESET}")
    print(f"  {RED}  Critical: {counts['CRITICAL']}  {RESET} — completely wrong, will mislead")
    print(f"  {YELLOW}  Stale:    {counts['STALE']}  {RESET} — partially outdated")
    print(f"  {DIM}  Minor:    {counts['MINOR']}  {RESET} — cosmetic / low impact")
    print(f"  {GREEN}  OK:       {counts['OK']}  {RESET} — accurate, no action needed")
    print()
    print(f"  {BOLD}{counts['CRITICAL'] + counts['STALE']} issues require attention{RESET}")
    time.sleep(0.3)

    # Phase 5 — Interactive Resolution
    phase_header(5, "Interactive Resolution")
    print(f"  {DIM}(In a real session, Claude asks you to choose for each issue){RESET}\n")

    issues = [r for r in results if r["status"] in ("CRITICAL", "STALE")]
    for i, issue in enumerate(issues, 1):
        color = RED if issue["status"] == "CRITICAL" else YELLOW
        print(f"  {color}[{i}/{len(issues)}]{RESET} {issue['claim']['file']}:{issue['claim']['line']}")
        print(f"       Claim: {issue['claim']['claim']}")
        print(f"       Reality: {issue['detail']}")
        print(f"       {DIM}→ Auto-selecting: Fix the doc to match code{RESET}")
        print()
        time.sleep(0.2)

    # Phase 6 — Atomic Commits
    phase_header(6, "Atomic Commits")
    commits = [
        "docs: update Express version from 4.x to 5.x in README",
        "docs: fix validateToken signature in README to match src/auth.ts",
        "docs: update config path from .yaml to .json in README",
        "docs: update PostgreSQL version from 13 to 16 in CLAUDE.md",
        "docs: update format.ts path from helpers/ to utils/ in CLAUDE.md",
        "docs: remove legacy/ constraint (dir no longer exists) in CLAUDE.md",
        "docs: update React version from 17 to 19 in CLAUDE.md",
    ]
    for commit in commits:
        time.sleep(0.15)
        print(f"  {GREEN}+{RESET} {commit}")

    print(f"\n  {BOLD}{len(commits)} atomic commits created{RESET}")
    time.sleep(0.3)

    # Phase 7 — CLAUDE.md Trim
    phase_header(7, "CLAUDE.md Trim")
    print(f"  Reviewing CLAUDE.md for redundancies...\n")
    time.sleep(0.3)

    print(f"  {RED}- Always run `npm run lint` before committing{RESET}")
    print(f"    {DIM}↳ Redundant: pre-commit hook already enforces this{RESET}")
    print()
    print(f"  {RED}- Never modify `legacy/` directory — it's frozen{RESET}")
    print(f"    {DIM}↳ Removed: directory no longer exists{RESET}")
    print()
    print(f"  {GREEN}  Kept 4 instructions, removed 2, updated 3{RESET}")
    print()

    print(f"  {BOLD}Trimmed CLAUDE.md:{RESET}")
    print(f"  {DIM}─────────────────────────────────────{RESET}")
    trimmed = [
        "# CLAUDE.md",
        "- Database is PostgreSQL 16",
        "- Use `src/utils/format.ts` for string formatting",
        "- App uses React 19 for the frontend",
        "- Check `docs/API.md` for endpoint specs",
    ]
    for line in trimmed:
        print(f"  {GREEN}  {line}{RESET}")
    print(f"  {DIM}─────────────────────────────────────{RESET}")

    print(f"\n{BOLD}{GREEN}Done!{RESET} Audit complete — 7 commits applied, CLAUDE.md trimmed.\n")


if __name__ == "__main__":
    run_demo()
