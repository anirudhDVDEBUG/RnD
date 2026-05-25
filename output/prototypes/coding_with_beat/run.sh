#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Install dependencies if needed
if ! python3 -c "import rich" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "=== Coding with Beat — Demo Mode ==="
echo ""
python3 codebeat_demo.py
