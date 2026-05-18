# Technical Details

## What It Does

The HTML Slide Generator is a Claude Code skill (a structured prompt template in SKILL.md) that instructs Claude to produce single-file HTML presentations. There is no runtime, no framework, no build step — Claude's output IS the product: one `.html` file with inline CSS and vanilla JS that implements keyboard navigation, touch/swipe support, a progress bar, responsive typography via `clamp()`, and print styles.

The skill works by giving Claude a detailed structural template, layout vocabulary (title/content/image/two-column/quote/code/CTA slides), and design constraints (max 6 lines per slide, one idea per slide, high-contrast palettes). Claude fills in the content based on the user's topic/outline.

## Architecture

```
~/.claude/skills/html_slide_generator/SKILL.md
    |
    v
Claude Code (reads skill on matching trigger)
    |
    v
Single .html file written to working directory
    (inline CSS + vanilla JS, zero dependencies)
```

**Key components inside the generated HTML:**
- CSS: Flexbox slide layout, `clamp()` responsive font sizing, opacity transitions, `@media print`
- JS (~30 lines): Slide state machine, keyboard listener, touch event handler, progress updater
- No external fonts, no CDN links, no images unless user requests them

**Dependencies:** None at runtime. The skill itself requires only Claude Code (any version with skills support).

## Limitations

- **No speaker notes** — the generated deck is audience-facing only
- **No animations beyond fade** — keeps file size small and cross-browser safe
- **No embedded media** — images require base64 encoding (bloats file) or external URLs (breaks offline)
- **No PDF export built-in** — users must print-to-PDF from browser (print styles help here)
- **Slide count ceiling** — beyond ~30 slides, the single-file approach gets unwieldy
- **No collaborative editing** — it's a static file, not Google Slides

## Why It Matters

For teams building Claude-driven products:

- **Lead-gen / Marketing:** Instantly generate pitch decks, product overviews, or conference talks from bullet points. Sales teams can say "turn this email thread into a client deck" and get something presentable in seconds.
- **Agent Factories:** This is a clean example of a "skill as structured prompt" — no code to maintain, no API to host. Shows the pattern for building domain-specific Claude capabilities that ship as a single markdown file.
- **Ad Creatives:** The same template approach works for HTML ad units, landing pages, or email templates — self-contained HTML from natural language.
- **Content pipelines:** Combine with other skills (research, summarization) to go from raw notes to polished presentation in one agent loop.

## Source

[ToseaAI/awesome-html-slide-skills](https://github.com/ToseaAI/awesome-html-slide-skills) — curated list of HTML slide generation skills and template libraries for Claude Code, Codex, Cursor, and other AI agents.
