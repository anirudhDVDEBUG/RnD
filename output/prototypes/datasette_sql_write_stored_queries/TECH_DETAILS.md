# Technical Details

## What It Does

Datasette 1.0a31 introduces two related features that transform Datasette from a read-only data explorer into a lightweight CRUD application platform:

1. **SQL Write Queries** — Authenticated users with appropriate permissions can execute INSERT, UPDATE, DELETE, and other write statements directly through the Datasette web UI or JSON API. The permission system is granular: `insert-row`, `update-row`, `delete-row`, `create-table`, and `execute-sql` can each be granted independently per database or table.

2. **Stored Queries** (successor to "canned queries") — Users can save parameterized SQL queries with `:param` syntax. Datasette auto-generates an HTML form for each parameter, making it trivial to build data-entry interfaces without writing any frontend code. Stored queries can be private or shared across the instance.

## Architecture

```
┌─────────────────────────────────────────┐
│  Browser / API Client                    │
└──────────────┬──────────────────────────┘
               │ HTTP (JSON or HTML)
┌──────────────▼──────────────────────────┐
│  Datasette (ASGI app on uvicorn)         │
│  ├─ Permission checks (actor + db)      │
│  ├─ SQL parser (read vs write routing)  │
│  ├─ Stored query registry (SQLite meta) │
│  └─ Write execution (WAL mode)          │
└──────────────┬──────────────────────────┘
               │ sqlite3
┌──────────────▼──────────────────────────┐
│  SQLite database file (WAL mode)         │
└─────────────────────────────────────────┘
```

**Key files in this demo:**
- `demo_setup.py` — Creates the SQLite schema and seed data
- `demo_queries.py` — Exercises write queries and stored query creation via the API
- `datasette.yml` — Permission configuration
- `run.sh` — Orchestrates the full demo

**Dependencies:** `datasette>=1.0a31`, `httpx` (for API calls in demo), `sqlite-utils` (for setup)

## Limitations

- Write queries require WAL mode for concurrent access; heavy write loads may still hit SQLite's single-writer lock.
- No built-in migration system — schema changes must be managed externally.
- Stored queries are instance-scoped, not portable between Datasette deployments without export/import.
- The permission model relies on Datasette's actor system; without an auth plugin, access defaults to anonymous (root actor).
- No transaction grouping across multiple write statements in the UI (each query executes independently).

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent Factories** | Agents can use Datasette as a structured memory/state store — write observations, read context, all via HTTP API with zero ORM overhead. |
| **Lead-Gen / CRM** | Stored queries with parameter forms = instant data-entry UIs for sales teams, no app code required. |
| **Marketing / Content** | Store campaign metadata, A/B test results, or content calendars in SQLite; query and update via Datasette. |
| **Ad Creatives** | Track creative variants, performance metrics, and approval status with parameterized INSERT/UPDATE stored queries. |
| **Voice AI** | Voice agents can POST structured data (call logs, transcripts, intents) directly to Datasette's write API. |

The core insight: Datasette + write queries + stored queries = a zero-code CRUD backend that any AI agent can talk to over HTTP, with built-in permission controls and a human-usable UI for oversight.
