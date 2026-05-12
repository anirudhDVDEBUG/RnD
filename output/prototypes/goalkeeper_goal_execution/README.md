# Goalkeeper: Contract-Driven Goal Execution

**TL;DR:** Goalkeeper enforces a "Definition of Done" contract on every goal.
A judge subagent independently evaluates each criterion as PASS/FAIL, and the
goal loops until every criterion passes -- or declares failure. Think of it as
a CI gate for autonomous agent work.

## Headline Result

```
Goal: User Registration Endpoint
  Iteration 1 -> 2/5 criteria PASS, 3 FAIL (incomplete code)
  Iteration 2 -> 5/5 criteria PASS
  Status: SUCCESS in 2 iterations
```

The judge caught missing password hashing, email validation, and duplicate-user
checks on the first pass, then verified the fixes on the second.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- install, configure, run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- architecture, data flow, limitations
