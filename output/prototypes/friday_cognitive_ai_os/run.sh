#!/usr/bin/env bash
# FRIDAY Cognitive AI OS - Demo Runner
# Runs end-to-end without API keys (mock mode)
set -e

cd "$(dirname "$0")"

echo "=== FRIDAY Cognitive AI OS - Demo ==="
echo ""

# Clean prior demo memory so output is deterministic
rm -f friday/data/memory_store.json

# Run the demo (no external deps needed in mock mode)
python3 friday/main.py

echo "=== Demo complete. ==="
echo "Try interactive mode: python3 friday/main.py --interactive"
