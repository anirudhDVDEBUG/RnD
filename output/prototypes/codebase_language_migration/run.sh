#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================"
echo "  Codebase Language Migration Demo"
echo "  Python → TypeScript (offline, no API keys)"
echo "============================================"
echo ""

# Step 0: Run the source-language tests first (the behavioral contract)
echo "[pre] Running source Python tests (the behavioral contract)..."
echo ""
export PYTHONPATH="${PWD}:${PYTHONPATH:-}"
python3 -m pytest sample_project/tests/test_taskflow.py -v --tb=short 2>/dev/null \
  || python3 -m unittest discover -s sample_project/tests -p "test_*.py" -v
echo ""

# Step 1-5: Run the migration tool
echo "─────────────────────────────────────────────"
echo ""
python3 migrate.py

echo ""
echo "============================================"
echo "  Done. Check migration_output/ for results."
echo "============================================"
