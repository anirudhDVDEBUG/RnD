# iNaturalist Sightings: Git Scraping + Single-File Viewer

A complete data pipeline that periodically fetches wildlife observations from the iNaturalist API via GitHub Actions ("git scraping"), stores them as committed JSON, and displays them in a standalone HTML gallery with lazy-loaded thumbnails and a click-to-enlarge lightbox.

**Headline result:** One `viewer.html` file + one `clumps.json` file = a live, self-updating nature observation dashboard hosted entirely on GitHub, no server required.

---

- **How to set it up** -- see [HOW_TO_USE.md](HOW_TO_USE.md)
- **How it works under the hood** -- see [TECH_DETAILS.md](TECH_DETAILS.md)
- **Quick demo:** `bash run.sh` (generates mock data and opens a local viewer)

Source: [Simon Willison -- iNaturalist Sightings](https://simonwillison.net/2026/May/1/inat-sightings/#atom-everything)
