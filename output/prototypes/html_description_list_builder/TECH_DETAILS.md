# Technical Details

## What it does

This skill/tool generates spec-correct HTML `<dl>` (description list) markup from structured key-value data. It encodes the rules from the HTML5 spec that most developers get wrong: `<div>` is the *only* valid grouping element inside `<dl>`, a single `<dt>` can have multiple `<dd>` siblings, and `<dl>` has been "description list" (not "definition list") since 2008. The tool enforces these rules automatically so Claude always produces valid output.

The source material is Ben Myers' article ["On the \<dl\>"](https://benmyers.dev/blog/on-the-dl/), surfaced by Simon Willison. It's a deep dive into the semantics, accessibility, and correct usage of `<dl>`/`<dt>`/`<dd>` — an element most developers underuse or misuse.

## Architecture

```
examples.json          -- sample data (4 scenarios)
dl_builder.py          -- core logic (~70 lines)
  build_dl()           -- pure function: items[] -> HTML string
  main()               -- CLI wrapper: reads JSON from stdin or file arg
SKILL.md               -- Claude Code skill definition (trigger + rules)
run.sh                 -- demo runner, exercises all examples
```

**Data flow:** JSON input (file, stdin, or Python dict) -> `build_dl()` -> indented HTML string.

**Dependencies:** Python 3.9+ stdlib only (`json`, `sys`, `typing`). No pip packages.

**No model calls.** This is pure template logic — no LLM API needed. The skill file teaches Claude *when and how* to apply the rules; the Python script is a standalone reference implementation.

## Limitations

- **No HTML escaping.** Terms and descriptions are inserted as-is. If your data contains `<`, `>`, or `&`, sanitize before passing in (or extend with `html.escape()`).
- **No nested structures.** Each description is a flat string — no support for inline HTML, links, or nested lists inside `<dd>`.
- **No CSS output.** The tool produces markup only. Styling (grid, flexbox, etc.) is left to the consumer.
- **English-centric.** Heading text auto-generation title-cases the heading ID; may not suit all languages.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Lead-gen / marketing sites** | Product feature tables, pricing comparisons, and FAQ sections are natural `<dl>` use cases. Correct semantics improve SEO and screen-reader UX. |
| **Agent factories** | Agents that generate HTML (landing pages, emails, reports) need guardrails to produce valid markup. This skill prevents common `<dl>` mistakes without extra validation steps. |
| **Ad creatives** | Structured product specs in ads benefit from semantic HTML — screen readers and crawlers parse `<dl>` correctly where `<ul>` or `<table>` would be semantically wrong. |
| **Accessibility compliance** | ARIA-labeled description lists satisfy WCAG requirements. Automating this removes a common audit finding. |
