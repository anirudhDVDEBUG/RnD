# Agent Slash Commands with Behavioral Eval Gates

**TL;DR:** Define reusable agent slash commands as markdown, attach YAML rubrics that score output quality, and wire a CI gate that blocks merges when agent behaviour regresses. Zero API keys needed to run the demo.

## Headline Result

```
PASS  /review   (score: 92%  threshold: 80%)
PASS  /test-plan (score: 90%  threshold: 80%)
PASS  /refactor (score: 88%  threshold: 80%)
OVERALL: PASS — Safe to merge.
```

Three commands evaluated against 15 criteria in < 2 seconds, with a coloured terminal report and machine-readable JSON for CI.

## Quick Links

| Doc | What it covers |
|-----|----------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, configure, trigger phrases, first-60-seconds walkthrough |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, production relevance |

## Run It

```bash
bash run.sh
```

Source: [emaraschio/cursor-commands](https://github.com/emaraschio/cursor-commands)
