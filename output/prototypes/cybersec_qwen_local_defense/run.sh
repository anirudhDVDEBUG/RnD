#!/usr/bin/env bash
# CyberSecQwen-4B Demo Runner
# Runs mock demo by default. Set USE_REAL_MODEL=1 for actual model inference.
set -euo pipefail

cd "$(dirname "$0")"

echo "--- CyberSecQwen-4B Local Defense Demo ---"
echo ""

python3 cybersec_demo.py
