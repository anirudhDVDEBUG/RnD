# Prompt Cache Skills

**Drop-in prompt-caching analyzer and optimizer for LLM agent harnesses.** Scans your agent's prompt structure (Claude Code, Aider, Cline, or custom), finds cache-busting patterns, and applies fixes — cutting input token costs by 50-80%.

## Headline Result

```
Before: $3.00/MTok input  →  After: $0.30/MTok on cache hits (90% savings)
  Issues found: dynamic timestamps in system prompt, mis-ordered messages, missing breakpoints
  Fixes applied: 3 patches, 0 manual steps
```

## Quick Start

```bash
bash run.sh
```

No API keys needed — runs against mock agent configs and shows full analysis.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, skill setup, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why this matters

## Source

[OnlyTerp/prompt-cache-skills](https://github.com/OnlyTerp/prompt-cache-skills)
