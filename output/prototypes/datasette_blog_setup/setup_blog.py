#!/usr/bin/env python3
"""
Datasette Blog Setup — creates a SQLite-backed blog database,
seeds it with sample posts, configures metadata and templates,
and launches Datasette to serve it.
"""

import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import date, timedelta

DB_PATH = "blog.db"
METADATA_PATH = "metadata.json"
TEMPLATES_DIR = "templates"
PLUGINS_DIR = "plugins"


def create_database():
    """Create the blog SQLite database with schema and indexes."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            published DATE NOT NULL DEFAULT (date('now')),
            updated DATE,
            draft INTEGER NOT NULL DEFAULT 0,
            tags TEXT DEFAULT ''
        );
        CREATE INDEX idx_posts_published ON posts(published);
        CREATE INDEX idx_posts_slug ON posts(slug);

        CREATE TABLE tags (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE post_tags (
            post_id INTEGER REFERENCES posts(id),
            tag_id INTEGER REFERENCES tags(id),
            PRIMARY KEY (post_id, tag_id)
        );

        -- Enable FTS5 full-text search on posts
        CREATE VIRTUAL TABLE posts_fts USING fts5(
            title, body, content=posts, content_rowid=id
        );

        -- Triggers to keep FTS in sync
        CREATE TRIGGER posts_ai AFTER INSERT ON posts BEGIN
            INSERT INTO posts_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
        END;
        CREATE TRIGGER posts_ad AFTER DELETE ON posts BEGIN
            INSERT INTO posts_fts(posts_fts, rowid, title, body) VALUES('delete', old.id, old.title, old.body);
        END;
        CREATE TRIGGER posts_au AFTER UPDATE ON posts BEGIN
            INSERT INTO posts_fts(posts_fts, rowid, title, body) VALUES('delete', old.id, old.title, old.body);
            INSERT INTO posts_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
        END;
    """)
    conn.commit()
    return conn


def seed_posts(conn):
    """Insert sample blog posts."""
    today = date.today()
    posts = [
        {
            "slug": "welcome-to-the-datasette-blog",
            "title": "Welcome to the Datasette Blog",
            "body": (
                "We are excited to launch the official Datasette blog! "
                "This blog is itself powered by Datasette and SQLite, serving as a "
                "living demonstration of what the tool can do.\n\n"
                "Datasette turns any SQLite database into an instantly explorable "
                "web interface with a JSON API. Every table, view, and SQL query "
                "gets its own URL. Add plugins for markdown rendering, full-text "
                "search, authentication, and more.\n\n"
                "## Why a blog on Datasette?\n\n"
                "Because a blog is just structured data: titles, bodies, dates, and tags. "
                "SQLite handles it beautifully, and Datasette gives us an API, faceted "
                "browsing, and full-text search for free."
            ),
            "published": str(today),
            "tags": "announcement,datasette",
        },
        {
            "slug": "sqlite-as-a-content-store",
            "title": "Why SQLite Makes a Great Content Store",
            "body": (
                "SQLite is the most deployed database in the world, and it turns out "
                "it's also a fantastic choice for content management.\n\n"
                "### Advantages\n\n"
                "- **Single file**: Your entire blog is one `.db` file you can copy, "
                "back up, or version-control.\n"
                "- **Fast reads**: Blog workloads are read-heavy. SQLite excels here.\n"
                "- **Full-text search**: FTS5 gives you production-grade search with "
                "no external service.\n"
                "- **JSON support**: `json_each()` lets you store and query structured "
                "metadata.\n\n"
                "### When NOT to use SQLite\n\n"
                "If you need concurrent writes from multiple processes or horizontal "
                "scaling across servers, reach for PostgreSQL. For a single-author or "
                "small-team blog, SQLite is more than enough."
            ),
            "published": str(today - timedelta(days=1)),
            "tags": "sqlite,architecture",
        },
        {
            "slug": "datasette-plugins-for-blogging",
            "title": "Essential Datasette Plugins for Blogging",
            "body": (
                "Datasette's plugin ecosystem makes it easy to add features to your blog.\n\n"
                "### Must-have plugins\n\n"
                "1. **datasette-render-markdown** - Renders markdown columns as HTML. "
                "Perfect for post bodies.\n"
                "2. **datasette-search-all** - Adds a site-wide search box across all tables.\n"
                "3. **datasette-cors** - Enables CORS headers so you can build a "
                "headless CMS with a JS frontend.\n"
                "4. **datasette-auth-tokens** - Protect draft posts with token-based auth.\n"
                "5. **datasette-atom** - Generate Atom feeds for your blog posts automatically.\n\n"
                "### Installing plugins\n\n"
                "```bash\n"
                "pip install datasette-render-markdown datasette-search-all\n"
                "```\n\n"
                "Plugins are discovered automatically — just install and restart Datasette."
            ),
            "published": str(today - timedelta(days=2)),
            "tags": "plugins,tutorial",
        },
        {
            "slug": "deploying-datasette-blog",
            "title": "Deploy Your Datasette Blog in One Command",
            "body": (
                "Datasette includes built-in deployment commands for major cloud platforms.\n\n"
                "### Fly.io\n\n"
                "```bash\n"
                "datasette publish fly blog.db --app my-blog \\\n"
                "  --metadata metadata.json \\\n"
                "  --install datasette-render-markdown\n"
                "```\n\n"
                "### Vercel\n\n"
                "```bash\n"
                "datasette publish vercel blog.db \\\n"
                "  --metadata metadata.json \\\n"
                "  --project my-blog\n"
                "```\n\n"
                "### Google Cloud Run\n\n"
                "```bash\n"
                "datasette publish cloudrun blog.db \\\n"
                "  --metadata metadata.json \\\n"
                "  --service my-blog\n"
                "```\n\n"
                "Each command packages your database, metadata, templates, and plugins "
                "into a container and deploys it."
            ),
            "published": str(today - timedelta(days=3)),
            "tags": "deployment,tutorial",
        },
        {
            "slug": "json-api-for-everything",
            "title": "Every Page is an API: Using Datasette as a Headless CMS",
            "body": (
                "One of Datasette's killer features is that every HTML page has a "
                "corresponding `.json` endpoint. Append `.json` to any URL and you "
                "get structured data back.\n\n"
                "### Example\n\n"
                "```\n"
                "GET /blog/posts.json?_sort_desc=published&draft=0\n"
                "```\n\n"
                "Returns:\n"
                "```json\n"
                '{"rows": [{"id": 1, "title": "...", "body": "...", ...}], ...}\n'
                "```\n\n"
                "This means you can use Datasette as a headless CMS — store your "
                "content in SQLite, serve it via Datasette's API, and render it with "
                "any frontend framework (Next.js, Astro, HTMX).\n\n"
                "Enable `datasette-cors` to allow cross-origin requests from your "
                "frontend domain."
            ),
            "published": str(today - timedelta(days=4)),
            "tags": "api,tutorial",
        },
    ]

    tags_set = set()
    for p in posts:
        for t in p["tags"].split(","):
            tags_set.add(t.strip())

    cur = conn.cursor()

    # Insert tags
    for tag in sorted(tags_set):
        cur.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
    conn.commit()

    # Get tag id map
    tag_map = {}
    for row in cur.execute("SELECT id, name FROM tags"):
        tag_map[row[1]] = row[0]

    # Insert posts and link tags
    for p in posts:
        cur.execute(
            "INSERT INTO posts (slug, title, body, published, tags) VALUES (?, ?, ?, ?, ?)",
            (p["slug"], p["title"], p["body"], p["published"], p["tags"]),
        )
        post_id = cur.lastrowid
        for t in p["tags"].split(","):
            t = t.strip()
            if t in tag_map:
                cur.execute(
                    "INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)",
                    (post_id, tag_map[t]),
                )

    conn.commit()
    print(f"  Seeded {len(posts)} posts and {len(tags_set)} tags")


def create_metadata():
    """Create Datasette metadata configuration."""
    metadata = {
        "title": "Datasette Blog",
        "description": "A blog powered by Datasette and SQLite",
        "license": "Apache-2.0",
        "databases": {
            "blog": {
                "tables": {
                    "posts": {
                        "sort_desc": "published",
                        "label_column": "title",
                        "facets": ["tags"],
                        "hidden": False,
                    },
                    "tags": {"label_column": "name"},
                    "post_tags": {"hidden": True},
                    "posts_fts": {"hidden": True},
                }
            }
        },
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  Created {METADATA_PATH}")


def create_templates():
    """Create custom Jinja2 templates for the blog."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    # Custom index page
    index_html = """\
{% extends "base.html" %}

{% block title %}Datasette Blog{% endblock %}

{% block content %}
<style>
  .blog-header { text-align: center; padding: 2rem 0; border-bottom: 2px solid #e0e0e0; margin-bottom: 2rem; }
  .blog-header h1 { font-size: 2.5rem; color: #1a1a2e; }
  .blog-header p { color: #666; font-size: 1.1rem; }
  .blog-nav { display: flex; gap: 1rem; justify-content: center; margin: 1rem 0; }
  .blog-nav a { padding: 0.5rem 1rem; background: #1a1a2e; color: white; border-radius: 4px; text-decoration: none; }
  .blog-nav a:hover { background: #16213e; }
  .blog-info { max-width: 700px; margin: 0 auto; line-height: 1.7; }
  .blog-info h2 { color: #1a1a2e; }
  .blog-info ul { padding-left: 1.5rem; }
</style>

<div class="blog-header">
  <h1>Datasette Blog</h1>
  <p>A fully functional blog powered by Datasette and SQLite</p>
</div>

<div class="blog-nav">
  <a href="/blog/posts?draft=0&_sort_desc=published">All Posts</a>
  <a href="/blog/tags">Tags</a>
  <a href="/blog/posts.json?_sort_desc=published&draft=0">JSON API</a>
</div>

<div class="blog-info">
  <h2>About this blog</h2>
  <p>This blog demonstrates using <strong>Datasette</strong> as a lightweight blogging engine.
     Every page has a JSON API. Full-text search is built in. Content lives in a single
     SQLite file.</p>

  <h2>Features</h2>
  <ul>
    <li>SQLite-backed content store (single portable file)</li>
    <li>Full-text search via FTS5</li>
    <li>Faceted browsing by tags</li>
    <li>JSON API on every endpoint</li>
    <li>Custom Jinja2 templates</li>
    <li>One-command deployment to Fly.io, Vercel, or Cloud Run</li>
  </ul>
</div>
{% endblock %}
"""

    with open(os.path.join(TEMPLATES_DIR, "index.html"), "w") as f:
        f.write(index_html)

    print(f"  Created {TEMPLATES_DIR}/index.html")


def create_plugin():
    """Create a custom plugin for markdown rendering fallback."""
    os.makedirs(PLUGINS_DIR, exist_ok=True)

    plugin_code = '''\
"""
Simple markdown-to-HTML plugin for Datasette.
Falls back to basic formatting if datasette-render-markdown is not installed.
"""
from datasette import hookimpl
import re


def simple_markdown(text):
    """Minimal markdown: headers, bold, code blocks, lists, paragraphs."""
    if not text:
        return text
    lines = text.split("\\n")
    html_lines = []
    in_code = False
    in_list = False

    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                html_lines.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            html_lines.append(line)
            continue

        # Headers
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
            continue
        if line.startswith("## "):
            html_lines.append(f"<h3>{line[3:]}</h3>")
            continue
        if line.startswith("# "):
            html_lines.append(f"<h2>{line[2:]}</h2>")
            continue

        # List items
        if line.strip().startswith("- ") or re.match(r"^\\d+\\. ", line.strip()):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item = re.sub(r"^[\\s]*[-\\d.]+\\s*", "", line)
            # Bold
            item = re.sub(r"\\*\\*(.+?)\\*\\*", r"<strong>\\1</strong>", item)
            # Inline code
            item = re.sub(r"`(.+?)`", r"<code>\\1</code>", item)
            html_lines.append(f"<li>{item}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False

        # Bold
        line = re.sub(r"\\*\\*(.+?)\\*\\*", r"<strong>\\1</strong>", line)
        # Inline code
        line = re.sub(r"`(.+?)`", r"<code>\\1</code>", line)

        if line.strip():
            html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_code:
        html_lines.append("</code></pre>")

    return "\\n".join(html_lines)


@hookimpl
def render_cell(value, column, table, database, datasette):
    if table == "posts" and column == "body" and isinstance(value, str):
        return simple_markdown(value)
'''

    with open(os.path.join(PLUGINS_DIR, "render_markdown.py"), "w") as f:
        f.write(plugin_code)
    print(f"  Created {PLUGINS_DIR}/render_markdown.py")


def verify_database():
    """Print database stats for verification."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    post_count = cur.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    tag_count = cur.execute("SELECT COUNT(*) FROM tags").fetchone()[0]
    fts_count = cur.execute("SELECT COUNT(*) FROM posts_fts").fetchone()[0]

    print(f"\n  Database verification:")
    print(f"    Posts: {post_count}")
    print(f"    Tags:  {tag_count}")
    print(f"    FTS entries: {fts_count}")

    print(f"\n  Recent posts:")
    for row in cur.execute(
        "SELECT slug, published, tags FROM posts ORDER BY published DESC"
    ):
        print(f"    [{row[1]}] {row[0]}  (tags: {row[2]})")

    # Test FTS
    results = cur.execute(
        "SELECT title FROM posts WHERE id IN (SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'sqlite')"
    ).fetchall()
    print(f"\n  FTS search for 'sqlite': {len(results)} result(s)")
    for r in results:
        print(f"    - {r[0]}")

    conn.close()


def main():
    print("=" * 60)
    print("  Datasette Blog Setup")
    print("=" * 60)

    print("\n[1/5] Creating database schema...")
    conn = create_database()

    print("[2/5] Seeding sample posts...")
    seed_posts(conn)
    conn.close()

    print("[3/5] Writing metadata config...")
    create_metadata()

    print("[4/5] Creating custom templates...")
    create_templates()

    print("[5/5] Creating markdown plugin...")
    create_plugin()

    verify_database()

    print("\n" + "=" * 60)
    print("  Setup complete!")
    print("=" * 60)
    print(f"\n  Files created:")
    print(f"    {DB_PATH}           - SQLite database with blog content")
    print(f"    {METADATA_PATH}   - Datasette configuration")
    print(f"    {TEMPLATES_DIR}/          - Custom Jinja2 templates")
    print(f"    {PLUGINS_DIR}/            - Custom Datasette plugins")
    print(f"\n  To launch the blog:")
    print(f"    datasette blog.db --metadata metadata.json \\")
    print(f"      --template-dir templates/ --plugins-dir plugins/")
    print(f"\n  Then open: http://127.0.0.1:8001")

    return 0


if __name__ == "__main__":
    sys.exit(main())
