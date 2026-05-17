# Technical Details

## What This Does

This is a Claude Code skill that encodes CSS architecture knowledge — specifically the pattern of structuring stylesheets using cascade layers (`@layer`), CSS custom properties as design tokens, and semantic component classes. It activates when a user asks about CSS organization or Tailwind migration, and guides Claude to produce structured, maintainable CSS instead of suggesting utility frameworks.

The included `css_architect.py` is a proof-of-concept converter that demonstrates the architecture by parsing HTML with Tailwind utility classes and outputting structured CSS with proper layering.

## Architecture

```
SKILL.md              — Skill definition (trigger rules + knowledge)
css_architect.py      — Demo converter (Tailwind HTML → structured CSS)
```

### Data Flow (skill activation)

1. User asks Claude Code about CSS organization
2. Skill triggers based on intent matching (keywords: organize, structure, Tailwind migration)
3. Claude applies the encoded architecture pattern:
   - Identifies repeated utility patterns in user's code
   - Extracts design tokens (colors, spacing, typography)
   - Creates layer structure with proper specificity ordering
   - Converts utility clusters to named component classes

### Data Flow (demo converter)

1. Parses HTML for `class="..."` attributes
2. Separates semantic class names from Tailwind utilities
3. Maps Tailwind utilities → CSS properties using lookup table
4. Replaces hard-coded values with custom property references
5. Wraps output in `@layer` declarations

### Dependencies

- Python 3.8+ (standard library only — `re`, `sys`, `collections`)
- No external packages required

## Key CSS Concepts Applied

| Concept | Purpose |
|---------|---------|
| `@layer` | Controls specificity without `!important` wars |
| Custom properties | Single source of truth for design values |
| Native nesting | Component scoping without BEM verbosity |
| Layout primitives | Reusable patterns (stack, cluster, sidebar) |

## Limitations

- **Not a build tool** — This skill provides architectural guidance, not automated refactoring. The demo converter handles common utilities but doesn't cover responsive variants (`md:`, `lg:`), hover states, or arbitrary values (`w-[300px]`).
- **No runtime analysis** — Cannot detect which styles are actually used in production (no tree-shaking equivalent).
- **Opinionated** — Follows a specific architecture (Every Layout + cascade layers). Other valid approaches exist (CSS Modules, atomic CSS with meaningful names, etc.).
- **Doesn't generate reset/normalize** — Assumes you'll bring your own CSS reset.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | Skills like this let you encode domain expertise (CSS architecture) into reusable agent behaviors — same pattern works for any specialized knowledge |
| **Marketing / Ad creatives** | Teams building landing pages with Claude benefit from consistent CSS output that doesn't depend on Tailwind CDN or build steps |
| **Lead-gen tools** | Generated pages with structured CSS load faster (no utility framework overhead), improving Core Web Vitals |
| **Voice AI / conversational** | When voice agents generate web artifacts, structured CSS is more maintainable than utility soup |

## Source Context

- Julia Evans wrote about her experience [moving away from Tailwind](https://jvns.ca/blog/2026/05/15/moving-away-from-tailwind--and-learning-to-structure-my-css-/) after taking CSS seriously as a technology
- Simon Willison [highlighted the post](https://simonwillison.net/2026/May/16/julia-evans/#atom-everything), noting the broader trend of developers reconsidering utility-first approaches
- Modern CSS (2024-2026) has closed most of the gaps that made Tailwind attractive: native nesting, `:has()`, container queries, cascade layers
