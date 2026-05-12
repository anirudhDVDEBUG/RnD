#!/usr/bin/env bash
# Goalkeeper Demo -- runs end-to-end with zero external dependencies.
set -euo pipefail
cd "$(dirname "$0")"
python3 demo.py
