#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
HTML="$DIR/qr-code-generator.html"
PORT="${PORT:-8765}"

echo "============================================"
echo "  QR Code Generator — Local Demo"
echo "============================================"
echo ""
echo "Starting local server on http://localhost:${PORT}"
echo "Serving: $HTML"
echo ""

# Try to open a browser (best-effort, non-blocking)
if command -v xdg-open &>/dev/null; then
  (sleep 1 && xdg-open "http://localhost:${PORT}/qr-code-generator.html") &
elif command -v open &>/dev/null; then
  (sleep 1 && open "http://localhost:${PORT}/qr-code-generator.html") &
else
  echo "Open http://localhost:${PORT}/qr-code-generator.html in your browser."
fi

echo "Press Ctrl+C to stop."
echo ""

# Serve the directory with Python's built-in HTTP server
python3 -m http.server "$PORT" --directory "$DIR"
