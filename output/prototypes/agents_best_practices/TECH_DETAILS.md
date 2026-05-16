# Technical Details

## What It Does

This is a **knowledge injection skill** for Claude Code. It provides a structured reference document (SKILL.md) that Claude Code loads into context when it detects the user asking about agent design, agentic workflows, prompt engineering for agents, or MCP integration. The skill contains provider-neutral patterns and principles distilled from production agent systems — no code execution, no external calls, just high-quality reference material that shapes Claude's responses.

The skill covers six domains: agent design principles, workflow patterns (sequential, parallel, router, iterative, human-in-the-loop), prompt engineering techniques, cross-platform portability, quality/safety controls, and practical implementation steps.

## Architecture

```
~/.claude/skills/agents_best_practices/
└── SKILL.md          # Single file, ~3KB of structured best practices
```

- **No dependencies** — pure Markdown with YAML frontmatter
- **No model calls** — the skill IS the knowledge; Claude Code uses it as context
- **No data flow** — loaded on-demand when trigger conditions match
- **Trigger matching** — Claude Code's built-in skill system matches user intent against the `description` field in SKILL.md frontmatter

### Key Files in Source Repo

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill itself — YAML frontmatter + structured Markdown |
| `README.md` | Repo documentation |

## Limitations

- **Static knowledge** — patterns don't auto-update; you manually update SKILL.md as practices evolve
- **No execution** — this skill advises, it doesn't scaffold code or run agents for you
- **Trigger precision** — may activate on tangentially related queries (e.g., "how do I build an agent" when the user means a real estate agent)
- **Single-skill scope** — doesn't compose with other skills; if you have conflicting agent guidance in another skill, Claude may blend them unpredictably
- **No validation** — cannot verify whether the user actually follows the advice

## Why This Matters for Claude-Driven Products

| Domain | Relevance |
|--------|-----------|
| **Agent Factories** | Directly applicable — provides the architectural patterns for building agent-creation platforms |
| **Lead-Gen / Marketing** | Multi-agent pipelines (research → qualify → outreach) benefit from the sequential and router patterns |
| **Ad Creatives** | Iterative refinement pattern maps to creative generation → review → revision loops |
| **Voice AI** | Human-in-the-loop and fail-gracefully principles are critical for real-time voice agent design |
| **MCP Integration** | Explicit guidance on clean MCP server interfaces helps teams building tool-augmented agents |

The skill essentially codifies tribal knowledge that agent builders accumulate over months — having it available in-context means faster architecture decisions and fewer anti-patterns in production systems.
