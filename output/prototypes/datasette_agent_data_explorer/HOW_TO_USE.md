# How to Use Datasette Agent

## Option A: Run the mock demo (no API key)

```bash
bash run.sh
```

This creates a sample SQLite database and runs 5 conversational queries through a mock agent, showing the full question -> SQL -> results flow.

## Option B: Install the real Datasette Agent

### 1. Install

```bash
pip install datasette datasette-agent
# Optional: chart generation
pip install datasette-agent-charts
```

### 2. Configure an LLM backend

Datasette Agent uses [LLM](https://llm.datasette.io/) for model access. Pick one:

```bash
# Gemini (fast, cheap — used by the official demo)
pip install llm-gemini
llm keys set gemini
# paste your API key

# Or OpenAI
pip install llm
llm keys set openai

# Or Claude
pip install llm-claude-3
llm keys set claude
```

### 3. Start Datasette with your database

```bash
datasette serve your_database.db
```

Opens at `http://localhost:8001`. Navigate to the Agent tab in the UI.

### 4. Ask questions

Type plain-English questions in the Agent interface:

- "What are the top 10 rows by revenue?"
- "Show me a chart of sales by month"
- "How many unique customers placed orders in 2025?"

The agent generates SQL, runs it, and returns formatted results (and charts if the plugin is installed).

## As a Claude Code Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/datasette_agent_data_explorer
cp SKILL.md ~/.claude/skills/datasette_agent_data_explorer/SKILL.md
```

### Trigger phrases

The skill activates when you say things like:

- "Help me set up Datasette Agent to explore my SQLite data"
- "I want a conversational interface for querying my database"
- "Set up a natural-language SQL assistant with Datasette"
- "How do I add chart generation to Datasette Agent?"

## First 60 Seconds

```
$ bash run.sh

======================================================================
  Datasette Agent  --  Mock Data Explorer Demo
======================================================================

  Database: power_plants.db (30 global power plants)

  USER (1/5): What are the top 5 countries by total power plant capacity?

  [Agent thinking] I'll query the power_plants table, summing capacity_mw
  grouped by country, ordered descending.

  [Agent] Executing SQL:
    SELECT country, COUNT(*) AS num_plants,
           ROUND(SUM(capacity_mw), 0) AS total_capacity_mw
    FROM power_plants GROUP BY country
    ORDER BY total_capacity_mw DESC LIMIT 5

  [Results] 5 row(s):

  country | num_plants | total_capacity_mw
  --------|------------|------------------
  China   | 4          | 35633
  Brazil  | 2          | 22370
  ...
```

Each question shows the agent's reasoning, the generated SQL, and the query results — exactly mirroring the real Datasette Agent workflow.
