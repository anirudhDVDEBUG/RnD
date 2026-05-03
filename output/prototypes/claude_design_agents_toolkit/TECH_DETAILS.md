# Technical Details — Claude Design Agents Toolkit

## What it does

The toolkit provides four template-driven Python agents that generate production-ready UI artifacts: responsive HTML layouts with Tailwind CSS, color palettes expanded into 10-shade scales, design token systems (CSS variables + Tailwind config), and structured component specifications. All generation is deterministic and offline — no LLM calls at runtime — making it suitable for Claude Code skill/hook integration where the AI orchestrates which agents to invoke based on user intent.

The design-lint hook module (`design_hooks.py`) performs static analysis on generated HTML, catching accessibility issues (missing alt tags, empty buttons), hardcoded colors/spacing that should use tokens, and missing responsive breakpoints.

## Architecture

```
design_agents.py        # Core module — all four agents + DesignTokens
  LayoutAgent           # Template lookup + variable interpolation
  ColorAgent            # HSL colour math -> 10-shade palettes
  ComponentAgent        # Structured spec registry (props, classes, HTML)
  DesignToCodeAgent     # Orchestrator: layout + tokens + Tailwind CDN -> full page

design_hooks.py         # Lint module — regex-based HTML static analysis
demo.py                 # CLI driver — runs all agents, writes output/
```

**Data flow:**
1. User selects layout type + theme -> `DesignToCodeAgent`
2. `ColorAgent` generates palettes via HSL manipulation (`colorsys`)
3. `LayoutAgent` interpolates app name into pre-built Tailwind templates
4. Output: standalone HTML (Tailwind CDN), CSS variables file, Tailwind config JSON
5. Optional: `design_hooks.lint_html()` checks output for consistency issues

**Dependencies:** Python 3.8+ standard library only (`colorsys`, `json`, `re`, `dataclasses`, `pathlib`). No pip packages.

**Model calls:** None at runtime. The toolkit is designed to be *called by* Claude Code as a skill, not to call Claude itself. Claude handles the NL understanding; the agents handle deterministic generation.

## Limitations

- **Template-bound:** Layout generation is limited to the three built-in templates (dashboard, landing, form). Custom layouts require adding new templates to `LAYOUT_TEMPLATES`.
- **No image/screenshot input:** Cannot parse Figma files, screenshots, or design images. "Design-to-code" means structured description to code, not visual-to-code.
- **No JavaScript logic:** Generated HTML is static markup + Tailwind classes. Interactive behavior (modals, dropdowns, state) must be added separately.
- **Five components only:** The component spec library covers button, card, input, avatar, and badge. Real projects need 20-50+ components.
- **No framework output:** Generates raw HTML, not React/Vue/Svelte components. Framework adaptation is left to Claude or the developer.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Lead-gen / marketing sites** | Generate landing pages with consistent brand tokens in seconds. Feed layout + theme to Claude, get deployable HTML. |
| **Ad creatives** | Rapid A/B variant generation — swap themes (`ocean` -> `sunset`) to produce visually distinct pages from the same layout. |
| **Agent factories** | Design agents are composable building blocks. An agent-factory system can wire `DesignToCodeAgent` into a pipeline that also generates copy, images, and deploys. |
| **Internal tools** | Dashboard layout + component specs give Claude a head start on admin panels, reducing prompt iterations. |
| **Design systems** | The token generation (palette expansion, CSS vars, Tailwind config) automates the tedious parts of setting up a design system. |
