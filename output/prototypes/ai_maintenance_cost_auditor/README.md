# AI Maintenance Cost Auditor

**TL;DR:** Static analysis tool that applies James Shore's inverse-rate principle to AI-generated code — if your AI writes code 3x faster, maintenance costs must drop to 1/3 or you're accumulating debt faster than you're shipping. Zero dependencies, runs on any Python 3.10+ codebase.

## Headline Result

```
  OVERALL VERDICT
  Average maintenance multiplier:  1.7x
  Speed multiplier:               3.0x
  Product (speed x maintenance):  5.1x

  Shore's Rule: speed x maintenance must be <= 1.0
  Result: UNSUSTAINABLE
```

The auditor caught 15 maintenance red flags in a typical AI-generated file — commented-out code, bare excepts, deep nesting, duplicated report formatters, unused imports — and quantified that the 3x speed gain was illusory: you'd spend 5x more maintaining it.

## Quick Start

```bash
bash run.sh            # runs demo on included samples
python3 auditor.py .   # audit your own code
```

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, Claude skill setup, CLI usage
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, scoring model, limitations

## Origin

Based on [James Shore's inverse-rate principle](https://www.jamesshore.com/v2/blog/2026/you-need-ai-that-reduces-your-maintenance-costs), via [Simon Willison](https://simonwillison.net/2026/May/11/james-shore/#atom-everything).
