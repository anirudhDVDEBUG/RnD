"""PPC campaign analyzer — evaluates ACoS, identifies waste, recommends optimizations."""

import argparse
import sys

from . import mock_data

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def analyze_campaign(campaign_id: str) -> None:
    campaign = mock_data.PPC_CAMPAIGNS.get(campaign_id)
    if not campaign:
        print(f"Campaign '{campaign_id}' not found. Available: {', '.join(mock_data.PPC_CAMPAIGNS.keys())}")
        sys.exit(1)

    total_spend = campaign["total_spend"]
    total_sales = campaign["total_sales"]
    acos = (total_spend / total_sales * 100) if total_sales > 0 else 0
    roas = total_sales / total_spend if total_spend > 0 else 0
    cpc = total_spend / campaign["clicks"] if campaign["clicks"] > 0 else 0
    ctr = campaign["clicks"] / campaign["impressions"] * 100 if campaign["impressions"] > 0 else 0
    cvr = campaign["total_orders"] / campaign["clicks"] * 100 if campaign["clicks"] > 0 else 0

    print(f"\n{'='*60}")
    print(f"  PPC CAMPAIGN ANALYZER")
    print(f"{'='*60}")
    print(f"\n  Campaign: {campaign['name']}")
    print(f"  Status: {campaign['status']}  |  Running: {campaign['days_running']} days")
    print(f"  Daily budget: ${campaign['daily_budget']:.2f}")

    print(f"\n--- CAMPAIGN METRICS ---")
    print(f"  Total Spend:     ${total_spend:,.2f}")
    print(f"  Total Sales:     ${total_sales:,.2f}")
    print(f"  Orders:          {campaign['total_orders']}")
    print(f"  ACoS:            {acos:.1f}%")
    print(f"  ROAS:            {roas:.2f}x")
    print(f"  CPC:             ${cpc:.2f}")
    print(f"  CTR:             {ctr:.2f}%")
    print(f"  CVR:             {cvr:.1f}%")

    # Analyze search terms
    terms = campaign["search_terms"]
    converting = [t for t in terms if t["orders"] > 0]
    wasted = [t for t in terms if t["orders"] == 0 and t["spend"] > 0]
    wasted_spend = sum(t["spend"] for t in wasted)

    print(f"\n--- SEARCH TERM ANALYSIS ---")
    print(f"  Converting terms:     {len(converting)}/{len(terms)}")
    print(f"  Non-converting terms: {len(wasted)}/{len(terms)}")
    print(f"  Wasted spend:         ${wasted_spend:,.2f} ({wasted_spend/total_spend*100:.1f}% of total)")

    # Top converting terms
    top_converting = sorted(converting, key=lambda t: t["orders"], reverse=True)[:5]
    print(f"\n--- TOP CONVERTING SEARCH TERMS ---")
    if tabulate:
        table = [[t["term"], t["orders"], f"${t['sales']:,.2f}",
                   f"${t['spend']:,.2f}", f"{t['spend']/t['sales']*100:.1f}%"]
                  for t in top_converting]
        print(tabulate(table, headers=["Term", "Orders", "Sales", "Spend", "ACoS"], tablefmt="simple"))
    else:
        for t in top_converting:
            term_acos = t["spend"] / t["sales"] * 100 if t["sales"] > 0 else 0
            print(f"  {t['term']:<30} {t['orders']:>3} orders  ${t['sales']:>8,.2f} sales  ACoS {term_acos:.1f}%")

    # Negative keyword candidates
    print(f"\n--- NEGATIVE KEYWORD CANDIDATES ---")
    for t in wasted:
        print(f"  - \"{t['term']}\" (${t['spend']:.2f} spent, 0 orders, {t['clicks']} clicks)")

    # Recommendations
    optimized_acos = (total_spend - wasted_spend) / total_sales * 100
    print(f"\n--- OPTIMIZATION RECOMMENDATIONS ---")
    print(f"  1. Add {len(wasted)} negative keywords to eliminate ${wasted_spend:.2f} wasted spend")
    print(f"  2. Projected ACoS after cleanup: {acos:.1f}% -> {optimized_acos:.1f}%")
    print(f"  3. Increase bids on top 3 converters (ACoS < 27%)")
    if ctr < 0.5:
        print(f"  4. CTR is low ({ctr:.2f}%) — improve main image and title")
    if cvr < 10:
        print(f"  5. CVR at {cvr:.1f}% — optimize listing content and A+ for better conversion")
    print()


def main():
    parser = argparse.ArgumentParser(description="Amazon PPC Campaign Analyzer")
    parser.add_argument("--campaign", default="demo_campaign", help="Campaign ID")
    args = parser.parse_args()
    analyze_campaign(args.campaign)


if __name__ == "__main__":
    main()
