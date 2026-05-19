# Technical Details

## What it does

The iNaturalist Wildlife Sighting Logger is a Claude Code skill backed by a zero-dependency Python module. It takes unstructured wildlife observation notes (species names, locations, counts, behavioral notes) and produces two outputs: a publication-ready Markdown report and a structured JSON export. The skill layer tells Claude *how* to gather observation data conversationally and format it according to iNaturalist conventions, while the Python module handles species lookup, quality-grade assessment, and seasonal flagging.

The demo uses real data from Simon Willison's May 18, 2026 LA River sighting post (Glaucous-winged Gull, Brown Pelican, Snowy Egret, Canada Goose) to show end-to-end formatting.

## Architecture

```
User prompt ("I saw birds on my walk")
        |
        v
  SKILL.md  (Claude Code skill trigger + formatting instructions)
        |
        v
  Claude gathers: species, location, date, notes, photos
        |
        v
  sighting_logger.py  (optional structured backend)
    +-- SPECIES_DB        : common name -> scientific name lookup (15 species)
    +-- UNCOMMON_SPECIES  : regional/seasonal flags
    +-- INATURALIST_FIELDS: suggested observation fields per taxon
    +-- Sighting          : dataclass per observation
    +-- SightingReport    : generates Markdown + JSON
        |
        v
  Output: sighting_report.md + sighting_report.json
```

### Key files

| File | Purpose |
|------|---------|
| `SKILL.md` | Claude Code skill definition with trigger phrases and formatting steps |
| `sighting_logger.py` | Python module: species DB, quality assessment, Markdown/JSON generation |
| `run.sh` | Demo runner using mock data from the source post |

### Dependencies

- Python 3.7+ standard library only (`dataclasses`, `json`, `datetime`)
- No API keys, no network calls, no external packages

## Limitations

- **Species database is small.** The built-in `SPECIES_DB` has ~15 North American birds. Unknown species get `scientific_name: "Unknown"`. In production, you'd hit the iNaturalist taxa API.
- **No photo analysis.** The skill records photo counts but does not examine image files for species ID. Pair with a vision model or iNaturalist's CV suggestions for that.
- **No GPS geocoding.** Coordinates must be provided manually; there's no address-to-lat/lon conversion.
- **No iNaturalist API integration.** Output is formatted for manual upload. A real integration would use the iNaturalist observations API (`POST /observations`) to submit directly.
- **Regional flags are hardcoded** for Southern California. Other regions would need their own seasonal/range data.

## Why it matters

- **Agent-driven citizen science.** This is a clean pattern for Claude skills that bridge conversational input and structured data output -- applicable to any domain where users dictate unstructured notes that need to become database records (field surveys, inspections, inventory counts).
- **Lead-gen / content angle.** Nature blogs, birding communities, and eco-tourism operators could use this to auto-generate sighting reports from walk notes -- content that drives organic SEO traffic.
- **Skill authoring reference.** The SKILL.md demonstrates best practices: clear trigger/anti-trigger rules, step-by-step instructions, example output, and tips. Useful as a template for building other Claude Code skills.
- **Zero-dependency pattern.** Shows that useful skills don't need heavy frameworks. The Python module is <200 lines with no pip installs, making it easy to bundle and deploy.
