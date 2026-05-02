#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== iNaturalist Sightings: Git Scraping + Viewer Demo ==="
echo ""

# 1. Generate mock data (no API key needed)
echo "[1/3] Generating mock observation data..."
python3 mock_data.py
echo ""

# 2. Show a sample of the JSON
echo "[2/3] Preview of clumps.json:"
python3 -c "
import json
with open('clumps.json') as f:
    data = json.load(f)
for i, clump in enumerate(data):
    obs = clump['observations']
    place = obs[0].get('place_guess', 'Unknown')
    names = [o.get('common_name','?') for o in obs]
    joined = ', '.join(names)
    print(f'  Clump {i+1}: {place} ({len(obs)} obs) -> {joined}')
"
echo ""

# 3. Serve the viewer
echo "[3/3] Opening viewer..."
echo "  Serving at http://localhost:8765/viewer.html"
echo "  Press Ctrl+C to stop."
echo ""
python3 -m http.server 8765 --bind 127.0.0.1
