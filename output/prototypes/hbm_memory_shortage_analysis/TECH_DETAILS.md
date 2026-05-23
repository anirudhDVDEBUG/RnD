# Technical Details

## What it does

This tool models the semiconductor memory wafer capacity tradeoff caused by surging HBM (High Bandwidth Memory) demand from AI/GPU workloads. It quantifies how reallocating wafer starts from DDR/LPDDR to HBM — at a 3.2x wafer-intensity penalty per GB — reduces effective consumer memory supply and drives up prices for smartphones, laptops, and tablets. The analysis includes per-manufacturer allocation breakdowns, a multi-year supply trajectory, per-segment consumer impact estimates, and equity implications for emerging markets.

The core insight comes from David Oks's analysis (via Simon Willison): the memory industry is a 3-company oligopoly with hard-learned supply discipline. When HBM demand surges, capacity doesn't expand — it gets reallocated from consumer memory, and the 3x+ wafer intensity of HBM amplifies the squeeze.

## Architecture

### Key files

| File | Purpose |
|------|---------|
| `hbm_analysis.py` | Core analysis engine — data models, computation, display |
| `SKILL.md` | Claude Code skill definition with trigger phrases and structured knowledge |
| `run.sh` | Wrapper script for end-to-end demo |

### Data flow

```
Embedded reference data (manufacturers, scenarios, segments)
  → compute_effective_supply_index() — models wafer reallocation
  → estimate_segment_impact() — traces price effects to consumer devices
  → display_results() or JSON output
```

### Data models

- **MemoryManufacturer**: Samsung/SK Hynix/Micron capacity and allocation splits
- **WaferScenario**: Time-series snapshots of HBM/DDR/LPDDR wafer share (2022-2027)
- **ConsumerImpact**: Per-segment memory cost, BOM fraction, and affected regions

### Dependencies

- Python 3.8+ standard library only (`json`, `sys`, `dataclasses`)
- No external packages, no API keys, no network calls

## Limitations

- **Static data**: Uses embedded reference figures, not live market data. Numbers are illustrative estimates based on public reporting, not proprietary fab data.
- **Linear supply model**: The effective supply index uses a simplified linear model. Real wafer economics involve yield curves, technology node transitions, and contract commitments.
- **No demand elasticity**: Does not model demand-side responses (consumers switching to refurbished devices, OEMs reducing memory per device, etc.).
- **Three-manufacturer assumption**: Treats Samsung, SK Hynix, and Micron as the complete market. Niche/emerging players (e.g., CXMT in China) are excluded.
- **No temporal dynamics**: Price increases are modeled as instantaneous; real pricing flows through 6-12 month contract cycles.

## Why it matters for Claude-driven products

- **Lead-gen / market intelligence**: The analysis framework can be extended with live data feeds to generate automated market briefs on memory pricing for hardware procurement teams.
- **Marketing / content**: The equity angle (AI demand pricing out emerging-market smartphone buyers) is a compelling narrative for tech policy content.
- **Agent factories**: The structured data output (`--json`) is designed for downstream agent consumption — feed it into a research agent that monitors semiconductor supply chain shifts.
- **Ad creatives**: Understanding component cost drivers helps creative agents frame value propositions for budget electronics brands.
- **Voice AI**: The skill's trigger phrases and structured knowledge base make it a natural fit for voice-driven market briefings.
