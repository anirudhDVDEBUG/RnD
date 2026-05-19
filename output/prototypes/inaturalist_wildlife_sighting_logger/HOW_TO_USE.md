# How to Use

## As a Claude Code Skill (primary use)

### Install

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/inaturalist_wildlife_sighting_logger
   ```

2. Copy the skill file:
   ```bash
   cp SKILL.md ~/.claude/skills/inaturalist_wildlife_sighting_logger/SKILL.md
   ```

3. Optionally copy the Python helper for structured output:
   ```bash
   cp sighting_logger.py ~/.claude/skills/inaturalist_wildlife_sighting_logger/
   ```

4. Restart Claude Code. The skill auto-activates on trigger phrases.

### Trigger phrases

Say any of these to Claude Code:

- "I saw some birds on my walk, help me log them"
- "Format my wildlife sightings for iNaturalist"
- "Create an observation report from my nature walk notes"
- "Help me organize my bird photos and species list"
- "Turn my field notes into structured citizen-science records"

Claude will ask for species, location, date, notes, and photo info, then produce a formatted report.

## As a standalone Python script

### Requirements

- Python 3.7+
- No external dependencies (stdlib only)

### Run the demo

```bash
bash run.sh
```

This produces:
- Console output with the full Markdown report
- `sighting_report.md` -- the formatted report file
- `sighting_report.json` -- structured JSON for programmatic use

### Pipe in your own data

```bash
echo '{
  "date": "2026-05-18",
  "location": "Central Park, NYC",
  "observer": "Jane",
  "sightings": [
    {"common_name": "American Robin", "count": 3, "photos": 1, "notes": "Foraging on lawn"}
  ]
}' | python3 sighting_logger.py --json
```

## First 60 seconds

1. Run `bash run.sh`
2. See the Markdown report printed to terminal with 4 species from the LA River
3. Open `sighting_report.md` -- copy-paste ready for a blog post or field journal
4. Open `sighting_report.json` -- feed into your own tools or upload scripts
5. Notice the quality-grade cues and seasonal flags (e.g., Glaucous-winged Gull flagged as uncommon in SoCal)
