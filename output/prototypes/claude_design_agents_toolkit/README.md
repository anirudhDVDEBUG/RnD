# Claude Design Agents Toolkit

**TL;DR:** Four specialized Python agents that generate production-ready UI layouts (HTML + Tailwind), color palettes with design tokens, component specs, and full design-to-code pages — all without API keys.

## Headline result

```
$ bash run.sh

  Generated 6 files:
    dashboard.html        — sidebar + header + stats grid (responsive Tailwind)
    landing.html          — hero + features + CTA landing page
    form.html             — signup form with validation styling
    design-tokens.css     — CSS custom properties (50+ variables)
    tailwind.extend.json  — drop-in Tailwind theme config
    component-specs.json  — 5 component specs with props & classes
```

Open any `.html` file in a browser — it works immediately via Tailwind CDN.

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure as a Claude skill, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, business relevance
