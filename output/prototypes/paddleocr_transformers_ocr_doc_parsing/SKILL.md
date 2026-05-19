---
name: PaddleOCR 3.5 Transformers OCR & Document Parsing
description: |
  Set up and run PaddleOCR 3.5 with a Transformers backend for text detection, text recognition, full OCR pipelines, and document parsing.
  TRIGGER: user mentions PaddleOCR, OCR with transformers, document parsing with PaddleOCR, PP-OCRv5, or PaddleOCR-VL
---

# PaddleOCR 3.5: OCR & Document Parsing with Transformers Backend

Run OCR and document parsing tasks using PaddleOCR 3.5 with the Hugging Face Transformers inference backend.

## When to use

- "Set up PaddleOCR with a Transformers backend"
- "Run OCR on an image or PDF using PaddleOCR 3.5"
- "Parse a document layout and extract text with PaddleOCR-VL"
- "Use PP-OCRv5 models for text detection and recognition"
- "Extract text from images for RAG or document AI pipelines"

## How to use

### 1. Install dependencies

```bash
# For CUDA 12.6 (adjust for your hardware)
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install PaddleOCR with Transformers support
python -m pip install "paddleocr==3.5.0" "paddlex==3.5.2" "transformers>=5.4.0"
```

### 2. Run OCR from Python

```python
from paddleocr import PaddleOCR

pipeline = PaddleOCR(
    device="gpu:0",
    engine="transformers",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine_config={"dtype": "float32"},
)

results = pipeline.predict("path/to/image.png")
for result in results:
    print(result)
```

### 3. Run OCR from CLI

```bash
paddleocr ocr -i image.png --device gpu:0 --engine transformers
```

### 4. Engine configuration

```python
engine_config = {
    "dtype": "bfloat16",
    "attn_implementation": "sdpa",
}

pipeline = PaddleOCR(device="gpu:0", engine="transformers", engine_config=engine_config)
```

### 5. Key models

| Task | Model |
|---|---|
| Text detection + recognition | PP-OCRv5 |
| Document parsing | PaddleOCR-VL 1.5 |

Models auto-download from HF Hub when `engine="transformers"` is set.

## References

- [Blog Post](https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers)
- [GitHub](https://github.com/PaddlePaddle/PaddleOCR)
