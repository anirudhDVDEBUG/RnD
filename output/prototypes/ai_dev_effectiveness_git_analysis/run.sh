#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=========================================="
echo "  AI Dev Effectiveness Analyzer"
echo "=========================================="
echo ""

# --- Demo mode (no external deps or API keys needed) ---
echo "[1/3] Running demo analysis with mock data..."
echo ""
python3 "$SCRIPT_DIR/analyze.py" --demo
echo ""

# --- JSON output ---
echo "[2/3] JSON output (first 30 lines):"
echo ""
python3 "$SCRIPT_DIR/analyze.py" --demo --output json | head -30
echo "  ..."
echo ""

# --- Analyze THIS repo if we're inside one ---
echo "[3/3] Analyzing current repo ($(pwd))..."
echo ""
if [ -d .git ] || git rev-parse --git-dir >/dev/null 2>&1; then
    python3 "$SCRIPT_DIR/analyze.py" --repo "$(git rev-parse --show-toplevel)" --since 2025-01-01
else
    echo "  (Not inside a git repo — skipping live analysis)"
fi

echo ""
echo "Done. Run 'python3 analyze.py --repo /path/to/repo' on any git repo."
