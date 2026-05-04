# Doc Audit — Catch Stale Documentation Before It Misleads

**A Claude Code skill that audits your repo's docs against the actual codebase, finds lies, and trims your CLAUDE.md back to essentials.**

## Headline Result

```
$ claude "audit docs"

Phase 3 — Cross-Reference complete:
  12 claims verified across 4 doc files
  3 CRITICAL: reference deleted files/wrong signatures
  2 STALE: outdated defaults, renamed params
  7 OK: accurate

Phase 5 — Interactive Resolution:
  > README.md L42: claims `validateToken(jwt)` but actual signature is `validateToken(token, opts)`
  > Fix doc / Fix code / Remove / Skip? [1]
```

Every fix becomes an atomic commit. CLAUDE.md gets trimmed to only what's true.

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install the skill in 30 seconds, trigger phrases
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, 7-phase pipeline, limitations

## Demo

```bash
bash run.sh
```

Runs a self-contained demo against a mock repo showing all 7 phases in action.
