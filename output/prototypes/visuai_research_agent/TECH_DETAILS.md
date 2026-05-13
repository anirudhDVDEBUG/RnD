# Technical Details — VisuAI Research Agent

## What It Does

VisuAI Research Agent is a deterministic, five-stage pipeline that takes a tabular dataset (CSV/Excel/JSON) and produces a set of publication-ready visualizations without any manual configuration. It profiles the data to understand column types and distributions, classifies the research domain via keyword matching on column names, selects appropriate chart types based on variable relationships, and renders both static PNGs (300 DPI) and interactive HTML files using Plotly.

The "autonomous agent" framing means there are no manual chart-selection or styling steps — the pipeline makes every decision from data to finished figure. The original upstream repo envisions an LLM-powered agent loop; this prototype implements the same pipeline deterministically so it runs without API keys.

## Architecture

```
dataset.csv
    |
    v
[1] ingest()        -- pandas read_csv / read_excel / read_json
    |
    v
[2] profile()       -- column type detection, descriptive stats, missing values
    |
    v
[3] detect_domain() -- keyword scoring against 5 domain vocabularies
    |                   (biomedical, social_science, engineering,
    |                    environmental, economics)
    v
[4] recommend_visualizations()
    |               -- rule-based selection: histograms for numeric distributions,
    |                  scatter for pairwise correlations, box for cat×num,
    |                  heatmap for ≥3 numeric, bar for categorical counts
    v
[5] render_all()    -- Plotly Express + Graph Objects
    |                  domain-specific color palettes, publication font/margin
    |
    v
output/
  ├── fig_01_histogram.png   (900×550 @2x)
  ├── fig_01_histogram.html  (interactive, CDN plotly.js)
  ├── ...
  └── report.json            (profile + recommendations + file manifest)
```

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Full pipeline — all 5 stages + CLI entry point |
| `generate_sample_data.py` | Creates a 200-row mock clinical-trial CSV |
| `run.sh` | One-shot demo: venv, install, generate data, run |
| `requirements.txt` | 4 dependencies (pandas, numpy, plotly, kaleido) |

### Dependencies

- **pandas** — data loading, profiling, type detection
- **numpy** — sample data generation, numeric operations
- **plotly** — interactive charts (Express for convenience, Graph Objects for heatmaps)
- **kaleido** — server-side PNG/SVG export from Plotly figures

No LLM API keys required. No network calls at runtime.

## Limitations

- **Domain detection is keyword-based**, not semantic. Columns named unconventionally may default to "general".
- **Chart selection is rule-based** — it covers the most common chart types (histogram, scatter, box, heatmap, bar) but does not generate specialized plots (violin, network graph, Sankey, geographic maps).
- **No LLM reasoning** — the upstream repo positions itself as an AI agent with LLM-driven decisions. This prototype replaces that with deterministic heuristics, which is more reliable but less flexible for edge cases.
- **Single-file pipeline** — no streaming, no incremental updates. Designed for datasets that fit in memory (up to ~1M rows on a typical machine).
- **No time-series handling** — datetime columns are profiled but not visualized with line charts.

## Why It Matters for Claude-Driven Products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Demonstrates a structured multi-stage agent pipeline pattern (ingest → reason → act → export) that can be templated for other data-processing agents |
| **Lead-gen / marketing** | Auto-generating charts from campaign performance CSVs (impressions, clicks, conversions) with zero manual config |
| **Ad creatives** | Quick data-backed infographic generation from A/B test results |
| **Voice AI** | Pair with a voice interface: "Show me the biomarker distribution" triggers the pipeline and serves the HTML chart |
| **Research tooling** | Embeddable in Claude Skills for researchers who need fast, styled visualizations during analysis sessions |

The core pattern — profile data, detect context, select action, render output — is reusable across any domain where Claude needs to turn raw data into a presentable artifact.
