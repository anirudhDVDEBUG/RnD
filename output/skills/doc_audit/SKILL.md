---
name: doc-audit
description: |
  Audit your repo's documentation against the actual codebase, then trim CLAUDE.md back to essentials.
  TRIGGER: user says "audit docs", "check documentation", "docs out of date", "trim CLAUDE.md", "documentation drift", "stale docs", "doc debt"
---

# Doc Audit — Documentation Reality-Check & Trim

A 7-phase pipeline that discovers every doc in your repo, extracts the claims they make, cross-references those claims against the actual code, triages discrepancies, walks you through interactive resolution, creates atomic commits for each fix, and finally trims your CLAUDE.md down to the essentials.

## When to use

- "Audit my docs against the codebase"
- "Check if my documentation is out of date"
- "Trim my CLAUDE.md to only what matters"
- "Find stale or inaccurate documentation"
- "Clean up documentation tech debt"

## How to use

### Phase 1 — Discovery
Scan the repo for all documentation files: README.md, CLAUDE.md, CONTRIBUTING.md, docs/, inline doc-comments, and any other markdown or text files that make claims about the codebase.

```
Find every .md file, docstring, and structured comment across the repo.
Build an inventory of all documentation sources.
```

### Phase 2 — Claim Extraction
Parse each doc and extract discrete, verifiable claims (e.g., "the project uses Express 4", "run `npm test` to execute the test suite", "`src/auth.ts` exports a `validateToken` function").

### Phase 3 — Cross-Reference
For each extracted claim, check the actual codebase:
- Does the referenced file/function/class exist?
- Does the described behavior match the implementation?
- Are CLI commands, env vars, and config options accurate?
- Are dependency versions correct?

### Phase 4 — Triage
Categorize every discrepancy by severity:
- **Critical**: completely wrong (references deleted files, wrong API signatures)
- **Stale**: partially outdated (old defaults, renamed params)
- **Minor**: cosmetic or low-impact (typos in paths, outdated badge URLs)
- **OK**: claim is accurate — no action needed

Present a summary table of findings grouped by severity.

### Phase 5 — Interactive Resolution
For each Critical and Stale issue, present the discrepancy and ask the user:
1. **Fix the doc** to match the code
2. **Fix the code** to match the doc
3. **Remove the claim** entirely
4. **Skip** for now

### Phase 6 — Atomic Commits
Apply each accepted fix as its own atomic commit with a clear message, e.g.:
```
docs: fix validateToken signature in README to match src/auth.ts
```

### Phase 7 — CLAUDE.md Trim
Review CLAUDE.md (if present) and remove:
- Redundant instructions that duplicate repo conventions already enforced by tooling
- Outdated references resolved in earlier phases
- Overly verbose sections that can be condensed
- Claims that no longer apply to the current codebase

Present the trimmed CLAUDE.md diff for user approval before committing.

## Tips

- Run this after major refactors, dependency upgrades, or when onboarding reveals confusion.
- Works best when the repo has a mix of README, CLAUDE.md, and inline docs to cross-check.
- Each fix is an atomic commit so you can easily revert individual changes.

## References

- Source: [MahmoudKhaledd/claude-skill-doc-audit](https://github.com/MahmoudKhaledd/claude-skill-doc-audit)
- Tags: documentation-audit, claude-skill, technical-debt, developer-tools
