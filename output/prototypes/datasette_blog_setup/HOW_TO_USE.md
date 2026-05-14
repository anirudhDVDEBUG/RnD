# How to Use — Datasette Blog Setup

## Install

```bash
# Python 3.9+ required
pip install datasette datasette-render-markdown datasette-search-all sqlite-utils
```

Or use the pinned versions:

```bash
pip install -r requirements.txt
```

## Quick Start (bash run.sh)

```bash
bash run.sh
```

This will:
1. Install dependencies
2. Create `blog.db` with schema, FTS5 indexes, and 5 sample posts
3. Query the database via CLI to prove everything works
4. Verify Datasette can load the database

No API keys, no external services, no Docker required.

## Launch the Live Blog Server

After running `run.sh`:

```bash
datasette blog.db \
  --metadata metadata.json \
  --template-dir templates/ \
  --plugins-dir plugins/
```

Open http://127.0.0.1:8001 in your browser. You'll see:

- **Home page** with styled blog header and navigation
- **Posts table** at `/blog/posts` with faceted tag filtering
- **JSON API** at `/blog/posts.json?_sort_desc=published&draft=0`
- **Full-text search** at `/blog/posts?_search=sqlite`

## Using as a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/datasette_blog_setup
cp SKILL.md ~/.claude/skills/datasette_blog_setup/SKILL.md
```

**Trigger phrases** that activate this skill:

- "Set up a blog with Datasette"
- "Create a data-powered blog using SQLite"
- "Configure Datasette to serve blog content"
- "Deploy a Datasette-based website with blog posts"
- "Build a lightweight SQLite blog"

## First 60 Seconds

```
$ bash run.sh

[1/4] Installing dependencies...
  Done.

[2/4] Setting up blog database, templates, and plugins...
  Seeded 5 posts and 7 tags
  Created metadata.json
  Created templates/index.html
  Created plugins/render_markdown.py

  Database verification:
    Posts: 5
    Tags:  7
    FTS entries: 5

[3/4] Querying the blog via sqlite-utils CLI...

--- All published posts (newest first) ---
  slug                              | title                                      | published
  welcome-to-the-datasette-blog     | Welcome to the Datasette Blog              | 2026-05-14
  sqlite-as-a-content-store         | Why SQLite Makes a Great Content Store      | 2026-05-13
  ...

--- Full-text search for 'plugin' ---
  title                                   | published
  Essential Datasette Plugins for Blogging | 2026-05-12

--- JSON API preview (first post) ---
[{"id": 1, "slug": "welcome-to-the-datasette-blog", ...}]

[4/4] Verifying Datasette can load the database...
  Datasette inspection: OK

  To launch the live blog server, run:
    datasette blog.db --metadata metadata.json \
      --template-dir templates/ --plugins-dir plugins/
```

## Adding Your Own Posts

Use `sqlite-utils` to insert new posts:

```bash
sqlite-utils insert blog.db posts - --json <<'JSON'
[{
  "slug": "my-first-post",
  "title": "My First Post",
  "body": "Hello world! This is **markdown** content.",
  "published": "2026-05-14",
  "draft": 0,
  "tags": "personal"
}]
JSON
```

## Deploying

```bash
# Fly.io
datasette publish fly blog.db --metadata metadata.json --app my-blog --install datasette-render-markdown

# Vercel
datasette publish vercel blog.db --metadata metadata.json --project my-blog

# Cloud Run
datasette publish cloudrun blog.db --metadata metadata.json --service my-blog
```
