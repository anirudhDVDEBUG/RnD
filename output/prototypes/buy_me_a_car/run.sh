#!/usr/bin/env bash
# Buy Me A Car - demo runner
# Runs the full used-car-buying workflow with mock data (no API keys needed).

set -euo pipefail
cd "$(dirname "$0")"

echo "Running Buy Me A Car demo..."
python3 car_buyer.py
