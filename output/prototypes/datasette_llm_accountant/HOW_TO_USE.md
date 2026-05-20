# How to Use datasette-llm

## Install

```bash
pip install datasette-llm
```

This installs the plugin and its dependency on `llm`. Datasette auto-discovers it via Python entry points.

You also need at least one LLM model plugin and its API key:

```bash
llm install llm-claude-3    # or llm-gpt-4, etc.
llm keys set anthropic      # paste your API key
```

## Claude Skill setup

This repo includes a Claude Code skill for install/config/troubleshooting help:

```bash
mkdir -p ~/.claude/skills/datasette_llm_accountant
cp SKILL.md ~/.claude/skills/datasette_llm_accountant/SKILL.md
```

**Trigger phrases:**
- "How do I add LLM prompting to my Datasette instance?"
- "Help me install and configure datasette-llm"
- "I'm getting an error with llm_prompt_context() not collecting responses"
- "Debug my datasette-llm plugin hook"

## First 60 seconds

### 1. Create a database and start Datasette

```bash
sqlite3 demo.db "CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);"
sqlite3 demo.db "INSERT INTO products VALUES (1,'Widget',9.99,100),(2,'Gadget',24.50,42);"
datasette serve demo.db
```

### 2. Verify the plugin loaded

```bash
datasette plugins
```

You should see `datasette-llm` in the list.

### 3. Use LLM features

Open `http://localhost:8001` -- datasette-llm adds LLM-powered query assistance to your Datasette UI. Any plugin can inject additional context via the `llm_prompt_context()` hook.

### 4. Write a custom context plugin

```python
from datasette import hookimpl

@hookimpl
def llm_prompt_context(datasette, request):
    return "Always format currency with $ prefix."
```

Save this as a Datasette plugin and it will automatically contribute context to every LLM prompt.

## Demo (no API keys needed)

```bash
bash run.sh
```

This runs a self-contained simulation showing the `llm_prompt_context()` hook architecture and the v0.1a8 chain-collection fix. Input: a user query ("Show me average price by category"). Output: assembled context from 3 mock plugins, mock-generated SQL, and executed query results.
