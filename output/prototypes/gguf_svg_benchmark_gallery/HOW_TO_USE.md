# How to Use

## Install (real inference mode)

```bash
pip install llm llm-gguf
# or for llama.cpp backend:
pip install llm llm-llama-cpp
```

Download GGUF variants:
```bash
pip install huggingface-hub
huggingface-cli download unsloth/granite-4.1-3b-GGUF --local-dir ./models
```

## As a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/gguf_svg_benchmark_gallery
cp SKILL.md ~/.claude/skills/gguf_svg_benchmark_gallery/SKILL.md
```

**Trigger phrases:**
- "Compare SVG output across all GGUF quantizations of a model"
- "Benchmark different quantized model sizes for image generation"
- "Generate an SVG gallery from multiple GGUF files"
- "Run the pelican SVG benchmark against a local model"

## CLI Usage (without Claude)

```bash
# Run against real models
python benchmark.py --models-dir ./models --prompt "Generate an SVG of a pelican riding a bicycle"

# Or use the shell script with mock data (no GPU needed)
bash run.sh
```

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output:**
```
[*] Generating mock SVGs for 8 quantization levels...
[*] Created output/granite-4.1-3b-Q2_K.svg (1247 bytes)
[*] Created output/granite-4.1-3b-Q4_K_M.svg (1389 bytes)
[*] Created output/granite-4.1-3b-Q5_K_M.svg (1156 bytes)
[*] Created output/granite-4.1-3b-Q6_K.svg (1423 bytes)
[*] Created output/granite-4.1-3b-Q8_0.svg (1312 bytes)
[*] Created output/granite-4.1-3b-IQ4_NL.svg (1098 bytes)
[*] Created output/granite-4.1-3b-F16.svg (1567 bytes)
[*] Created output/granite-4.1-3b-BF16.svg (1501 bytes)
[*] Gallery written to gallery.html
[*] Open gallery.html in a browser to compare results.
```

Open `gallery.html` — you see a responsive grid of SVG cards, each labeled with the quantization name and file size.

## Real Inference Mode

```bash
python benchmark.py --models-dir ./models \
  --prompt "Generate an SVG of a pelican riding a bicycle" \
  --output-dir ./output
python gallery_builder.py --input-dir ./output --output gallery.html
```

Requires a machine with enough RAM to load each GGUF file sequentially (3B models need ~2-6 GB depending on quantization).
