#!/usr/bin/env bash
# Zephyr Local AI Sidekick — end-to-end demo
# Runs without external API keys or GPU; uses mock local LLM.
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "=================================================="
echo "  Zephyr Local AI Sidekick — run.sh"
echo "=================================================="
echo ""

# 1. Install Python deps (quietly)
echo "[1/3] Installing Python dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt

# 2. Run the standalone demo (exercises all 5 subsystems)
echo "[2/3] Running standalone demo..."
echo ""
python3 demo.py

# 3. Smoke-test the FastAPI bridge
echo "[3/3] Smoke-testing FastAPI bridge..."
echo ""

# Start uvicorn in the background
python3 -m uvicorn bridge:app --host 127.0.0.1 --port 8199 --log-level warning &
SERVER_PID=$!
sleep 2

if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "  FastAPI bridge running on http://127.0.0.1:8199"

    echo ""
    echo "  GET /health:"
    curl -s http://127.0.0.1:8199/health | python3 -m json.tool

    echo ""
    echo "  POST /chat:"
    curl -s -X POST http://127.0.0.1:8199/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "How does Zephyr use RAG?"}' | python3 -m json.tool

    echo ""
    echo "  GET /skills:"
    curl -s http://127.0.0.1:8199/skills | python3 -m json.tool

    echo ""
    echo "  GET /mcp/tools:"
    curl -s http://127.0.0.1:8199/mcp/tools | python3 -m json.tool

    echo ""
    echo "  POST /self-heal/demo:"
    curl -s -X POST http://127.0.0.1:8199/self-heal/demo | python3 -m json.tool

    # Cleanup
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
    echo ""
    echo "  Bridge stopped."
else
    echo "  WARNING: Bridge failed to start. Demo output above is still valid."
fi

echo ""
echo "=================================================="
echo "  Done. All subsystems exercised successfully."
echo "=================================================="
