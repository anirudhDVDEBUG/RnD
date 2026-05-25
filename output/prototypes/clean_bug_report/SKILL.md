---
name: clean_bug_report
description: |
  Write clean, human-first bug reports and GitHub issues following Armin Ronacher's guidelines.
  Strips out AI slop, fake root-cause analysis, and speculative implementation suggestions.
  TRIGGER: user wants to file a bug report, write an issue, report a problem, create a GitHub issue, or draft a bug ticket.
---

# Clean Bug Report

Generate clear, concise bug reports that focus on what the human actually observed — no AI slop, no speculative root causes, no fake-minimal repros.

## When to use

- "Help me write a bug report"
- "I need to file a GitHub issue"
- "Draft an issue for this problem I'm seeing"
- "Report this bug upstream"
- "Write up this error as an issue"

## How to use

### Step 1: Gather the facts from the user

Ask the user for exactly four things:

1. **What command or action did you run?** (exact input, CLI command, API call, UI action)
2. **What did you expect to happen?**
3. **What happened instead?**
4. **What is the exact error message or log output?** (verbatim, not paraphrased)

Also collect if available:
- Software version / commit hash
- OS / environment
- Whether the issue is reproducible and how often

### Step 2: Draft the issue

Write the bug report following these rules:

- **DO** use the reporter's own words and observations
- **DO** include exact error messages, logs, and stack traces verbatim
- **DO** include a minimal reproduction if the user has one they actually tested
- **DO** keep it short and factual
- **DON'T** speculate on root causes
- **DON'T** suggest implementation strategies or fixes
- **DON'T** draw analogies to adjacent code that may be wrong
- **DON'T** list error classes that "might or might not matter"
- **DON'T** pad the report with confident-sounding but unverified analysis
- **DON'T** reword the user's observations through an LLM voice — preserve their original phrasing

### Step 3: Format

Use this structure:

```markdown
## Description

[One or two sentences describing the problem in plain language.]

## Steps to reproduce

1. [Exact command or action]
2. [Next step if applicable]

## Expected behavior

[What should have happened.]

## Actual behavior

[What happened instead.]

## Error output

```
[Exact error message or log, verbatim]
```

## Environment

- Version: [X.Y.Z]
- OS: [e.g. Ubuntu 24.04, macOS 15.1]
- [Any other relevant environment details]
```

### Step 4: Review with the user

Present the draft and ask:
- "Does this accurately capture what you observed?"
- "Is there anything I added that you didn't actually verify yourself?"

Remove anything the user cannot personally confirm.

## Philosophy

As Armin Ronacher notes about AI-generated issue reports:

> The most frustrating failure mode right now is that people submit issues that are not in their own voice. They contain an observed problem somewhere, but it has been thrown into a clanker and the clanker reworded it and made a huge mess of it. Typically, it was prompted so badly that the conclusions produced are more often than not inaccurate but always full of confidence. The result is complete guesswork on root causes, fake-minimal repros, suggested implementation strategies, analogies to adjacent but often the wrong code, and long lists of error classes that might or might not matter.

The goal is to condense issue reports to what the human actually observed — nothing more.

## References

- [Quoting Armin Ronacher — Simon Willison](https://simonwillison.net/2026/May/24/armin-ronacher/#atom-everything)
- [Original post by Armin Ronacher](https://lucumr.pocoo.org/2026/5/24/pi-oss/)
