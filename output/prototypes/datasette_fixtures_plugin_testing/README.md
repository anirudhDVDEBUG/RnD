# datasette-fixtures: Instant Test Data for Datasette Plugins

**TL;DR:** `datasette-fixtures` is a new plugin that gives you Datasette's entire internal fixture database in one command — no manual SQL, no seed scripts. Install it, and your plugin tests get dozens of realistic tables (including `roadside_attractions`) for free.

**Headline result:** One command, full fixture database:

```
$ uvx --prerelease=allow --with datasette-fixtures datasette --get /fixtures/roadside_attractions.json
[{"pk":1,"name":"The Mystery Spot","address":"465 Mystery Spot Road..."},...]
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install steps, skill setup, and a "first 60 seconds" walkthrough.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, how `populate_fixture_database` works, limitations.
- **[run.sh](run.sh)** — Run `bash run.sh` for an end-to-end demo (no API keys needed).

## What's in the demo

- `demo_fixtures.py` — Creates a fixture database locally, lists tables, and queries sample data.
- `test_plugin_example.py` — Shows how a real Datasette plugin test would use fixtures.
- `run.sh` — Orchestrates the demo end-to-end.

## Source

- [datasette-fixtures 0.1a0 announcement](https://simonwillison.net/2026/May/24/datasette-fixtures/#atom-everything)
