---
name: datasette_agent_data_explorer
description: |
  Use datasette-agent to explore, query, and analyze data in Datasette instances via an AI-powered conversational interface.
  TRIGGER when: user wants to explore a Datasette database, run SQL queries conversationally, analyze data in SQLite databases via Datasette, or set up datasette-agent.
  DO NOT TRIGGER when: user is working with raw SQLite without Datasette, or using unrelated database tools.
---

# Datasette Agent Data Explorer

Use `datasette-agent` to interact with Datasette instances through an AI-powered conversational interface that can execute SQL queries and display results.

## When to use

- "Help me explore this Datasette database"
- "Set up datasette-agent for my SQLite data"
- "I want to query my Datasette instance conversationally"
- "Analyze the data in my Datasette tables using AI"
- "Install and configure datasette-agent"

## How to use

### 1. Install datasette-agent

```bash
pip install datasette-agent
```

Requires an existing Datasette instance. Install Datasette if needed:

```bash
pip install datasette
```

### 2. Start Datasette with your database

```bash
datasette serve mydata.db
```

### 3. Use datasette-agent

`datasette-agent` provides an AI assistant that can:
- Execute SQL queries against your Datasette instance
- Display query results as tables
- Explore database schema and relationships
- Handle truncated responses gracefully (tables still display even if results are truncated)

### 4. Key features (v0.1a3)

- **"View SQL query" buttons** for both visible tables and collapsed SQL result tool calls
- Clean handling of reasoning chunks (empty ones are not displayed)
- Improved truncated response handling — users see full table output even when the agent receives truncated data

### 5. Extensibility

Datasette Agent is designed as an extensible AI assistant for Datasette. It leverages the Datasette plugin ecosystem for additional functionality.

## References

- Release notes: https://github.com/datasette/datasette-agent/releases/tag/0.1a3
- Blog post: https://datasette.io/blog/2026/datasette-agent/
- Source: https://simonwillison.net/2026/May/21/datasette-agent-2/#atom-everything
