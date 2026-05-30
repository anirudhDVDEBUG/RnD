---
name: datasette_sql_write_stored_queries
description: |
  Set up and use Datasette's SQL write queries and stored queries features.
  TRIGGER when: user wants to execute write SQL against a Datasette instance, save stored queries, set up Datasette with write permissions, create templated insert/update/delete queries, or manage canned/stored queries in Datasette.
  DO NOT TRIGGER when: user is working with other database tools, raw SQLite without Datasette, or read-only Datasette usage.
---

# Datasette SQL Write Queries & Stored Queries

Set up and use Datasette 1.0a31+ features for executing write SQL queries and saving stored queries.

## When to use

- "Set up Datasette with write query support"
- "Create a stored query in Datasette"
- "Execute INSERT/UPDATE/DELETE SQL in Datasette"
- "Configure Datasette write permissions for users"
- "Migrate canned queries to stored queries in Datasette"

## How to use

### 1. Install or upgrade Datasette to 1.0a31+

```bash
pip install datasette>=1.0a31
```

### 2. Launch Datasette with a writable database

By default Datasette opens databases in read-only mode. To allow write queries, pass the database without the `-i` (immutable) flag:

```bash
datasette mydata.db
```

### 3. Execute write queries

Users with the appropriate permissions can:

1. Navigate to a database page.
2. Select **Actions → Execute write SQL**.
3. Choose a template (e.g. INSERT, UPDATE, DELETE) or write custom SQL.
4. Execute the query.

Permissions are granular — a user may have `insert-row` or `update-row` permission but not `create-table`.

### 4. Save stored queries

Stored queries (previously called "canned queries") let you save and share parameterized SQL:

1. Write a query in the SQL editor.
2. Click **Save as stored query**.
3. Choose visibility: **private** (only you) or **shared** (other instance members).
4. Stored queries appear in the database page for easy re-use.

### 5. Configure permissions via metadata

Use `datasette.yml` (or `metadata.json`) to grant write permissions:

```yaml
databases:
  mydata:
    permissions:
      insert-row:
        id: my-user
      update-row:
        id: my-user
      delete-row:
        id: my-user
```

### 6. Use parameterized queries

Stored queries support named parameters using `:param` syntax:

```sql
INSERT INTO documents (title, body) VALUES (:title, :body)
```

Datasette renders a form for each parameter when the stored query is executed.

## Key concepts

- **Write queries**: Execute INSERT, UPDATE, DELETE, and other write SQL statements directly through the Datasette UI (requires permissions).
- **Stored queries**: Save frequently-used SQL queries (read or write) for easy re-use, with private or shared visibility.
- **Permissions**: Datasette's permission system controls who can execute write queries, with granular controls per table and operation.

## References

- [Datasette 1.0a31 release announcement](https://simonwillison.net/2026/May/29/datasette/#atom-everything)
- [SQL write queries and stored queries blog post](https://datasette.io/blog/2026/sql-write-queries/)
- [Datasette releases on GitHub](https://github.com/simonw/datasette/releases/tag/1.0a31)
- [Datasette blog](https://datasette.io/blog/)
