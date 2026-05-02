# How to Use

## Install

```bash
git clone <this-repo>
cd inat_sightings_git_scraping_viewer
pip install -r requirements.txt   # click, httpx
```

No API keys required -- iNaturalist's v1 API is public and unauthenticated.

## As a Claude Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/inat_sightings_git_scraping_viewer
cp SKILL.md ~/.claude/skills/inat_sightings_git_scraping_viewer/SKILL.md
```

**Trigger phrases that activate it:**
- "Set up git scraping to track iNaturalist observations"
- "Build an HTML page that displays sightings with thumbnails and a lightbox"
- "Create a GitHub Actions workflow that fetches JSON and commits it"
- "Build a single-file web app that loads JSON from a raw GitHub URL"

## First 60 Seconds

### Option A: Mock demo (no network)

```bash
bash run.sh
# Generates mock clumps.json, prints a preview, serves viewer at localhost:8765
```

Open `http://localhost:8765/viewer.html` -- you'll see 6 clumps of nature observations with thumbnails in a responsive grid. Click any image for a lightbox view.

### Option B: Real iNaturalist data

```bash
# Fetch observations for a specific user
python fetch.py simonw -o clumps.json

# Then open the viewer
python3 -m http.server 8765
# Visit http://localhost:8765/viewer.html
```

### Option C: Deploy with git scraping

1. Push this repo to GitHub.
2. Edit `.github/workflows/scrape.yml` -- set the username(s) you want to track.
3. Enable Actions in the repo settings.
4. The workflow runs every 6 hours, fetches observations, and commits `clumps.json`.
5. Host `viewer.html` on GitHub Pages (or anywhere) -- it fetches `clumps.json` from the raw GitHub URL.

To point the viewer at your raw GitHub JSON, set the URL before loading:

```html
<script>window.CLUMPS_URL = 'https://raw.githubusercontent.com/YOU/REPO/refs/heads/main/clumps.json';</script>
```

GitHub serves raw files with CORS headers, so the viewer works from any origin.

## CLI Reference

```
Usage: fetch.py [OPTIONS] USERNAMES...

  Fetch observations for one or more iNaturalist usernames and group into clumps.

Options:
  --hours INTEGER  Max hours between observations in a clump (default: 2)
  --km FLOAT       Max km between observations in a clump (default: 5)
  -o, --output     Output file (default: clumps.json)
```
