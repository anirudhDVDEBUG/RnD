# How To Use

## Installation (30 seconds)

This is a **Claude Code Skill** — no pip/npm install needed. Just place the skill file:

```bash
mkdir -p ~/.claude/skills/html_slide_generator
cp SKILL.md ~/.claude/skills/html_slide_generator/SKILL.md
```

That's it. Claude Code auto-discovers skills from `~/.claude/skills/`.

## Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Create a presentation about [topic]"
- "Turn these notes into slides"
- "Generate an HTML slide deck for my talk"
- "Make a pitch deck for [product/idea]"
- "Build a slideshow from this outline"

## First 60 Seconds

**Input** (you type in Claude Code):
```
Make a 5-slide presentation about why Python is great for data science
```

**Output** (Claude writes to your working directory):
```
python-data-science-slides.html
```

**Open it:**
```bash
# macOS
open python-data-science-slides.html

# Linux
xdg-open python-data-science-slides.html

# Or just drag into any browser
```

**Navigate:**
- Arrow keys / Space / Enter = next slide
- Left arrow / Backspace = previous slide
- Swipe on mobile
- Progress bar at bottom shows position

## Customization Tips

You can guide the output by being specific:

- "Dark theme, minimal, 8 slides" — controls aesthetics and length
- "Include a code slide showing a pandas example" — triggers code-slide layout
- "Two-column comparison of SQL vs NoSQL" — triggers two-column layout
- "End with a CTA slide linking to our signup page" — controls closing slide

## Running the Demo (no Claude needed)

```bash
bash run.sh
```

This runs a Python script that generates a sample presentation locally, proving the template works. Open `demo-output/ai-trends-2026-slides.html` in your browser.
