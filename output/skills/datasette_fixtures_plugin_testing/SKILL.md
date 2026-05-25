---
name: datasette_fixtures_plugin_testing
description: |
  Set up and use datasette-fixtures for plugin testing with Datasette's built-in fixture database.
  TRIGGER: datasette fixtures, datasette plugin testing, datasette test suite, populate_fixture_database, datasette-fixtures
---

# Datasette Fixtures — Plugin Testing Skill

Use the `datasette-fixtures` plugin to quickly spin up Datasette's own fixture database for plugin test suites and local exploration.

## When to use

- "Set up fixture data for my Datasette plugin tests"
- "Run Datasette with the fixtures database locally"
- "How do I use populate_fixture_database for plugin testing?"
- "Try out datasette-fixtures without installing Datasette"
- "I need sample Datasette tables for development"

## How to use

### 1. Quick trial with `uvx` (no install needed)

Run Datasette with the fixtures database in one command:

```bash
uvx --prerelease=allow \
  --with datasette-fixtures datasette \
  --get /fixtures/roadside_attractions.json
```

This outputs JSON from the built-in `roadside_attractions` fixture table.

### 2. Install as a dependency for plugin tests

Add `datasette-fixtures` to your plugin's test dependencies:

```
# pyproject.toml
[project.optional-dependencies]
test = ["datasette-fixtures", "pytest", "pytest-asyncio"]
```

Then install:

```bash
pip install -e ".[test]"
```

### 3. Use `populate_fixture_database` in tests

Datasette 1.0a30+ exposes a helper to create fixture tables programmatically:

```python
from datasette.fixtures import populate_fixture_database
import sqlite3

def create_fixture_db(path):
    conn = sqlite3.connect(path)
    populate_fixture_database(conn)
    conn.close()
```

This creates the same tables used by Datasette's own test suite (e.g., `roadside_attractions`, and many others), giving your plugin tests realistic data to work with.

### 4. Run Datasette with fixtures interactively

Start a local Datasette server with the fixtures database loaded:

```bash
uvx --prerelease=allow --with datasette-fixtures datasette
```

Then browse to `http://localhost:8001/fixtures` to explore the fixture tables.

## Key details

- **Requires:** Datasette >= 1.0a30
- **Plugin:** `datasette-fixtures` (currently at 0.1a0, pre-release)
- **Fixture tables include:** `roadside_attractions` and the full set of tables from Datasette's internal test suite
- The `--prerelease=allow` flag is needed because both Datasette 1.x and datasette-fixtures are currently alpha releases

## References

- [datasette-fixtures 0.1a0 announcement](https://simonwillison.net/2026/May/24/datasette-fixtures/#atom-everything)
- [datasette-fixtures GitHub releases](https://github.com/datasette/datasette-fixtures/releases/tag/0.1a0)
- [Datasette plugin testing docs — populate_fixture_database](https://docs.datasette.io/en/latest/testing_plugins.html#datasette-fixtures-populate-fixture-database)
- [Datasette 1.0a30 changelog](https://docs.datasette.io/en/latest/changelog.html#a30-2026-05-24)
