# Technical Details

## What It Does

This pipeline fetches wildlife observation data from the iNaturalist public API (species, photos, dates, locations) and renders them as static HTML pages suitable for embedding in a personal blog or static site. Observations are grouped by date into "sightings," each containing one or more species with photo grids. The output includes paginated listing pages and an Atom feed for RSS readers.

The design follows Simon Willison's "beats" pattern — treating syndicated content (sightings) as first-class blog entries alongside regular posts, with their own archive, search integration, and feed.

## Architecture

```
sync_sightings.py        # Main entry point: fetch, group, render
  |
  +-- fetcher.py         # iNaturalist API client (httpx)
  |     -> GET /v1/observations?user_login=X&photos=true
  |
  +-- grouper.py         # Groups observations by date into sightings
  |
  +-- renderer.py        # Jinja2 templates -> HTML + Atom XML
  |
  +-- mock_data.py       # Sample observations for demo/testing
  |
  output/
    index.html           # Latest sightings landing page
    page{N}.html         # Paginated archive
    feed.xml             # Atom feed
```

## Data Flow

1. **Fetch** — `fetcher.py` calls `api.inaturalist.org/v1/observations` with pagination, returns raw JSON.
2. **Group** — `grouper.py` clusters observations by `observed_on` date, extracts species names, photo URLs (upsized from `square` to `medium`), and source links.
3. **Render** — `renderer.py` uses Jinja2 to produce HTML pages and an Atom feed. Templates are inline strings (no external template files needed).

## Dependencies

- `httpx` — async-capable HTTP client for API calls
- `jinja2` — template rendering for HTML/XML output

No database, no build tool, no framework. Pure Python + two libraries.

## Limitations

- **No authentication** — uses the public iNaturalist API (rate-limited to ~100 req/min). For heavy backfills, add delays.
- **No local photo caching** — images are hotlinked from iNaturalist CDN. For production, proxy or cache locally.
- **No incremental sync** — each run fetches from scratch (or from `--since`). No state file for last-run tracking (trivial to add).
- **No search index** — generates static HTML only. Site-level search requires external tooling (e.g., Pagefind, Lunr).
- **Photos are CC-licensed per user** — check `license_code` before republishing.

## Why This Matters for Claude-Driven Products

- **Content syndication as a pattern**: The same fetch-group-render pipeline works for any API-backed content (social posts, commits, bookmarks). Useful for agent-generated marketing sites or personal brand pages.
- **Agent factory fodder**: A Claude agent could run this pipeline on a schedule, generating daily nature content for SEO or social feeds without human intervention.
- **Lead-gen sites**: Niche wildlife/nature blogs with auto-updating content can drive organic traffic. This is the engine.
- **Beats model**: Simon Willison's "beats" concept (multiple syndicated content types on one blog) is a blueprint for AI-curated content hubs.

## References

- [Source article](https://simonwillison.net/2026/May/2/sightings/#atom-everything)
- [Example PR](https://github.com/simonw/simonwillisonblog/pull/668)
- [iNaturalist API docs](https://api.inaturalist.org/v1/docs/)
