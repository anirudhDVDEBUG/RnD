# How to Use: html_rich_output

## What it is

A **Claude Code skill** — a markdown file that teaches Claude a new output behavior. No server, no API keys, no runtime dependencies.

## Install (30 seconds)

```bash
# Create the skill directory and copy the file
mkdir -p ~/.claude/skills/html_rich_output
cp SKILL.md ~/.claude/skills/html_rich_output/SKILL.md
```

That's it. Claude Code automatically loads skills from `~/.claude/skills/` on startup.

## Trigger phrases

Say any of these (or similar) to Claude Code and the skill activates:

| Phrase | What you get |
|--------|-------------|
| "Create an HTML artifact reviewing this PR" | Color-coded review with inline annotations |
| "Explain this code visually with diagrams" | SVG flow diagrams + collapsible explanations |
| "Make it HTML" / "Render as HTML" | Converts any explanation to rich HTML |
| "Create a rich report of these findings" | Structured report with navigation + filters |
| "Give me an interactive visualization" | Charts, sortable tables, toggleable views |

## First 60 seconds

**1. Install the skill** (see above).

**2. Open Claude Code in any project** and ask:

```
Review this file and create an HTML artifact with your findings
```

**3. Claude generates a file** like `review_output.html` in your working directory.

**4. Open it:**

```bash
xdg-open review_output.html   # Linux
open review_output.html        # macOS
```

You'll see a full interactive page — sticky header, severity badges, collapsible details, code diffs with suggestions, all in one self-contained file.

## Running the demo

This repo includes a standalone Python demo that shows what the skill's output looks like:

```bash
bash run.sh
```

This generates `pr_review_output.html` — a mock PR review with 6 findings, an SVG architecture diagram, and interactive severity filtering. Open it in any browser.

## Notes

- The skill produces **self-contained HTML** — no CDN links, no external JS/CSS. Works offline.
- Output files are placed in your **current working directory**.
- The skill does NOT trigger for simple text questions or when you're building a web app — only when you explicitly ask for rich/visual/HTML output.
