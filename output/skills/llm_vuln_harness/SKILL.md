---
name: llm_vuln_harness
description: |
  Automated vulnerability research harness using Claude to find, validate, and report security bugs in large codebases.
  TRIGGER when: user wants to find security vulnerabilities in code, run automated bug-finding, do LLM-assisted security auditing, or set up a vulnerability research pipeline.
  DO NOT TRIGGER when: user is writing exploit code for malicious purposes, generating slop bug reports, or targeting systems without authorization.
---

# LLM Vulnerability Research Harness

A structured approach to using Claude for automated security bug discovery in large codebases, inspired by [Mozilla's work hardening Firefox with Claude](https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything).

## When to use

- "Find security vulnerabilities in this codebase"
- "Run an automated security audit on this project"
- "Set up a vulnerability research pipeline for this repo"
- "Check this C/C++/Rust code for memory safety bugs"
- "Do a deep security review like Mozilla did with Firefox"

## How to use

### Step 1: Scope the target

Identify the codebase area to audit. Narrow the attack surface:

- Parser code (HTML, XML, XSLT, CSS, JSON, etc.)
- IPC boundaries and serialization/deserialization
- Memory management (allocators, ref-counting, lifetimes)
- Legacy code with long histories (high-value targets — Mozilla found 15–20 year old bugs)
- Input handling from untrusted sources

### Step 2: Steer, scale, and stack

Apply Mozilla's three-layer methodology:

1. **Steer** — Give Claude focused prompts with specific vulnerability classes:
   - Use-after-free, double-free, buffer overflows
   - Integer overflow/underflow in size calculations
   - Type confusion across interfaces
   - Race conditions in concurrent code
   - Logic errors in state machines

2. **Scale** — Break the codebase into reviewable chunks. For each chunk:
   ```
   Review [file/module] for [vulnerability class].
   Trace data flow from untrusted input to sensitive operations.
   Identify assumptions that could be violated.
   Provide a concrete trigger scenario if a bug is found.
   ```

3. **Stack** — Use multi-pass review:
   - Pass 1: Broad scan for candidate issues
   - Pass 2: Deep-dive validation of candidates (filter noise)
   - Pass 3: Write reproduction steps and assess severity

### Step 3: Validate findings

For each candidate bug:

1. Trace the code path manually to confirm reachability
2. Check if existing defense-in-depth measures (sandboxing, ASLR, bounds checks) mitigate the issue
3. Determine if the bug is exploitable or only a theoretical concern
4. Classify severity (Critical / High / Medium / Low)
5. Write a clear bug report with:
   - Root cause analysis
   - Affected code location (file:line)
   - Minimal reproduction scenario
   - Suggested fix

### Step 4: Generate fix patches

For confirmed vulnerabilities:

1. Propose minimal, targeted fixes (avoid refactoring unrelated code)
2. Add regression tests that exercise the vulnerable path
3. Verify the fix doesn't break existing tests
4. Document the defense-in-depth principle the fix strengthens

## Key lessons from Mozilla's Firefox work

- **Signal over noise**: The value is in filtering out false positives. A plausible-but-wrong report costs maintainers more than no report. Validate thoroughly before reporting.
- **Legacy code is high-value**: Old, rarely-touched code accumulates latent bugs. Prioritize modules with long histories.
- **Defense-in-depth works**: Many discovered bugs were already mitigated by existing sandboxing and safety layers. Note mitigations in reports.
- **Volume matters**: Mozilla went from ~20-30 security fixes/month to 423 in a single month by scaling this approach.

## Important constraints

- Only use on codebases you are authorized to test
- This is for defensive security research, not exploitation
- Always validate findings — do not submit unverified AI-generated bug reports to open source projects
- Be transparent about AI-assisted discovery when reporting bugs

## References

- [Behind the Scenes Hardening Firefox with Claude Mythos Preview](https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything) — Simon Willison's coverage
- [Mozilla Hacks: Behind the Scenes Hardening Firefox](https://hacks.mozilla.org/2026/05/behind-the-scenes-hardening-firefox/) — Original Mozilla blog post
