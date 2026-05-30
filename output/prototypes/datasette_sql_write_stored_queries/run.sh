#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "  Datasette SQL Write Queries & Stored Queries Demo"
echo "  (Datasette 1.0a31+)"
echo "============================================================"

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is required"
    exit 1
fi

# Install dependencies if needed
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q datasette sqlite-utils httpx

# Step 1: Create the demo database
echo ""
echo "Step 1: Creating demo database..."
python3 demo_setup.py

# Step 2: Start Datasette in background
echo ""
echo "Step 2: Starting Datasette on port 8001..."
datasette demo.db --metadata datasette.yml --port 8001 --host 127.0.0.1 &
DATASETTE_PID=$!

# Ensure cleanup on exit
cleanup() {
    if kill -0 $DATASETTE_PID 2>/dev/null; then
        kill $DATASETTE_PID 2>/dev/null
        wait $DATASETTE_PID 2>/dev/null || true
    fi
    rm -f demo.db demo.db-wal demo.db-shm
}
trap cleanup EXIT

# Step 3: Run the demo queries
echo ""
echo "Step 3: Running write query demonstrations..."
python3 demo_queries.py

echo ""
echo "============================================================"
echo "  To explore interactively:"
echo "  datasette demo.db --metadata datasette.yml --port 8001"
echo "  Then visit: http://localhost:8001/demo"
echo "============================================================"
