# How to Use: PaddleOCR 3.5 with Transformers Backend

## Install

### 1. Install PyTorch (match your hardware)

```bash
# CUDA 12.6
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# CPU only
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 2. Install PaddleOCR + Transformers

```bash
pip install "paddleocr==3.5.0" "paddlex==3.5.2" "transformers>=5.4.0"
```

That's it. No PaddlePaddle framework install needed.

## Claude Skill setup

This prototype includes a SKILL.md. To install it as a Claude Code skill:

```bash
mkdir -p ~/.claude/skills/paddleocr-transformers
cp SKILL.md ~/.claude/skills/paddleocr-transformers/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Set up PaddleOCR with a Transformers backend"
- "Run OCR on an image using PaddleOCR 3.5"
- "Parse a document with PaddleOCR-VL"
- "Use PP-OCRv5 for text detection"
- "Extract text from images for RAG"

## First 60 seconds

### Mock mode (no GPU / no install)

```bash
bash run.sh
```

Output:

```
  Task 1: Text Detection + Recognition (PP-OCRv5)
  Input : sample registration document image
  Model : PP-OCRv5 (text det + rec)

  Text                                Confidence
  REGISTRATION No.                         0.987
  MH-04-AS-1234                            0.994
  Owner Name:                              0.991
  John Smith                               0.985
  ...

  Task 2: Document Parsing (PaddleOCR-VL 1.5)
  [TITLE] INVOICE #INV-2024-0042
  [TABLE] Detected table with 9 cells:
    | Item         | Qty          | Price        |
    | Widget A     | 10           | $25.00       |
    | Widget B     | 5            | $42.50       |
  [PARAGRAPH] Total: $462.50
```

Results are also saved to `output_results.json`.

### Live mode (requires GPU + model download)

```bash
OCR_MODE=live bash run.sh
```

Models (~1-2 GB) auto-download from Hugging Face Hub on first run.

### Python API (live)

```python
from paddleocr import PaddleOCR

pipeline = PaddleOCR(
    device="gpu:0",
    engine="transformers",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

results = pipeline.predict("path/to/image.png")
for result in results:
    print(result)
```

### CLI (live)

```bash
paddleocr ocr \
  -i path/to/image.png \
  --device gpu:0 \
  --engine transformers
```

## Engine configuration

Control dtype, attention implementation, and device via `engine_config`:

```python
pipeline = PaddleOCR(
    device="gpu:0",
    engine="transformers",
    engine_config={
        "dtype": "bfloat16",            # float32, bfloat16, float16
        "attn_implementation": "sdpa",   # sdpa, eager, flash_attention_2
    },
)
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: paddleocr` | `pip install paddleocr==3.5.0` |
| `No module named 'torch'` | Install PyTorch for your hardware first |
| CUDA out of memory | Use `"dtype": "bfloat16"` or `"float16"` in engine_config |
| Slow first run | Models download from HF Hub on first use (~1-2 GB) |
