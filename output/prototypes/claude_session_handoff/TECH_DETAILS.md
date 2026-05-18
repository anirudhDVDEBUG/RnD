# Technical Details — Claude Session Handoff

## What It Does

Claude Session Handoff is a Claude Code skill that solves the "cold start" problem when switching between Claude sessions. Each time you end a session, the skill generates a structured `STATUS.md` document containing the branch name, last commit, uncommitted changes, completed tasks, blockers, and prioritized next steps. The next agent reads this file and resumes work without re-analyzing the entire codebase.

The skill operates entirely through Claude Code's skill system — it's a markdown instruction file that teaches Claude a specific workflow pattern. The companion Python script (`handoff.py`) in this prototype demonstrates the same logic standalone, reading real git state or using mock data.

## Architecture

### Skill Layer (SKILL.md)

The skill is a structured markdown file placed in `~/.claude/skills/claude-skill-handoff/SKILL.md`. Claude Code loads it automatically and follows the instructions when trigger phrases are detected. The skill defines:

- **Trigger phrases** — natural language patterns that activate the workflow
- **STATUS.md template** — the exact format for handoff documents
- **Commit protocol** — `[WIP]` prefix convention for in-progress snapshots
- **Receiving protocol** — how the next agent should bootstrap from STATUS.md

### Python Demo (handoff.py)

```
handoff.py
  ├── detect_git_state()    — runs git commands, collects branch/commit/diff/status
  ├── mock_git_state()      — returns realistic fake state for demos
  ├── generate_status_md()  — templates state + annotations into STATUS.md format
  └── main()                — CLI: --mock, --repo, --output, --json
```

**Data flow**: `git CLI → detect_git_state() → dict → generate_status_md() → markdown string → file or stdout`

### Key Files

| File | Purpose |
|---|---|
| `SKILL.md` | Claude Code skill definition (the actual product) |
| `handoff.py` | Standalone Python demo of the handoff logic |
| `run.sh` | End-to-end demo script |
| `STATUS.md` | Generated output (created by the tool at runtime) |

### Dependencies

**Zero external dependencies.** The Python script uses only stdlib modules: `subprocess`, `argparse`, `json`, `pathlib`, `datetime`. The skill itself is pure markdown — no runtime dependencies at all.

## Limitations

- **No cross-machine state** — STATUS.md lives in the repo. If you switch machines, you need to push/pull the commit containing it.
- **No automatic trigger** — the user must explicitly ask for a handoff. There's no hook that fires on session end.
- **Git-centric** — the skill assumes a git workflow. Non-git projects get a degraded experience (no branch/commit/diff info).
- **No binary state** — STATUS.md captures text summaries, not full memory snapshots. Complex mental models or multi-file reasoning chains are lossy.
- **Single-project scope** — each STATUS.md covers one repo. Multi-repo workflows need separate handoffs.
- **No conflict resolution** — if two agents write STATUS.md concurrently, standard git merge conflicts apply.

## Why This Matters for Claude-Driven Products

**Agent factories / orchestration**: Any system that spawns multiple Claude sessions for a single project (e.g., one agent per feature branch, or a supervisor + worker pattern) needs structured handoff. This skill provides the protocol.

**Developer tools / productivity**: Teams using Claude Code for daily coding hit the "context amnesia" wall every session. A 30-second handoff saves 5-10 minutes of re-orientation per session start.

**Lead-gen / marketing automation**: Long-running content campaigns managed by Claude agents benefit from session continuity — the next agent knows which assets were created, which are in review, and what's next in the pipeline.

**Cost optimization**: Instead of maintaining expensive long-running sessions, teams can use short sessions with structured handoffs, reducing API costs while preserving continuity.
