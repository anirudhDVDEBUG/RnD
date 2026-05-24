#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Installing dependencies ==="
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "=== Running Nemotron-Labs Diffusion LM Demo ==="
echo ""

python3 nemotron_dlm_demo.py --all --verbose
