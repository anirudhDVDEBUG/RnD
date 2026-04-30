"""Seed the business backlog with hand-curated picks.

Idempotent: re-running updates the pitch text but preserves history. Use
this whenever you (the human or Claude) want to mark items as 'this is
worth building'.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from trendforge import store

PICKS = [
    {
        "url": "https://github.com/buluslan/gpt-image2-ecommerce",
        "notes": "Claude skill for D2C product imagery (Shopify-friendly).",
        "pitch": (
            "200-SKU Shopify store needs ~1000 ad-ready images/year. Photo studios "
            "charge Rs 500-2000 per SKU; this skill produces them at API cost (~Rs 2). "
            "Sell as 'Send your product feed, get 1000 ad-ready creatives in 24h' "
            "flat-fee retainer. Bundle with Meta Ads Manager handoff for 2x ASP. "
            "Margin business with zero auth complexity — fastest path to first revenue."
        ),
    },
    {
        "url": "https://github.com/msk3d0ut/claude-skill-ugc-prompt",
        "notes": "Claude skill: second-by-second UGC video-ad prompts for Higgsfield/Sora 2.",
        "pitch": (
            "UGC ads dominate 2026 Meta/TikTok spend. Brands pay Rs 50K-2L per "
            "creator-shot UGC video. With this skill + Higgsfield API key, generate "
            "50 ad variations overnight, A/B test in Meta, iterate creative at a "
            "speed no human shop can match. Productize as '30 video ads in 30 days' "
            "retainer for D2C brands. Skill is the IP; volume + testing loop is the moat."
        ),
    },
    {
        "url": "https://github.com/kycloudtech/website-visual-scorer",
        "notes": "Claude skill: B2B website conversion scoring across 5 dimensions.",
        "pitch": (
            "Direct PitchBot upsell. After cold-email, run prospect's site through "
            "scorer, attach 1-page audit to the second touch: 'Your site scores 4/10 "
            "on CTA hierarchy. Want us to fix it for Rs X?' US CRO consultancies "
            "charge $5-20K for exactly this audit. Conversion of B2B outreach goes up "
            "because you deliver value before asking for the meeting. CRO retainer is the upsell."
        ),
    },
    {
        "url": "https://github.com/masteranime/n8n-claude-skills",
        "notes": "Production Claude Skills for n8n built from 100+ real workflows.",
        "pitch": (
            "n8n is the open-source Zapier — 100K+ active instances. Combining n8n's "
            "reliable workflow runtime with Claude reasoning gives the missing piece: "
            "workflows that adapt instead of break. Self-hosted n8n + Claude skill "
            "library + custom MCP servers, sold as managed offering to Indian SMEs "
            "who can't afford Zapier ($200/mo) and won't trust US clouds with their "
            "data. 100 mid-size clients @ Rs 15K/mo = Rs 1.8 cr ARR with one engineer."
        ),
    },
    {
        "url": "https://github.com/wxtsky/byob",
        "notes": "Bring Your Own Browser — let Claude drive your already-logged-in Chrome.",
        "pitch": (
            "STRATEGIC UNLOCK. Standard browser-use libraries spin up fresh headless "
            "Chrome with no login state. BYOB connects to your real session — Meta "
            "Ads Manager, Shopify Admin, HubSpot, Naukri RESDEX, Gmail. With this:\n"
            "  - ARIA reads RESDEX directly (no API needed)\n"
            "  - PitchBot posts from your real LinkedIn\n"
            "  - Set-and-forget Meta Ads Manager agent becomes possible\n"
            "Pitch: 'Autonomous campaign manager — reads Shopify, manages Meta Ads "
            "every night, kills underperformers, scales winners.' 5% of ad spend "
            "managed; 20 clients @ Rs 5L/mo avg spend = Rs 50L/mo management fees."
        ),
    },
]


def main():
    db = store.DB_PATH
    n_updated = 0
    n_missing = []
    with store.get_conn(db) as conn:
        for p in PICKS:
            cur = conn.execute(
                "UPDATE items SET pinned = 1, notes = ?, business_pitch = ? WHERE url = ?",
                (p["notes"], p["pitch"], p["url"]),
            )
            if cur.rowcount == 0:
                # The repo wasn't in the local DB — insert a stub so the
                # pitch is at least preserved.
                store.insert_item(
                    conn,
                    url=p["url"],
                    source="manual",
                    title=p["url"].rsplit("/", 1)[-1],
                    raw_metadata={"manual": True},
                )
                conn.execute(
                    "UPDATE items SET pinned = 1, notes = ?, business_pitch = ?, status = 'pinned' WHERE url = ?",
                    (p["notes"], p["pitch"], p["url"]),
                )
                n_missing.append(p["url"])
            else:
                conn.execute(
                    "UPDATE items SET status = 'pinned' WHERE url = ?", (p["url"],)
                )
            n_updated += 1
        conn.commit()

    print(f"Updated {n_updated} pinned items. Missing-from-DB inserted as stubs: {n_missing}")


if __name__ == "__main__":
    main()
