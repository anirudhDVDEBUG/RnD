---
name: html_rich_output
description: |
  Generate rich, interactive HTML output instead of plain Markdown for explanations, reviews, visualizations, and documentation.
  TRIGGER when: user asks for an explanation with diagrams, a PR review artifact, an interactive visualization, a rich report, or says "make it HTML", "render as HTML", "create an HTML artifact", "visual explanation", "interactive output".
  DO NOT TRIGGER when: user wants a simple text answer, wants to edit existing HTML files, or is building a web application.
---

# HTML Rich Output

Generate rich, interactive HTML documents as output instead of plain Markdown. HTML allows inline SVG diagrams, color-coded annotations, collapsible sections, interactive widgets, in-page navigation, and other features that make complex information easier to understand.

## When to use

- "Help me review this PR by creating an HTML artifact that describes it"
- "Explain this code visually with diagrams"
- "Create a rich HTML report of these findings"
- "Give me an interactive visualization of this data"
- "Render this diff with inline annotations and color-coding"

## How to use

1. **Identify the output goal.** Determine what the user wants explained, reviewed, or visualized.

2. **Create a single self-contained HTML file.** Write the output as a standalone `.html` file with all CSS and JS inlined (no external dependencies). Place it in the current working directory with a descriptive filename.

3. **Use rich HTML features where they add value:**
   - **SVG diagrams** for architecture, data flow, or concept illustrations
   - **Color-coded sections** for severity levels, diff annotations, or categorization
   - **Collapsible `<details>` elements** for hiding verbose content behind summaries
   - **Sticky navigation / table of contents** for long documents
   - **Inline `<style>` blocks** with a clean, readable design (light background, good contrast, readable fonts)
   - **Interactive elements** using vanilla JS (tabs, filters, search, toggles)
   - **Syntax-highlighted code blocks** using `<pre><code>` with inline CSS coloring
   - **Tables with alternating row colors** for structured data

4. **Follow these HTML output conventions:**
   - Use `<!DOCTYPE html>` with `<meta charset="utf-8">` and a viewport meta tag
   - Include a `<title>` matching the content
   - Keep all styles in a single `<style>` block in `<head>`
   - Keep all scripts in a single `<script>` block before `</body>`
   - Use semantic HTML (`<main>`, `<section>`, `<article>`, `<nav>`, `<header>`)
   - Make the page responsive and readable on different screen sizes
   - Use a professional color palette (not garish)

5. **Tell the user how to view it.** After writing the file, inform the user they can open it in a browser (e.g., `open output.html` on macOS, `xdg-open output.html` on Linux).

## Example prompt patterns

**PR Review:**
> Create an HTML artifact reviewing this PR. Render the actual diff with inline margin annotations, color-code findings by severity.

**Code Explanation:**
> Explain how this streaming/backpressure logic works as an interactive HTML page with SVG flow diagrams.

**Data Report:**
> Summarize these benchmark results as a rich HTML report with charts and sortable tables.

## References

- Source article: [Using Claude Code: The Unreasonable Effectiveness of HTML](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything)
- Examples gallery: https://thariqs.github.io/html-effectiveness/
- Related: [Useful patterns for building HTML tools](https://simonwillison.net/2025/Dec/10/html-tools/)
