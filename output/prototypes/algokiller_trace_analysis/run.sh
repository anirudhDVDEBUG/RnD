#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "  ak_search — ARM64 Cipher Algorithm Recovery Demo"
echo "============================================================"
echo ""

# Step 1: Generate mock trace files
echo "[1/3] Generating mock ARM64 execution traces..."
python3 generate_mock_trace.py
echo ""

# Step 2: Analyze first trace (AES + ChaCha20)
echo "[2/3] Scanning aes_chacha_trace.log for cipher evidence..."
echo ""
python3 ak_search.py sample_traces/aes_chacha_trace.log
echo ""

# Step 3: Analyze second trace (DES + SHA-256), JSON output
echo "[3/3] Scanning des_sha256_trace.log (JSON output)..."
echo ""
python3 ak_search.py sample_traces/des_sha256_trace.log --format json
echo ""

echo "============================================================"
echo "  Done. Two traces analyzed, algorithms recovered."
echo "============================================================"
