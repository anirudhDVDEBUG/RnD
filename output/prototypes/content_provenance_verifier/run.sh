#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "============================================"
echo "  Content Provenance Verifier — Demo"
echo "============================================"
echo ""

# Fix sample hashes (ensures mock signatures verify correctly)
python3 cli.py fix-hashes

# Step 1: Verify all sample files
echo ">>> Step 1: Verifying sample files..."
echo ""
python3 cli.py verify-all

# Step 2: Show supported source types
echo ""
echo ">>> Step 2: IPTC Digital Source Types"
python3 cli.py source-types

# Step 3: Demonstrate signing a new file
echo ""
echo ">>> Step 3: Signing demo — create & verify Content Credentials"
python3 cli.py sign-demo

echo ""
echo "Done. See HOW_TO_USE.md for integration instructions."
