# How to Use

## Install

```bash
pip install "datasette>=1.0a31"
```

Or from this repo:

```bash
pip install -r requirements.txt
```

## As a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
cp -r skill/ ~/.claude/skills/datasette_sql_write_stored_queries/
```

The skill contains a `SKILL.md` that triggers on phrases like:

- "Set up Datasette with write query support"
- "Create a stored query in Datasette"
- "Execute INSERT/UPDATE/DELETE SQL in Datasette"
- "Configure Datasette write permissions"
- "Migrate canned queries to stored queries"

## First 60 Seconds

```bash
# 1. Run the demo end-to-end
bash run.sh

# 2. Or start Datasette manually with the demo database
datasette demo.db --metadata datasette.yml

# 3. Visit http://localhost:8001 → pick a database → Actions → Execute write SQL
```

### What `run.sh` does:

1. Creates a SQLite database with a `documents` table
2. Starts Datasette in the background with write permissions enabled
3. Executes INSERT queries via the Datasette JSON API
4. Creates a stored query via the API
5. Queries data back to prove writes landed
6. Tears down the server

### Example API interaction (from the demo):

```bash
# Execute a write query
curl -X POST http://localhost:8001/demo/-/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "INSERT INTO documents (title, body) VALUES (:title, :body)", "params": {"title": "Hello", "body": "World"}}'
```

## Configuration

### datasette.yml (permissions for write access)

```yaml
databases:
  demo:
    permissions:
      execute-sql:
        id: "*"
      insert-row:
        id: "*"
      update-row:
        id: "*"
      delete-row:
        id: "*"
```

For production, replace `"*"` with specific user IDs from your auth plugin.
