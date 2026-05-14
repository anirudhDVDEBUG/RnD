# Datasette Blog Setup

**A complete, SQLite-backed blog in a single command.** Datasette turns a SQLite database into an instantly browsable website with JSON API, full-text search, faceted tag filtering, and one-command cloud deployment.

## Headline Result

```
$ bash run.sh
  Seeded 5 posts and 7 tags
  FTS search for 'sqlite': 1 result(s)

--- All published posts (newest first) ---
  slug                              | title                                      | published   | tags
  welcome-to-the-datasette-blog     | Welcome to the Datasette Blog              | 2026-05-14  | announcement,datasette
  sqlite-as-a-content-store         | Why SQLite Makes a Great Content Store      | 2026-05-13  | sqlite,architecture
  datasette-plugins-for-blogging    | Essential Datasette Plugins for Blogging    | 2026-05-12  | plugins,tutorial
  ...
```

Run `bash run.sh` to create the database, seed posts, and query everything locally — no API keys needed.

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, and launch the blog in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why this matters

## Source

Based on [Welcome to the Datasette blog](https://simonwillison.net/2026/May/13/welcome-to-the-datasette-blog/#atom-everything) by Simon Willison.
