# Technical Details — Datasette Blog Setup

## What It Does

Datasette is an open-source Python tool (created by Simon Willison) that takes any SQLite database and instantly serves it as an explorable web application with a full JSON API. This prototype uses Datasette as a lightweight blogging engine: blog posts, tags, and metadata live in a single `.db` file, and Datasette provides the web UI, search, faceted browsing, and API layer with zero application code.

The key insight from the [official Datasette blog launch](https://simonwillison.net/2026/May/13/welcome-to-the-datasette-blog/#atom-everything) is that a blog is just structured data — and Datasette already knows how to serve structured data beautifully.

## Architecture

```
blog.db (SQLite)
  ├── posts          — id, slug, title, body (markdown), published, tags, draft
  ├── tags           — id, name
  ├── post_tags      — many-to-many junction table
  └── posts_fts      — FTS5 virtual table for full-text search

metadata.json        — Datasette config: sort order, facets, label columns, hidden tables
templates/index.html — Custom Jinja2 homepage template
plugins/render_markdown.py — Datasette plugin hook that renders markdown body cells as HTML
```

### Data Flow

1. `setup_blog.py` creates the SQLite schema with FTS5 triggers for automatic search index updates
2. Sample posts are inserted with tags linked via junction table
3. Datasette reads `blog.db` + `metadata.json` at startup
4. Every table/row gets an HTML page AND a `.json` endpoint automatically
5. The custom template overrides the homepage; the plugin renders markdown in post body cells
6. FTS5 powers the search — queries go through SQLite directly, no external search service

### Key Dependencies

| Package | Role |
|---|---|
| `datasette` | Core web server, API, template engine |
| `datasette-render-markdown` | Renders markdown columns as HTML (optional — the included plugin provides a fallback) |
| `datasette-search-all` | Adds site-wide search UI across all tables |
| `sqlite-utils` | CLI tool for querying/inserting data without writing Python |

### No External Services Required

- No database server (SQLite is embedded)
- No search engine (FTS5 is built into SQLite)
- No API framework (Datasette generates the API automatically)
- No CMS admin panel (use `sqlite-utils` CLI or any SQLite editor)

## Limitations

- **Single-writer**: SQLite doesn't support concurrent writes from multiple processes. Fine for a single-author blog, not for a high-traffic CMS with multiple editors.
- **No built-in auth editing UI**: There's no admin dashboard for writing posts in a browser. You manage content via CLI (`sqlite-utils`), a SQLite GUI, or a custom write API plugin.
- **Static-ish**: Datasette serves content dynamically but doesn't have built-in caching, CDN integration, or static site generation. For high traffic, put a CDN (Cloudflare, Fastly) in front.
- **Template customization requires Jinja2 knowledge**: The default UI is functional but generic. Full design control requires writing Jinja2 templates.
- **Plugin ecosystem is niche**: Compared to WordPress or Ghost, fewer plugins exist. You may need to write custom Datasette plugins for advanced features.

## Why This Matters for Claude-Driven Products

**Content publishing pipeline**: Datasette's JSON API makes it trivial to build an AI content pipeline — have Claude generate blog posts, insert them via `sqlite-utils`, and they're instantly live with search and API access. No CMS integration headaches.

**Lead-gen and marketing sites**: A Datasette blog can serve as a lightweight, data-rich content hub. Combine it with programmatic SEO: generate hundreds of long-tail posts from structured data (product comparisons, market research, FAQ pages) and serve them through Datasette's faceted browsing.

**Agent factories**: Datasette's automatic JSON API means any agent can read and write blog content without a custom backend. An agent that monitors trends could auto-publish daily summaries, and a reader-facing agent could search the blog via the API to answer questions.

**Rapid prototyping**: For anyone building Claude-powered products, Datasette eliminates the "I need a backend" blocker. Drop data into SQLite, point Datasette at it, and you have a browsable web UI + API in seconds. This is especially useful for demos, MVPs, and internal tools.

## References

- [Welcome to the Datasette blog](https://simonwillison.net/2026/May/13/welcome-to-the-datasette-blog/#atom-everything)
- [Datasette documentation](https://docs.datasette.io/)
- [Datasette GitHub](https://github.com/simonw/datasette)
- [sqlite-utils documentation](https://sqlite-utils.datasette.io/)
