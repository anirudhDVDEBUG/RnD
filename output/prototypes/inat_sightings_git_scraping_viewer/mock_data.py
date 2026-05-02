#!/usr/bin/env python3
"""Generate realistic mock clumps.json for demo purposes (no API key needed)."""
import json
import random

SPECIES = [
    ("Western Fence Lizard", "Sceloporus occidentalis", "reptile"),
    ("Anna's Hummingbird", "Calypte anna", "bird"),
    ("California Poppy", "Eschscholzia californica", "plant"),
    ("Monarch Butterfly", "Danaus plexippus", "insect"),
    ("Western Bluebird", "Sialia mexicana", "bird"),
    ("Coast Live Oak", "Quercus agrifolia", "plant"),
    ("Red-tailed Hawk", "Buteo jamaicensis", "bird"),
    ("Pacific Tree Frog", "Pseudacris regilla", "amphibian"),
    ("Turkey Vulture", "Cathartes aura", "bird"),
    ("California Scrub-Jay", "Aphelocoma californica", "bird"),
    ("Black Phoebe", "Sayornis nigricans", "bird"),
    ("Coyote Brush", "Baccharis pilularis", "plant"),
    ("Western Tiger Swallowtail", "Papilio rutulus", "insect"),
    ("Great Blue Heron", "Ardea herodias", "bird"),
    ("California Towhee", "Melozone crissalis", "bird"),
]

PLACES = [
    ("Golden Gate Park, San Francisco, CA", 37.7694, -122.4862),
    ("Muir Woods, Mill Valley, CA", 37.8970, -122.5811),
    ("Point Reyes National Seashore, CA", 38.0682, -122.8783),
    ("Big Basin Redwoods, Boulder Creek, CA", 37.1750, -122.2228),
    ("Mount Tamalpais, CA", 37.9235, -122.5965),
]

# Placeholder images from picsum (CC0) — used as stand-ins for iNat thumbnails
PHOTO_IDS = [237, 433, 582, 659, 718, 783, 790, 837, 870, 1003, 1015, 1024, 1025, 1074, 1084]


def make_photo(seed):
    pid = PHOTO_IDS[seed % len(PHOTO_IDS)]
    return {
        "small": f"https://picsum.photos/id/{pid}/240/240",
        "large": f"https://picsum.photos/id/{pid}/1024/1024",
    }


def generate():
    random.seed(42)
    clumps = []
    obs_id = 100000

    for clump_idx in range(6):
        place_name, base_lat, base_lon = random.choice(PLACES)
        num_obs = random.randint(2, 5)
        observations = []

        for i in range(num_obs):
            common, scientific, _group = random.choice(SPECIES)
            obs_id += random.randint(1, 100)
            day = random.randint(1, 28)
            month = random.choice([3, 4, 5])
            observations.append(
                {
                    "id": obs_id,
                    "species_guess": common,
                    "common_name": common,
                    "scientific_name": scientific,
                    "photos": [make_photo(obs_id + j) for j in range(random.randint(1, 3))],
                    "observed_on": f"2026-{month:02d}-{day:02d} 10:{random.randint(0,59):02d}",
                    "place_guess": place_name,
                    "latitude": round(base_lat + random.uniform(-0.01, 0.01), 5),
                    "longitude": round(base_lon + random.uniform(-0.01, 0.01), 5),
                }
            )
        clumps.append({"observations": observations})

    return clumps


if __name__ == "__main__":
    data = generate()
    with open("clumps.json", "w") as f:
        json.dump(data, f, indent=2)
    total = sum(len(c["observations"]) for c in data)
    print(f"Generated {len(data)} clumps with {total} observations -> clumps.json")
