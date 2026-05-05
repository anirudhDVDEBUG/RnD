# GGUF SVG Benchmark Gallery

**TL;DR:** Run the same SVG-generation prompt against every GGUF quantization of a model, then view results side-by-side in an auto-generated HTML gallery. Instantly see whether Q2_K produces worse pelicans than Q8_0.

## Headline Result

On Granite 4.1 3B, **quantization level has no consistent correlation with SVG output quality** — a Q2_K variant can produce better art than F16. This challenges the assumption that bigger = better for creative tasks on small models.

## Quick Start

```bash
bash run.sh        # generates mock SVGs + opens gallery.html
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) — install, configure, run with real models
- [TECH_DETAILS.md](TECH_DETAILS.md) — architecture, limitations, relevance
