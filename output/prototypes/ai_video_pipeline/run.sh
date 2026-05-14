#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== AI Video Pipeline — Demo ==="
echo ""

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>&1 | tail -1

# Run in MOCK mode (no API keys needed)
echo ""
export MOCK=1
python3 pipeline.py "The Future of Artificial Intelligence" 3

echo ""
echo "Done. Check output/ for generated files."
