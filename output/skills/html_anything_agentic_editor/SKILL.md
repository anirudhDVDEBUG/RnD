---
name: html_anything_agentic_editor
description: |
  Agentic HTML editor skill — generates production-ready HTML for multiple surfaces (magazine, deck, poster, social post, prototype, data report, Hyperframes) using nexu-io/html-anything.
  Triggers: "create an HTML page", "generate a poster", "make a slide deck in HTML", "design a magazine layout", "build an HTML prototype", "create a social media card", "generate a data report", "html-anything"
---

# HTML Anything — Agentic HTML Editor

Use the [nexu-io/html-anything](https://github.com/nexu-io/html-anything) toolkit to generate polished, single-file HTML content across 9 surface types with 75+ built-in design skills. Your local AI agent writes the HTML — you ship it.

## When to use

- "Create an HTML landing page / poster / magazine layout"
- "Generate a slide deck as a single HTML file"
- "Design a social media card for XHS / Twitter / WeChat"
- "Build an interactive prototype in HTML"
- "Create a data report with charts and visuals as HTML"

## Surfaces

| Surface | Description |
|---------|-------------|
| **Magazine** | Long-form editorial layouts with rich typography |
| **Deck** | Slide-based presentations in a single HTML file |
| **Poster** | Print-ready or digital poster designs |
| **XHS / Tweet** | Social media cards sized for Xiaohongshu, X (Twitter), Zhihu |
| **Prototype** | Interactive UI prototypes with clickable elements |
| **Data Report** | Structured reports with tables, charts, and data visualization |
| **Hyperframes** | Multi-frame interactive HTML experiences |

## How to use

### 1. Install html-anything

```bash
git clone https://github.com/nexu-io/html-anything.git
cd html-anything
npm install
npm run dev
```

The local dev server provides a sandboxed preview environment.

### 2. Generate HTML content

When asked to create visual HTML content, follow these steps:

1. **Choose the surface** — Determine which surface type fits the request (deck, poster, magazine, social card, prototype, data report, or Hyperframes).

2. **Write a single self-contained HTML file** — All CSS and JS must be inline. Use modern CSS (grid, flexbox, custom properties) for layout. Include all assets inline (SVG, base64 images, or CSS gradients).

3. **Follow design best practices:**
   - Use a cohesive color palette (3-5 colors max)
   - Apply consistent typography with a clear hierarchy
   - Ensure responsive sizing appropriate to the chosen surface
   - For decks: use CSS scroll-snap for slide transitions
   - For posters: use fixed dimensions (e.g., A3, 1080×1920)
   - For social cards: match platform aspect ratios (1:1 for XHS, 16:9 for Twitter)
   - For data reports: use semantic HTML tables and inline SVG charts

4. **Save the file** to the html-anything project directory or the current working directory.

5. **Preview** — Open in the html-anything sandboxed preview server, or directly in a browser.

### 3. Export

html-anything supports 1-click export to multiple targets:

- **HTML** — Standalone `.html` file, ready to deploy
- **PNG** — Rasterized screenshot for sharing
- **WeChat** — Formatted for WeChat article embedding
- **X (Twitter)** — Optimized card format
- **Zhihu** — Compatible with Zhihu article format

### 4. Example: Generate a presentation deck

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Quarterly Review</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-snap-type: y mandatory; }
    .slide {
      height: 100vh; width: 100vw;
      scroll-snap-align: start;
      display: flex; align-items: center; justify-content: center;
      flex-direction: column; padding: 4rem;
      font-family: system-ui, sans-serif;
    }
    .slide:nth-child(odd) { background: #1a1a2e; color: #eee; }
    .slide:nth-child(even) { background: #f0f0f5; color: #1a1a2e; }
    h1 { font-size: 3rem; margin-bottom: 1rem; }
    p { font-size: 1.4rem; max-width: 600px; text-align: center; }
  </style>
</head>
<body>
  <div class="slide">
    <h1>Q1 2026 Review</h1>
    <p>Key highlights and metrics</p>
  </div>
  <div class="slide">
    <h1>Revenue Growth</h1>
    <p>+32% quarter-over-quarter</p>
  </div>
</body>
</html>
```

## Key principles

- **Zero API key required** — Works with Claude Code, Cursor, Codex, Gemini, Copilot, and other coding agents out of the box
- **Local-first** — All generation and preview happens locally with sandboxed rendering
- **Single-file output** — Every surface produces one self-contained HTML file with no external dependencies
- **BYOK (Bring Your Own Key)** — Compatible with any LLM backend the user has configured

## References

- Repository: https://github.com/nexu-io/html-anything
- 75 built-in skills across 9 surface types
- Built with Next.js, supports HTML/PNG/social platform export
