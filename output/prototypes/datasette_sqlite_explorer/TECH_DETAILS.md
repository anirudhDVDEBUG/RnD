# Technical Details: Datasette SQLite Explorer

## What it does

Datasette is a Python tool that wraps any SQLite database file with a read-only web interface and a JSON API. You point it at one or more `.db` files and it immediately serves a browsable UI with table views, faceted filtering, and a SQL query editor. Every page also has a `.json` endpoint, so the same instance doubles as a REST API. Version 1.0a29 (released May 12, 2026) is the latest alpha in the 1.0 series, fixing edge cases around empty tables, mobile Safari column actions, and a segfault race condition in concurrent test teardown.

The core value proposition: go from "I have a SQLite file" to "I have a queryable web API" in under 10 seconds with no schema configuration, no ORM, no server setup.

## Architecture

**Runtime:** Python 3.9+ with ASGI (built on Starlette/uvicorn).

**Key components:**
- `datasette.app.Datasette` -- Main application class. Wraps SQLite connections, manages plugin hooks, handles routing.
- `datasette.views` -- View layer: table browser, row detail, SQL query executor, database-level views.
- `datasette.utils.TokenRestrictions` -- New in 1.0 alpha series. Creates `"_r"` restriction dictionaries for scoped API tokens, allowing fine-grained access control.
- Plugin system -- Hooks for `extra_template_vars`, `prepare_connection`, `register_routes`, etc. Over 100 community plugins.

**Data flow:**
1. Datasette opens SQLite files in read-only mode (`?mode=ro`)
2. HTTP request hits ASGI server
3. Router dispatches to appropriate view (table, row, database, or custom SQL)
4. View executes SQL against the SQLite connection pool
5. Response rendered as HTML (Jinja2 templates) or JSON based on `Accept` header / `.json` extension

**Dependencies:** `starlette`, `uvicorn`, `jinja2`, `pint`, `sqlite-utils` (optional). No database server required -- just the `.db` file on disk.

## Limitations

- **Read-only by default.** Write operations require the `datasette-write` plugin or custom ASGI middleware. Not a replacement for a full CRUD backend.
- **SQLite only.** Does not support PostgreSQL, MySQL, or other databases. If your data isn't in SQLite, you need to convert it first (e.g., with `sqlite-utils`).
- **Single-node.** No built-in clustering or replication. For high-traffic use, deploy behind a CDN or use `datasette publish` to platforms with auto-scaling.
- **Alpha API surface.** The 1.0 alpha series may still change internal APIs between releases. Plugin authors should pin versions.
- **No built-in auth UI.** Token-based auth is supported but there's no login page -- tokens must be generated and distributed separately.

## Why it matters for Claude-driven products

**Agent factories / tool-use pipelines:**
Datasette's JSON API is a natural fit for LLM tool-use. An agent can query structured data via HTTP without needing database drivers or connection management. Point Claude at `datasette serve` and it can answer questions about any SQLite dataset through the API.

**Lead-gen and marketing analytics:**
Teams often dump CRM exports, ad performance data, or scrape results into SQLite. Datasette lets non-technical stakeholders explore that data in a browser, while engineers can use the same instance as an API backend for dashboards or reports.

**Rapid prototyping:**
When building a Claude-powered app, you often need a quick data layer. Instead of setting up Postgres + an ORM + migrations, `datasette serve sample.db` gives you a queryable API in one command. Good for hackathons, demos, and internal tools.

**Data publishing:**
`datasette publish` deploys a read-only data API to Vercel/Fly/Cloud Run. Useful for sharing research datasets, public records, or curated collections that Claude agents can query programmatically.

## 1.0a29 specific changes

- Table headers and column action buttons now display on empty tables (#2701)
- Fixed column actions dialog on Mobile Safari (#2708)
- Fixed segfault race condition between concurrent `Datasette.close()` calls in tests (#2709)

## References

- [datasette 1.0a29 release notes](https://simonwillison.net/2026/May/12/datasette/#atom-everything)
- [GitHub: simonw/datasette](https://github.com/simonw/datasette)
- [Documentation](https://docs.datasette.io/en/latest/)
