# Technical Details

## What it does

This project packages Mozilla's "Steer, Scale, Stack" vulnerability research methodology — the same approach that scaled Firefox security fixes from ~25/month to 423 in a single month — as a reusable Claude Code skill and demo harness.

The **skill** (`SKILL.md`) teaches Claude a structured process: scope the attack surface, run multi-pass reviews targeting specific vulnerability classes, validate findings for reachability and exploitability, then generate actionable bug reports with root causes, trigger scenarios, and minimal fixes. The **demo harness** (`vuln_harness.py`) implements this pipeline with pattern-matching heuristics against sample vulnerable C code, showing exactly what the output looks like without requiring API calls.

## Architecture

```
SKILL.md                    # Claude Code skill definition (drop into ~/.claude/skills/)
vuln_harness.py             # Main scanner: steer/scale/stack pipeline
report_generator.py         # Terminal report formatter (color, severity badges)
sample_targets/
  parser.c                  # Intentionally vulnerable parser (4 bugs)
  ipc_handler.c             # Intentionally vulnerable IPC handler (4 bugs)
run.sh                      # One-command demo runner
```

### Data flow

1. **Scan** (`scan_directory`) — Discovers all `.c/.cpp/.h` files in the target directory
2. **Steer** — Runs 8 vulnerability-class-specific detectors, each targeting one bug type:
   - `detect_buffer_overflow` — unbounded copies into fixed buffers
   - `detect_use_after_free` — access to freed memory
   - `detect_integer_overflow` — unchecked arithmetic feeding allocations
   - `detect_double_free` — duplicate free() on error paths
   - `detect_untrusted_length` — attacker-controlled sizes in memcpy
   - `detect_format_string` — user data as printf format argument
   - `detect_null_deref` — missing NULL checks after malloc
   - `detect_toctou` — race conditions in multi-step checks
3. **Scale** — Each file is processed independently (parallelizable in production)
4. **Stack** — Two-pass pipeline:
   - Pass 1: Broad pattern scan produces candidate findings
   - Pass 2: Validation pass filters false positives, adds mitigation notes
5. **Report** — Formats findings with severity, location, root cause, trigger, and fix

### In production (with Claude API)

Each detector would be replaced by an LLM call with a focused prompt:

```
Review {file} for {vulnerability_class}.
Trace data flow from untrusted input to sensitive operations.
Identify assumptions that could be violated.
Provide a concrete trigger scenario if a bug is found.
```

Pass 2 would be a separate LLM call asking Claude to verify reachability of each candidate finding. This is where the real value lies — filtering noise so maintainers only see validated issues.

### Dependencies

- **Python 3.10+** (stdlib only: `re`, `dataclasses`, `pathlib`, `json`)
- No external packages required for the demo
- Production use would add `anthropic` SDK for Claude API calls

## Limitations

- **Pattern matching, not reasoning.** The demo detectors use regex heuristics. They catch the planted bugs but would miss complex, multi-file vulnerability chains that require semantic understanding. The real power comes from Claude's ability to trace data flows across function boundaries.
- **C/C++ only.** The demo targets C code. The skill itself works with any language Claude can read, but the sample detectors are C-specific.
- **No interprocedural analysis.** Each file is scanned independently. Real vulnerabilities often span multiple files and require understanding call graphs.
- **No compilation or dynamic analysis.** This is purely static. A production harness would pair with fuzzing, sanitizers (ASan, MSan), or symbolic execution.
- **Validation is simulated.** Pass 2 marks everything as validated. In production, Claude would actually trace code paths and determine reachability.

## Why it matters

For teams building Claude-driven products:

- **Security-as-a-service.** This methodology can be packaged as an automated security review product. Point it at a GitHub repo, get a prioritized vulnerability report. High value for enterprises that can't staff enough security engineers.
- **Agent factory pattern.** The steer/scale/stack approach is a general template for any LLM-driven code analysis: pick a focus area (steer), break the problem into chunks (scale), use multi-pass refinement to filter noise (stack). Applies beyond security to code quality, compliance, migration planning.
- **Lead-gen for security consultancies.** Run free scans on open-source dependencies, surface real findings, offer remediation services. Mozilla's results (423 fixes in one month) demonstrate the throughput is real.
- **CI/CD integration.** Run the skill as a pre-merge check. Flag new code that introduces vulnerability patterns before it ships.

## References

- [Behind the Scenes Hardening Firefox with Claude Mythos Preview](https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything) — Simon Willison
- [Mozilla Hacks: Behind the Scenes Hardening Firefox](https://hacks.mozilla.org/2026/05/behind-the-scenes-hardening-firefox/) — Original Mozilla post
