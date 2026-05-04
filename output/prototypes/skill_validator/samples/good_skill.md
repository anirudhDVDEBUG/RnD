---
name: code_reviewer
description: |
  Review code changes for bugs, style issues, and security concerns.
  TRIGGER: user says "review my code", "check this PR", "code review", "find bugs in my code", or references reviewing/auditing code changes.
---

# Code Reviewer

Automated code review that checks for bugs, style violations, and security concerns.

## When to use

- "Review my code changes"
- "Check this PR for issues"
- "Find bugs in my code"
- "Do a code review on this file"
- "Are there security issues in my changes?"

## How to use

1. **Identify the target** — Use `git diff` or read the file the user specifies.
2. **Analyze the code** — Check for common bug patterns, style violations, and OWASP top-10 security issues.
3. **Generate the report** — Output a structured review with severity levels and suggested fixes.
4. **Offer to apply fixes** — If critical issues are found, offer to apply the suggested changes using the Edit tool.

## References

- Source: [example/code-reviewer](https://github.com/example/code-reviewer)
- OWASP Top 10: [owasp.org/top10](https://owasp.org/www-project-top-ten/)
