"""Fetch observations from the iNaturalist API v1."""

import httpx


def fetch_observations(username: str, page: int = 1, per_page: int = 30, since: str = None):
    """Fetch observations from iNaturalist API v1."""
    params = {
        "user_login": username,
        "order": "desc",
        "order_by": "observed_on",
        "per_page": per_page,
        "page": page,
        "photos": "true",
    }
    if since:
        params["d1"] = since

    resp = httpx.get("https://api.inaturalist.org/v1/observations", params=params)
    resp.raise_for_status()
    return resp.json()
