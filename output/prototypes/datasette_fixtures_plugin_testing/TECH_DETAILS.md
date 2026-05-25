# Technical Details: datasette-fixtures

## What it does

`datasette-fixtures` is a Datasette plugin (v0.1a0, pre-release) that bundles Datasette's internal fixture database as a first-class installable package. When installed alongside Datasette, it automatically registers a `fixtures` database containing dozens of tables — the same tables Datasette's own test suite uses. This eliminates the need for plugin authors to manually create test data or copy fixture-generation code from Datasette's internals.

The core mechanism is `populate_fixture_database(conn)`, a function exposed by Datasette >= 1.0a30 in `datasette.fixtures`. It takes a SQLite connection and creates a standardized set of tables (`roadside_attractions`, `facetable`, `searchable`, etc.) with realistic sample data. The plugin simply calls this function during Datasette's startup hook, making the fixtures available at `/fixtures`.

## Architecture

### Key components

- **`datasette.fixtures.populate_fixture_database(conn)`** — Datasette-side function (added in 1.0a30) that creates all fixture tables in a given SQLite connection. This is the public API plugin authors should use.
- **`datasette-fixtures` plugin** — A thin wrapper that calls `populate_fixture_database` during Datasette's `startup` hook, registering an in-memory (or on-disk) `fixtures` database.
- **Fixture tables** — Include `roadside_attractions`, `facetable`, `searchable`, `binary_data`, `compound_primary_key`, and many others covering edge cases like FTS, JSON columns, and compound keys.

### Data flow

```
datasette startup
  -> datasette-fixtures plugin hook
    -> sqlite3.connect(":memory:") or temp file
      -> populate_fixture_database(conn)
        -> CREATE TABLE + INSERT for each fixture
    -> register "fixtures" database with Datasette
  -> /fixtures/* routes become available
```

### Dependencies

- **Runtime:** `datasette >= 1.0a30` (pre-release alpha)
- **Python:** 3.9+
- **No external API keys or services required**

## Limitations

- **Pre-release only:** Both `datasette` 1.x and `datasette-fixtures` 0.1a0 are alpha. The `populate_fixture_database` API may change before stable release.
- **Read-only test data:** The fixture data is static and predefined. You cannot customize which tables are created or inject your own rows through this API — it's all-or-nothing.
- **Not a general seed tool:** This is specifically for testing Datasette plugins against Datasette's own fixture schema. It's not a general-purpose database seeder.
- **In-memory by default:** When used via the plugin, the database is recreated on each startup. For persistent fixtures, call `populate_fixture_database` against an on-disk SQLite file.

## Why it matters for Claude-driven products

- **Agent factories / tool builders:** If you're building MCP servers or Claude tools that expose Datasette databases, `datasette-fixtures` gives you instant realistic data for integration testing without crafting SQL by hand.
- **Lead-gen and marketing analytics:** Datasette is increasingly used as a lightweight analytics backend. Having standardized fixture data means you can prototype dashboards and Claude-powered query agents against a known schema before connecting real data.
- **Rapid prototyping:** Combined with `uvx`, you can spin up a fully-populated Datasette instance in under 5 seconds — useful for demoing Claude skills that read from structured databases.
- **Plugin ecosystem growth:** Lower barrier to plugin testing = more plugins = richer Datasette ecosystem, which benefits anyone using Datasette as an AI-accessible data layer.

## References

- [datasette-fixtures 0.1a0 announcement](https://simonwillison.net/2026/May/24/datasette-fixtures/#atom-everything)
- [GitHub releases](https://github.com/datasette/datasette-fixtures/releases/tag/0.1a0)
- [Datasette plugin testing docs](https://docs.datasette.io/en/latest/testing_plugins.html#datasette-fixtures-populate-fixture-database)
- [Datasette 1.0a30 changelog](https://docs.datasette.io/en/latest/changelog.html#a30-2026-05-24)
