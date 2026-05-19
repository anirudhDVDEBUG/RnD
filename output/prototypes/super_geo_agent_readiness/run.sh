#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Super GEO & Agent Readiness Demo ==="
echo ""

# --- Pass 1: Audit the well-configured sample site ---
echo "[Pass 1] Auditing well-configured sample site..."
echo ""
python3 geo_audit.py sample_site
echo ""

# --- Pass 2: Audit a bare / missing site to show failure mode ---
BARE_DIR=$(mktemp -d)
mkdir -p "$BARE_DIR"
cat > "$BARE_DIR/index.html" <<'HTML'
<!DOCTYPE html>
<html><head><title>Bare Site</title></head>
<body><h1>Hello World</h1><p>No structured data here.</p></body></html>
HTML

echo "[Pass 2] Auditing a bare site with no GEO signals..."
echo ""
python3 geo_audit.py "$BARE_DIR" || true
rm -rf "$BARE_DIR"

echo ""
echo "Done. Compare the two reports above to see what GEO readiness looks like."
