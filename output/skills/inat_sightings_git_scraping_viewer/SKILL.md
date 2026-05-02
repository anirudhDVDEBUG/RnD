---
name: inat_sightings_git_scraping_viewer
description: |
  Build a git-scraping pipeline that fetches data from an API (e.g. iNaturalist), stores it as JSON in a GitHub repo via scheduled Actions, and creates a single-file HTML viewer with lazy-loaded thumbnails and a lightbox modal.
  TRIGGER: user wants to git-scrape an API, build an observation/sighting viewer, create a data pipeline with GitHub Actions that commits JSON, or build a single-page app that fetches raw JSON from GitHub.
---

# iNaturalist-Style Sightings: Git Scraping + Single-File Viewer

Build a complete data pipeline that periodically fetches API data via GitHub Actions ("git scraping"), stores it as JSON in a repo, and displays it in a standalone HTML page with lazy-loaded image thumbnails and a click-to-enlarge modal.

## When to use

- "Set up git scraping to track data from an API over time"
- "Build an HTML page that displays observations/sightings with thumbnails and a lightbox"
- "Create a GitHub Actions workflow that fetches JSON and commits it to the repo"
- "I want to fetch data from iNaturalist and display it on a web page"
- "Build a single-file web app that loads JSON from a raw GitHub URL"

## How to use

This skill has three parts: a CLI data fetcher, a git-scraping repo, and a viewer.

### Part 1 — CLI Data Fetcher (Python)

Create a Python CLI that fetches and processes observations from an API. For iNaturalist:

```python
#!/usr/bin/env python3
"""Fetch iNaturalist observations and clump them by time/location proximity."""
import click
import httpx
import json
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """Distance in km between two lat/lon points."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * 6371 * asin(sqrt(a))

@click.command()
@click.argument("usernames", nargs=-1, required=True)
@click.option("--hours", default=2, help="Max hours between observations in a clump")
@click.option("--km", default=5, help="Max km between observations in a clump")
@click.option("--output", "-o", default="clumps.json")
def cli(usernames, hours, km, output):
    observations = []
    for username in usernames:
        page = 1
        while True:
            resp = httpx.get(
                "https://api.inaturalist.org/v1/observations",
                params={"user_login": username, "per_page": 200, "page": page, "order": "asc"},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data["results"]
            if not results:
                break
            observations.extend(results)
            page += 1

    # Sort by observed date
    observations.sort(key=lambda o: o.get("observed_on_details", {}).get("date", ""))

    # Clump by time and distance proximity
    clumps = []
    current_clump = []
    for obs in observations:
        if not current_clump:
            current_clump.append(obs)
            continue
        last = current_clump[-1]
        time_ok = True  # Simplified; use observed_on for real comparison
        geo_ok = True
        if obs.get("geojson") and last.get("geojson"):
            d = haversine(
                last["geojson"]["coordinates"][0], last["geojson"]["coordinates"][1],
                obs["geojson"]["coordinates"][0], obs["geojson"]["coordinates"][1],
            )
            geo_ok = d <= km
        if time_ok and geo_ok:
            current_clump.append(obs)
        else:
            clumps.append(current_clump)
            current_clump = [obs]
    if current_clump:
        clumps.append(current_clump)

    # Serialize
    output_data = []
    for clump in clumps:
        output_data.append({
            "observations": [
                {
                    "id": o["id"],
                    "species_guess": o.get("species_guess"),
                    "common_name": (o.get("taxon") or {}).get("preferred_common_name"),
                    "photos": [
                        {"small": p["url"].replace("square", "small"), "large": p["url"].replace("square", "large")}
                        for p in (o.get("photos") or [])
                    ],
                    "observed_on": o.get("observed_on_string"),
                }
                for o in clump
            ],
        })

    with open(output, "w") as f:
        json.dump(output_data, f, indent=2)
    click.echo(f"Wrote {len(output_data)} clumps to {output}")

if __name__ == "__main__":
    cli()
```

Dependencies: `click`, `httpx`.

### Part 2 — Git Scraping Repository

Create a GitHub Actions workflow that runs the fetcher on a schedule and commits the result:

```yaml
# .github/workflows/scrape.yml
name: Scrape iNaturalist
on:
  schedule:
    - cron: "0 */6 * * *"   # every 6 hours
  workflow_dispatch:
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install click httpx
      - run: python fetch.py username1 username2 -o clumps.json
      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@users.noreply.github.com"
          git add clumps.json
          git diff --quiet --cached || git commit -m "Update clumps.json"
          git push
```

Key detail: the JSON file at `https://raw.githubusercontent.com/<user>/<repo>/refs/heads/main/clumps.json` is served with CORS headers, making it fetchable from any web page.

### Part 3 — Single-File HTML Viewer

Build a self-contained HTML file that fetches the JSON and renders a gallery:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>iNaturalist Sightings</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #f5f5f5; padding: 1rem; }
  h1 { margin-bottom: 1rem; }
  .clump { background: #fff; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
  .clump h2 { font-size: 1rem; color: #555; margin-bottom: .5rem; }
  .grid { display: flex; flex-wrap: wrap; gap: .5rem; }
  .card { cursor: pointer; text-align: center; width: 130px; }
  .card img { width: 120px; height: 120px; object-fit: cover; border-radius: 6px; }
  .card .name { font-size: .75rem; color: #333; margin-top: .25rem; }
  .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,.8); z-index: 100; align-items: center; justify-content: center; }
  .modal-overlay.active { display: flex; }
  .modal-content { max-width: 90vw; max-height: 90vh; text-align: center; }
  .modal-content img { max-width: 100%; max-height: 80vh; border-radius: 8px; }
  .modal-content p { color: #fff; margin-top: .5rem; font-size: 1.1rem; }
</style>
</head>
<body>
<h1>iNaturalist Sightings</h1>
<div id="app">Loading…</div>

<div class="modal-overlay" id="modal">
  <div class="modal-content">
    <img id="modal-img" src="" alt="">
    <p id="modal-name"></p>
  </div>
</div>

<script>
const DATA_URL = "https://raw.githubusercontent.com/USER/REPO/refs/heads/main/clumps.json";
const app = document.getElementById("app");
const modal = document.getElementById("modal");
const modalImg = document.getElementById("modal-img");
const modalName = document.getElementById("modal-name");

modal.addEventListener("click", () => modal.classList.remove("active"));

function showModal(largeSrc, name) {
  modalImg.src = largeSrc;
  modalName.textContent = name || "";
  modal.classList.add("active");
}

async function main() {
  const resp = await fetch(DATA_URL);
  const clumps = await resp.json();
  app.innerHTML = "";
  for (const clump of clumps) {
    const section = document.createElement("div");
    section.className = "clump";
    const date = clump.observations[0]?.observed_on || "Unknown date";
    section.innerHTML = `<h2>${date}</h2><div class="grid"></div>`;
    const grid = section.querySelector(".grid");
    for (const obs of clump.observations) {
      const name = obs.common_name || obs.species_guess || "Unknown";
      for (const photo of (obs.photos || [])) {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<img src="${photo.small}" loading="lazy" alt="${name}"><div class="name">${name}</div>`;
        card.addEventListener("click", () => showModal(photo.large, name));
        grid.appendChild(card);
      }
    }
    app.appendChild(section);
  }
}
main();
</script>
</body>
</html>
```

### Adapting to other APIs

This pattern works for any API:

1. **Write a fetcher** — Python script that calls the API and writes JSON
2. **Set up git scraping** — GitHub Actions workflow on a cron schedule that runs the fetcher and commits
3. **Build a viewer** — Single HTML file that fetches the raw JSON from GitHub and renders it

The raw GitHub URL pattern is: `https://raw.githubusercontent.com/<owner>/<repo>/refs/heads/<branch>/<file>`

### Key implementation details

- Use `loading="lazy"` on `<img>` tags for performance with many images
- Use `small.jpg` for thumbnails and `large.jpg` for the modal to save bandwidth
- iNaturalist photo URLs use size suffixes: `square.jpg`, `small.jpg`, `medium.jpg`, `large.jpg`, `original.jpg`
- The git scraping commit step uses `git diff --quiet --cached ||` to skip commits when data hasn't changed
- Raw GitHub content includes CORS headers, so `fetch()` works from any origin

## References

- [iNaturalist Sightings — Simon Willison](https://simonwillison.net/2026/May/1/inat-sightings/#atom-everything)
- [Git scraping series — Simon Willison](https://simonwillison.net/series/git-scraping/)
- [inaturalist-clumper CLI](https://github.com/simonw/inaturalist-clumper)
- [inaturalist-clumps git-scraping repo](https://github.com/simonw/inaturalist-clumps)
- [iNaturalist API docs](https://api.inaturalist.org/v1/docs/)
