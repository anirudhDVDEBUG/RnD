#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Cord Agent Fabric — Demo ==="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found."
  exit 1
fi

# Install deps (stdlib only, so this is a no-op safety net)
if [ -f requirements.txt ]; then
  pip install -q -r requirements.txt 2>/dev/null || true
fi

echo "Running cord_demo.py ..."
echo ""
python3 cord_demo.py

echo ""
echo "=== Output files ==="
ls -lh cord_mesh_state.json 2>/dev/null || echo "(no output file found)"
