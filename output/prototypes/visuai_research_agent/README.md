# VisuAI Research Agent

**TL;DR** — Feed it a CSV of research data; get back publication-ready interactive charts (HTML + PNG) with domain-appropriate palettes, axis labels, and legends. Zero configuration needed.

## Headline Result

```
$ bash run.sh
[1/5] Ingesting dataset ...     200 rows x 8 columns
[2/5] Profiling data ...        4 numeric, 3 categorical, 0 missing
[3/5] Detecting domain ...      biomedical
[4/5] Recommending ...          8 visualizations
[5/5] Rendering to output/ ...  16 files (PNG + interactive HTML)
```

Outputs include scatter plots, histograms, box plots, correlation heatmaps, and bar charts — all styled for the detected research domain.

## Quick Links

| Doc | What it covers |
|-----|----------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, run, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations |
