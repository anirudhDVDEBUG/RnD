#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Customer Request → Code Pipeline ==="
echo ""

# No external dependencies needed — pure Python 3.10+
python3 pipeline.py sample_requests.json
