#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Anti-Sycophancy Reviewer ==="
echo ""

# Run with bundled sample data (no API keys needed)
python3 reviewer.py sample_responses.json

echo ""
echo "--- JSON output mode ---"
python3 reviewer.py sample_responses.json --json
