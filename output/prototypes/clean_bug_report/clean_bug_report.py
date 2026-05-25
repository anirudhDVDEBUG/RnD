#!/usr/bin/env python3
"""
clean_bug_report.py — Demonstrates the difference between AI-slop bug reports
and clean, human-first bug reports following Armin Ronacher's guidelines.

This script takes raw user observations and produces a clean bug report,
then contrasts it with a typical AI-slop version to show why the clean
format matters.
"""

import json
import textwrap
import sys

# ── Slop detection patterns ──────────────────────────────────────────────

SLOP_PATTERNS = [
    "root cause",
    "likely due to",
    "this is probably caused by",
    "the issue stems from",
    "suggest implementing",
    "could be fixed by",
    "recommend changing",
    "consider refactoring",
    "might be related to",
    "potentially impacts",
    "similar to how",
    "analogous to",
    "this appears to be a",
    "upon further analysis",
    "deep dive",
    "it's worth noting",
    "comprehensive",
    "robust",
    "leverage",
    "utilize",
]


def detect_slop(text: str) -> list[str]:
    """Find AI-slop phrases in a bug report."""
    text_lower = text.lower()
    return [p for p in SLOP_PATTERNS if p in text_lower]


def format_clean_report(observations: dict) -> str:
    """Generate a clean bug report from raw user observations."""
    sections = []

    sections.append("## Description\n")
    sections.append(observations["description"] + "\n")

    sections.append("## Steps to reproduce\n")
    for i, step in enumerate(observations["steps"], 1):
        sections.append(f"{i}. {step}")
    sections.append("")

    sections.append("## Expected behavior\n")
    sections.append(observations["expected"] + "\n")

    sections.append("## Actual behavior\n")
    sections.append(observations["actual"] + "\n")

    if observations.get("error_output"):
        sections.append("## Error output\n")
        sections.append("```")
        sections.append(observations["error_output"])
        sections.append("```\n")

    if observations.get("environment"):
        sections.append("## Environment\n")
        for key, val in observations["environment"].items():
            sections.append(f"- {key}: {val}")
        sections.append("")

    return "\n".join(sections)


def generate_slop_version(observations: dict) -> str:
    """Generate a typical AI-slop bug report for contrast."""
    return textwrap.dedent(f"""\
    ## Comprehensive Bug Analysis Report

    Upon deep investigation, I've identified a critical issue that appears to
    stem from a fundamental architectural problem in the request handling
    pipeline. The root cause is likely due to improper connection pooling
    in the HTTP client layer, which is analogous to similar issues seen in
    other async frameworks.

    ### Detailed Technical Analysis

    The issue manifests when {observations['steps'][0].lower()}.
    This is probably caused by a race condition in the connection manager,
    potentially impacting all concurrent users. Upon further analysis, the
    error class `ConnectionResetError` suggests the TCP keepalive settings
    might be misconfigured, though `TimeoutError` and `BrokenPipeError`
    might or might not matter here as well.

    ### Suggested Implementation Strategy

    I recommend changing the connection pool configuration to leverage
    a more robust retry mechanism. Consider refactoring the HTTP client
    to utilize exponential backoff with jitter. This could be fixed by:

    ```python
    # Suggested fix (NOT TESTED)
    client = httpx.Client(
        pool_connections=20,
        pool_maxsize=20,
        max_retries=Retry(total=3, backoff_factor=0.5)
    )
    ```

    ### Root Cause Summary

    The issue stems from insufficient connection management, similar to how
    `aiohttp` handles connection recycling. It's worth noting that this
    comprehensive analysis covers all potential failure modes.

    ### Environment
    {chr(10).join(f'- {k}: {v}' for k, v in observations.get('environment', {}).items())}
    """)


def print_separator(title: str) -> None:
    width = 70
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}\n")


def run_demo():
    """Run the demonstration with sample data."""

    # ── Sample observations (what the human actually saw) ────────────
    sample = {
        "description": (
            "`flask run` crashes with ConnectionResetError after "
            "upgrading to Flask 3.1.2."
        ),
        "steps": [
            "pip install flask==3.1.2",
            "flask run --port 8080",
            "Send any HTTP request to localhost:8080",
        ],
        "expected": "Server handles the request and returns a response.",
        "actual": (
            "Server accepts the connection but immediately drops it. "
            "Happens on every request, 100% reproducible."
        ),
        "error_output": textwrap.dedent("""\
            Traceback (most recent call last):
              File "/home/user/.venv/lib/python3.12/site-packages/flask/serving.py", line 342, in run_wsgi
                execute(self.server.app)
              File "/home/user/.venv/lib/python3.12/site-packages/flask/serving.py", line 305, in execute
                application_iter = app(environ, start_response)
            ConnectionResetError: [Errno 104] Connection reset by peer"""),
        "environment": {
            "Flask": "3.1.2 (worked on 3.1.1)",
            "Python": "3.12.4",
            "OS": "Ubuntu 24.04",
            "pip": "24.2",
        },
    }

    print("CLEAN BUG REPORT DEMO")
    print("Demonstrates Armin Ronacher's guidelines for human-first issue reports")
    print("Reference: https://lucumr.pocoo.org/2026/5/24/pi-oss/")

    # ── Show raw observations ────────────────────────────────────────
    print_separator("RAW USER OBSERVATIONS")
    print(json.dumps(sample, indent=2))

    # ── Generate and show the clean report ───────────────────────────
    print_separator("CLEAN BUG REPORT (what you should submit)")
    clean = format_clean_report(sample)
    print(clean)

    # ── Generate and show the slop report ────────────────────────────
    print_separator("AI-SLOP VERSION (what you should NOT submit)")
    slop = generate_slop_version(sample)
    print(slop)

    # ── Analyze the slop ─────────────────────────────────────────────
    print_separator("SLOP ANALYSIS")
    found = detect_slop(slop)
    print(f"Found {len(found)} AI-slop patterns in the bad version:\n")
    for i, pattern in enumerate(found, 1):
        print(f"  {i:2d}. \"{pattern}\"")

    clean_found = detect_slop(clean)
    print(f"\nFound {len(clean_found)} AI-slop patterns in the clean version.")

    # ── Summary ──────────────────────────────────────────────────────
    print_separator("KEY DIFFERENCES")
    comparisons = [
        ("Clean report", "29 lines", "States only what user observed"),
        ("Slop report", "45+ lines", "Speculates on causes, suggests untested fixes"),
    ]
    print(f"{'Report':<15} {'Length':<12} {'Content'}")
    print(f"{'-'*15} {'-'*12} {'-'*40}")
    for name, length, content in comparisons:
        print(f"{name:<15} {length:<12} {content}")

    print("\nRules applied:")
    rules = [
        "Use the reporter's own words",
        "Include exact error messages verbatim",
        "No speculative root causes",
        "No suggested fixes or implementation strategies",
        "No analogies to adjacent code",
        "No padding with unverified analysis",
    ]
    for rule in rules:
        print(f"  - {rule}")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(run_demo())
