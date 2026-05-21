#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
HTML="$DIR/token_speed_demo.html"

echo "=== Token Speed Visualizer ==="
echo ""
echo "HTML demo ready at: $HTML"
echo ""

# Try to open in browser
if command -v xdg-open &>/dev/null; then
  echo "Opening in browser..."
  xdg-open "$HTML" 2>/dev/null &
elif command -v open &>/dev/null; then
  echo "Opening in browser..."
  open "$HTML"
else
  echo "Open this file in any browser to use the demo:"
  echo "  file://$HTML"
fi

echo ""
echo "Features:"
echo "  - Preset speeds: 5, 10, 30, 50, 100, 200, 400, 800 tokens/sec"
echo "  - Adjustable slider from 5-800 t/s"
echo "  - Real-time token count & elapsed time"
echo "  - Dark mode support"
echo ""
echo "No dependencies required - pure HTML/CSS/JS."

# Also serve via Python if available (for convenience)
if command -v python3 &>/dev/null; then
  echo ""
  echo "Starting local server at http://localhost:8765/token_speed_demo.html"
  echo "(Press Ctrl+C to stop)"
  cd "$DIR"
  python3 -m http.server 8765 --bind 127.0.0.1 2>/dev/null &
  SERVER_PID=$!
  sleep 1
  echo "Server running (PID $SERVER_PID). Visit: http://localhost:8765/token_speed_demo.html"
  # Keep alive for 30s then exit
  sleep 30
  kill $SERVER_PID 2>/dev/null || true
  echo "Server stopped after 30s."
fi
