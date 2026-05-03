"""Group observations by date into sighting entries."""

from itertools import groupby


def group_into_sightings(observations):
    """Group observations by observed_on date into sighting entries."""
    keyfunc = lambda obs: obs["observed_on"]
    sightings = []

    sorted_obs = sorted(observations, key=keyfunc, reverse=True)
    for date, group in groupby(sorted_obs, key=keyfunc):
        obs_list = list(group)
        sightings.append({
            "date": date,
            "place": obs_list[0].get("place_guess", "Unknown location"),
            "species": [
                o["taxon"]["preferred_common_name"]
                for o in obs_list
                if o.get("taxon") and o["taxon"].get("preferred_common_name")
            ],
            "photos": [
                {
                    "url": p["url"].replace("square", "medium"),
                    "label": o["taxon"].get("preferred_common_name", o["taxon"]["name"]),
                }
                for o in obs_list
                if o.get("taxon")
                for p in o.get("photos", [])[:1]
            ],
            "time_start": min(o.get("time_observed_at") or "" for o in obs_list),
            "time_end": max(o.get("time_observed_at") or "" for o in obs_list),
            "source_urls": [o["uri"] for o in obs_list],
        })

    return sightings
