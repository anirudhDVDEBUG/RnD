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

Install PyTorch for your hardware first, then the PaddleOCR stack:

```bash
# For CUDA 12.6 (adjust the index URL for your hardware: CPU, ROCm, etc.)
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install PaddleOCR with Transformers support
python -m pip install "paddleocr==3.5.0" "paddlex==3.5.2" "transformers>=5.4.0"
```

### 2. Run OCR from the command line

```bash
paddleocr ocr \
  -i https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png \
  --device gpu:0 \
  --engine transformers
```

### 3. Run OCR from Python

```python
from paddleocr import PaddleOCR

pipeline = PaddleOCR(
    device="gpu:0",
    engine="transformers",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine_config={
        "dtype": "float32",
    },
)

results = pipeline.predict(
    "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png"
)

for result in results:
    print(result)
```

### 4. Engine configuration options

Customize the Transformers engine via `engine_config`:

```python
engine_config = {
    "dtype": "bfloat16",              # float32, bfloat16, float16
    "device_type": "gpu",              # gpu or cpu
    "device_id": 0,                    # GPU device ID
    "attn_implementation": "sdpa",     # Attention implementation (sdpa, eager, flash_attention_2)
}

pipeline = PaddleOCR(
    device="gpu:0",
    engine="transformers",
    engine_config=engine_config,
)
```

### 5. Key models

| Task | Model family |
|---|---|
| Text detection & recognition | PP-OCRv5 |
| Document parsing | PaddleOCR-VL 1.5 |

Models are automatically downloaded from the Hugging Face Hub when `engine="transformers"` is set.

### 6. Common use cases

- **RAG pipelines**: Extract text from scanned documents for retrieval-augmented generation.
- **Document AI**: Parse invoices, receipts, forms, and reports.
- **Document search**: Index extracted text for full-text search.
- **Agent workflows**: Give agents the ability to read images and documents.

## References

- [PaddleOCR 3.5 Blog Post (Hugging Face)](https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers)
- [PaddleOCR Models on Hugging Face](https://huggingface.co/PaddlePaddle)
- [PaddleOCR Documentation](https://www.paddleocr.ai/)
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [Hugging Face Demo](https://huggingface.co/spaces/PaddlePaddle/paddleocr-3.5-transformers-demo)
