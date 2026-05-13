# How to Use: Datasette SQLite Explorer

## Installation

```bash
pip install 'datasette>=1.0a29'
```

Requires Python 3.9+. No external API keys needed.

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/datasette_sqlite_explorer
cp SKILL.md ~/.claude/skills/datasette_sqlite_explorer/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Spin up a datasette instance for this SQLite database"
- "I want to explore my .db file in a browser"
- "Create an API from this SQLite database"
- "Configure datasette API tokens with restrictions"
- "Publish this database with datasette"

Once installed, Claude Code will automatically use this skill when you mention datasette or SQLite exploration.

## First 60 seconds

**Step 1:** Run the demo:

```bash
bash run.sh
```

**Step 2:** You'll see output like:

```
Created demo database: demo.db
  - ai_tools: 12 rows
  - trend_signals: 576 rows
  - upcoming_reviews: 0 rows (tests 1.0a29 empty-table fix)

Starting Datasette on http://localhost:8001 ...
Datasette is ready!

============================================================
  Top 5 AI tools by GitHub stars
  GET /demo/ai_tools.json?_sort_desc=stars&_size=5
============================================================
[
  {"id": 4, "name": "Ollama", "stars": 112000, ...},
  {"id": 8, "name": "Dify", "stars": 52000, ...},
  ...
]
```

**Step 3:** Open http://localhost:8001 in your browser to get the full web UI with table browsing, filtering, and SQL editor.

**Step 4:** Try your own queries:

```bash
# JSON API - filter by category
curl 'http://localhost:8001/demo/ai_tools.json?category=coding-agent'

# Custom SQL via API
curl 'http://localhost:8001/demo.json?sql=select+name,stars+from+ai_tools+order+by+stars+desc+limit+3&_shape=array'
```

## Using with your own database

```bash
# Serve any SQLite file
datasette serve your_data.db

# Multiple databases at once
datasette serve db1.db db2.db analytics.db

# Custom port
datasette serve your_data.db --port 9000
```

## Publishing

```bash
# Deploy to Vercel (free tier works)
datasette publish vercel mydata.db --project my-datasette

# Deploy to Fly.io
datasette publish fly mydata.db --app my-datasette
```

## Plugins

```bash
datasette install datasette-vega           # Charts and visualizations
datasette install datasette-cluster-map    # Map visualizations
datasette install datasette-export-notebook # Jupyter notebook export
```
