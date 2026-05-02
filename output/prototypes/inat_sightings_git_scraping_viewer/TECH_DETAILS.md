# Technical Details

## What It Does

This project implements the "git scraping" pattern popularized by Simon Willison: a GitHub Actions workflow runs on a cron schedule, fetches data from a public API, and commits the result as a JSON file in the repo. Because every change is a git commit, you get a full history of how the data evolved over time -- for free, with no database.

The fetcher pulls observations from the iNaturalist API, groups them into "clumps" by temporal and geographic proximity (using haversine distance), and writes a lightweight JSON file. A standalone HTML viewer loads this JSON (either locally or from a raw GitHub URL) and renders a responsive photo grid with lazy loading and a lightbox modal.

## Architecture

```
fetch.py                    CLI fetcher (click + httpx)
  |
  v
clumps.json                 Committed data artifact
  |
  v
viewer.html                 Single-file viewer (vanilla JS, no build step)

.github/workflows/scrape.yml   Cron-triggered Actions workflow
mock_data.py                   Generates demo data for offline use
```

### Data Flow

1. **Fetch:** `fetch.py` pages through the iNaturalist `/v1/observations` endpoint for given usernames, collecting all observations.
2. **Clump:** Observations are sorted by date, then grouped into clumps where consecutive observations are within `--hours` hours and `--km` km of each other (haversine formula).
3. **Serialize:** Each clump is flattened to an array of lightweight observation objects (id, species, photos, location, date).
4. **Commit:** The GitHub Actions workflow commits `clumps.json` only if it changed (`git diff --quiet --cached`).
5. **Display:** `viewer.html` fetches the JSON, renders a card grid with `loading="lazy"` on images, and opens a lightbox modal on click.

### Key Dependencies

- **Python:** `click` (CLI), `httpx` (HTTP client)
- **Frontend:** Zero dependencies -- vanilla HTML/CSS/JS
- **Infrastructure:** GitHub Actions (free tier), GitHub raw content CDN (CORS-enabled)

## Limitations

- **Rate limits:** iNaturalist API is unauthenticated and rate-limited. The fetcher does not handle 429 responses or implement exponential backoff. For heavy users with thousands of observations, you may hit limits.
- **No incremental fetch:** Every run fetches the full observation history. For users with 10,000+ observations, this is slow. A production version would store a cursor/timestamp and fetch only new data.
- **Static clumping:** Clumps are computed once at fetch time. The viewer has no filtering, search, or date-range selection.
- **No map view:** Observations have lat/lon but the viewer only shows a photo grid, not a map.
- **Single repo:** The pattern commits data to the same repo as the code. For high-frequency scraping, a dedicated data repo avoids polluting the code history.

## Why This Matters for Claude-Driven Products

- **Agent data pipelines:** The git-scraping pattern is a zero-infrastructure way for an agent to collect and version external data. Claude can generate the fetcher, the workflow YAML, and the viewer in one shot.
- **Lead-gen / monitoring:** Replace iNaturalist with any public API (job boards, product listings, social feeds) and you have a free, auditable data collection pipeline.
- **Single-file deliverables:** The viewer is one HTML file with no build step -- ideal for agents that need to produce self-contained artifacts a human can immediately open and evaluate.
- **Composability:** The JSON-on-GitHub pattern means any downstream tool (another Action, a Claude agent, a Zapier webhook) can consume the data by fetching a single URL.
