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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


def parse_date(obs):
    """Extract a sortable datetime string from an observation."""
    details = obs.get("observed_on_details") or {}
    return details.get("date", obs.get("observed_on", ""))


@click.command()
@click.argument("usernames", nargs=-1, required=True)
@click.option("--hours", default=2, help="Max hours between observations in a clump")
@click.option("--km", default=5.0, help="Max km between observations in a clump")
@click.option("--output", "-o", default="clumps.json")
def cli(usernames, hours, km, output):
    """Fetch observations for one or more iNaturalist usernames and group into clumps."""
    observations = []
    for username in usernames:
        click.echo(f"Fetching observations for {username}...")
        page = 1
        while True:
            resp = httpx.get(
                "https://api.inaturalist.org/v1/observations",
                params={
                    "user_login": username,
                    "per_page": 200,
                    "page": page,
                    "order": "asc",
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data["results"]
            if not results:
                break
            observations.extend(results)
            click.echo(f"  page {page}: {len(results)} observations")
            page += 1

    observations.sort(key=parse_date)

    # Clump by time and distance proximity
    clumps = []
    current_clump = []
    for obs in observations:
        if not current_clump:
            current_clump.append(obs)
            continue
        last = current_clump[-1]

        # Check geographic proximity
        geo_ok = True
        if obs.get("geojson") and last.get("geojson"):
            d = haversine(
                last["geojson"]["coordinates"][0],
                last["geojson"]["coordinates"][1],
                obs["geojson"]["coordinates"][0],
                obs["geojson"]["coordinates"][1],
            )
            geo_ok = d <= km

        # Check temporal proximity
        time_ok = True
        last_date = parse_date(last)
        obs_date = parse_date(obs)
        if last_date and obs_date:
            try:
                t1 = datetime.fromisoformat(last_date)
                t2 = datetime.fromisoformat(obs_date)
                time_ok = abs((t2 - t1).total_seconds()) <= hours * 3600
            except ValueError:
                pass

        if time_ok and geo_ok:
            current_clump.append(obs)
        else:
            clumps.append(current_clump)
            current_clump = [obs]
    if current_clump:
        clumps.append(current_clump)

    # Serialize to lightweight JSON
    output_data = []
    for clump in clumps:
        output_data.append(
            {
                "observations": [
                    {
                        "id": o["id"],
                        "species_guess": o.get("species_guess"),
                        "common_name": (o.get("taxon") or {}).get(
                            "preferred_common_name"
                        ),
                        "scientific_name": (o.get("taxon") or {}).get("name"),
                        "photos": [
                            {
                                "small": p["url"].replace("square", "small"),
                                "large": p["url"].replace("square", "large"),
                            }
                            for p in (o.get("photos") or [])
                        ],
                        "observed_on": o.get("observed_on_string"),
                        "place_guess": o.get("place_guess"),
                        "latitude": (o.get("geojson") or {}).get("coordinates", [None, None])[1],
                        "longitude": (o.get("geojson") or {}).get("coordinates", [None, None])[0],
                    }
                    for o in clump
                ],
            }
        )

    with open(output, "w") as f:
        json.dump(output_data, f, indent=2)
    click.echo(f"Wrote {len(output_data)} clumps ({sum(len(c['observations']) for c in output_data)} observations) to {output}")


if __name__ == "__main__":
    cli()
