#!/usr/bin/env python3
"""
iNaturalist Wildlife Sighting Logger

Structures, formats, and organizes wildlife observation notes into clean,
publishable records suitable for citizen-science platforms like iNaturalist.
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


# Known species database (common_name -> scientific_name)
SPECIES_DB = {
    "glaucous-winged gull": "Larus glaucescens",
    "brown pelican": "Pelecanus occidentalis",
    "snowy egret": "Egretta thula",
    "canada goose": "Branta canadensis",
    "great blue heron": "Ardea herodias",
    "american robin": "Turdus migratorius",
    "red-tailed hawk": "Buteo jamaicensis",
    "mallard": "Anas platyrhynchos",
    "anna's hummingbird": "Calypte anna",
    "house sparrow": "Passer domesticus",
    "american crow": "Corvus brachyrhynchos",
    "northern mockingbird": "Mimus polyglottos",
    "black-crowned night-heron": "Nycticorax nycticorax",
    "double-crested cormorant": "Nannopterum auritum",
    "western gull": "Larus occidentalis",
}

# Seasonal context for Southern California
UNCOMMON_SPECIES_HINTS = {
    "brown pelican": "Uncommon inland; typically coastal. Verify location if far from ocean.",
    "snowy egret": "Year-round resident along CA waterways. Expected here.",
    "glaucous-winged gull": "More common in the Pacific Northwest; uncommon in SoCal. Worth documenting.",
}

INATURALIST_FIELDS = {
    "bird": ["Alive or Dead", "Bird Count Method", "Nesting", "Sex", "Life Stage"],
    "default": ["Alive or Dead", "Habitat"],
}


@dataclass
class Sighting:
    common_name: str
    scientific_name: str = ""
    date: str = ""
    location: str = ""
    coordinates: Optional[str] = None
    count: str = "1"
    photos: int = 0
    notes: str = ""
    quality_cues: list = field(default_factory=list)

    def __post_init__(self):
        if not self.scientific_name:
            key = self.common_name.lower()
            self.scientific_name = SPECIES_DB.get(key, "Unknown")
        if not self.quality_cues:
            self.quality_cues = self._assess_quality()

    def _assess_quality(self) -> list:
        cues = []
        if self.photos > 0:
            cues.append("photo: YES")
        else:
            cues.append("photo: MISSING (required for verifiable observation)")
        if self.location:
            cues.append("location: YES")
        else:
            cues.append("location: MISSING")
        if self.date:
            cues.append("date: YES")
        else:
            cues.append("date: MISSING")
        cues.append("community ID: pending upload")
        return cues


@dataclass
class SightingReport:
    title: str
    date: str
    location: str
    observer: str
    sightings: list  # list of Sighting
    trip_notes: str = ""

    def to_markdown(self) -> str:
        lines = []
        lines.append(f"# {self.title}")
        lines.append(f"**Date:** {self.date} | **Observer:** {self.observer}")
        lines.append("")

        # Species checklist table
        lines.append("| # | Species | Count | Photos |")
        lines.append("|---|---------|-------|--------|")
        for i, s in enumerate(self.sightings, 1):
            lines.append(f"| {i} | {s.common_name} | {s.count} | {s.photos} |")
        lines.append("")

        # Detailed entries
        for s in self.sightings:
            lines.append(f"## {s.common_name} (*{s.scientific_name}*)")
            lines.append(f"- **Date:** {s.date}")
            lines.append(f"- **Location:** {s.location}")
            if s.coordinates:
                lines.append(f"- **Coordinates:** {s.coordinates}")
            lines.append(f"- **Count:** {s.count}")
            lines.append(f"- **Photos:** {s.photos}")
            lines.append(f"- **Notes:** {s.notes}")
            lines.append(f"- **Quality grade cues:** {', '.join(s.quality_cues)}")

            # Seasonal/location flags
            key = s.common_name.lower()
            if key in UNCOMMON_SPECIES_HINTS:
                lines.append(f"- **Flag:** {UNCOMMON_SPECIES_HINTS[key]}")

            # Suggested iNaturalist fields
            obs_fields = INATURALIST_FIELDS.get("bird", INATURALIST_FIELDS["default"])
            lines.append(f"- **Suggested iNaturalist fields:** {', '.join(obs_fields)}")
            lines.append("")

        # Trip notes
        if self.trip_notes:
            lines.append("## Trip Notes")
            lines.append(self.trip_notes)
            lines.append("")

        # Upload checklist
        lines.append("## iNaturalist Upload Checklist")
        lines.append("- [ ] Photos are clear and show identifying features")
        lines.append("- [ ] GPS coordinates are accurate (check map preview)")
        lines.append("- [ ] Date and time are correct")
        lines.append("- [ ] License is set (CC-BY or CC-BY-NC recommended)")
        lines.append("- [ ] Add to relevant projects (e.g., City Nature Challenge)")
        lines.append("- [ ] Review community ID suggestions after upload")
        lines.append("")

        return "\n".join(lines)

    def to_json(self) -> str:
        data = {
            "title": self.title,
            "date": self.date,
            "location": self.location,
            "observer": self.observer,
            "trip_notes": self.trip_notes,
            "species_count": len(self.sightings),
            "sightings": [asdict(s) for s in self.sightings],
        }
        return json.dumps(data, indent=2)


def parse_sightings_from_dict(data: dict) -> SightingReport:
    """Parse a dict of observation data into a SightingReport."""
    sightings = []
    for entry in data.get("sightings", []):
        s = Sighting(
            common_name=entry["common_name"],
            scientific_name=entry.get("scientific_name", ""),
            date=data.get("date", ""),
            location=entry.get("location", data.get("location", "")),
            coordinates=entry.get("coordinates"),
            count=str(entry.get("count", "1")),
            photos=entry.get("photos", 0),
            notes=entry.get("notes", ""),
        )
        sightings.append(s)

    return SightingReport(
        title=data.get("title", f"Wildlife Sightings -- {data.get('location', 'Unknown')}"),
        date=data.get("date", datetime.now().strftime("%Y-%m-%d")),
        location=data.get("location", "Unknown"),
        observer=data.get("observer", "Observer"),
        sightings=sightings,
        trip_notes=data.get("trip_notes", ""),
    )


def demo():
    """Run a demo with the sighting data from Simon Willison's post."""
    data = {
        "title": "Wildlife Sightings -- Los Angeles River, CA, US",
        "date": "2026-05-18",
        "location": "Los Angeles River, CA, US",
        "observer": "Simon Willison",
        "trip_notes": (
            "Morning walk along the LA River. Primary target was Brown Pelican -- "
            "successfully spotted near the channel. Bonus sighting of Canada Goose "
            "goslings near the swan boat lake. Glaucous-winged Gull is uncommon for "
            "SoCal and worth flagging for community review."
        ),
        "sightings": [
            {
                "common_name": "Glaucous-winged Gull",
                "count": 1,
                "photos": 2,
                "notes": "Observed along the river channel. Uncommon for this region -- verify ID.",
            },
            {
                "common_name": "Brown Pelican",
                "count": 1,
                "photos": 1,
                "notes": "Single individual spotted near the river; photo quality limited.",
            },
            {
                "common_name": "Snowy Egret",
                "count": 1,
                "photos": 2,
                "notes": "Wading near the bank. Clear view of yellow feet (key field mark).",
            },
            {
                "common_name": "Canada Goose",
                "count": "2+",
                "photos": 2,
                "location": "Swan boat lake area, Los Angeles River, CA, US",
                "notes": "Adults with goslings observed. Active nesting behavior.",
            },
        ],
    }

    report = parse_sightings_from_dict(data)

    print("=" * 70)
    print("  iNaturalist Wildlife Sighting Logger -- Demo Output")
    print("=" * 70)
    print()

    # Markdown output
    md = report.to_markdown()
    print(md)

    # JSON output
    print("=" * 70)
    print("  JSON Export (for programmatic use)")
    print("=" * 70)
    print(report.to_json())

    # Write outputs to files
    with open("sighting_report.md", "w") as f:
        f.write(md)
    with open("sighting_report.json", "w") as f:
        f.write(report.to_json())

    print()
    print(f"[OK] Markdown report written to: sighting_report.md")
    print(f"[OK] JSON export written to:     sighting_report.json")
    print(f"[OK] {len(report.sightings)} species logged, ready for iNaturalist upload.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # Accept JSON from stdin
        input_data = json.load(sys.stdin)
        report = parse_sightings_from_dict(input_data)
        print(report.to_markdown())
    else:
        demo()
