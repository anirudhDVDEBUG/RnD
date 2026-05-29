#!/usr/bin/env python3
"""
Domain availability checker using the digmyname.com API.
Falls back to mock data when the API is unreachable.
"""

import json
import sys
import urllib.request
import urllib.error
from typing import List, Optional

API_BASE = "https://api.digmyname.com/check"
DEFAULT_TLDS = ["com", "net", "io", "dev", "ai", "co", "org", "app", "xyz"]

# Mock data used when the API is unreachable (demo/offline mode)
MOCK_RESULTS = {
    "com": {"available": False, "registrars": [
        {"name": "Namecheap", "price": "$8.88"},
        {"name": "GoDaddy", "price": "$9.99"},
    ]},
    "net": {"available": True, "registrars": [
        {"name": "Namecheap", "price": "$10.98"},
        {"name": "Cloudflare", "price": "$9.77"},
    ]},
    "io": {"available": True, "registrars": [
        {"name": "Namecheap", "price": "$28.88"},
        {"name": "Porkbun", "price": "$25.99"},
    ]},
    "dev": {"available": True, "registrars": [
        {"name": "Cloudflare", "price": "$10.11"},
        {"name": "Google Domains", "price": "$12.00"},
    ]},
    "ai": {"available": False, "registrars": [
        {"name": "Namecheap", "price": "$58.98"},
        {"name": "GoDaddy", "price": "$64.99"},
    ]},
    "co": {"available": True, "registrars": [
        {"name": "Namecheap", "price": "$11.98"},
        {"name": "Porkbun", "price": "$10.87"},
    ]},
    "org": {"available": False, "registrars": [
        {"name": "Namecheap", "price": "$9.98"},
        {"name": "Cloudflare", "price": "$8.57"},
    ]},
    "app": {"available": True, "registrars": [
        {"name": "Cloudflare", "price": "$14.00"},
        {"name": "Google Domains", "price": "$14.00"},
    ]},
    "xyz": {"available": True, "registrars": [
        {"name": "Namecheap", "price": "$1.98"},
        {"name": "Porkbun", "price": "$1.00"},
    ]},
}


def check_domain_live(name: str, tlds: List[str]) -> Optional[dict]:
    """Try the live digmyname.com API. Returns None on failure."""
    tld_param = ",".join(tlds)
    url = f"{API_BASE}?domain={name}&tlds={tld_param}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "domain-check-proto/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception):
        return None


def check_domain_mock(name: str, tlds: List[str]) -> dict:
    """Return mock results for demo/offline use."""
    results = []
    for tld in tlds:
        mock = MOCK_RESULTS.get(tld, {"available": True, "registrars": []})
        results.append({
            "domain": f"{name}.{tld}",
            "available": mock["available"],
            "registrars": mock["registrars"],
        })
    return {"query": name, "results": results, "source": "mock"}


def format_table(data: dict) -> str:
    """Format results as a readable table."""
    lines = []
    source = data.get("source", "live API")
    lines.append(f"Domain availability for: {data['query']}  (source: {source})")
    lines.append("")
    lines.append(f"{'Domain':<25} {'Status':<12} {'Best Price':<14} {'Registrar'}")
    lines.append("-" * 70)

    for r in data["results"]:
        domain = r["domain"]
        status = "AVAILABLE" if r["available"] else "TAKEN"
        registrars = r.get("registrars", [])
        if registrars:
            best = min(registrars, key=lambda x: float(x["price"].replace("$", "")))
            price = best["price"]
            reg = best["name"]
        else:
            price = "-"
            reg = "-"
        lines.append(f"{domain:<25} {status:<12} {price:<14} {reg}")

    # Summary
    available = [r for r in data["results"] if r["available"]]
    lines.append("")
    lines.append(f"Summary: {len(available)}/{len(data['results'])} domains available")
    if available:
        cheapest = None
        for r in available:
            for reg in r.get("registrars", []):
                p = float(reg["price"].replace("$", ""))
                if cheapest is None or p < cheapest[1]:
                    cheapest = (r["domain"], p, reg["name"])
        if cheapest:
            lines.append(f"Best deal: {cheapest[0]} at ${cheapest[1]:.2f} via {cheapest[2]}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python domain_check.py <name> [tld1,tld2,...]")
        print("Example: python domain_check.py myproject com,io,dev")
        sys.exit(1)

    name = sys.argv[1].split(".")[0]  # strip TLD if user passes full domain
    tlds = sys.argv[2].split(",") if len(sys.argv) > 2 else DEFAULT_TLDS

    print(f"Checking domain availability for '{name}' across {len(tlds)} TLDs...")
    print()

    # Try live API first, fall back to mock
    data = check_domain_live(name, tlds)
    if data and "results" in data:
        data["source"] = "digmyname.com API"
    else:
        print("[INFO] API unreachable — using mock data for demo purposes\n")
        data = check_domain_mock(name, tlds)

    print(format_table(data))
    print()

    # Also dump raw JSON for programmatic use
    print("--- Raw JSON ---")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
