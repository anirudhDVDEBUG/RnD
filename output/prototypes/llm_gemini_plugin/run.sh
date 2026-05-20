#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== llm-gemini 0.32a0 — Reasoning Token Streaming Demo ==="
echo ""
echo "No API key needed — this uses mock data to show the workflow."
echo ""

python3 demo_llm_gemini.py
