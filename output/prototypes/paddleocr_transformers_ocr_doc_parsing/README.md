# PaddleOCR 3.5: OCR & Document Parsing with Transformers Backend

PaddleOCR 3.5 now runs natively on the Hugging Face Transformers inference stack, eliminating the need for PaddlePaddle. This means PP-OCRv5 (text detection + recognition) and PaddleOCR-VL 1.5 (document parsing) can be used with standard PyTorch workflows, CUDA, and HF model hub downloads -- no separate framework install required.

**Headline result:** Full OCR pipeline (detect + recognize) on a document image in ~2 lines of Python, using `engine="transformers"` with automatic model download from HF Hub.

```
  Text                                Confidence
  REGISTRATION No.                         0.987
  MH-04-AS-1234                            0.994
  Owner Name:                              0.991
  John Smith                               0.985
  ...
```

## Quick start

```bash
bash run.sh            # mock mode, no GPU needed
OCR_MODE=live bash run.sh   # live mode with real models
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) -- install, configure, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, models, limitations
