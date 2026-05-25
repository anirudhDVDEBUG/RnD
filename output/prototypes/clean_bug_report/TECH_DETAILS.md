# Technical Details

## What It Does

This is a Claude Code **skill** (a structured prompt in `SKILL.md`) that constrains Claude's behavior when writing bug reports. Instead of producing the typical AI-padded issue with speculative root causes and untested fixes, it forces Claude to:

1. Ask the user four specific questions (command, expected, actual, error output)
2. Use the user's own words verbatim
3. Format the report in a standard template
4. Review the draft with the user and remove anything unverified

The demo script (`clean_bug_report.py`) illustrates the difference by generating both a clean and a slop version from the same observations, then running a pattern detector to flag AI-slop phrases.

## Architecture

```
SKILL.md              — The skill definition (drop into ~/.claude/skills/)
clean_bug_report.py   — Demo: clean vs. slop side-by-side comparison
run.sh                — Entry point: runs the demo
```

**Data flow in the skill:**
User observations -> Claude asks clarifying questions -> structured template -> user review -> final report

**Data flow in the demo:**
Sample observations (dict) -> `format_clean_report()` -> clean output
                           -> `generate_slop_version()` -> slop output
                           -> `detect_slop()` -> pattern analysis

**Dependencies:** Python 3.10+ stdlib only. No external packages, no API keys.

## Limitations

- The skill is a prompt — it guides Claude but cannot enforce behavior with 100% certainty. Claude may occasionally add mild commentary.
- The slop detector in the demo uses simple substring matching, not semantic analysis. It catches common patterns but isn't exhaustive.
- The skill doesn't auto-file issues on GitHub. It produces markdown text that the user pastes manually (or pipes to `gh issue create`).
- It doesn't validate that the user's reproduction steps actually work — it trusts the user's observations as-is.

## Why This Matters

For anyone building Claude-driven products (agent factories, support bots, developer tools):

- **Issue quality directly affects triage speed.** Maintainers spend significant time untangling AI-padded reports to find the actual observation buried inside. This skill eliminates that overhead.
- **Trust signal.** Clean, factual reports get faster responses from maintainers. AI-slop reports get closed or deprioritized.
- **Reusable pattern.** The same "gather facts, format template, review with human" pattern applies to any structured output task — support tickets, incident reports, change requests.
- **Prompt engineering reference.** The SKILL.md demonstrates how to constrain Claude with explicit DO/DON'T rules rather than vague instructions.

## References

- [Quoting Armin Ronacher — Simon Willison](https://simonwillison.net/2026/May/24/armin-ronacher/#atom-everything)
- [Original post by Armin Ronacher](https://lucumr.pocoo.org/2026/5/24/pi-oss/)
