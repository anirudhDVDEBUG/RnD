## Summary
The staged diff introduces a new user registration endpoint. There are two significant issues: an SQL injection vulnerability and a missing rate-limit check.

## Findings

| # | Severity | File | Line | Description | Suggestion |
|---|----------|------|------|-------------|------------|
| 1 | critical | auth/register.py | 42 | Raw string interpolation in SQL query allows injection. | Use parameterised queries: `cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))` |
| 2 | warning | auth/register.py | 58 | No rate-limiting on registration endpoint; enables brute-force account creation. | Add `@rate_limit(max=5, per=60)` decorator. |
| 3 | info | auth/register.py | 15 | Unused import `os` — dead code. | Remove `import os`. |

## Verdict: needs-work
