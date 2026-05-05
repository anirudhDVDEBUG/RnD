#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== nvidia_claude_proxy Demo ==="
echo ""

# Install dependencies
if ! python3 -c "import flask" 2>/dev/null; then
    echo "[SETUP] Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "[PROXY] Starting in MOCK mode (no NVIDIA_API_KEY needed for demo)..."
echo ""

# Start proxy in background
python3 proxy.py &
PROXY_PID=$!

# Wait for server to start
sleep 2

echo ""
echo "--- Test 1: Basic message translation ---"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8082/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "What is the capital of France?"}]
  }')

echo "Request:  POST /v1/messages model=claude-sonnet-4-20250514"
echo "Response: $(echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE")"
echo ""

echo "--- Test 2: Different model mapping ---"
echo ""

RESPONSE2=$(curl -s -X POST http://localhost:8082/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4-20250514",
    "max_tokens": 128,
    "system": "You are a helpful assistant.",
    "messages": [{"role": "user", "content": "Explain quantum computing in one sentence."}]
  }')

echo "Request:  POST /v1/messages model=claude-opus-4-20250514 (maps to kimi-k2)"
echo "Response: $(echo "$RESPONSE2" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE2")"
echo ""

echo "--- Test 3: Health check ---"
echo ""
curl -s http://localhost:8082/health | python3 -m json.tool
echo ""

echo "--- Test 4: Dashboard stats ---"
echo ""
echo "Dashboard available at: http://localhost:8082/dashboard"
echo "Stats after 2 requests:"
curl -s http://localhost:8082/health | python3 -m json.tool
echo ""

echo "=== Demo complete ==="
echo "The proxy translated 2 Anthropic API requests into OpenAI format."
echo "In production, these would be forwarded to NVIDIA NIM endpoints."
echo ""

# Cleanup
kill $PROXY_PID 2>/dev/null || true
