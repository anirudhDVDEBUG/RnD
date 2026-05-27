# Hermes Dreaming -- Staged Self-Improvement Engine

**Nothing changes without your approval.** Hermes Dreaming analyzes an agent's interaction history, proposes updates to memory, skills, and facts, then waits at a human review gate before applying anything.

## Headline Result

```
$ bash run.sh
=== Dream: Generated 8 proposals ===
  [+] a3f1  memory_update   Remember user interest: Python         (conf: 80%)
  [+] b7c2  skill_update    Add skill: pytest                      (conf: 85%)
  [!] d9e4  fact_update     Correct fact: default_app_port         (conf: 85%)
  ...
=== Approved 8 | Applied 8 ===
  Memory: 4 entries | Skills: 4 entries | Facts: 1 entry
```

Zero API keys. Zero external deps. Pure Python 3.10+.

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- install, configure, run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- architecture, data flow, limitations
