"""Amazon listing optimizer — scores and rewrites titles, bullets, and backend keywords."""

import argparse
import sys

from . import mock_data
from .utils import score_title, score_bullets


OPTIMIZED = {
    "B0EXAMPLE01": {
        "title": "Insulated Water Bottle 32oz - Stainless Steel Vacuum Flask, Keeps Cold 24hrs Hot 12hrs, Leak-Proof Lid, BPA Free Sports Bottle for Gym Hiking Outdoor",
        "bullets": [
            "KEEPS DRINKS ICE COLD 24 HOURS & HOT 12 HOURS - Double-wall vacuum insulation technology locks in temperature so your beverages stay perfectly chilled or piping hot all day long",
            "PREMIUM 18/8 STAINLESS STEEL - Food-grade, BPA-free, rust-proof construction that won't retain flavors or odors, ensuring every sip tastes fresh and clean",
            "LEAK-PROOF DESIGN WITH ONE-HAND LID - Secure twist cap with silicone seal prevents spills in your gym bag, backpack, or car cup holder, opens easily with one hand",
            "PERFECT 32OZ CAPACITY FOR ALL-DAY HYDRATION - Large enough for a full workout session yet fits standard cup holders, ideal for gym, hiking, camping, office, and daily commute",
            "LIFETIME GUARANTEE & ECO-FRIENDLY CHOICE - Replace 2,000+ single-use plastic bottles, backed by our hassle-free lifetime warranty and dedicated customer support team",
        ],
        "backend_keywords": "water bottle insulated stainless steel vacuum flask 32oz cold hot leak proof BPA free gym hiking outdoor camping sports fitness workout travel reusable eco friendly metal thermos double wall",
    },
}


def optimize_listing(asin: str) -> None:
    listing = mock_data.LISTINGS.get(asin)
    if not listing:
        print(f"ASIN {asin} not found in mock data.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  AMAZON LISTING OPTIMIZER")
    print(f"{'='*60}")
    print(f"\n  ASIN: {asin}")
    print(f"  Product: {listing['title']}")
    print(f"  Price: ${listing['price']}  |  Category: {listing['category']}")
    print(f"  Marketplace: {listing['marketplace']}")

    # Score original
    title_score = score_title(listing["title"])
    bullet_score = score_bullets(listing["bullets"])
    orig_bk_count = len(listing["backend_keywords"].split())

    print(f"\n--- ORIGINAL SCORES ---")
    print(f"  Title:           {title_score['score']}/100")
    for issue in title_score["issues"]:
        print(f"    ! {issue}")
    print(f"  Bullets:         {bullet_score['score']}/100")
    for issue in bullet_score["issues"]:
        print(f"    ! {issue}")
    print(f"  Backend KW:      {orig_bk_count} terms")

    # Optimized version
    opt = OPTIMIZED.get(asin)
    if opt:
        new_title_score = score_title(opt["title"])
        new_bullet_score = score_bullets(opt["bullets"])
        new_bk_count = len(opt["backend_keywords"].split())

        print(f"\n--- OPTIMIZED SCORES ---")
        print(f"  Title:           {title_score['score']}/100 -> {new_title_score['score']}/100")
        print(f"  Bullets:         {bullet_score['score']}/100 -> {new_bullet_score['score']}/100")
        print(f"  Backend KW:      {orig_bk_count} -> {new_bk_count} indexed terms")

        print(f"\n--- OPTIMIZED TITLE ---")
        print(f"  {opt['title']}")

        print(f"\n--- OPTIMIZED BULLETS ---")
        for i, bullet in enumerate(opt["bullets"], 1):
            print(f"  {i}. {bullet}")

        print(f"\n--- BACKEND KEYWORDS ---")
        print(f"  {opt['backend_keywords']}")
    else:
        print(f"\n  (No pre-built optimization for this ASIN in demo mode)")

    print()


def main():
    parser = argparse.ArgumentParser(description="Amazon Listing Optimizer")
    parser.add_argument("--asin", default="B0EXAMPLE01", help="ASIN to optimize")
    args = parser.parse_args()
    optimize_listing(args.asin)


if __name__ == "__main__":
    main()
