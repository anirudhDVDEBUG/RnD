# Technical Details — Honeydew Data Modeling Plugin

## What it does

The Honeydew coding-agents plugin exposes a **semantic data layer** to AI coding agents via the Model Context Protocol (MCP). Instead of agents guessing table names, column types, and join paths, they query Honeydew's centrally managed catalogue of **entities**, **attributes**, **relationships**, and **metric definitions**. When the agent needs SQL, the plugin generates it from these shared definitions — guaranteeing that business logic (e.g. "net revenue = total - discounts") is applied consistently.

The plugin acts as a bridge: the AI agent sends high-level semantic requests ("give me total revenue by region"), and the Honeydew backend resolves them into warehouse-specific SQL that respects the organisation's canonical data model.

## Architecture

```
┌──────────────┐       MCP / stdio        ┌──────────────────┐
│  Claude Code │  ◄──────────────────────► │  Honeydew MCP    │
│  / Cursor    │   tool calls & results    │  Server (Python) │
└──────────────┘                           └────────┬─────────┘
                                                    │ REST API
                                                    ▼
                                           ┌──────────────────┐
                                           │  Honeydew Cloud  │
                                           │  Semantic Layer   │
                                           │  (entities,       │
                                           │   metrics, SQL    │
                                           │   generation)     │
                                           └────────┬─────────┘
                                                    │
                                                    ▼
                                           ┌──────────────────┐
                                           │  Data Warehouse  │
                                           │  (Snowflake /    │
                                           │   BigQuery /     │
                                           │   Databricks)    │
                                           └──────────────────┘
```

### Key files (in the source repo)

| File / Module | Role |
|---------------|------|
| `honeydew_mcp_server.py` | MCP server entry-point — registers tools, handles stdio transport |
| `honeydew_client.py` | REST client wrapping the Honeydew API (entities, metrics, SQL gen) |
| `tools/` | Individual MCP tool definitions (list_entities, describe_entity, generate_sql, etc.) |
| `requirements.txt` | Python deps: `honeydew-ai`, `mcp`, `httpx` |

### Key files (in this demo)

| File | Role |
|------|------|
| `honeydew_mock.py` | Mock semantic-layer client with synthetic e-commerce catalogue |
| `demo.py` | End-to-end walkthrough: explore entities, browse metrics, generate SQL |
| `run.sh` | One-command demo runner |

## Dependencies

- **honeydew-ai** — official Python SDK for the Honeydew platform
- **mcp** — Model Context Protocol SDK for exposing tools to AI agents
- **httpx** — async HTTP client used under the hood

The demo in this repo uses zero external dependencies (stdlib only).

## MCP tools exposed

| Tool | Description |
|------|-------------|
| `list_entities` | Return all entities defined in the workspace |
| `describe_entity` | Show attributes, types, and relationships for a given entity |
| `list_metrics` | Return all pre-defined business metrics |
| `get_metric` | Get the expression, description, and filters for a metric |
| `generate_sql` | Turn metric names + dimensions + filters into warehouse SQL |

## Limitations

- **Read-only** — the plugin queries the semantic layer but does not create or modify entities/metrics. Model authoring is done in the Honeydew UI.
- **No query execution** — SQL is generated but not executed. You still need warehouse credentials and a query runner.
- **Honeydew account required** — the real plugin needs an active Honeydew workspace and API key. There is no free tier publicly documented.
- **No row-level security passthrough** — the generated SQL does not embed user-level access controls; those must be enforced at the warehouse layer.
- **Latency** — each tool call hits the Honeydew REST API; cold starts or large models may add 1-2 seconds per call.

## Why this matters for product builders

| Use case | How Honeydew helps |
|----------|--------------------|
| **Agent factories** | Agents that build dashboards or data pipelines can pull metric definitions from a single source of truth instead of hard-coding SQL per client. |
| **Lead-gen / marketing analytics** | Ad-spend, conversion, and funnel metrics are defined once in Honeydew and queried consistently across all agents and notebooks. |
| **Ad creatives / reporting** | Automatically generate performance reports backed by canonical metrics — no risk of "which revenue number is right?" debates. |
| **Voice AI** | A voice agent can answer "What was last month's revenue?" by calling `generate_sql`, executing the result, and reading back the number — all grounded in the official metric definition. |
| **Claude-driven products** | Any Claude-powered app that touches analytics data benefits from a semantic layer: fewer hallucinated column names, consistent business logic, and warehouse-agnostic SQL. |
