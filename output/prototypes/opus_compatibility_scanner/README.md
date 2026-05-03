# Opus Compatibility Scanner

**Audit your Claude Code project for 70+ breaking changes before upgrading from Opus 4.6 to 4.7.** One command scans CLAUDE.md, AGENTS.md, settings.json, hooks, MCP configs, and Anthropic SDK call sites — then prints a severity-ranked migration report.

```
$ python3 scanner.py /path/to/your/project

========================================================================
  OPUS COMPATIBILITY SCANNER — 4.6 → 4.7 Migration Report
========================================================================
  Files scanned:    12
  Patterns checked: 70
  Issues found:     38

  Summary:  11 CRITICAL  |  18 WARNING  |  9 INFO
========================================================================
```

**Zero dependencies.** Pure Python 3.8+ stdlib. No API keys needed.

---

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, run, integrate as a Claude skill
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, pattern categories, limitations
