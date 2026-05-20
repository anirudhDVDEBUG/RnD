# AnyDesign Analyzer

**Point Claude at any screenshot, live website, or Figma file and get back a structured `design.md` with a complete token system, component inventory, and reconstruction notes — ready for implementation.**

## Headline Result

```
Input:  a SaaS dashboard screenshot
Output: design.md with 12 colors, 10 spacing tokens, 10 components, DTCG JSON, and layout notes
Time:   < 3 seconds
```

## What It Does

AnyDesign Analyzer is a Claude Code skill that reverse-engineers any visual design into a structured design system document. It extracts color palettes, typography scales, spacing systems, shadows, border radii, and component inventories — all formatted in the DTCG (Design Token Community Group) standard.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, skill setup, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, relevance
- **[Source repo](https://github.com/uxKero/anydesign)**

## Quick Demo

```bash
bash run.sh
# Produces design.md with mock SaaS dashboard data (no deps required)
```
