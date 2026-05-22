#!/bin/bash
set -e

echo "Appshot Store Preview Generator — Demo"
echo "======================================="
echo ""

# Check Node.js availability
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is required but not found. Install Node 18+."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "WARNING: Node.js 18+ recommended (found v$NODE_VERSION)"
fi

# Clean previous output
rm -rf ./demo_output

# Run the demo
node demo.js

# Show output files
echo "--- Output Files ---"
ls -la ./demo_output/
echo ""
echo "Done. Open demo_output/storyboard.html in a browser for the visual preview."
