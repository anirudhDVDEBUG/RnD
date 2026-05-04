# Technical Details: Doc Audit

## What It Does

Doc Audit is a Claude Code skill that implements a 7-phase pipeline for auditing documentation against a live codebase. It uses Claude's code understanding to extract verifiable claims from docs (file paths, function signatures, CLI commands, dependency versions), then cross-references each claim against the actual source tree. Discrepancies are triaged by severity, resolved interactively with the developer, and committed as individual atomic changes.

The final phase specifically targets CLAUDE.md — the instruction file for Claude Code itself — trimming it down to only claims that are still true and instructions that aren't redundant with tooling already in place.

## Architecture

### Key Files

- `SKILL.md` — The skill definition; contains the full pipeline instructions Claude follows
- No runtime code — this is a pure prompt-engineering skill that leverages Claude Code's built-in file reading, grep, glob, and git capabilities

### Data Flow

```
Discovery (glob *.md, find docstrings)
    ↓
Claim Extraction (parse each doc → list of assertions)
    ↓
Cross-Reference (for each claim: read/grep actual code)
    ↓
Triage (classify: Critical / Stale / Minor / OK)
    ↓
Interactive Resolution (user chooses fix strategy per issue)
    ↓
Atomic Commits (git commit per fix)
    ↓
CLAUDE.md Trim (remove redundant/stale lines, show diff)
```

### Dependencies

- **Claude Code** with skills support (the only runtime dependency)
- **Git** (for atomic commits)
- No external APIs, no pip packages, no node modules

### Model Calls

Every phase runs within a single Claude Code session. The skill doesn't make separate API calls — it instructs Claude Code how to use its existing tools (Read, Grep, Glob, Bash/git) in a structured sequence.

## Limitations

- **No automated testing of CLI claims**: if docs say "run `npm test`", it verifies the script exists in package.json but doesn't execute it to confirm it passes
- **Subjective claims ignored**: "this project is fast" or "easy to use" are skipped — only verifiable factual claims are checked
- **Large repos**: in repos with 100+ doc files, the discovery phase may hit context limits; works best with <50 doc files
- **No cross-repo checks**: can't verify claims about external services or URLs being live
- **Interactive only**: requires human in the loop for resolution decisions (by design)

## Why It Matters

For teams building Claude-driven products (agent factories, lead-gen tools, marketing automation):

1. **CLAUDE.md hygiene**: stale CLAUDE.md instructions cause Claude to hallucinate or follow outdated patterns — this skill keeps the instruction file honest
2. **Onboarding speed**: accurate docs mean new team members (and new Claude sessions) ramp up faster
3. **Trust**: if your docs lie about your API, your AI-generated integrations will be wrong from the start
4. **Maintenance cost**: documentation debt compounds — catching drift early prevents expensive rewrites

## Source

- [MahmoudKhaledd/claude-skill-doc-audit](https://github.com/MahmoudKhaledd/claude-skill-doc-audit)
