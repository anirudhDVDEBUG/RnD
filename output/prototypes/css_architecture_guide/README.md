# CSS Architecture Guide

**A Claude Code skill that helps you migrate from Tailwind to structured, maintainable CSS using modern features like cascade layers, custom properties, and layout primitives.**

Inspired by [Julia Evans' post on moving away from Tailwind](https://simonwillison.net/2026/May/16/julia-evans/#atom-everything) — this skill teaches Claude to guide CSS architecture decisions instead of reaching for utility frameworks.

## Headline Result

```
INPUT:  <div class="flex flex-col gap-4 p-6 rounded-lg shadow-md bg-white">
OUTPUT: @layer components { .card { display: flex; flex-direction: column; ... } }
```

Converts Tailwind utility clusters into semantic component classes with design tokens — zero magic numbers, full cascade layer structure.

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install the skill, trigger phrases, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, limitations, why it matters
- [SKILL.md](SKILL.md) — The actual skill file to install
