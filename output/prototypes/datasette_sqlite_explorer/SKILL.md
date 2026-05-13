---
name: datasette_sqlite_explorer
description: |
  Spin up and configure Datasette instances to explore, publish, and build APIs on top of SQLite databases.
  TRIGGER: user mentions datasette, wants to explore a SQLite database via web UI, needs to publish or share a database, asks about datasette API tokens or token restrictions, or wants to build an instant JSON API from a .db file.
---

# Datasette SQLite Explorer

Set up and configure [Datasette](https://datasette.io/) to explore SQLite databases through a web interface and instant JSON API.

## When to use

- "Spin up a datasette instance for this SQLite database"
- "I want to explore my .db file in a browser"
- "Create an API from this SQLite database"
- "Configure datasette API tokens with restrictions"
- "Publish this database with datasette"

## How to use

### 1. Install Datasette

```bash
pip install datasette
# or with uvx for isolated installs:
uvx datasette
```

Requires Python 3.9+. As of version 1.0a29, Datasette is in the 1.0 alpha series with stable core features.

### 2. Launch Datasette on a database

```bash
datasette serve mydata.db
# Opens at http://localhost:8001
```

For multiple databases:
```bash
datasette serve db1.db db2.db
```

### 3. Configure API token restrictions (1.0a29+)

Use the `TokenRestrictions.abbreviated(datasette)` utility method to create `"_r"` restriction dictionaries for scoped API tokens:

```python
from datasette.utils import TokenRestrictions

# Create abbreviated restriction dicts for token scoping
restrictions = TokenRestrictions.abbreviated(datasette)
```

### 4. Publish a database

```bash
# Publish to Vercel
datasette publish vercel mydata.db --project my-datasette

# Publish to Fly.io
datasette publish fly mydata.db --app my-datasette

# Publish to Google Cloud Run
datasette publish cloudrun mydata.db --service my-datasette
```

### 5. Install plugins

```bash
datasette install datasette-vega        # Charts
datasette install datasette-cluster-map  # Map visualizations
datasette install datasette-export-notebook  # Jupyter export
```

### Key notes for 1.0a29

- Table headers and column options now display even on empty tables (#2701)
- Fixed column actions dialog on Mobile Safari (#2708)
- Fixed segfault race condition between concurrent `Datasette.close()` calls in tests (#2709)

## References

- Source: [datasette 1.0a29 release notes](https://simonwillison.net/2026/May/12/datasette/#atom-everything)
- GitHub: [simonw/datasette](https://github.com/simonw/datasette)
- Documentation: [docs.datasette.io](https://docs.datasette.io/en/latest/)
