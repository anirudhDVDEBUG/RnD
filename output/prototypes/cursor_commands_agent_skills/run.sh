#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Agent Skills — Behavioral Eval Demo"
echo "============================================"
echo ""

# --- 1. Install deps ---
echo "[1/4] Installing dependencies ..."
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null
echo "  Done."

# --- 2. List available commands ---
echo ""
echo "[2/4] Discovered slash commands:"
for cmd in commands/*.md; do
    name=$(head -1 "$cmd" | sed 's/^#\s*//')
    echo "  - $name  ($(basename "$cmd"))"
done

# --- 3. List rubrics ---
echo ""
echo "[3/4] Discovered eval rubrics:"
for rub in eval/rubrics/*.yaml; do
    echo "  - $(basename "$rub" .yaml)"
done

# --- 4. Run evals + gate check ---
echo ""
echo "[4/4] Running behavioral evals against mock outputs ..."
echo ""
python3 eval/run_evals.py \
    --rubrics-dir eval/rubrics \
    --mock-dir eval/mock_outputs \
    --output eval-results.json

python3 eval/check_gate.py --results eval-results.json

echo ""
echo "Raw results saved to: eval-results.json"
echo "Done."
