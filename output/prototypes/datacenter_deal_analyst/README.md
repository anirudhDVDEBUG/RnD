# Data Center Deal Analyst

**TL;DR:** A Claude Code skill that produces structured risk reports for data center infrastructure deals — covering environmental violations, regulatory exposure, political optics, and business trade-offs. Inspired by the xAI/Anthropic Colossus controversy.

## Headline Result

```
  SIDE-BY-SIDE COMPARISON
                                         Colossus        Wind River
  Environmental Risk                     CRITICAL               LOW
  Regulatory Risk                            HIGH               LOW
  Political Risk                             HIGH               LOW
  Overall Risk                           CRITICAL               LOW
  Recommendation              Seek alternatives           Proceed
```

The demo analyzes the real xAI Colossus deal (Memphis, TN) against a hypothetical clean-energy alternative, producing the comparison above in seconds.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations

## Run the Demo

```bash
bash run.sh
```

No API keys needed. Uses mock data from public reporting.

## Source

[Notes on the xAI/Anthropic data center deal — Simon Willison](https://simonwillison.net/2026/May/7/xai-anthropic/#atom-everything)
