# BioSymphony Fermentation DoE

**Agentic AI harness for Design-of-Experiments planning in fermentation, bioprocess, and biomanufacturing.** Generates statistically rigorous DoE matrices (CCD, Box-Behnken, full factorial) with built-in biosafety gating and automatic scale-up/scale-down bridging between bioreactor volumes.

## Headline result

```
CCD design:        47 total runs, 43 after biosafety gating
Scale-up bridging:  bench (2L) -> pilot (200L), constant kLa
Safety flags:       4 blocked (axial points outside safe operating limits)
```

A 5-factor fed-batch CHO optimization DoE — planned, safety-checked, and bridged to pilot scale — in under 1 second, zero API keys.

## Quick links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure the Claude skill, first 60-second walkthrough
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, relevance to Claude-driven products
- **[Source repo](https://github.com/BioSymphony/biosymphony-ferm-doe)** — Full BioSymphony implementation
