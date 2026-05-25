#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== Datasette Jump Menu Plugin Demo ==="
echo ""

# Step 1: Create sample database
echo "Creating sample database with bookmarks..."
python setup_demo.py
echo ""

# Step 2: Install the plugin in development mode
echo "Installing plugin (datasette-jump-bookmarks)..."
pip install -e datasette-jump-bookmarks/ --quiet 2>/dev/null || pip install -e datasette-jump-bookmarks/
echo "Plugin installed."
echo ""

# Step 3: Verify plugin is registered
echo "Verifying plugin registration..."
python -c "
from datasette_jump_bookmarks import jump_items_sql
result = jump_items_sql(datasette=None, actor=None, request=None)
print(f'Hook returned {len(result)} query tuple(s):')
for sql, db, params in result:
    print(f'  DB: {db}')
    print(f'  SQL: {sql}')
print()
print('Plugin hook is working correctly!')
"
echo ""

# Step 4: Test the SQL query against the actual database
echo "Testing jump menu query against sample.db..."
python -c "
import sqlite_utils

db = sqlite_utils.Database('sample.db')
# Simulate what Datasette does: bind :q to %search_term%
results = list(db.execute('SELECT label, url, description FROM bookmarks WHERE label LIKE :q', {'q': '%cl%'}).fetchall())
print(f'Search for \"cl\" returns {len(results)} result(s):')
for row in results:
    print(f'  [{row[0]}] -> {row[1]}')
    print(f'    {row[2]}')
print()

results = list(db.execute('SELECT label, url, description FROM bookmarks WHERE label LIKE :q', {'q': '%%'}).fetchall())
print(f'Empty search returns all {len(results)} bookmarks:')
for row in results:
    print(f'  [{row[0]}] -> {row[1]}')
"
echo ""
echo "=== Demo complete ==="
echo "To run Datasette with this plugin:"
echo "  datasette sample.db --port 8001"
echo "Then press / on any page to open the Jump menu."
