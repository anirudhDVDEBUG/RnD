# Technical Details

## What It Does

This is a Claude Code agent skill (prompt-based, no runtime server) that
constrains LLM output when writing Chinese-language postmortem documents.
It enforces:

- **Tone**: Objective, blameless third-person (客观冷静，不指责个人)
- **Syntax**: Short sentences (≤30 chars), English technical terms preserved
- **Structure**: Mandatory sections — summary, impact table, timeline, 5-Whys
  root cause, fix, action items with owner/deadline/acceptance, lessons learned
- **Formatting**: ISO 8601 timestamps, quantified metrics, Markdown tables

The companion Python script (`postmortem_generator.py`) provides a standalone
demonstration: it takes structured incident data and produces a formatted
postmortem, then lints it against the style rules.

## Architecture

```
SKILL.md                  ← Prompt injected into Claude Code context
                            (tone rules, structure template, review checklist)

postmortem_generator.py   ← Standalone demo / reference implementation
  ├─ IncidentData         ← Dataclass for structured incident input
  ├─ generate_postmortem()← Renders incident → Markdown postmortem
  ├─ lint_postmortem()    ← Style checker (sentence length, blame detection,
  │                          required sections, time format)
  └─ main()              ← Demo with realistic mock data
```

**Dependencies**: Python 3.10+ stdlib only (re, dataclasses, json).
No model calls, no API keys, no external packages.

**Data flow** (when used as a Claude Code skill):
1. User triggers skill with a phrase like "写 postmortem"
2. Claude loads `SKILL.md` system prompt constraints
3. Claude interviews user or accepts structured input
4. Claude generates postmortem following mandated template
5. Claude self-checks against the review checklist in the skill

## Limitations

- **Prompt-only enforcement** — the style rules rely on Claude following
  instructions. There's no hard runtime validation when used as a skill
  (the Python linter is a separate offline tool).
- **Chinese-only** — tone/syntax rules are designed for Simplified Chinese
  technical writing. English postmortems need different conventions.
- **Postmortem scope only** — the full `luoling8192/technical-writing` repo
  covers 4 document types (design docs, review drafts, postmortems, sharing
  decks). This prototype only implements the postmortem scenario.
- **No LLM integration in demo** — the Python script uses mock data to show
  output format; it doesn't call Claude API. The real value comes from
  installing the SKILL.md into Claude Code.

## Why It Matters

For teams building Claude-driven products:

- **Agent factories**: Shows how a single SKILL.md file can constrain Claude's
  output format for domain-specific documents — a pattern reusable for any
  vertical (legal, medical, financial reporting).
- **Quality at scale**: Postmortems written by 50 engineers now follow the same
  structure, making them searchable, comparable, and automatable.
- **Lead-gen / consulting**: Firms selling SRE-as-a-service can embed this
  skill to produce client-ready incident reports automatically.
- **Composable skills**: Demonstrates the Claude Code skill pattern — drop a
  markdown file, get constrained behavior. No server, no deploy, no infra.
