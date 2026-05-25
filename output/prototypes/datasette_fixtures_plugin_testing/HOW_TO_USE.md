# How to Use datasette-fixtures

## Option A: Quick trial with `uvx` (no install)

```bash
uvx --prerelease=allow --with datasette-fixtures datasette --get /fixtures/roadside_attractions.json
```

This runs Datasette with the fixtures database and returns JSON — nothing to install.

To launch the full web UI:

```bash
uvx --prerelease=allow --with datasette-fixtures datasette
# Browse http://localhost:8001/fixtures
```

## Option B: Install as a dependency

```bash
pip install datasette-fixtures
# or add to pyproject.toml:
# [project.optional-dependencies]
# test = ["datasette-fixtures", "pytest", "pytest-asyncio"]
```

Requires Datasette >= 1.0a30 (pre-release). Both packages need `--pre` or `--prerelease=allow`.

```bash
pip install --pre datasette datasette-fixtures
```

## Claude Code Skill Setup

This is a **Claude Code Skill**. To install it:

1. Copy the `SKILL.md` file into your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/datasette_fixtures_plugin_testing
   cp SKILL.md ~/.claude/skills/datasette_fixtures_plugin_testing/SKILL.md
   ```

2. **Trigger phrases** that activate the skill:
   - "Set up fixture data for my Datasette plugin tests"
   - "Run Datasette with the fixtures database locally"
   - "How do I use populate_fixture_database for plugin testing?"
   - "datasette fixtures"
   - "datasette plugin testing"
   - "datasette test suite"

Once installed, Claude Code will automatically use this skill when you mention Datasette fixtures or plugin testing.

## First 60 Seconds

### 1. Clone and run the demo

```bash
git clone <this-repo>
cd datasette_fixtures_plugin_testing
pip install -r requirements.txt
bash run.sh
```

### 2. What you'll see

```
=== datasette-fixtures Demo ===

--- Creating fixture database ---
Created fixture database: demo_fixtures.db

--- Tables in fixture database ---
  1. roadside_attractions
  2. facetable
  3. searchable
  ... (dozens more)

--- Sample data from roadside_attractions ---
  Row 1: The Mystery Spot | 465 Mystery Spot Road, Santa Cruz, CA 95065
  Row 2: Winchester Mystery House | 525 S Winchester Blvd, San Jose, CA 95128
  ...

--- Running plugin test example ---
test_fixture_tables_exist ... PASSED
test_roadside_attractions_has_data ... PASSED
test_query_fixture_data ... PASSED

All tests passed!
```

### 3. Use in your own plugin tests

```python
from datasette.fixtures import populate_fixture_database
import sqlite3

def create_fixture_db(path="test_fixtures.db"):
    conn = sqlite3.connect(path)
    populate_fixture_database(conn)
    conn.close()
    return path
```

That's it — your plugin tests now have the same tables Datasette's own CI uses.
