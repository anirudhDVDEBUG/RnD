#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running cue agent profile manager demo..."
echo ""
node src/cue.js demo
