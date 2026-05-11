#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────
# Cloudflare Tunnel Route Manager — Demo
# Runs entirely with mock data (no cloudflared or API keys needed)
# ─────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$(mktemp -d)"
CONFIG="$DEMO_DIR/config.yml"
MANAGER="$SCRIPT_DIR/tunnel_manager.py"

trap 'rm -rf "$DEMO_DIR"' EXIT

echo "============================================"
echo " Cloudflare Tunnel Route Manager — Demo"
echo "============================================"
echo ""
echo "Working with mock config at: $CONFIG"
echo ""

# Ensure PyYAML is available
pip install -q pyyaml 2>/dev/null || pip3 install -q pyyaml 2>/dev/null || true

# ── Step 1: Initialize a tunnel config ──────────────────────
echo "── Step 1: Initialize tunnel config ──"
python3 "$MANAGER" -c "$CONFIG" init "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
echo ""

echo "── Initial config file ──"
cat "$CONFIG"
echo ""

# ── Step 2: List routes (should show only catch-all) ────────
echo "── Step 2: List routes (empty tunnel) ──"
python3 "$MANAGER" -c "$CONFIG" list
echo ""

# ── Step 3: Add routes for various services ─────────────────
echo "── Step 3: Add routes ──"
python3 "$MANAGER" -c "$CONFIG" add api.example.com http://localhost:8000 --no-dns
echo ""

python3 "$MANAGER" -c "$CONFIG" add demo.example.com http://localhost:7860 --no-dns
echo ""

python3 "$MANAGER" -c "$CONFIG" add dashboard.example.com http://localhost:8501 --no-dns
echo ""

# ── Step 4: List all routes ─────────────────────────────────
echo "── Step 4: List all routes ──"
python3 "$MANAGER" -c "$CONFIG" list

# ── Step 5: Show the resulting config file ──────────────────
echo "── Step 5: Resulting config.yml ──"
cat "$CONFIG"
echo ""

# ── Step 6: Remove a route ──────────────────────────────────
echo "── Step 6: Remove a route ──"
python3 "$MANAGER" -c "$CONFIG" remove demo.example.com
echo ""

# ── Step 7: Final state ─────────────────────────────────────
echo "── Step 7: Final route list ──"
python3 "$MANAGER" -c "$CONFIG" list

echo "── Final config.yml ──"
cat "$CONFIG"
echo ""

echo "============================================"
echo " Demo complete!"
echo " In production, restart your tunnel with:"
echo "   cloudflared tunnel run <tunnel-name>"
echo "============================================"
