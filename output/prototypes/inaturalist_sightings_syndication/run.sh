#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Install dependencies if needed
if ! python3 -c "import jinja2" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Run with mock data (no API key needed)
python3 sync_sightings.py --mock
