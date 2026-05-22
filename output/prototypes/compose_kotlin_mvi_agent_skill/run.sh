#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Cleaning previous output..."
rm -rf generated_output

echo "Running MVI scaffold generator..."
python3 mvi_scaffold.py

echo ""
echo "Done. See generated_output/ for the full Kotlin source tree."
