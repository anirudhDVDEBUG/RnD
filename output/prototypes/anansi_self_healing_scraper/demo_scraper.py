#!/usr/bin/env python3
"""
Anansi Self-Healing Scraper — Local Demo

Simulates Anansi's core behavior without requiring pip install of the real package:
  1. Fetches a live page via requests (or falls back to mock HTML)
  2. Extracts data with CSS selectors (BeautifulSoup)
  3. Demonstrates "self-healing": when a selector fails, it searches for
     semantically similar elements and repairs the selector automatically.
  4. Shows stealth-mode metadata (TLS fingerprint, user-agent rotation).
"""

import json
import time
import random
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Mock HTML pages — used when requests/BS4 are available, or as pure fallback
# ---------------------------------------------------------------------------

MOCK_PAGES = {
    "https://example-shop.com/products": """
    <html><head><title>Example Shop</title></head>
    <body>
      <div class="product-listing">
        <div class="product-card" data-id="1">
          <h2 class="product-name">Wireless Headphones</h2>
          <span class="product-price">$79.99</span>
          <span class="stock-status in-stock">In Stock</span>
          <a href="/products/1" class="product-link">View</a>
        </div>
        <div class="product-card" data-id="2">
          <h2 class="product-name">Mechanical Keyboard</h2>
          <span class="product-price">$149.00</span>
          <span class="stock-status in-stock">In Stock</span>
          <a href="/products/2" class="product-link">View</a>
        </div>
        <div class="product-card" data-id="3">
          <h2 class="product-name">USB-C Hub</h2>
          <span class="product-price">$34.50</span>
          <span class="stock-status out-of-stock">Out of Stock</span>
          <a href="/products/3" class="product-link">View</a>
        </div>
      </div>
    </body></html>
    """,
    # Same page after a redesign — class names changed
    "https://example-shop.com/products?v2": """
    <html><head><title>Example Shop v2</title></head>
    <body>
      <div class="catalog-grid">
        <article class="item-tile" data-product-id="1">
          <h3 class="item-title">Wireless Headphones</h3>
          <div class="item-pricing">$79.99</div>
          <span class="availability available">In Stock</span>
          <a href="/shop/1" class="item-detail-link">Details</a>
        </article>
        <article class="item-tile" data-product-id="2">
          <h3 class="item-title">Mechanical Keyboard</h3>
          <div class="item-pricing">$149.00</div>
          <span class="availability available">In Stock</span>
          <a href="/shop/2" class="item-detail-link">Details</a>
        </article>
        <article class="item-tile" data-product-id="3">
          <h3 class="item-title">USB-C Hub</h3>
          <div class="item-pricing">$34.50</div>
          <span class="availability unavailable">Out of Stock</span>
          <a href="/shop/3" class="item-detail-link">Details</a>
        </article>
      </div>
    </body></html>
    """,
}

# ---------------------------------------------------------------------------
# Stealth / TLS fingerprint simulation
# ---------------------------------------------------------------------------

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

TLS_CIPHERS = [
    "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
]


def chrome_tls_fingerprint():
    """Simulate a Chrome-like JA3 TLS fingerprint."""
    ja3_raw = f"771,{','.join(str(random.randint(49150,49200)) for _ in range(12))},0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0"
    ja3_hash = hashlib.md5(ja3_raw.encode()).hexdigest()
    return {"ja3_raw_sample": ja3_raw[:60] + "...", "ja3_hash": ja3_hash}


# ---------------------------------------------------------------------------
# Self-healing selector engine
# ---------------------------------------------------------------------------

# Heuristic: map semantic roles to fallback selector patterns
SELECTOR_HEALING_MAP = {
    "name": ["[class*='name']", "[class*='title']", "h1", "h2", "h3", "h4", "[itemprop='name']"],
    "price": ["[class*='price']", "[class*='pricing']", "[class*='cost']", "[itemprop='price']"],
    "status": ["[class*='stock']", "[class*='availability']", "[class*='avail']"],
    "link": ["a[href]", "[class*='link']", "[class*='detail']"],
}


@dataclass
class HealingResult:
    original_selector: str
    healed_selector: Optional[str]
    succeeded: bool
    attempts: int


@dataclass
class ScrapeResult:
    url: str
    data: List[Dict]
    healing_log: List[HealingResult] = field(default_factory=list)
    stealth_info: Dict = field(default_factory=dict)
    elapsed_ms: int = 0


def _try_select(soup, selector: str):
    """Try a CSS selector, return list of matched elements or empty list."""
    try:
        return soup.select(selector)
    except Exception:
        return []


def _heal_selector(soup, role: str, original: str) -> HealingResult:
    """Attempt to find a working selector when the original fails."""
    candidates = SELECTOR_HEALING_MAP.get(role, [])
    for i, candidate in enumerate(candidates, 1):
        matches = _try_select(soup, candidate)
        if matches:
            return HealingResult(
                original_selector=original,
                healed_selector=candidate,
                succeeded=True,
                attempts=i,
            )
    return HealingResult(
        original_selector=original,
        healed_selector=None,
        succeeded=False,
        attempts=len(candidates),
    )


def scrape(url: str, selectors: Dict[str, str], stealth: bool = True) -> ScrapeResult:
    """
    Core scrape function.
    - Fetches HTML (from mock pages in this demo).
    - Applies CSS selectors via BeautifulSoup.
    - Self-heals broken selectors by probing alternatives.
    """
    from bs4 import BeautifulSoup

    start = time.time()

    # Resolve HTML
    html = MOCK_PAGES.get(url)
    if html is None:
        # Try live fetch
        try:
            import requests
            ua = random.choice(USER_AGENTS)
            resp = requests.get(url, headers={"User-Agent": ua}, timeout=10)
            resp.raise_for_status()
            html = resp.text
        except Exception:
            html = list(MOCK_PAGES.values())[0]  # fallback

    soup = BeautifulSoup(html, "html.parser")

    # Stealth metadata
    stealth_info = {}
    if stealth:
        stealth_info = {
            "user_agent": random.choice(USER_AGENTS),
            "tls_fingerprint": chrome_tls_fingerprint(),
            "stealth_mode": True,
        }

    # Extract data per selector, with self-healing
    healing_log = []

    # Find all "item containers" — product cards, tiles, articles, etc.
    container_selectors = [".product-card", ".item-tile", "article", ".card", "tr"]
    containers = []
    for cs in container_selectors:
        containers = _try_select(soup, cs)
        if containers:
            break

    if not containers:
        # Fallback: treat whole page as one container
        containers = [soup]

    extracted = []
    for container in containers:
        row = {}
        for role, selector in selectors.items():
            matches = _try_select(container, selector)
            if matches:
                row[role] = matches[0].get_text(strip=True)
            else:
                # Self-heal
                heal = _heal_selector(container, role, selector)
                healing_log.append(heal)
                if heal.succeeded and heal.healed_selector:
                    healed_matches = _try_select(container, heal.healed_selector)
                    if healed_matches:
                        row[role] = healed_matches[0].get_text(strip=True)
                    else:
                        row[role] = None
                else:
                    row[role] = None
        if any(v is not None for v in row.values()):
            extracted.append(row)

    elapsed = int((time.time() - start) * 1000)

    return ScrapeResult(
        url=url,
        data=extracted,
        healing_log=healing_log,
        stealth_info=stealth_info,
        elapsed_ms=elapsed,
    )


# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------

def _print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def run_demo():
    print("Anansi Self-Healing Scraper — Demo")
    print("=" * 60)

    # --- Demo 1: Normal scrape ---
    _print_section("DEMO 1: Normal Scrape (selectors match)")
    selectors = {
        "name": ".product-name",
        "price": ".product-price",
        "status": ".stock-status",
    }
    result = scrape("https://example-shop.com/products", selectors, stealth=True)
    print(f"\nURL: {result.url}")
    print(f"Extracted {len(result.data)} items in {result.elapsed_ms}ms")
    print(f"\nData:")
    for item in result.data:
        print(f"  {json.dumps(item)}")
    print(f"\nSelector healing needed: {len(result.healing_log)} repairs")

    # --- Demo 2: Site redesign — selectors break, self-healing kicks in ---
    _print_section("DEMO 2: Site Redesign — Self-Healing Selectors")
    print("\nUsing SAME selectors on redesigned page (classes changed)...")
    print(f"  Original selectors: {json.dumps(selectors, indent=4)}")
    result2 = scrape("https://example-shop.com/products?v2", selectors, stealth=True)
    print(f"\nURL: {result2.url}")
    print(f"Extracted {len(result2.data)} items in {result2.elapsed_ms}ms")
    print(f"\nData (recovered via self-healing):")
    for item in result2.data:
        print(f"  {json.dumps(item)}")
    print(f"\nHealing log ({len(result2.healing_log)} repairs):")
    for h in result2.healing_log:
        status = "HEALED" if h.succeeded else "FAILED"
        print(f"  [{status}] '{h.original_selector}' -> '{h.healed_selector}' ({h.attempts} attempts)")

    # --- Demo 3: Stealth / TLS fingerprint info ---
    _print_section("DEMO 3: Stealth Mode — TLS Fingerprint")
    print(f"\nStealth metadata:")
    print(json.dumps(result2.stealth_info, indent=2))

    # --- Summary ---
    _print_section("SUMMARY")
    print(f"""
  - Scraped 2 versions of the same page
  - Original selectors worked on v1 ({len(result.data)} items, 0 heals)
  - Same selectors BROKE on v2 but self-healed ({len(result2.data)} items, {len(result2.healing_log)} heals)
  - Stealth mode simulated Chrome TLS fingerprint
  - No API keys required, no external services needed

  Ready to try the real thing? pip install anansi-scraper
""")


if __name__ == "__main__":
    run_demo()
