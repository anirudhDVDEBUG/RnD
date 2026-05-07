# vLLM V0 to V1: RL Migration Validator

**TL;DR:** vLLM V1 silently breaks reinforcement learning pipelines because it returns raw logprobs (pre-temperature/penalties) by default, enables prefix caching (stale after weight updates), and uses async scheduling. This tool validates your V1 config and shows exactly which settings cause policy ratio divergence, clip rate spikes, and KL blowup.

**Headline result:** A naive V1 migration causes clip rate to jump from 0.02 to 0.20 and policy ratio to diverge to 1.12 -- all fixable with 3 config flags.

```
  Metric                 Naive V1       Correct V1     Status
  ---------------------- -------------- -------------- ----------
  Clip rate              0.2037         0.0237         FIXED
  Policy ratio mean      1.1237         1.0037         FIXED
  KL divergence          0.1937         0.0087         FIXED
```

## Quick Start

```bash
bash run.sh
```

No API keys or GPU required. See [HOW_TO_USE.md](HOW_TO_USE.md) for installation and skill setup, [TECH_DETAILS.md](TECH_DETAILS.md) for the full technical breakdown.

## Source

Based on: [vLLM V0 to V1: Correctness Before Corrections in RL](https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections) (ServiceNow AI, HuggingFace Blog)
