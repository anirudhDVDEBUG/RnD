# Technical Details: High-Quality Slides

## What it does

This is a Claude Code skill that enforces a strict 5-phase workflow for generating HTML slide presentations. Rather than letting Claude produce slides in a single shot (which tends toward generic, text-heavy results), the skill breaks the process into Research, Narrative Architecture, Content Writing, Visual Design, and Review. Each phase has explicit quality gates -- e.g., max 6 bullets per slide, max 8 words per bullet, mandatory speaker notes, required keyboard navigation in the output.

The output is a single self-contained `.html` file with all CSS and JS inlined. No build step, no external CDN, no framework dependency. The file opens in any modern browser and supports arrow-key navigation, fullscreen mode, touch swipe, a progress bar, and print-friendly styles.

## Architecture

```
SKILL.md (the skill definition)
  |
  v
Claude Code (reads skill, follows 5-phase workflow)
  |
  +-- Phase 1: Research --> uses web search, file reading, codebase tools
  +-- Phase 2: Narrative Architecture --> designs story arc, slide outline
  +-- Phase 3: Content Writing --> writes bullets, speaker notes
  +-- Phase 4: HTML Generation --> produces single .html with inline CSS/JS
  +-- Phase 5: Review --> checks facts, flow, grammar, rendering
  |
  v
slides.html (self-contained, zero-dependency output)
```

**Key files in this demo repo:**

| File | Purpose |
|------|---------|
| `SKILL.md` | The actual skill definition (drop into `~/.claude/skills/`) |
| `generate_slides.py` | Standalone Python demo showing the output format |
| `run.sh` | Generates two sample decks for evaluation |

**Dependencies:** Python 3.7+ standard library only (`argparse`, `json`, `html`, `os`, `datetime`). The skill itself has zero dependencies -- it's a markdown file that Claude interprets.

**Model calls:** The skill doesn't make API calls itself. Claude Code's underlying model (Claude) does all the generation. The skill is a structured prompt that shapes Claude's output. In a typical run, Claude makes 1-3 web search calls during Phase 1 research, then generates the HTML in a single tool call.

## Limitations

- **No real-time data:** Research quality depends on Claude's web search tool availability. Without it, the skill falls back to Claude's training data.
- **No images:** The output is text-only HTML. No image generation, no stock photo integration. You can manually add `<img>` tags after generation.
- **No animations beyond transitions:** Slide transitions use CSS opacity/transform. No complex animations like chart builds or reveal sequences.
- **No collaboration features:** No export to PPTX/Google Slides. It's a standalone HTML file.
- **Speaker notes are data attributes:** They exist in the HTML but aren't displayed by default (you'd need a presenter view extension).
- **Single-file constraint:** Everything is inlined, so very large decks (30+ slides) produce large HTML files, though still typically under 50 KB.

## Why it matters

For teams building Claude-driven products:

- **Lead-gen / marketing:** Generate pitch decks and sales materials on demand. A sales agent could produce a custom deck per prospect using CRM data as research input.
- **Ad creatives:** The HTML output format could be adapted for interactive ad units or landing page hero sections.
- **Agent factories:** The 5-phase workflow pattern (research -> plan -> write -> build -> review) is a reusable template for any content-generation agent. Fork this skill to make agents that produce reports, proposals, or documentation.
- **Content at scale:** Combine with scheduling to auto-generate weekly briefing decks from data feeds.

The key insight is the **phased workflow with quality gates**. Most LLM slide generators produce mediocre output because they try to do everything in one pass. Forcing research-first and review-last dramatically improves coherence and factual accuracy.
