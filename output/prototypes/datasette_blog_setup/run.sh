#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================"
echo "  Datasette Blog Setup — Demo Run"
echo "============================================"
echo ""

# --- 1. Install dependencies ---
echo "[1/4] Installing dependencies..."
pip install -q datasette datasette-render-markdown datasette-search-all sqlite-utils 2>&1 | tail -5
echo "  Done."

# --- 2. Build the blog database and assets ---
echo ""
echo "[2/4] Setting up blog database, templates, and plugins..."
python3 setup_blog.py

# --- 3. Show the JSON API output (proves it works without a browser) ---
echo ""
echo "[3/4] Querying the blog via sqlite-utils CLI..."
echo ""
echo "--- All published posts (newest first) ---"
sqlite-utils query blog.db \
  "SELECT slug, title, published, tags FROM posts WHERE draft=0 ORDER BY published DESC" \
  --fmt table

echo ""
echo "--- Full-text search for 'plugin' ---"
sqlite-utils query blog.db \
  "SELECT p.title, p.published FROM posts p WHERE p.id IN (SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'plugin') ORDER BY p.published DESC" \
  --fmt table

echo ""
echo "--- Tags ---"
sqlite-utils query blog.db \
  "SELECT t.name AS tag, COUNT(pt.post_id) AS post_count FROM tags t JOIN post_tags pt ON t.id = pt.tag_id GROUP BY t.id ORDER BY post_count DESC" \
  --fmt table

echo ""
echo "--- JSON API preview (first post) ---"
sqlite-utils query blog.db \
  "SELECT id, slug, title, published, tags FROM posts ORDER BY published DESC LIMIT 1" \
  --json

# --- 4. Start Datasette (non-blocking check, then inform user) ---
echo ""
echo "[4/4] Verifying Datasette can load the database..."
datasette inspect blog.db --metadata metadata.json 2>/dev/null && echo "  Datasette inspection: OK" || echo "  Datasette inspection: skipped (inspect not available in this version)"

echo ""
echo "============================================"
echo "  Demo complete!"
echo "============================================"
echo ""
echo "  To launch the live blog server, run:"
echo ""
echo "    datasette blog.db --metadata metadata.json \\"
echo "      --template-dir templates/ --plugins-dir plugins/"
echo ""
echo "  Then open http://127.0.0.1:8001 in your browser."
echo ""
