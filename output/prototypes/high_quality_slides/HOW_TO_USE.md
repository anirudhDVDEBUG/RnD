# How to Use: High-Quality Slides Skill

## What this is

A **Claude Code skill** (not an MCP server, not a CLI tool). You drop a markdown file into your skills directory and Claude Code gains the ability to generate presentation-quality HTML slide decks on demand.

## Install the skill

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/high_quality_slides

# Copy the skill definition
cp SKILL.md ~/.claude/skills/high_quality_slides/SKILL.md
```

That's it. No `pip install`, no `npm install`, no API keys.

## Trigger phrases

Say any of these to Claude Code and the skill activates:

- "Create a presentation about [topic]"
- "Make slides for my talk on [subject]"
- "Build a pitch deck for [product/idea]"
- "Generate a slide deck summarizing [content]"
- "Turn this research into a presentation"

## First 60 seconds

**Input** (in Claude Code):
```
Create a presentation about the rise of AI agents in enterprise software
```

**What happens:**
1. Claude researches the topic (web search, file reading, codebase exploration)
2. Designs a narrative arc: opening hook -> 3-5 body sections -> closing CTA
3. Writes concise bullet content (max 6 bullets, max 8 words each)
4. Generates a single self-contained HTML file with all CSS/JS inline
5. Reviews for factual accuracy, flow, and grammar

**Output:** A file like `slides.html` in your working directory.

```
slides.html (single file, ~8 KB, zero dependencies)
  - Title slide with gradient headline
  - 5-7 content slides with bullets and speaker notes
  - Closing slide with call-to-action
  - Arrow key / Space / F(ullscreen) navigation
  - Progress bar at top
  - Print-friendly styles
```

Open it: `open slides.html` (macOS) or `xdg-open slides.html` (Linux).

## Running the standalone demo

This repo includes a Python demo that shows what the skill's output looks like:

```bash
# No dependencies needed (Python 3.7+ standard library only)
bash run.sh
```

This generates two sample HTML decks:
- `slides_ai_agents.html` -- 9-slide deck on AI agents
- `slides_claude_skills.html` -- 7-slide deck on building Claude skills

## Customization tips

When triggering the skill, you can specify:

| Parameter | Example |
|-----------|---------|
| Audience | "for a technical audience" / "for executives" |
| Slide count | "make it 8 slides" (default: 10-15) |
| Colors | "use blue and white branding" |
| Source material | "based on this document: [paste/link]" |
| Purpose | "for a live talk" / "for async reading" / "pitch deck" |
