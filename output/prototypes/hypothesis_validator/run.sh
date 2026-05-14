#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "--- hypothesis_validator demo ---"
python3 validate_hypothesis.py
