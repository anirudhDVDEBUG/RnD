# Technical Details

## What It Does

FigMirror takes a reference figure from a scientific paper and replicates its visual style onto new data. The upstream tool (VILA-Lab/FigMirror) uses a vision-language model to analyze a reference image, extract a structured style specification (colors, fonts, layout, markers, grid settings), and then generate matplotlib code that applies that style to arbitrary user data. The result is a publication-ready figure that visually matches the original paper's aesthetic while plotting entirely different data.

This demo implements the style-application pipeline locally: given an already-extracted style spec (JSON), it configures matplotlib rcParams and renders user data with matching colors, markers, line styles, typography, and layout — producing both raster (PNG, 300 DPI) and vector (PDF) outputs.

## Architecture

```
reference_figure.png
        │
        ▼
  [Style Analysis]        ← Claude vision / VLM extracts style attributes
        │
        ▼
  reference_style.json    ← Structured spec: colors, fonts, layout, markers
        │
        ▼
  figmirror_demo.py       ← Applies style to user data via matplotlib
        │
        ├── output_figure.png  (300 DPI raster)
        └── output_figure.pdf  (vector for publication)
```

### Key Files

| File | Purpose |
|------|---------|
| `figmirror_demo.py` | Core engine: loads style JSON + CSV data, renders styled figure |
| `generate_reference.py` | Creates a synthetic "paper figure" for demo purposes |
| `reference_style.json` | Style specification (colors, typography, layout, axes, legend) |
| `sample_data.csv` | Example training metrics data |
| `SKILL.md` | Claude Code skill definition with trigger phrases |

### Dependencies

- `matplotlib` — rendering engine
- `numpy`, `pandas` — data handling
- `seaborn` — optional, for additional plot types
- `Pillow` — optional, for image-based style extraction

No GPU, no external API keys, no network access needed for the demo.

### Model Calls

The upstream FigMirror tool calls a vision-language model (e.g., Claude, GPT-4V) to analyze the reference figure image. This demo skips that step by using a pre-extracted style JSON, so it runs fully offline.

In a real Claude skill workflow, the style analysis happens in-context: Claude examines the reference image, extracts style attributes, and writes the matplotlib code — all within a single conversation turn.

## Limitations

- **Style extraction fidelity**: Automated color extraction from screenshots can be imprecise — hex values may need manual tuning for exact matches.
- **Chart type coverage**: Works best for line plots, scatter plots, and bar charts. Heatmaps, violin plots, and 3D figures require more manual adjustment.
- **Font matching**: System font availability varies. If the paper uses a proprietary font (e.g., Minion Pro), the skill falls back to the closest available serif/sans-serif family.
- **Complex layouts**: Multi-panel figures with insets, broken axes, or overlaid annotations need manual post-processing.
- **No automatic data mapping**: The user must specify which data columns map to which visual elements — the tool only replicates style, not semantics.

## Why It Matters for Claude-Driven Products

| Use Case | Application |
|----------|-------------|
| **Marketing / Ad Creatives** | Replicate the "look" of competitor visuals or brand-compliant chart styles at scale |
| **Agent Factories** | Embed as a skill in autonomous report-generation agents that maintain consistent visual identity across documents |
| **Lead-Gen Reports** | Auto-generate branded charts for prospect-facing materials that match a company's established figure style |
| **Research Automation** | Batch-produce publication-ready figures that conform to a journal's style guidelines |
| **Voice AI Dashboards** | Generate styled analytics figures on-demand from voice-triggered data queries |

The skill is composable: it pairs naturally with data-fetching MCP servers (SQL, APIs) and document-assembly skills to create end-to-end report pipelines where every chart looks like it came from the same publication.
