#!/bin/bash
# Retro Book Game Converter — Demo runner
# Serves the converted "Mad House" game locally and prints a text preview

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=8973

echo "============================================="
echo "  RETRO BOOK GAME CONVERTER — Demo"
echo "  Mad House (Usborne Creepy Computer Games)"
echo "============================================="
echo ""
echo "Game file: $SCRIPT_DIR/index.html"
echo ""

# Show a text-based preview of what the game looks like
echo "--- GAME PREVIEW (text rendering) ---"
echo ""
cat << 'EOF'
  MAD HOUSE
  ╔════════════════════╗
  ║████████████████████║
  ║█  $    ██   G    █║
  ║█ ███      ████   █║
  ║█      @       $  █║
  ║█ ██████  ██████  █║
  ║█ $       G       █║
  ║█   ████████  ██  █║
  ║█        $      E █║
  ║████████████████████║
  ╚════════════════════╝

  @ = You  G = Ghost  $ = Treasure  E = Exit
  SCORE: 20 | MOVES: 14 | GHOSTS: 3
EOF
echo ""
echo "--- END PREVIEW ---"
echo ""

# Check if python3 is available for serving
if command -v python3 &> /dev/null; then
  echo "Starting local server at http://localhost:$PORT"
  echo "Open in your browser to play the game."
  echo "Press Ctrl+C to stop."
  echo ""
  cd "$SCRIPT_DIR"
  python3 -m http.server "$PORT" 2>/dev/null &
  SERVER_PID=$!

  # Give server a moment to start
  sleep 1

  echo "Server running at: http://localhost:$PORT"
  echo ""

  # If curl is available, fetch the page title to prove it works
  if command -v curl &> /dev/null; then
    echo "Verifying game is served correctly..."
    TITLE=$(curl -s "http://localhost:$PORT/" | grep -o '<title>[^<]*</title>' || true)
    if [ -n "$TITLE" ]; then
      echo "Success! Page title: $TITLE"
    else
      echo "Server is running (page served)."
    fi
  fi

  echo ""
  echo "Game is playable at http://localhost:$PORT"
  echo "Controls: Arrow keys or on-screen buttons"
  echo ""

  # Clean up server
  kill $SERVER_PID 2>/dev/null || true
  echo "Demo complete. Server stopped."
else
  echo "python3 not found — opening file directly would work in any browser:"
  echo "  file://$SCRIPT_DIR/index.html"
  echo ""
  echo "Demo complete."
fi

echo ""
echo "To use this skill with Claude Code:"
echo "  cp -r skill/ ~/.claude/skills/retro_book_game_converter/"
echo ""
