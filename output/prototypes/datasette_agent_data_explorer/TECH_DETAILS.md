# Technical Details: Datasette Agent

## What it does

Datasette Agent adds a conversational AI layer on top of [Datasette](https://datasette.io/), the open-source tool for exploring SQLite databases. When a user types a natural-language question, the agent uses LLM tool-calling to inspect the database schema, generate SQLite-compatible SQL, execute queries, and return formatted results. With the `datasette-agent-charts` plugin, it can also render visualizations from query output.

The architecture is deliberately simple: Datasette serves the database and provides the web UI; the Agent plugin wires up LLM tool-calling to Datasette's query API; the LLM backend is swappable via Simon Willison's [LLM library](https://llm.datasette.io/) (Gemini, OpenAI, Claude, local models).

## Architecture

```
User Question (plain English)
        |
        v
  Datasette Agent Plugin
        |
        v
  LLM (via llm library)  <-- tool-calling interface
    |         |
    v         v
  inspect   execute_sql    <-- tools exposed to the LLM
  schema
    |         |
    v         v
  SQLite Database (via Datasette)
        |
        v
  Formatted Results / Charts
```

**Key components:**

| Component | Role |
|---|---|
| `datasette` | Serves SQLite databases, provides REST API and web UI |
| `datasette-agent` | Plugin that adds the conversational agent tab; manages LLM tool-calling loop |
| `datasette-agent-charts` | Optional plugin; renders charts from query results using the agent's output |
| `llm` + provider plugin | Abstraction layer for model access (Gemini, OpenAI, Claude, etc.) |

**Data flow:**
1. User submits a question via the web UI
2. Agent sends the question + available tools (schema inspection, SQL execution) to the LLM
3. LLM calls tools iteratively: inspects schema, writes SQL, executes it
4. Agent collects results and renders them in the UI
5. If charts plugin is installed, the LLM can also emit chart specifications

## Dependencies

- **Python 3.8+**
- **datasette** — SQLite web UI and API
- **datasette-agent** — the conversational agent plugin
- **llm** — model provider abstraction
- One LLM provider plugin (e.g., `llm-gemini`, `llm-claude-3`)
- **Optional:** `datasette-agent-charts` for visualization

## Limitations

- **SQLite only.** Does not work with Postgres, MySQL, or other databases. Datasette is SQLite-native.
- **Requires an LLM API key** for the real agent (Gemini, OpenAI, or Claude). The mock demo in this repo avoids that requirement.
- **Query accuracy depends on the model.** Complex joins or uncommon SQLite functions may need iteration. The agent does retry/refine, but it's not perfect.
- **No write operations.** The agent is read-only; it cannot INSERT, UPDATE, or DELETE data.
- **Chart generation is basic.** The charts plugin produces simple visualizations, not full BI dashboards.
- **No authentication built in.** If you deploy publicly, anyone can query your data. Use Datasette's permissions system or a reverse proxy for access control.

## Why this matters for Claude-driven products

- **Agent factories:** Datasette Agent is a clean reference implementation of the "LLM + tool-calling + structured data" pattern. It shows how to build a domain-specific agent that does something useful with minimal code — just expose tools and let the model iterate.
- **Lead-gen / marketing:** Drop a customer database into Datasette and let non-technical stakeholders query it conversationally. No SQL training needed.
- **Data exploration:** For any team sitting on SQLite data (analytics, logs, CRM exports), this provides instant self-service access without building a custom dashboard.
- **Plugin architecture:** The Datasette plugin model (schema inspection + SQL execution as LLM tools) is a pattern worth copying for any agent that needs structured data access.

## References

- [Announcement post](https://simonwillison.net/2026/May/21/datasette-agent-2/#atom-everything)
- [Datasette Agent blog post](https://datasette.io/blog/2026/datasette-agent/)
- [Live demo](https://agent.datasette.io/)
- [LLM library](https://llm.datasette.io/)
- [Demo video](https://www.youtube.com/watch?v=AFZKp6hbFjI)
