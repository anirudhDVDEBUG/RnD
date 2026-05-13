#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Datasette SQLite Explorer - Demo"
echo "============================================"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create the demo database
echo ""
echo "Creating demo database..."
python create_demo_db.py

# Start Datasette in background
echo ""
echo "Starting Datasette on http://localhost:8001 ..."
datasette serve demo.db --port 8001 --host 127.0.0.1 &
DATASETTE_PID=$!

# Ensure cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down Datasette (PID $DATASETTE_PID)..."
    kill "$DATASETTE_PID" 2>/dev/null || true
    wait "$DATASETTE_PID" 2>/dev/null || true
    echo "Done."
}
trap cleanup EXIT

# Run API demo queries
python demo_api_queries.py

# Keep running so user can browse
echo ""
echo "Datasette is running. Press Ctrl+C to stop."
wait "$DATASETTE_PID"
