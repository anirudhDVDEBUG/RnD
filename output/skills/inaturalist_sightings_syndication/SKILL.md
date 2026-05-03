---
name: inaturalist_sightings_syndication
description: |
  Build a content syndication pipeline that pulls iNaturalist wildlife sightings (photos, species, dates) into a personal blog or website. Generates pages with search, pagination, RSS feeds, and integrates sightings into existing site features like homepage, archives, and search.
  TRIGGER: iNaturalist syndication, wildlife sightings blog, nature photography feed, iNaturalist API integration, beats syndication system
---

# iNaturalist Sightings Syndication

Syndicate your iNaturalist observations — species names, photos, dates, and locations — into a personal blog or static site as first-class content entries.

## When to use

- "I want to show my iNaturalist sightings on my blog"
- "Pull my wildlife photos from iNaturalist into my website"
- "Build a sightings page that syndicates from iNaturalist"
- "Add nature photography observations as blog content"
- "Create a beats-style syndication feed from iNaturalist"

## How to use

### 1. Fetch observations from the iNaturalist API

Use the public iNaturalist API v1 to pull observations for a given user:

```python
import httpx

def fetch_observations(username: str, page: int = 1, per_page: int = 30):
    """Fetch observations from iNaturalist API v1."""
    resp = httpx.get(
        "https://api.inaturalist.org/v1/observations",
        params={
            "user_login": username,
            "order": "desc",
            "order_by": "observed_on",
            "per_page": per_page,
            "page": page,
            "photos": "true",
        },
    )
    resp.raise_for_status()
    return resp.json()
```

Key fields per observation:
- `observation.taxon.preferred_common_name` — species common name
- `observation.taxon.name` — scientific name
- `observation.observed_on` — date string
- `observation.time_observed_at` — full timestamp
- `observation.photos[].url` — photo URLs (replace `square` with `medium` or `large` for bigger sizes)
- `observation.place_guess` — location description
- `observation.uri` — link back to iNaturalist

### 2. Group observations into sightings

Group observations by date (or date + time window) to create "sighting" entries that may contain multiple species:

```python
from itertools import groupby
from datetime import datetime

def group_into_sightings(observations):
    """Group observations by date into sighting entries."""
    keyfunc = lambda obs: obs["observed_on"]
    sightings = []
    for date, group in groupby(sorted(observations, key=keyfunc, reverse=True), key=keyfunc):
        obs_list = list(group)
        sightings.append({
            "date": date,
            "species": [o["taxon"]["preferred_common_name"] for o in obs_list if o.get("taxon")],
            "photos": [
                {
                    "url": p["url"].replace("square", "medium"),
                    "label": o["taxon"].get("preferred_common_name", o["taxon"]["name"]),
                }
                for o in obs_list if o.get("taxon")
                for p in o.get("photos", [])[:1]
            ],
            "time_start": min(o.get("time_observed_at") or "" for o in obs_list),
            "time_end": max(o.get("time_observed_at") or "" for o in obs_list),
            "source_urls": [o["uri"] for o in obs_list],
        })
    return sightings
```

### 3. Render sightings as blog content

Generate HTML or Markdown entries for each sighting. Include:
- Date and time range
- Species names as a comma-separated list in the heading
- Photo grid with alt text set to species names
- Link back to original iNaturalist observation

```html
<article class="sighting">
  <h2>Sighting {{ time_range }} — {{ species | join(", ") }}</h2>
  <div class="sighting-photos">
    {% for photo in photos %}
    <figure>
      <img src="{{ photo.url }}" alt="{{ photo.label }}" loading="lazy" />
      <figcaption>{{ photo.label }}</figcaption>
    </figure>
    {% endfor %}
  </div>
  <time datetime="{{ date }}">{{ date | format_date }}</time>
</article>
```

### 4. Add search, pagination, and RSS

- **Pagination**: Paginate sightings (e.g., 30 per page) with next/prev links.
- **Search**: Index species names and dates so sightings appear in site search.
- **RSS**: Generate an RSS/Atom feed for sightings at `/sightings/feed/`.
- **Homepage integration**: Include recent sightings in the homepage content stream alongside blog posts and other syndicated content.

### 5. Back-populate historical data

Page through all iNaturalist observations to import historical sightings:

```python
def backfill_all(username: str):
    page = 1
    while True:
        data = fetch_observations(username, page=page, per_page=200)
        if not data["results"]:
            break
        sightings = group_into_sightings(data["results"])
        save_sightings(sightings)  # your persistence function
        page += 1
```

### 6. Automate updates

Set up a cron job or webhook to periodically pull new observations:

```bash
# Run every hour
0 * * * * python sync_inaturalist.py --username YOUR_USERNAME --since last_run
```

## Key considerations

- iNaturalist photo URLs use size suffixes: `square`, `small`, `medium`, `large`, `original`
- Rate limit: the public API allows ~100 requests/minute without authentication
- Respect iNaturalist's terms — photos are CC-licensed per user settings; check `observation.license_code`
- Consider caching photos locally to reduce load on iNaturalist's servers

## References

- Source article: https://simonwillison.net/2026/May/2/sightings/#atom-everything
- Example PR: https://github.com/simonw/simonwillisonblog/pull/668
- Beats syndication system: https://simonwillison.net/2026/Feb/20/beats/
- iNaturalist API docs: https://api.inaturalist.org/v1/docs/
- iNaturalist: https://www.inaturalist.org/
