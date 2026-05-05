#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=8765

echo "============================================="
echo "  Redis Array Playground"
echo "============================================="
echo ""
echo "Starting local server on http://localhost:$PORT"
echo "Open the URL above in your browser to explore"
echo "Redis Array commands interactively."
echo ""
echo "Press Ctrl+C to stop the server."
echo "---------------------------------------------"
echo ""
echo "Available sample commands to try:"
echo "  1. Click 'Load Sample Data' to populate arrays"
echo "  2. Select ARGREP → key: fruits, CONTAINS, cherry"
echo "  3. Select ARSCAN → key: fruits, pattern: *berry*"
echo "  4. Select ARGETRANGE → key: fruits, start: 0, end: 4"
echo "  5. Select AROP → key: scores, index: 0, INCR"
echo ""
echo "============================================="
echo ""

# Prefer python3, fall back to python
if command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "ERROR: Python is required to serve the playground."
  echo "Install Python 3 and try again."
  exit 1
fi

cd "$DIR"
$PYTHON -m http.server "$PORT"
