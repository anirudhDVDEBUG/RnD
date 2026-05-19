#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "──────────────────────────────────────────────"
echo "  Open Agent Leaderboard Evaluator — Demo"
echo "──────────────────────────────────────────────"
echo ""

# Install deps if needed (all stdlib, so this is a no-op for most setups)
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
fi

echo "▶ Running full evaluation across 6 benchmarks (mock data)..."
echo ""
python3 evaluate.py --output results.json

echo ""
echo "▶ Running single-benchmark mode (SWE-Bench only)..."
echo ""
python3 evaluate.py --benchmark swe

echo ""
echo "▶ Running leaderboard comparison view..."
echo ""
python3 evaluate.py --compare

echo ""
echo "──────────────────────────────────────────────"
echo "  ✓ All demos complete. See results.json for"
echo "    structured output."
echo "──────────────────────────────────────────────"
