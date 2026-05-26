#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Running Claude Writing Skills pipeline demo..."
echo ""

python3 pipeline.py
