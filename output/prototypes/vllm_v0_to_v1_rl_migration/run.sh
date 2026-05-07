#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "vLLM V0 -> V1 RL Migration Validator"
echo "======================================"
echo ""

python3 demo.py
