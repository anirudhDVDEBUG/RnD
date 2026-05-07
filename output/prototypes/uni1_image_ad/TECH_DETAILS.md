# Technical Details

## What It Does

uni1-image-ad is a Claude Code skill workbench that wraps Luma Labs' uni-1 image generation API specifically for Meta ad creative production. It provides two main workflows: (1) reverse-engineering an existing ad image into a structured prompt template (extracting composition, color palette, typography cues, and CTA placement), and (2) generating new ad creatives by combining those templates with brand parameters and sending optimized prompts to the uni-1 model.

The skill handles the full lifecycle: prompt construction from brand YAML configs, API calls with polling for async generation, downloading results, and organizing outputs with reproducibility logs.

## Architecture

```
generate_ad.py          — Main entry: reads brand config, builds prompt, calls Luma API, saves output
reverse_engineer.py     — Analyzes reference ad, extracts visual DNA into template.yaml
brand_config.py         — Parses brand YAML (colors, tone, CTA, platform)
luma_client.py          — Thin wrapper around Luma Dream Machine /generations/image endpoint
templates/              — Pre-built prompt templates for common ad formats
output/                 — Generated images + prompt_log.json + template.yaml
```

### Data Flow

1. User provides brand params (CLI flags or YAML) + optional reference image
2. `reverse_engineer.py` (if reference provided) uses vision analysis to extract a template
3. `generate_ad.py` merges template + brand config into a detailed uni-1 prompt
4. `luma_client.py` POSTs to `https://api.lumalabs.ai/dream-machine/v1/generations/image`
5. Polls generation status until complete (~10-30s)
6. Downloads final image, saves to `output/` with metadata log

### Dependencies

- `requests` — HTTP client for Luma API
- `pyyaml` — Brand config and template parsing
- `Pillow` — Image validation and format conversion
- Python 3.9+

### Model Details

- **Model**: Luma uni-1 (via Dream Machine API)
- **Supported aspect ratios**: 1:1, 9:16, 16:9, 1.91:1, 4:5
- **Output resolution**: Up to 1024px on longest side
- **Generation time**: 10-30 seconds typical

## Limitations

- No text rendering in generated images (uni-1 cannot reliably produce readable text; add text overlays in post-production)
- Reverse-engineering requires Claude vision or similar multimodal model to analyze reference — the script itself does structured prompt extraction, not pixel-level copying
- No built-in brand guideline enforcement beyond color palette hints in the prompt
- Rate-limited by Luma API (check your plan's limits)
- Generated images are not guaranteed to match exact brand colors since uni-1 interprets color descriptions loosely

## Why This Matters for Claude-Driven Products

- **Ad Creatives at Scale**: Marketing teams can generate dozens of A/B test variants without a designer in the loop — ideal for lead-gen and performance marketing pipelines
- **Template Marketplace**: The reverse-engineer workflow creates reusable templates that could power an agent-driven creative marketplace
- **Skill Composability**: Pairs naturally with copywriting skills (generate headline + image together) for full ad production agents
- **Cost Efficiency**: At ~$0.03-0.10 per generation, dramatically cheaper than stock photo licensing or freelance design for iteration
