# Technical Details: PaddleOCR 3.5 with Transformers Backend

## What it does

PaddleOCR 3.5 introduces a Hugging Face Transformers inference backend (`engine="transformers"`) that replaces the PaddlePaddle runtime entirely. This lets users run PaddleOCR's production-grade OCR models -- PP-OCRv5 for text detection/recognition and PaddleOCR-VL 1.5 for document layout parsing -- using standard PyTorch + Transformers, with models hosted on the Hugging Face Hub. The result is a full OCR pipeline (detect text regions, recognize characters, optionally parse document structure) that fits into existing PyTorch/Transformers workflows without installing the PaddlePaddle framework.

The key engineering contribution is a compatibility layer inside `paddleocr` and `paddlex` that translates PaddleOCR's pipeline API into Transformers model loading and inference calls. Users get the same `PaddleOCR(engine="transformers")` interface but the backend runs `AutoModel.from_pretrained()` under the hood.

## Architecture

```
User code
  │
  ▼
PaddleOCR Python API  (paddleocr==3.5.0)
  │
  ├── Pipeline orchestration (paddlex==3.5.2)
  │     ├── Text detection      → PP-OCRv5 det model (HF Hub)
  │     ├── Text recognition    → PP-OCRv5 rec model (HF Hub)
  │     ├── Doc orientation     → optional classifier
  │     ├── Doc unwarping       → optional dewarp model
  │     └── Document parsing    → PaddleOCR-VL 1.5 (HF Hub)
  │
  ▼
Transformers engine adapter
  │
  ├── AutoModel.from_pretrained(...)
  ├── dtype / device / attention config
  └── PyTorch inference (CUDA / CPU)
```

### Key files in this prototype

| File | Purpose |
|---|---|
| `ocr_demo.py` | Demo script with live + mock modes |
| `run.sh` | Entry point, defaults to mock mode |
| `requirements.txt` | Declared dependencies |
| `SKILL.md` | Claude Code skill definition |

### Dependencies

- **paddleocr 3.5.0** -- pipeline API and CLI
- **paddlex 3.5.2** -- model orchestration layer
- **transformers >= 5.4.0** -- inference backend
- **PyTorch** -- tensor computation (CUDA or CPU)

No PaddlePaddle install is needed when using `engine="transformers"`.

### Models

| Model | Task | Params | HF Hub |
|---|---|---|---|
| PP-OCRv5 (det) | Text detection | ~4M | PaddlePaddle/PP-OCRv5_server_det |
| PP-OCRv5 (rec) | Text recognition | ~12M | PaddlePaddle/PP-OCRv5_server_rec |
| PaddleOCR-VL 1.5 | Document parsing | ~2B | PaddlePaddle/PaddleOCR-VL-1.5 |

## Limitations

- **GPU recommended.** PP-OCRv5 runs on CPU but is slow. PaddleOCR-VL 1.5 (2B params) effectively requires a GPU with >=8 GB VRAM.
- **First-run download.** Models are fetched from HF Hub on first use (1-2 GB for OCR, larger for VL). No offline bundle.
- **Language coverage.** PP-OCRv5 supports ~80 languages but accuracy varies; best on Chinese and English.
- **No streaming.** Results are returned after full inference; no token-level streaming for the VL model.
- **No built-in PDF support.** You must convert PDF pages to images before calling the pipeline (e.g., via `pdf2image`).
- **Transformers version pinning.** Requires transformers >= 5.4.0; may break on future major versions.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **RAG / Document AI** | Extract text from scanned documents, invoices, receipts to feed into retrieval pipelines. Pairs well with Claude for question-answering over extracted content. |
| **Agent workflows** | Give Claude-based agents the ability to "read" images and documents by calling PaddleOCR as a tool or MCP server, enabling document-grounded reasoning. |
| **Lead-gen / Marketing** | Parse business cards, flyers, competitor materials automatically. Extract structured data (names, prices, dates) for CRM ingestion. |
| **Ad creative analysis** | OCR ad screenshots to extract copy, CTAs, and pricing for competitive intelligence pipelines. |
| **Voice AI** | Pre-process printed menus, signs, or forms into text that voice agents can read back to users. |

## References

- [PaddleOCR 3.5 Blog Post](https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers)
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [HF Demo Space](https://huggingface.co/spaces/PaddlePaddle/paddleocr-3.5-transformers-demo)
