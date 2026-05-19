#!/usr/bin/env python3
"""
PaddleOCR 3.5 with Transformers Backend - Demo Script

Demonstrates OCR text detection + recognition and document parsing
using PaddleOCR 3.5's Hugging Face Transformers engine.

Falls back to mock mode when paddleocr/GPU are unavailable.
"""

import json
import sys
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Mock data for demo without GPU / model downloads
# ---------------------------------------------------------------------------
MOCK_OCR_RESULTS = [
    {"text": "REGISTRATION No.", "confidence": 0.987, "bbox": [[26, 20], [340, 20], [340, 56], [26, 56]]},
    {"text": "MH-04-AS-1234", "confidence": 0.994, "bbox": [[350, 20], [620, 20], [620, 56], [350, 56]]},
    {"text": "Owner Name:", "confidence": 0.991, "bbox": [[26, 80], [200, 80], [200, 110], [26, 110]]},
    {"text": "John Smith", "confidence": 0.985, "bbox": [[210, 80], [400, 80], [400, 110], [210, 110]]},
    {"text": "Vehicle Class:", "confidence": 0.978, "bbox": [[26, 140], [230, 140], [230, 170], [26, 170]]},
    {"text": "LMV - Light Motor Vehicle", "confidence": 0.963, "bbox": [[240, 140], [560, 140], [560, 170], [240, 170]]},
    {"text": "Date of Issue:", "confidence": 0.992, "bbox": [[26, 200], [220, 200], [220, 230], [26, 230]]},
    {"text": "15/03/2024", "confidence": 0.997, "bbox": [[230, 200], [400, 200], [400, 230], [230, 230]]},
    {"text": "Valid Until:", "confidence": 0.989, "bbox": [[26, 260], [200, 260], [200, 290], [26, 290]]},
    {"text": "14/03/2039", "confidence": 0.996, "bbox": [[210, 260], [400, 260], [400, 290], [210, 290]]},
]

MOCK_DOC_PARSE_RESULTS = {
    "layout_elements": [
        {"type": "title", "bbox": [50, 30, 550, 70], "text": "INVOICE #INV-2024-0042"},
        {"type": "table", "bbox": [50, 100, 550, 350], "cells": [
            {"row": 0, "col": 0, "text": "Item"},
            {"row": 0, "col": 1, "text": "Qty"},
            {"row": 0, "col": 2, "text": "Price"},
            {"row": 1, "col": 0, "text": "Widget A"},
            {"row": 1, "col": 1, "text": "10"},
            {"row": 1, "col": 2, "text": "$25.00"},
            {"row": 2, "col": 0, "text": "Widget B"},
            {"row": 2, "col": 1, "text": "5"},
            {"row": 2, "col": 2, "text": "$42.50"},
        ]},
        {"type": "paragraph", "bbox": [50, 370, 550, 410], "text": "Total: $462.50"},
        {"type": "paragraph", "bbox": [50, 420, 550, 460], "text": "Payment due within 30 days."},
    ]
}


def try_live_ocr(image_url: str):
    """Attempt live OCR using PaddleOCR with Transformers backend."""
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        return None

    device = "gpu:0" if _gpu_available() else "cpu"
    print(f"[LIVE] Initializing PaddleOCR pipeline (device={device}, engine=transformers)...")

    pipeline = PaddleOCR(
        device=device,
        engine="transformers",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        engine_config={"dtype": "float32"},
    )

    results = pipeline.predict(image_url)
    return results


def _gpu_available():
    """Check if a CUDA GPU is available via torch."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


def run_mock_ocr():
    """Run mock OCR demo."""
    print("=" * 65)
    print("  PaddleOCR 3.5 + Transformers  --  OCR Demo (mock mode)")
    print("=" * 65)
    print()
    print("[INFO] paddleocr not installed or no GPU -- using mock results.")
    print("[INFO] Install paddleocr>=3.5.0 + transformers>=5.4.0 for live mode.")
    print()

    # --- OCR results ---
    print("-" * 65)
    print("  Task 1: Text Detection + Recognition (PP-OCRv5)")
    print("-" * 65)
    print(f"  Input : sample registration document image")
    print(f"  Model : PP-OCRv5 (text det + rec)")
    print(f"  Engine: Hugging Face Transformers")
    print()
    print(f"  {'Text':<35} {'Confidence':>10}")
    print(f"  {'─' * 35} {'─' * 10}")
    for item in MOCK_OCR_RESULTS:
        print(f"  {item['text']:<35} {item['confidence']:>10.3f}")
    print()
    print(f"  Total text regions detected: {len(MOCK_OCR_RESULTS)}")
    print()

    # --- Document parsing results ---
    print("-" * 65)
    print("  Task 2: Document Parsing (PaddleOCR-VL 1.5)")
    print("-" * 65)
    print(f"  Input : sample invoice document")
    print(f"  Model : PaddleOCR-VL 1.5")
    print()

    for elem in MOCK_DOC_PARSE_RESULTS["layout_elements"]:
        etype = elem["type"].upper()
        if etype == "TABLE":
            print(f"  [{etype}] Detected table with {len(elem['cells'])} cells:")
            # Render a simple table
            rows = {}
            for cell in elem["cells"]:
                rows.setdefault(cell["row"], {})[cell["col"]] = cell["text"]
            for r in sorted(rows):
                vals = [rows[r].get(c, "") for c in sorted(rows[r])]
                print(f"    | {' | '.join(f'{v:<12}' for v in vals)} |")
        else:
            print(f"  [{etype}] {elem['text']}")
    print()

    # --- JSON output ---
    output_path = Path("output_results.json")
    combined = {
        "ocr_results": MOCK_OCR_RESULTS,
        "doc_parse_results": MOCK_DOC_PARSE_RESULTS,
    }
    output_path.write_text(json.dumps(combined, indent=2))
    print(f"  Results saved to: {output_path}")
    print()

    print("=" * 65)
    print("  Demo complete. See HOW_TO_USE.md for live-mode instructions.")
    print("=" * 65)


def run_live_ocr():
    """Run live OCR demo."""
    image_url = "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png"

    print("=" * 65)
    print("  PaddleOCR 3.5 + Transformers  --  OCR Demo (LIVE mode)")
    print("=" * 65)
    print()
    print(f"  Input: {image_url}")
    print()

    results = try_live_ocr(image_url)
    if results is None:
        print("[WARN] Live OCR failed, falling back to mock mode.")
        run_mock_ocr()
        return

    for result in results:
        print(result)

    print()
    print("=" * 65)
    print("  Live OCR complete.")
    print("=" * 65)


def main():
    mode = os.environ.get("OCR_MODE", "auto")

    if mode == "live":
        run_live_ocr()
    elif mode == "mock":
        run_mock_ocr()
    else:
        # Auto: try live, fall back to mock
        try:
            import paddleocr  # noqa: F401
            run_live_ocr()
        except ImportError:
            run_mock_ocr()


if __name__ == "__main__":
    main()
