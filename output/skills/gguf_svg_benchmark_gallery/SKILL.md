---
name: gguf_svg_benchmark_gallery
description: |
  Benchmark quantized GGUF model variants by generating SVG images from the same prompt across all available quantizations, then compile results into an HTML gallery for visual comparison.
  TRIGGER: user wants to compare GGUF quantizations, benchmark SVG generation across model sizes, test visual output quality of quantized models, or create a pelican-style gallery of LLM outputs.
---

# GGUF SVG Benchmark Gallery

Run a single SVG-generation prompt against multiple GGUF quantized variants of the same model and produce a static HTML gallery comparing the results.

## When to use

- "Compare SVG output across all GGUF quantizations of a model"
- "Benchmark different quantized model sizes for image generation"
- "Generate an SVG gallery from multiple GGUF files"
- "Test how quantization affects creative output quality"
- "Run the pelican SVG benchmark against a local model"

## How to use

### Prerequisites

- `llm` CLI installed (`pip install llm`)
- `llm-llama-cpp` or `llm-gguf` plugin installed for local GGUF inference
- One or more GGUF model files downloaded (e.g. from Unsloth on HuggingFace)

### Steps

1. **Download GGUF variants** from HuggingFace (e.g. `unsloth/granite-4.1-3b-GGUF`):
   ```bash
   huggingface-cli download unsloth/granite-4.1-3b-GGUF --local-dir ./models
   ```

2. **Run the SVG prompt against each variant**:
   ```bash
   PROMPT="Generate an SVG of a pelican riding a bicycle"
   mkdir -p output
   for model_file in models/*.gguf; do
     name=$(basename "$model_file" .gguf)
     llm -m "gguf:$model_file" "$PROMPT" > "output/${name}.svg"
   done
   ```

3. **Generate the HTML gallery**:
   ```bash
   echo '<!DOCTYPE html><html><head><title>GGUF SVG Benchmark</title><style>
   .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem;padding:1rem}
   .card{border:1px solid #ccc;padding:1rem;border-radius:8px}
   .card h3{font-size:0.9rem;word-break:break-all}
   .card img{width:100%;height:auto}
   </style></head><body><h1>GGUF SVG Benchmark Gallery</h1><div class="grid">' > gallery.html

   for svg in output/*.svg; do
     name=$(basename "$svg" .svg)
     size=$(stat -f%z "$svg" 2>/dev/null || stat -c%s "$svg")
     echo "<div class=\"card\"><h3>${name} (${size}B)</h3><img src=\"${svg}\"></div>" >> gallery.html
   done

   echo '</div></body></html>' >> gallery.html
   ```

4. **Review the gallery** by opening `gallery.html` in a browser. Compare visual quality across quantization levels (Q2_K, Q4_K_M, Q8_0, F16, etc.).

### Tips

- Sort results by model file size to see if there's a correlation between quantization level and output quality
- The original experiment showed no clear pattern between size and quality for SVG generation on small (3B) models
- Try with larger base models (8B, 30B) for potentially more distinguishable differences
- Use a consistent system prompt and temperature (0) for reproducible comparisons

## References

- Source: [Granite 4.1 3B SVG Pelican Gallery](https://simonwillison.net/2026/May/4/granite-41-3b-svg-pelican-gallery/#atom-everything) by Simon Willison
- [Example gallery output](https://simonw.github.io/granite-4.1-3b-gguf-pelicans/)
- [Unsloth GGUF collection](https://huggingface.co/unsloth/granite-4.1-3b-GGUF)
- [IBM Granite 4.1 announcement](https://research.ibm.com/blog/granite-4-1-ai-foundation-models)
