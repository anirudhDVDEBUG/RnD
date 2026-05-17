---
name: css_architecture_guide
description: |
  Guide for structuring CSS without utility frameworks like Tailwind.
  TRIGGER when: user wants to organize CSS, move away from Tailwind, structure stylesheets, or learn CSS architecture patterns.
  DO NOT TRIGGER when: user is setting up Tailwind, using CSS-in-JS, or asking about JavaScript frameworks.
---

# CSS Architecture Guide

A skill for helping developers structure their CSS effectively without relying on utility-first frameworks, inspired by Julia Evans' approach to taking CSS seriously as a technology.

## When to use

- "Help me organize my CSS without Tailwind"
- "How should I structure my stylesheets for a project?"
- "I want to move away from Tailwind and use plain CSS"
- "What's the best way to architect CSS for maintainability?"
- "Help me refactor my utility classes into structured CSS"

## How to use

### Core Principles

1. **Respect CSS as a technology** — CSS solves genuinely hard layout and design problems. Many frustrations (like centering) have been addressed in modern CSS. Learn what CSS offers before reaching for abstractions.

2. **Use modern CSS features** — Leverage flexbox, grid, custom properties (variables), container queries, `:has()`, nesting, and cascade layers (`@layer`) to write clean, maintainable styles.

3. **Structure your stylesheets**:
   - **Base/Reset layer**: Normalize or reset browser defaults
   - **Design tokens**: Use CSS custom properties for colors, spacing, typography scales
   - **Layout primitives**: Reusable layout patterns (stack, cluster, sidebar, grid)
   - **Component styles**: Scoped styles for UI components
   - **Utility overrides**: Minimal one-off utilities only where needed

4. **Naming conventions**: Use a lightweight naming system (BEM-lite, data attributes, or native CSS nesting with clear selectors) to communicate intent.

5. **Cascade layers** (`@layer`): Order your specificity intentionally:
   ```css
   @layer reset, tokens, layout, components, utilities;
   ```

### Migration Steps (from Tailwind)

1. Audit existing utility usage — identify repeated patterns
2. Extract design tokens (colors, spacing, fonts) into custom properties
3. Create layout primitives that replace common flex/grid utility combos
4. Convert component-level utility clusters into named component classes
5. Keep only truly one-off utilities; delete the rest

### Example: Structured Component

```css
@layer components {
  .card {
    display: grid;
    gap: var(--space-m);
    padding: var(--space-l);
    border-radius: var(--radius-m);
    background: var(--surface-1);
    box-shadow: var(--shadow-sm);

    & .card-title {
      font-size: var(--text-lg);
      font-weight: 600;
    }

    & .card-body {
      line-height: var(--leading-relaxed);
    }
  }
}
```

## References

- [Julia Evans: Moving away from Tailwind, and learning to structure my CSS](https://jvns.ca/blog/2026/05/15/moving-away-from-tailwind--and-learning-to-structure-my-css-/)
- [Simon Willison's commentary](https://simonwillison.net/2026/May/16/julia-evans/#atom-everything)
- [Every Layout](https://every-layout.dev/) — Layout primitives approach
- [CSS Cascade Layers spec](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_layers)
