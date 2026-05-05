#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Checking for TRE library..."
if ldconfig -p 2>/dev/null | grep -q libtre || [ -f /usr/local/lib/libtre.so ] || brew list tre &>/dev/null 2>&1; then
    echo "TRE library found."
else
    echo "WARNING: TRE library not found. Will run in mock mode."
    echo "  Install: sudo apt-get install libtre-dev (Debian/Ubuntu)"
    echo ""
fi

echo ""
python3 redos_benchmark.py
