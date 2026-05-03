#!/usr/bin/env python3
"""Sync iNaturalist sightings and render as static HTML."""

import argparse
import os
import sys

from grouper import group_into_sightings
from renderer import render_all


def main():
    parser = argparse.ArgumentParser(description="Sync iNaturalist sightings to static HTML")
    parser.add_argument("--username", default=os.environ.get("INAT_USERNAME"), help="iNaturalist username")
    parser.add_argument("--mock", action="store_true", help="Use mock data (no API call)")
    parser.add_argument("--backfill", action="store_true", help="Fetch all historical observations")
    parser.add_argument("--since", help="Only fetch observations after this date (YYYY-MM-DD)")
    parser.add_argument("--output", default=os.environ.get("OUTPUT_DIR", "output"), help="Output directory")
    parser.add_argument("--per-page", type=int, default=int(os.environ.get("SIGHTINGS_PER_PAGE", "3")))
    args = parser.parse_args()

    if args.mock or not args.username:
        print("[mock] Loading 12 sample sightings...")
        from mock_data import MOCK_OBSERVATIONS
        observations = MOCK_OBSERVATIONS
    else:
        from fetcher import fetch_observations
        observations = []
        page = 1
        per_page = int(os.environ.get("INAT_PER_PAGE", "30"))
        max_pages = None if args.backfill else 1

        while True:
            print(f"Fetching page {page} from iNaturalist for user '{args.username}'...")
            data = fetch_observations(args.username, page=page, per_page=per_page, since=args.since)
            results = data.get("results", [])
            if not results:
                break
            observations.extend(results)
            if max_pages and page >= max_pages:
                break
            page += 1

        if not observations:
            print("No observations found.")
            sys.exit(0)

    sightings = group_into_sightings(observations)
    print(f"Grouped into {len(sightings)} sighting entries.")

    stats = render_all(sightings, output_dir=args.output, per_page=args.per_page)
    print(f"\nDone. {len(sightings)} sightings, {stats['total_species']} species, {stats['pages']} pages.")
    print(f"Open {args.output}/index.html in your browser.")


if __name__ == "__main__":
    main()
