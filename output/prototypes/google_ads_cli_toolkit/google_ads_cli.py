#!/usr/bin/env python3
"""
Google Ads CLI Toolkit - Mock Demo
Simulates the google-ads-cli-toolkit workflow for evaluation purposes.
Uses mock data so no API keys are required.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
import random

# ─── Mock Data ───────────────────────────────────────────────────────────────

MOCK_CAMPAIGNS = [
    {"id": "123456789", "name": "Brand Awareness - Q2 2026", "status": "ENABLED",
     "budget_micros": 50_000_000, "type": "SEARCH", "bidding": "TARGET_CPA"},
    {"id": "987654321", "name": "Competitor Keywords", "status": "ENABLED",
     "budget_micros": 30_000_000, "type": "SEARCH", "bidding": "MAXIMIZE_CONVERSIONS"},
    {"id": "456789123", "name": "Display Remarketing - Summer", "status": "PAUSED",
     "budget_micros": 20_000_000, "type": "DISPLAY", "bidding": "TARGET_ROAS"},
    {"id": "321654987", "name": "YouTube Pre-Roll Ads", "status": "ENABLED",
     "budget_micros": 75_000_000, "type": "VIDEO", "bidding": "CPV"},
    {"id": "654321789", "name": "Shopping - Electronics", "status": "ENABLED",
     "budget_micros": 100_000_000, "type": "SHOPPING", "bidding": "MAXIMIZE_CLICKS"},
]

def _generate_metrics(campaign):
    random.seed(hash(campaign["id"]))
    impressions = random.randint(5000, 500000)
    clicks = int(impressions * random.uniform(0.01, 0.08))
    ctr = clicks / impressions if impressions else 0
    cost = clicks * random.uniform(0.50, 4.50)
    conversions = int(clicks * random.uniform(0.02, 0.15))
    conv_value = conversions * random.uniform(25.0, 150.0)
    return {
        "impressions": impressions,
        "clicks": clicks,
        "ctr": round(ctr * 100, 2),
        "avg_cpc": round(cost / clicks, 2) if clicks else 0,
        "cost": round(cost, 2),
        "conversions": conversions,
        "conv_rate": round((conversions / clicks * 100), 2) if clicks else 0,
        "conv_value": round(conv_value, 2),
        "roas": round(conv_value / cost, 2) if cost else 0,
    }

MOCK_AD_GROUPS = {
    "123456789": [
        {"id": "ag_001", "name": "Exact Match - Brand Terms", "status": "ENABLED", "cpc_bid": 2.50},
        {"id": "ag_002", "name": "Broad Match - Generic", "status": "ENABLED", "cpc_bid": 1.80},
    ],
    "987654321": [
        {"id": "ag_003", "name": "Competitor - Direct", "status": "ENABLED", "cpc_bid": 3.20},
        {"id": "ag_004", "name": "Competitor - Alternatives", "status": "PAUSED", "cpc_bid": 2.90},
    ],
}

MOCK_KEYWORDS = {
    "ag_001": [
        {"text": "brand name official", "match_type": "EXACT", "status": "ENABLED", "quality_score": 9},
        {"text": "brand name buy", "match_type": "EXACT", "status": "ENABLED", "quality_score": 8},
    ],
    "ag_003": [
        {"text": "competitor alternative", "match_type": "PHRASE", "status": "ENABLED", "quality_score": 6},
        {"text": "vs competitor", "match_type": "BROAD", "status": "ENABLED", "quality_score": 5},
    ],
}

MOCK_GTM_CONTAINERS = [
    {"id": "GTM-ABC123", "name": "Main Website", "tags": 24, "triggers": 18, "variables": 31},
    {"id": "GTM-DEF456", "name": "Landing Pages", "tags": 8, "triggers": 6, "variables": 12},
]

MOCK_GA4_REPORT = {
    "property": "properties/123456",
    "date_range": "last_28_days",
    "rows": [
        {"source": "google / cpc", "sessions": 12450, "users": 9830, "conversions": 342, "revenue": 28500.00},
        {"source": "google / organic", "sessions": 8920, "users": 7100, "conversions": 198, "revenue": 15200.00},
        {"source": "(direct) / (none)", "sessions": 5430, "users": 4200, "conversions": 87, "revenue": 6800.00},
        {"source": "facebook / cpc", "sessions": 3200, "users": 2800, "conversions": 45, "revenue": 3200.00},
        {"source": "email / newsletter", "sessions": 1890, "users": 1650, "conversions": 112, "revenue": 9400.00},
    ],
}


# ─── CLI Commands ────────────────────────────────────────────────────────────

def cmd_campaigns(args):
    """List campaigns with performance metrics."""
    print(f"\n{'='*90}")
    print(f"  GOOGLE ADS CAMPAIGNS — Customer ID: {args.customer_id}")
    print(f"{'='*90}")
    print(f"\n{'Campaign':<35} {'Status':<10} {'Budget/day':<12} {'Type':<10} {'Bidding':<20}")
    print(f"{'-'*35} {'-'*10} {'-'*12} {'-'*10} {'-'*20}")
    for c in MOCK_CAMPAIGNS:
        budget = f"${c['budget_micros']/1_000_000:.2f}"
        print(f"{c['name']:<35} {c['status']:<10} {budget:<12} {c['type']:<10} {c['bidding']:<20}")

    if args.metrics:
        print(f"\n{'Campaign':<35} {'Impr':>10} {'Clicks':>8} {'CTR':>7} {'CPC':>7} {'Cost':>10} {'Conv':>6} {'ROAS':>6}")
        print(f"{'-'*35} {'-'*10} {'-'*8} {'-'*7} {'-'*7} {'-'*10} {'-'*6} {'-'*6}")
        for c in MOCK_CAMPAIGNS:
            m = _generate_metrics(c)
            print(f"{c['name']:<35} {m['impressions']:>10,} {m['clicks']:>8,} {m['ctr']:>6.2f}% ${m['avg_cpc']:>5.2f} ${m['cost']:>9,.2f} {m['conversions']:>6} {m['roas']:>5.2f}x")
    print()


def cmd_query(args):
    """Execute a GAQL query (mock)."""
    print(f"\n  GAQL Query Execution (mock)")
    print(f"  Customer ID: {args.customer_id}")
    print(f"  Query: {args.gaql}\n")

    gaql_lower = args.gaql.lower()
    if "campaign" in gaql_lower:
        results = [{"campaign.id": c["id"], "campaign.name": c["name"],
                     "campaign.status": c["status"], **_generate_metrics(c)}
                    for c in MOCK_CAMPAIGNS[:3]]
    elif "ad_group" in gaql_lower:
        results = [{"ad_group.id": ag["id"], "ad_group.name": ag["name"],
                     "ad_group.status": ag["status"]}
                    for ags in MOCK_AD_GROUPS.values() for ag in ags]
    else:
        results = [{"message": "Query parsed successfully. No matching mock data for this resource type."}]

    print(f"  Results ({len(results)} rows):")
    print(f"  {json.dumps(results, indent=2)}\n")


def cmd_gtm(args):
    """Show GTM containers."""
    print(f"\n{'='*70}")
    print(f"  GOOGLE TAG MANAGER — Containers")
    print(f"{'='*70}")
    print(f"\n{'Container ID':<16} {'Name':<25} {'Tags':>6} {'Triggers':>10} {'Variables':>10}")
    print(f"{'-'*16} {'-'*25} {'-'*6} {'-'*10} {'-'*10}")
    for c in MOCK_GTM_CONTAINERS:
        print(f"{c['id']:<16} {c['name']:<25} {c['tags']:>6} {c['triggers']:>10} {c['variables']:>10}")
    print()


def cmd_ga4(args):
    """Show GA4 traffic report."""
    report = MOCK_GA4_REPORT
    print(f"\n{'='*85}")
    print(f"  GA4 ANALYTICS REPORT — {report['property']} — {report['date_range']}")
    print(f"{'='*85}")
    print(f"\n{'Source / Medium':<30} {'Sessions':>10} {'Users':>10} {'Conversions':>12} {'Revenue':>12}")
    print(f"{'-'*30} {'-'*10} {'-'*10} {'-'*12} {'-'*12}")
    total_sessions = total_users = total_conv = 0
    total_rev = 0.0
    for r in report["rows"]:
        print(f"{r['source']:<30} {r['sessions']:>10,} {r['users']:>10,} {r['conversions']:>12,} ${r['revenue']:>10,.2f}")
        total_sessions += r["sessions"]
        total_users += r["users"]
        total_conv += r["conversions"]
        total_rev += r["revenue"]
    print(f"{'-'*30} {'-'*10} {'-'*10} {'-'*12} {'-'*12}")
    print(f"{'TOTAL':<30} {total_sessions:>10,} {total_users:>10,} {total_conv:>12,} ${total_rev:>10,.2f}")
    print()


def cmd_status(args):
    """Show overall account status summary."""
    print(f"\n{'='*60}")
    print(f"  ACCOUNT STATUS — {args.customer_id}")
    print(f"{'='*60}")
    enabled = sum(1 for c in MOCK_CAMPAIGNS if c["status"] == "ENABLED")
    paused = sum(1 for c in MOCK_CAMPAIGNS if c["status"] == "PAUSED")
    total_budget = sum(c["budget_micros"] for c in MOCK_CAMPAIGNS) / 1_000_000
    total_cost = sum(_generate_metrics(c)["cost"] for c in MOCK_CAMPAIGNS)
    total_conv = sum(_generate_metrics(c)["conversions"] for c in MOCK_CAMPAIGNS)

    print(f"\n  Campaigns:     {len(MOCK_CAMPAIGNS)} total ({enabled} enabled, {paused} paused)")
    print(f"  Daily Budget:  ${total_budget:,.2f}")
    print(f"  Period Cost:   ${total_cost:,.2f}")
    print(f"  Conversions:   {total_conv:,}")
    print(f"  GTM Containers: {len(MOCK_GTM_CONTAINERS)}")
    print(f"  GA4 Sources:   {len(MOCK_GA4_REPORT['rows'])}")
    print(f"\n  Status: All systems operational (mock mode)")
    print()


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Google Ads CLI Toolkit — Manage Google Ads, GTM & GA4 from the terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--customer-id", default="123-456-7890",
                        help="Google Ads customer ID (default: 123-456-7890)")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # campaigns
    p_camp = sub.add_parser("campaigns", help="List campaigns and performance")
    p_camp.add_argument("--metrics", action="store_true", help="Include performance metrics")

    # query
    p_query = sub.add_parser("query", help="Execute a GAQL query")
    p_query.add_argument("gaql", help="GAQL query string")

    # gtm
    sub.add_parser("gtm", help="List GTM containers")

    # ga4
    sub.add_parser("ga4", help="Show GA4 analytics report")

    # status
    sub.add_parser("status", help="Account status summary")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "campaigns": cmd_campaigns,
        "query": cmd_query,
        "gtm": cmd_gtm,
        "ga4": cmd_ga4,
        "status": cmd_status,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
