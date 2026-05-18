#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Install dependencies
if ! python3 -c "import rich" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "=== AI Memory Reader — Demo Run ==="
echo ""

# Run with mock data and content previews
python3 ai_memory_reader.py --mock --content

echo ""
echo "=== Done. Run 'python3 ai_memory_reader.py' without --mock to scan real agent dirs ==="
