#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Equity Research Agent — Demo Run"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# No external dependencies needed — stdlib only
echo "[1/3] Full research report for NVDA (intermediate level)..."
python3 equity_research.py NVDA --level intermediate

echo ""
echo "[2/3] Quantitative stock screen..."
python3 equity_research.py --screen

echo ""
echo "[3/3] Side-by-side comparison: NVDA vs AAPL..."
python3 equity_research.py --compare NVDA AAPL --level beginner

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done. All analysis used mock data — no API keys needed."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
