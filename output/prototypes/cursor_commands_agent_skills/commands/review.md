# /review

## Purpose
Perform a structured code review on staged changes or a given diff.

## Inputs
- `target`: File path, git ref, or "staged" (required)
- `severity_filter`: Minimum severity to report — critical | warning | info (optional, default: info)

## Behavior
1. Obtain the diff (staged changes, file, or ref range).
2. Analyze every hunk for:
   - Security issues (injection, secrets, auth bypass)
   - Performance problems (N+1, unbounded loops, large allocations)
   - Style violations (naming, formatting, dead code)
   - Logic errors (off-by-one, null deref, race conditions)
3. Rate each finding: **critical**, **warning**, or **info**.
4. For every finding, provide a concrete fix suggestion with a code snippet.
5. Produce a final verdict: **ship** | **needs-work** | **block**.

## Output Format

```
## Summary
<1-2 sentence overview>

## Findings

| # | Severity | File | Line | Description | Suggestion |
|---|----------|------|------|-------------|------------|
| 1 | critical | ... | ... | ... | ... |

## Verdict: <ship | needs-work | block>
```
