#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Cleaning previous output..."
rm -rf output/

echo "Running Claude Design AI demo..."
node src/demo.js
