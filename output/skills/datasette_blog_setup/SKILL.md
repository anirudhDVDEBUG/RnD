---
name: datasette_blog_setup
description: |
  Set up and manage a blog powered by Datasette, the open-source data exploration tool.
  TRIGGER: datasette blog, data-powered blog, datasette content publishing, sqlite blog engine, datasette site setup
---

# Datasette Blog Setup

Create and manage a blog using Datasette — the open-source tool for exploring and publishing data stored in SQLite databases.

## When to use

- "Set up a blog with Datasette"
- "Create a data-powered blog using SQLite and Datasette"
- "Configure Datasette to serve blog content"
- "Deploy a Datasette-based website with blog posts"
- "Build a lightweight blog backed by a SQLite database"

## How to use

### 1. Install Datasette

```bash
pip install datasette
```

### 2. Create the blog database

Create a SQLite database to store blog posts:

```bash
sqlite3 blog.db <<'SQL'
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    published DATE NOT NULL DEFAULT (date('now')),
    updated DATE,
    draft INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_posts_published ON posts(published);
CREATE INDEX idx_posts_slug ON posts(slug);
SQL
```

### 3. Configure Datasette with templates

Create a `metadata.yml` for your blog:

```yaml
title: My Datasette Blog
description: A blog powered by Datasette and SQLite
databases:
  blog:
    tables:
      posts:
        sort_desc: published
        label_column: title
```

### 4. Add custom templates

Datasette supports custom templates. Create a `templates/` directory with Jinja2 templates to render blog posts with full HTML/CSS styling.

### 5. Install useful plugins

```bash
# Markdown rendering for post bodies
pip install datasette-render-markdown

# Full-text search across posts
pip install datasette-search-all

# JSON API for headless/static generation
pip install datasette-cors
```

### 6. Run locally

```bash
datasette blog.db --metadata metadata.yml --template-dir templates/
```

### 7. Deploy

Datasette supports multiple deployment targets:

```bash
# Deploy to Vercel
datasette publish vercel blog.db --metadata metadata.yml --install datasette-render-markdown

# Deploy to Fly.io
datasette publish fly blog.db --metadata metadata.yml --app my-blog

# Deploy to Google Cloud Run
datasette publish cloudrun blog.db --metadata metadata.yml --service my-blog
```

## Key features

- **SQLite-backed**: All content lives in a single portable `.db` file
- **API-first**: Every page automatically has a JSON API endpoint
- **Plugin ecosystem**: Extend with markdown rendering, full-text search, authentication, and more
- **Custom templates**: Full Jinja2 templating for complete design control
- **One-command deploy**: Publish to Vercel, Fly.io, or Cloud Run with a single command
- **Faceted browsing**: Built-in faceting lets readers filter posts by tags, dates, or categories

## References

- Source: [Welcome to the Datasette blog](https://datasette.io/blog/2026/new-blog/) — via [Simon Willison's Weblog](https://simonwillison.net/2026/May/13/welcome-to-the-datasette-blog/#atom-everything)
- [Datasette documentation](https://docs.datasette.io/)
- [Datasette GitHub repository](https://github.com/simonw/datasette)
