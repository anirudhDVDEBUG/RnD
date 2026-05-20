# How to Use: Gemini 3.5 Flash Guide Skill

## Install (30 seconds)

This is a **Claude Code skill** — a markdown file that Claude reads when trigger phrases match.

```bash
# Clone or copy the skill folder into Claude's skills directory
mkdir -p ~/.claude/skills
cp -r gemini_35_flash_guide ~/.claude/skills/gemini_35_flash_guide
```

No `pip install`, no `npm install`, no API keys. The skill is pure markdown consumed by Claude Code at runtime.

## What triggers it

Claude Code activates this skill when you mention any of:

| Trigger phrase | Example |
|---|---|
| `Gemini 3.5 Flash` | "What can Gemini 3.5 Flash do?" |
| `gemini-3.5-flash` | "Use gemini-3.5-flash for this task" |
| `Google I/O 2026` | "What models dropped at Google I/O 2026?" |
| `Gemini Flash pricing` | "Compare Gemini Flash pricing" |
| `migrating from Gemini 3 Flash Preview` | "I need to migrate from Gemini 3 Flash Preview" |

## First 60 seconds

**Step 1 — Install the skill** (see above).

**Step 2 — Open Claude Code** and ask a question:

```
You: What's the model ID for the latest Gemini Flash and how much does it cost?
```

**Step 3 — Claude responds** with structured data from the skill:

```
The latest Gemini Flash model is gemini-3.5-flash (GA, no -preview suffix).

Pricing per 1M tokens:
  Input:  $0.30
  Output: $1.20

This is roughly 3x the cost of Gemini 2.0 Flash ($0.10 / $0.40).
It skipped the preview stage and went straight to general availability.
```

**Step 4 — Ask a follow-up:**

```
You: Show me a Python snippet to call it.
```

Claude returns the `google-generativeai` SDK code and curl equivalent from the skill, ready to paste.

## Running the standalone demo

If you want to see the skill's content exercised outside Claude Code:

```bash
bash run.sh
```

This runs `demo.py`, which simulates four trigger scenarios (model spec, pricing comparison, API snippet, migration checklist) and prints the results. No API key or network access required.

## File layout

```
gemini_35_flash_guide/
├── SKILL.md           # The actual skill file Claude Code reads
├── demo.py            # Standalone demo exercising the skill content
├── run.sh             # One-command runner
├── requirements.txt   # Dependencies (stdlib only for demo)
├── README.md          # Overview
├── HOW_TO_USE.md      # This file
└── TECH_DETAILS.md    # Architecture and limitations
```
