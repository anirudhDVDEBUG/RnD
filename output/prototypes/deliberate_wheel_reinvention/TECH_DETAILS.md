# Technical Details

## What it does

This is a Claude Code **skill** — a markdown file that extends Claude's behavior when dropped into `~/.claude/skills/`. When triggered, Claude guides users through a structured learning exercise: picking a well-scoped reimplementation target in their domain of interest, defining a minimal version with clear boundaries, and coaching them through building it with an attempt-first-then-compare methodology.

The companion CLI tool (`wheel_reinvention.py`) demonstrates the skill's curated knowledge base: 18 reimplementation targets across 6 domains, each with effort estimates, essential behaviors, explicit exclusions, done-conditions, and transferable principles.

## Architecture

```
SKILL.md                  # The actual skill — Claude reads this at trigger time
wheel_reinvention.py      # Standalone demo + reference data
run.sh                    # End-to-end demo runner
```

**Key files:**

- `SKILL.md` — Contains the 4-step pedagogical framework (identify wheel, scope it, build with directed questions, extract the lesson) plus the domain-by-wheel reference table. This is the file Claude loads.
- `wheel_reinvention.py` — Pure Python (stdlib only, no dependencies). Contains a `DOMAINS` dict mapping 6 domains to 3 wheels each. Each wheel entry includes `essential_behaviors`, `leave_out`, `done_condition`, `transferable_principles`, and `next_wheels`. The `LearningPlan` dataclass generates day-by-day checkpoints based on effort estimates.

**Data flow:** User triggers skill via natural language -> Claude reads SKILL.md -> Claude uses the framework to guide a conversation (no API calls, no external data). The CLI tool is a standalone demonstration of the same knowledge base.

**Dependencies:** None. Python 3.10+ standard library only.

## Limitations

- The wheel catalog is hand-curated (18 entries across 6 domains). It does not cover ML/AI, mobile, embedded, or game development.
- The skill relies on Claude's own knowledge to provide detailed implementation guidance — it provides the *framework* and *scoping*, not step-by-step code walkthroughs.
- Effort estimates (1-5 days) assume an intermediate developer. Beginners may need 2-3x; experts may finish in hours.
- No persistence — the skill doesn't track which wheels a user has already reinvented across sessions.

## Why it matters for Claude-driven products

The "deliberate wheel reinvention" pattern is directly relevant to anyone building with Claude:

- **Agent factories:** Teams building AI agent platforms often lack deep understanding of the subsystems they orchestrate (search, parsing, data pipelines). Reinventing a core component helps architects make better design decisions about where to use an LLM vs. deterministic code.
- **Lead-gen / marketing:** Understanding how search indexes, template engines, and form validators actually work lets you build better Claude-powered content pipelines and avoid black-box dependencies.
- **Voice AI:** Building a simple parser or state machine from scratch teaches the same patterns used in dialog management and intent routing.
- **General:** The skill models a best practice for technical teams: structured upskilling that produces real artifacts, not just reading. A team that has reinvented a few key wheels makes fewer architectural mistakes when building on top of them.

## Source

Based on Andrew Quinn's observation (via Simon Willison): reinventing 4-5 wheels in a domain gets you to the frontier faster than idle study. Quinn demonstrated this by replacing a 3 GB SQLite database with a 10 MB finite state transducer — a project only possible because he'd previously reinvented enough wheels to recognize the opportunity.
