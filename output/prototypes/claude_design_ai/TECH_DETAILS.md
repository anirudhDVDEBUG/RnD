# Tech Details: Claude Design AI

## What it does

Claude Design AI is a Claude Code skill that turns Claude into a UI/UX architect. When activated by trigger phrases like "create a design system" or "screenshot to React", it instructs Claude to generate production-ready React components styled with Tailwind CSS. The skill provides Claude with structured knowledge about component patterns, design tokens, responsive breakpoints, dark mode implementation, accessibility attributes, and shadcn/ui conventions — so Claude produces consistent, high-quality front-end code rather than ad-hoc markup.

The skill handles the full spectrum from single-component generation ("make me a button with 5 variants") to complete design systems (theme provider, color tokens, typography scale, layout primitives, icon library, and assembled page templates).

## Architecture

### Key files

| File | Purpose |
|------|---------|
| `skill/SKILL.md` | The actual Claude Code skill definition — drop into `~/.claude/skills/` |
| `src/templates.js` | Component template functions: Button, Card, Input, Navbar, Hero, Icons, ThemeProvider, DarkModeToggle |
| `src/generator.js` | Orchestrator that calls templates, writes `.tsx` files to `output/` |
| `src/demo.js` | End-to-end demo: generates system, shows previews, prints file tree |

### Data flow

```
User prompt ("create a design system")
  → Claude Code matches skill trigger phrases
  → SKILL.md loaded as context
  → Claude generates React/Tailwind components following skill instructions
  → Components written to user's project directory
```

In the demo (`run.sh`), the flow is simulated locally:

```
demo.js → generator.js → templates.js → output/*.tsx files
```

### What gets generated

- **ThemeProvider**: React context + `useTheme` hook, persists to localStorage, toggles `dark` class on `<html>`
- **Components**: Button (5 variants x 3 sizes), Card (composable sub-components), Input (with validation states)
- **Layout**: Responsive Navbar with mobile hamburger menu, Hero section with gradient background
- **Icons**: 5 SVG icons as typed React components with configurable size/stroke
- **Config**: `tailwind.config.js` with custom color tokens, `design-tokens.json` for programmatic access
- **Barrel export**: `index.ts` for clean imports

### Dependencies

- **Runtime**: Node.js 16+ (zero npm dependencies — pure Node stdlib)
- **Generated code expects**: React 18+, Tailwind CSS 3.x, TypeScript 5+
- **Optional**: shadcn/ui (components are compatible but don't require it)

## Limitations

- **No actual screenshot analysis**: The skill gives Claude instructions for *how* to convert screenshots, but the quality of screenshot-to-code conversion depends entirely on Claude's vision capabilities. Complex UIs with custom illustrations or unusual layouts may not convert accurately.
- **No Figma API integration**: Despite the "Figma to React" trigger, there is no direct Figma API connection. Users describe Figma designs verbally or paste specs; Claude interprets them.
- **Tailwind-only styling**: All generated components use Tailwind CSS utility classes. If your project uses CSS Modules, styled-components, or vanilla CSS, you'll need to adapt the output.
- **No runtime component library**: This generates source code, not a packaged npm library. There's no versioning, changelog, or update mechanism.
- **Static templates in demo**: The demo uses fixed templates. In real Claude Code usage, Claude generates components dynamically based on your specific requirements.

## Why this matters

### For Claude-driven product builders

| Use case | Relevance |
|----------|-----------|
| **Lead-gen / landing pages** | Generate complete landing pages (Hero + CTA + features grid) in seconds. The skill produces exactly the kind of conversion-focused layouts that marketing teams need. |
| **Ad creatives** | Rapidly prototype ad landing page variants. Each generation includes dark/light mode, so you can A/B test both themes. |
| **Agent factories** | If you're building agents that create web products, this skill is a building block — agents can invoke it to generate front-end code as part of a larger pipeline. |
| **Marketing sites** | The design system approach (tokens + components + pages) means you get brand-consistent output across multiple generations. Change the tokens once, regenerate everything. |
| **SaaS dashboards** | The component set (cards, inputs, navbars) covers the core primitives for dashboard UIs. Add data tables and charts on top. |

### Key insight

The skill's value isn't the templates — it's the **structured prompt engineering** that makes Claude generate consistent, accessible, well-typed React code instead of sloppy one-off snippets. The SKILL.md acts as a persistent system prompt specialized for UI generation.
