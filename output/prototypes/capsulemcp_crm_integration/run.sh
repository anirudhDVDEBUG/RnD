#!/usr/bin/env bash
# run.sh — End-to-end demo of capsulemcp CRM integration
# Spins up a mock Capsule CRM API, runs the demo, then cleans up.
# Zero external dependencies — uses only Node.js built-in modules.
set -euo pipefail
cd "$(dirname "$0")"

MOCK_PORT=4100
export MOCK_PORT

echo "── Starting mock Capsule CRM API on port $MOCK_PORT ──"
node mock_capsule_server.js &
SERVER_PID=$!

# ensure cleanup on exit
cleanup() { kill "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT

# wait for server to be ready
for i in $(seq 1 20); do
  if node -e "
    const http = require('http');
    const req = http.get('http://localhost:$MOCK_PORT/api/v2/parties', {headers:{Authorization:'Bearer test'}}, (res) => {
      process.exit(res.statusCode === 200 ? 0 : 1);
    });
    req.on('error', () => process.exit(1));
    req.setTimeout(500, () => process.exit(1));
  " 2>/dev/null; then
    break
  fi
  sleep 0.25
done

echo ""
echo "── Running capsulemcp demo ──"
node demo.js

echo ""
echo "── Done. Mock server shut down. ──"
