#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Running MemoryBridge cross-tool AI memory demo..."
echo ""

node demo.mjs
