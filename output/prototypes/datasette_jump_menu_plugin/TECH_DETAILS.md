# Technical Details

## What it does

The `jump_items_sql()` plugin hook (new in Datasette 1.0a30) lets plugins register SQL queries whose results appear in Datasette's "Jump to..." overlay menu. When a user presses `/`, Datasette runs all registered queries with the typed search term as a `:q` parameter (wrapped in `%...%` for LIKE matching) and merges results into a single filterable list. Each result must provide `label` and `url` columns; an optional `description` column adds context below the label.

This demo plugin (`datasette-jump-bookmarks`) stores bookmarks in a SQLite table and exposes them through the jump menu, demonstrating the full hook lifecycle.

## Architecture

```
datasette-jump-bookmarks/
  pyproject.toml           -- entry-point registration
  datasette_jump_bookmarks.py  -- hook implementation (~20 lines)

setup_demo.py              -- creates sample.db with bookmarks table
run.sh                     -- end-to-end demo runner
```

**Data flow:**
1. Datasette discovers the plugin via `[project.entry-points.datasette]` in pyproject.toml.
2. On jump menu open, Datasette calls `jump_items_sql(datasette, actor, request)` on every plugin.
3. Plugin returns `[(sql, database_name, params)]` tuples.
4. Datasette executes each SQL with `:q` bound to the search term, collects rows, and renders them in the overlay.

**Dependencies:** datasette >= 1.0a30, sqlite-utils (for demo DB creation).

## Limitations

- Requires Datasette 1.0a30+ (alpha -- API may change before 1.0 stable).
- Jump menu queries run on every keystroke; complex queries or large tables without indexes will cause lag.
- No support for async/streaming results -- all items load synchronously.
- The `:q` parameter is always a `%term%` LIKE pattern; plugins cannot customize matching logic.
- No pagination -- all matching rows are returned (keep result sets small or add `LIMIT`).

## Why it matters for Claude-driven products

- **Agent factories:** Agents that spin up Datasette instances can auto-register navigation shortcuts for generated dashboards, making exploration frictionless.
- **Lead-gen / marketing:** A CRM-backed Datasette could expose contacts, campaigns, or deals via the jump menu for instant lookup by sales teams.
- **Ad creatives:** Creative asset databases become instantly searchable -- jump to any asset by name without leaving the analytics view.
- **Voice AI:** Voice-driven Datasette interfaces could map spoken queries to jump menu items for hands-free data navigation.
