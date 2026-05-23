# FTC "Active Listening" Settlement Analyzer

**TL;DR:** The FTC fined Cox Media Group, MindSift, and 1010 Digital Works ~$1M for marketing an "Active Listening" AI ad-targeting service that claimed to use smart-device microphones -- but actually just used standard behavioral data. This skill and demo analyze the deception, the settlement, and the takeaways for anyone building or buying AI marketing tools.

## Headline Result

```
VERDICT: "Active Listening" was standard ad targeting with a deceptive label.
         No microphone data was ever collected or used.
         Total penalty: $998,454 across three firms.
```

## Quick Start

```bash
bash run.sh
```

No API keys required. Produces a full analysis report from bundled case data.

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) -- Install the Claude skill, trigger phrases, first-60-seconds walkthrough
- [TECH_DETAILS.md](TECH_DETAILS.md) -- What the skill does, architecture, limitations
