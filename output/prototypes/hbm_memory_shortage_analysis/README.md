# HBM Memory Shortage & Consumer Electronics Repricing Analysis

**TL;DR:** AI's insatiable demand for HBM (High Bandwidth Memory) is cannibalizing wafer capacity for DDR and LPDDR, driving up memory costs for consumer electronics. By end of 2026, HBM will consume ~20% of wafer capacity (up from ~2% in 2022), and because each GB of HBM uses 3x+ the silicon of DDR/LPDDR, the effective supply squeeze hits budget smartphones in Africa and South Asia hardest.

## Headline Result

```
WAFER SUPPLY TRAJECTORY
  Scenario                   HBM%  Consumer%   Supply  Eff.Supply   Price+
  Pre-AI Boom (2022)          2.0%      98.0%   100.0       100.0     0.0%
  Projected (End 2026)       20.0%      80.0%    81.6        24.0    76.0% <--

Sub-$100 Smartphone: memory cost rises $8.00 → $14.08 (+$6.08)
  Retail price increase: ~$8.51 — potentially pricing out millions of first-time buyers
```

## Quick Start

```bash
bash run.sh
```

No API keys or external dependencies required (Python 3.8+ stdlib only).

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) — Installation, skill setup, trigger phrases
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data model, limitations

## Source

- [The memory shortage is causing a repricing of consumer electronics](https://simonwillison.net/2026/May/22/memory-shortage/#atom-everything) (Simon Willison)
- [AI is killing the cheap smartphone](https://davidoks.blog/p/ai-is-killing-the-cheap-smartphone) (David Oks)
