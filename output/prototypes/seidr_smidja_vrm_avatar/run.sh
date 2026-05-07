#!/usr/bin/env bash
# Seidr-Smidja VRM Avatar Generator -- End-to-end demo
# No external API keys required. Generates a valid VRM file using procedural mesh.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo " Seidr-Smidja VRM Avatar Generator - Demo"
echo "============================================"
echo ""

# Generate a cyberpunk-style avatar
echo "--- Creating cyberpunk avatar ---"
echo ""
python3 seidr_smidja.py --create --style cyberpunk --name "NeonKitsune"

echo ""
echo "--- Inspecting generated file ---"
echo ""
python3 seidr_smidja.py --inspect output/NeonKitsune.vrm

echo ""
echo "--- Creating anime-style avatar ---"
echo ""
python3 seidr_smidja.py --create --style anime --name "SakuraBot"

echo ""
echo "--- Creating fantasy avatar with accessories ---"
echo ""
python3 seidr_smidja.py --create --style fantasy --name "ElvenSage" --accessories "crown,cape"

echo ""
echo "============================================"
echo " All avatars generated in ./output/"
echo " Files are valid glTF binary (VRM format)"
echo "============================================"
ls -lh output/*.vrm
