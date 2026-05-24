# Technical Details

## What it does

Claude Design Studio is a template-based UI/UX generator that turns structured design specifications into self-contained HTML/CSS files. It ships as both a CLI tool and a Claude Code skill. The CLI accepts layout type, theme, accent color, and title as arguments (or a JSON spec file) and outputs a single HTML file with inline CSS — no JavaScript, no build step, no external assets. The Claude Code skill wraps this capability so that natural-language design prompts trigger structured HTML generation inside an agent session.

The core idea is composable components: sidebar, header, metric cards, charts, tables, forms, hero sections, and feature grids are each rendered independently and assembled based on the chosen layout template (dashboard, landing, form, card-grid). A palette generator derives a full color system from one accent hex + theme mode.

## Architecture

```
design_studio.py          # Single-file implementation
  DesignSpec              # Dataclass: title, layout, theme, accent, etc.
  palette_from_accent()   # Generates full light/dark palette from one hex color
  render_*()              # Component renderers (sidebar, header, metrics, chart, table, form, hero, features)
  generate_css()          # Builds complete stylesheet from palette + layout
  generate_design()       # Assembles components into full HTML page
  main()                  # CLI entry point (argparse)
```

**Data flow:** CLI args or JSON spec -> `DesignSpec` -> `palette_from_accent()` -> component renderers + `generate_css()` -> single HTML string -> file write.

**Dependencies:** Python 3.10+ standard library only (`json`, `os`, `argparse`, `dataclasses`). Zero third-party packages.

**Model calls:** None. The generator is deterministic and runs offline. When used as a Claude Code skill, Claude itself acts as the "model" that interprets natural language and decides which design parameters to use.

## Key files

| File | Purpose |
|------|---------|
| `design_studio.py` | All generation logic (palette, components, CSS, assembly) |
| `SKILL.md` | Claude Code skill definition (trigger phrases, usage instructions) |
| `run.sh` | End-to-end demo producing 4 HTML designs |

## Limitations

- **Four layout templates only:** dashboard, landing, form, card-grid. No freeform layout engine.
- **No JavaScript:** outputs are static HTML/CSS. No interactive charts, no animations beyond CSS hover.
- **No image assets:** uses text, CSS shapes, and Unicode symbols only.
- **No responsive breakpoints in current templates:** layouts use CSS Grid `auto-fit` but lack explicit media queries for mobile.
- **Mock data only:** metric values, table rows, and chart bars are hardcoded samples.
- **Single-page output:** does not generate multi-page sites or navigation between pages.

## Why it matters

For teams building Claude-driven products (lead-gen landing pages, marketing dashboards, ad creative previews, agent factory UIs):

- **Rapid prototyping:** go from idea to browser-viewable mockup in seconds, without Figma licenses or designer availability.
- **Skill composability:** the Claude Code skill pattern means this can be chained with other skills — e.g., generate a dashboard mockup, then hand it to a code-generation skill for React conversion.
- **Zero-dependency deploys:** output HTML files work anywhere — email them, drop them in S3, embed in docs.
- **Design system seeding:** the palette generator and component structure give teams a starting point for design tokens and component libraries.
