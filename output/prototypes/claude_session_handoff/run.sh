#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Claude Session Handoff — Demo"
echo "============================================"
echo ""

# --- Demo 1: Mock mode (no git required) ---
echo ">>> Demo 1: Generate STATUS.md from mock project state"
echo "    (simulates a feature/user-dashboard branch mid-sprint)"
echo ""
python3 handoff.py --mock
echo ""

# --- Demo 2: Write to file ---
echo "============================================"
echo ">>> Demo 2: Write STATUS.md to disk"
echo ""
python3 handoff.py --mock --output STATUS.md
echo "    Contents of STATUS.md:"
echo "    $(wc -l < STATUS.md) lines, $(wc -c < STATUS.md) bytes"
echo ""

# --- Demo 3: JSON output (machine-readable) ---
echo "============================================"
echo ">>> Demo 3: Raw git state as JSON (for programmatic use)"
echo ""
python3 handoff.py --mock --json
echo ""

# --- Demo 4: Real git state (if we're in a repo) ---
echo "============================================"
echo ">>> Demo 4: Detect real git state from this repo"
echo ""
python3 handoff.py --repo "$SCRIPT_DIR/../../.." 2>&1 | head -60
echo "    ..."
echo ""

echo "============================================"
echo "Done. STATUS.md written to: $SCRIPT_DIR/STATUS.md"
echo "A new Claude session can read this file to resume instantly."
echo "============================================"
