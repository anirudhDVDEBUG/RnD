# Technical Details

## What It Does

This tool automates A/B testing of GGUF quantized model variants on a creative SVG generation task. It iterates over every `.gguf` file in a directory, sends an identical prompt to each via the `llm` CLI (using llm-gguf or llm-llama-cpp plugins), captures the SVG output, and compiles all results into a static HTML gallery with metadata (file size, quantization name, SVG byte count).

The key finding from the original experiment (Simon Willison, May 2026): on IBM's Granite 4.1 3B model, quantization level did not predictably correlate with SVG output quality. A heavily quantized Q2_K variant sometimes produced more visually appealing results than the full F16 weights.

## Architecture

```
models/*.gguf          # Input: downloaded GGUF variants
       |
  benchmark.py         # Loops over models, calls llm CLI per file
       |
  output/*.svg         # Raw SVG outputs, one per quantization
       |
  gallery_builder.py   # Reads SVGs, builds HTML gallery
       |
  gallery.html         # Output: static comparison page
```

**Key files:**
- `benchmark.py` — orchestrates inference across all GGUF files; shells out to `llm` CLI
- `gallery_builder.py` — pure Python, no dependencies; reads SVG directory and emits HTML
- `mock_svgs.py` — generates procedural SVG pelicans with controlled variation (for demo/testing)
- `run.sh` — end-to-end demo using mock data

**Dependencies:** Python 3.8+, no pip packages required for gallery generation. Real inference needs `llm` + `llm-gguf`.

## Data Flow

1. User provides a prompt and a directory of GGUF files
2. `benchmark.py` iterates files sorted by size, invokes `llm -m gguf:<path> "<prompt>"` for each
3. Raw stdout (expected to be SVG markup) is saved to `output/<model-name>.svg`
4. `gallery_builder.py` scans the output directory, extracts metadata, and renders an HTML grid
5. Gallery includes inline SVGs (not external references) so it's fully portable as a single file

## Limitations

- **No parallel inference** — models are loaded sequentially (single GPU/CPU constraint)
- **No validation** — if a model outputs malformed SVG or non-SVG text, it's included as-is
- **No scoring** — quality comparison is purely visual (human judgment); no automated metric
- **Prompt sensitivity** — results vary significantly with prompt wording; not a general benchmark
- **Memory bound** — large models (30B+) may OOM on consumer hardware even at low quantizations

## Relevance to Claude-Driven Products

- **Ad creatives / Marketing:** Demonstrates that cheap quantized models can produce acceptable visual assets. A Claude agent could select the smallest model that passes a quality threshold, reducing inference cost for bulk SVG generation (icons, illustrations, diagrams).
- **Agent factories:** Pattern for automated model evaluation — an orchestrator agent downloads candidates, benchmarks them, and picks the best cost/quality tradeoff without human intervention.
- **Lead-gen:** The gallery format itself is a template for "model comparison" content that attracts developer traffic (SEO-friendly static pages).
- **Voice AI / Multimodal:** The benchmark pattern generalizes — swap SVG prompts for TTS quality tests or vision description accuracy across quantizations.
