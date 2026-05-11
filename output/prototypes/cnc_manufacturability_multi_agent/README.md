# CNC Manufacturability Multi-Agent System

**TL;DR:** A 5-stage pipeline that takes a CAD part's geometry, material, and tolerances, then automatically determines whether your CNC machine shop can manufacture it — replacing 30-60 minute manual feasibility reviews with a ~1 second automated assessment. Outputs a structured GO / NO-GO / CONDITIONAL verdict with tool availability, procurement costs, risk flags, and a full report.

## Headline Result

```
VERDICT: [COND] CONDITIONAL
Confidence: HIGH
1 tool(s) missing (est. $15 to procure). Match rate: 86%.
Est. setup time: 2.6 hours | 7 operations | Pipeline: 0.003s
```

## Quick Start

```bash
bash run.sh
```

No API keys, no GPU, no external services required. Runs three demo scenarios (Steel bracket, Aluminum plate, Titanium bracket) with different materials and tolerances.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install, skill setup, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, data flow, limitations, relevance

## Source

Based on [MachinaCheck](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/machinacheck) from the lablab.ai x AMD Developer Hackathon.
