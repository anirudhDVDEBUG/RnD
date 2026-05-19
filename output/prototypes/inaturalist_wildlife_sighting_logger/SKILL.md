---
name: inaturalist_wildlife_sighting_logger
description: |
  Helps document and organize wildlife sightings for citizen-science platforms like iNaturalist.
  TRIGGER when: user mentions bird sighting, wildlife observation, iNaturalist, citizen science logging, nature walk notes, species identification list, or wants to format observation data.
  DO NOT TRIGGER when: user is doing general photography editing, unrelated biology research, or pet identification.
---

# iNaturalist Wildlife Sighting Logger

A skill for structuring, formatting, and organizing wildlife observation notes into clean, publishable records suitable for citizen-science platforms like iNaturalist.

## When to use

- "I saw some birds on my walk, help me log them"
- "Format my wildlife sightings for iNaturalist"
- "Create an observation report from my nature walk notes"
- "Help me organize my bird photos and species list"
- "Turn my field notes into structured citizen-science records"

## How to use

### Step 1: Gather observation details

Collect the following from the user for each sighting:

- **Species name(s):** Common name and scientific name if known
- **Location:** As specific as possible (city, park, coordinates)
- **Date and time:** When the observation occurred
- **Photos:** File paths or descriptions of photos taken
- **Notes:** Behavior observed, habitat, weather, context
- **Count:** Number of individuals seen (if applicable)

### Step 2: Structure observations

For each species observed, create a structured record:

```markdown
## [Common Name] (*Scientific Name*)

- **Date:** YYYY-MM-DD
- **Location:** [Place name], [Region]
- **Coordinates:** [lat, lon] (if available)
- **Count:** [number or "present"]
- **Photos:** [list of photo files]
- **Notes:** [behavioral observations, habitat context]
- **Quality grade cues:** [research-grade checklist: photo, location, date, community ID]
```

### Step 3: Generate a summary report

Produce a consolidated sighting report in Markdown that includes:

1. **Header** with date, location, and observer name
2. **Species checklist** -- a quick table of all species with counts
3. **Detailed entries** -- one section per species with all fields
4. **Trip notes** -- overall narrative (weather, route, highlights)
5. **Upload checklist** -- reminders for iNaturalist submission (photo quality, GPS, licensing)

### Step 4: Validate and enrich

- Flag uncertain IDs and suggest similar species to compare
- Note if any species are uncommon for the reported location/season
- Suggest iNaturalist observation fields relevant to the taxa (e.g., "Alive or Dead", "Nesting", "Bird Count Method")

### Tips

- Always pair common names with scientific names for accuracy
- Encourage users to note distinguishing field marks for community ID
- Remind users that iNaturalist requires a photo or sound for verifiable observations
- Suggest adding observations to relevant iNaturalist projects (e.g., "City Nature Challenge", local birding groups)

## References

- Source post: https://simonwillison.net/2026/May/18/sighting-362781627/#atom-everything
- iNaturalist: https://www.inaturalist.org/
- iNaturalist observation fields guide: https://www.inaturalist.org/pages/managing-projects
