# Vibe Coding vs Agentic Engineering Review

**A Claude Code skill that reviews AI-generated diffs and scores them on Simon Willison's vibe-coding-to-agentic-engineering spectrum.** It catches the anti-patterns that slip through when you stop reading AI output carefully — nested error handling, scope creep, missing tests, security gaps — and tells you whether to ship, revise, or start over.

### Headline result

```
  Diff                                Score  Verdict          Context
  ------------------------------------------------------------------
  Vibe-coded auth endpoint            20/100  START OVER       production
  Well-reviewed utility function      97/100  SHIP IT          production
  Scope-creep refactor                74/100  NEEDS REVISION   production
  Quick prototype script             100/100  SHIP IT          throwaway
```

### Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, detectors, limitations, why it matters

### Quick demo

```bash
bash run.sh
```

Source: [Vibe coding and agentic engineering are getting closer than I'd like](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/#atom-everything) — Simon Willison, May 2026
