#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== alchemy-infra demo ==="
echo ""

# No npm dependencies needed — pure Node.js
node demo.mjs
