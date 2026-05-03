# How to Use

## Install

```bash
git clone <this-repo>
cd inaturalist_sightings_syndication
pip install -r requirements.txt
```

## Quick Start (mock data, no API key needed)

```bash
bash run.sh
# Opens output/index.html with 12 sample sightings
```

## Live Mode (real iNaturalist data)

```bash
python sync_sightings.py --username YOUR_INATURALIST_USERNAME
# Fetches your observations and generates output/
```

To back-populate all historical observations:

```bash
python sync_sightings.py --username YOUR_USERNAME --backfill
```

## First 60 Seconds

```
$ bash run.sh
[mock] Loading 12 sample sightings...
Grouped into 4 sighting entries.
Generating output/index.html ...
Generating output/page1.html (sightings 1-3)...
Generating output/page2.html (sightings 4-4)...
Generating output/feed.xml (Atom feed)...
Done. Open output/index.html in your browser.
```

Input: iNaturalist username (or mock data)
Output: Static HTML pages + Atom feed in `output/`

## As a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/inaturalist_sightings_syndication
cp SKILL.md ~/.claude/skills/inaturalist_sightings_syndication/
```

**Trigger phrases:**
- "I want to show my iNaturalist sightings on my blog"
- "Pull my wildlife photos from iNaturalist into my website"
- "Build a sightings page that syndicates from iNaturalist"
- "Add nature photography observations as blog content"

## Automation

Add a cron job to sync every hour:

```bash
0 * * * * cd /path/to/repo && python sync_sightings.py --username YOU --since last_run
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `INAT_USERNAME` | (required in live mode) | iNaturalist username |
| `INAT_PER_PAGE` | `30` | Observations per API page |
| `OUTPUT_DIR` | `output` | Where to write HTML files |
| `SIGHTINGS_PER_PAGE` | `3` | Sightings per HTML page |
