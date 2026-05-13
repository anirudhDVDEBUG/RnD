# Datasette SQLite Explorer

**Instantly turn any SQLite database into a browsable web UI and JSON API with zero configuration.** Datasette 1.0a29 gives you table exploration, full SQL queries, and scoped API tokens out of the box.

## Headline result

```
GET /demo/ai_tools.json?_sort_desc=stars&_size=3

[
  {"id": 4, "name": "Ollama",    "category": "local-inference", "stars": 112000},
  {"id": 8, "name": "Dify",      "category": "platform",       "stars": 52000},
  {"id": 9, "name": "Open WebUI", "category": "local-inference", "stars": 67000}
]
```

One command (`datasette serve demo.db`) and you have a full REST API.

## Quick start

```bash
bash run.sh
```

This creates a sample database, launches Datasette, and runs API queries to show it working.

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) -- Install, configure, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) -- Architecture, limitations, relevance
