#!/usr/bin/env python3
"""
Standalone demo — exercises the MCP server in-process (no stdio needed).
Shows what output the deep_research tool produces in mock mode.
"""
import os
import sys
from datetime import datetime, timezone

# Force mock mode for the demo
os.environ["MOCK"] = "1"

from server import MOCK_REPORT, TOOLS

def main():
    print("=" * 70)
    print("  gigaxity-deep-research MCP — Demo (mock mode)")
    print("=" * 70)
    print()

    # Show available tools
    print("Available MCP tools:")
    for t in TOOLS:
        print(f"  - {t['name']}: {t['description'][:80]}...")
    print()

    # Simulate a research call
    query = "AI-powered lead generation for B2B SaaS in 2026"
    depth = "standard"

    print(f"Calling deep_research(query=\"{query}\", depth=\"{depth}\")...")
    print("-" * 70)

    report = MOCK_REPORT.format(
        query=query,
        depth=depth,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    print(report)

    print("-" * 70)
    print()
    print("To use with real results, set OPENROUTER_API_KEY and unset MOCK.")
    print("MCP config for Claude Code — see HOW_TO_USE.md")


if __name__ == "__main__":
    main()
