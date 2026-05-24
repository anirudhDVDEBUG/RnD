# FigMirror: Paper Figure Style Replication

**Replicate the visual style of any scientific paper figure onto your own data.** Give it a reference figure from a published paper and your CSV — it extracts colors, fonts, markers, grids, and layout, then generates publication-ready matplotlib plots that match the original style.

## Headline Result

```
reference_figure.png  →  style extracted  →  output_figure.png (your data, their style)
```

Run `bash run.sh` to see a side-by-side demo: a "Nature-style" reference figure is generated, its style is extracted into JSON, and then your own training data is plotted in the same visual style — both PNG (300 DPI) and PDF (vector).

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure as a Claude skill, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, limitations, integration ideas
- **Source**: [VILA-Lab/FigMirror](https://github.com/VILA-Lab/FigMirror)
