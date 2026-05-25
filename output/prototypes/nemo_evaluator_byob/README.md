# NeMo Evaluator BYOB — Bring Your Own Benchmark

**Build custom LLM evaluation benchmarks in minutes.** Generate evaluation datasets, judge prompts, and NeMo Evaluator configs — then run scored evaluations with an LLM-as-judge pipeline. No API keys required for the demo.

## Headline Result

```
  Metric           Mean   Median  Std Dev    Min    Max
  accuracy         3.50      3.5     0.93      2      5
  completeness     4.00      4.0     0.76      3      5
  clarity          3.38      3.0     0.74      3      5

  Overall score (mean of all metrics): 3.62 / 5.00
```

8 tech-knowledge questions scored across 3 criteria by a mock LLM judge — dataset, config, and results generated end-to-end.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **Source:** [NVIDIA/skills — NeMo-Evaluator/byob](https://github.com/NVIDIA/skills/tree/main/skills/NeMo-Evaluator/byob)
