#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Voice AI Transport Evaluator ==="
echo ""
echo "Running default scenario (Voice AI / LLM Prompt Streaming)..."
echo ""
python3 evaluator.py
echo ""
echo "--- Running all scenarios ---"
echo ""
python3 evaluator.py --all-scenarios
echo ""
echo "--- JSON output (default scenario) ---"
echo ""
python3 evaluator.py --json
echo ""
echo "Done. See HOW_TO_USE.md for more options."
