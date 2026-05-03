# Technical Details

## What It Does

The Opus Compatibility Scanner is a static analysis tool that regex-scans your Claude Code project files for patterns that will break or change behavior when upgrading from Claude Opus 4.6 to 4.7. It checks 70+ patterns across 9 categories: model IDs, API parameters, settings.json schema, hook events, MCP configuration, subagent definitions, SDK call sites, token/context window references, and permission model changes. Each match is tagged with a severity (CRITICAL / WARNING / INFO) and a concrete fix suggestion.

It does not call any APIs or execute your code. It reads files, runs regexes, and prints a report. Pure static analysis.

## Architecture

```
scanner.py (single file, ~350 lines)
  |
  |- Pattern definitions: 9 lists of (regex, severity, id, message, suggestion) tuples
  |    MODEL_ID_PATTERNS      (7 patterns)   — deprecated model strings
  |    API_PARAM_PATTERNS     (10 patterns)  — removed/changed API params
  |    SETTINGS_PATTERNS      (10 patterns)  — settings.json schema changes
  |    HOOK_PATTERNS          (10 patterns)  — hook event renames/removals
  |    MCP_PATTERNS           (8 patterns)   — MCP protocol/transport changes
  |    SUBAGENT_PATTERNS      (6 patterns)   — subagent config format changes
  |    SDK_PATTERNS           (9 patterns)   — SDK import/method changes
  |    TOKEN_CONTEXT_PATTERNS (3 patterns)   — context window size changes
  |    PERMISSION_PATTERNS    (4 patterns)   — permission model updates
  |
  |- OpusCompatibilityScanner class
  |    scan() → walks directory tree, reads each file, matches all patterns per line
  |    Returns ScanResult with list of Issue dataclasses
  |
  |- format_report() → groups issues by severity, formats as text report
  |
  |- main() → CLI entry point, takes project path as argv[1]
```

**Data flow:** Directory walk -> file read -> line-by-line regex match -> Issue collection -> severity sort -> formatted report.

**Dependencies:** None. Pure Python 3.8+ stdlib (`re`, `json`, `pathlib`, `dataclasses`).

**Model calls:** None. This is a static analysis tool.

## Limitations

- **Regex-based, not AST-based.** It matches string patterns, so it can produce false positives (e.g., a comment mentioning `claude-opus-4-6` in prose) and may miss dynamically constructed model IDs.
- **Hypothetical migration.** Opus 4.7 does not exist yet. The patterns represent plausible breaking changes based on the trajectory of Claude SDK and Claude Code updates. The tool is a template — update the patterns when real 4.7 release notes arrive.
- **No auto-fix.** It reports issues but doesn't modify files. You fix them manually or ask Claude to apply the suggestions.
- **No dependency version checking.** It doesn't inspect `package.json` or `pyproject.toml` for SDK version constraints — it only scans source code and config files.
- **Single-file architecture.** Good for simplicity, but if you need to extend it with hundreds of patterns or AST parsing, you'd want to refactor.

## Why It Matters

If you're building Claude-driven products — agent factories, lead-gen pipelines, voice AI integrations, ad-creative generators — you likely have `CLAUDE.md` configs, `settings.json` tuning, hook scripts, MCP server definitions, and SDK call sites scattered across your codebase. A major model upgrade can silently break any of these. This scanner gives you a pre-flight checklist before you flip the switch.

Use cases:
- **Pre-upgrade audit** — Run before bumping your model ID to catch breaking changes.
- **CI gate** — Add `python3 scanner.py . | grep CRITICAL` to your CI pipeline to block deploys with unresolved critical issues.
- **Claude skill** — Install as a skill so Claude itself can scan your project on demand during a coding session.
- **Team onboarding** — New team members run the scanner to understand which parts of the codebase depend on model-specific behavior.
