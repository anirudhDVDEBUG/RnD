#!/usr/bin/env python3
"""Buy Me A Car - End-to-end used car buying assistant demo.

Demonstrates: listing search, CARFAX analysis, OTD calculation,
dealer outreach, negotiation strategy, and decision tracking.
"""

import sys
from mock_data import (
    MOCK_LISTINGS, MOCK_CARFAX, MOCK_CARFAX_RISKY,
    MOCK_VALUATIONS, BUYER_PROFILE,
)
from state_fees import calc_otd, COMMON_ADDONS


def header(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


# ── 1. Research & Search ─────────────────────────────────────────────────────

def search_listings():
    header("STEP 1: Research & Search")
    bp = BUYER_PROFILE
    print(f"Buyer: {bp['name']}  |  Budget: ${bp['budget']:,}  |  State: {bp['state']}")
    print(f"Preferences: {bp['preferences']}\n")

    fmt = "{:<6} {:<28} {:>7} {:>10} {:<8} {:<14} {:<12}"
    print(fmt.format("Year", "Vehicle", "Miles", "Price", "Type", "Location", "Deal"))
    print("-" * 90)
    for c in MOCK_LISTINGS:
        name = f"{c['make']} {c['model']} {c['trim']}"
        print(fmt.format(
            c["year"], name, f"{c['mileage']:,}", f"${c['asking_price']:,}",
            c["seller_type"], c["location"], c["deal_rating"],
        ))
    print(f"\n  Found {len(MOCK_LISTINGS)} listings matching criteria across "
          f"CarGurus, Autotrader, Cars.com, FB Marketplace.")
    return MOCK_LISTINGS


# ── 2. CARFAX Analysis ──────────────────────────────────────────────────────

def analyze_carfax(report: dict) -> str:
    header(f"STEP 2: CARFAX Analysis - {report['vehicle']}")
    red_flags = []

    if report["salvage_rebuild"]:
        red_flags.append("Salvage/rebuilt title")
    if report["frame_damage"]:
        red_flags.append("Frame damage reported")
    if report["flood_damage"]:
        red_flags.append("Flood damage reported")
    if not report["odometer_ok"]:
        red_flags.append("Odometer discrepancy")
    if report["owners"] > 2:
        red_flags.append(f"Excessive owners ({report['owners']})")
    if report["accidents"] > 0:
        red_flags.append(f"{report['accidents']} accident(s) on record")
    if report["recalls_open"] > 0:
        red_flags.append(f"{report['recalls_open']} open recall(s)")

    # Service regularity check
    gap_months = len(report["service_history"])
    if gap_months < 4 and report.get("owners", 1) > 1:
        red_flags.append("Sparse service history for multi-owner vehicle")

    print(f"  VIN:            {report['vin']}")
    print(f"  Owners:         {report['owners']}")
    print(f"  Accidents:      {report['accidents']}")
    print(f"  Title:          {report['title_status']}")
    print(f"  Service records: {report['service_records']}")
    print(f"  Last serviced:  {report['last_service']}")
    print(f"  Open recalls:   {report['recalls_open']}")

    if red_flags:
        if any(kw in f for f in red_flags for kw in ["Salvage", "Frame", "Flood", "Odometer"]):
            rating = "RED"
        else:
            rating = "YELLOW"
    else:
        rating = "GREEN"

    color_label = {"GREEN": "Clean - low risk", "YELLOW": "Minor concerns", "RED": "Significant risk"}

    print(f"\n  Risk Rating: [{rating}] {color_label[rating]}")
    if red_flags:
        for f in red_flags:
            print(f"    ! {f}")
    else:
        print("    No red flags detected.")

    print("\n  Service Timeline:")
    for svc in report["service_history"]:
        print(f"    {svc['date']}  {svc['mileage']:>6,} mi  {svc['description']}")

    return rating


# ── 3. OTD Price Calculation ─────────────────────────────────────────────────

def calculate_otd(listing: dict, offer_price: float, state: str = "TX"):
    header("STEP 3: OTD Price Calculation")
    vehicle = f"{listing['year']} {listing['make']} {listing['model']} {listing['trim']}"
    print(f"  Vehicle:    {vehicle}")
    print(f"  Asking:     ${listing['asking_price']:,.0f}")
    print(f"  Our offer:  ${offer_price:,.0f}")
    print(f"  State:      {state}\n")

    result = calc_otd(offer_price, state, local_tax_rate=0.02, doc_fee=150)

    print(f"  {'Negotiated price':<25} ${result['negotiated_price']:>10,.2f}")
    print(f"  {'Sales tax':<25} ${result['sales_tax']:>10,.2f}  ({result['sales_tax_rate']*100:.2f}%)")
    print(f"  {'Title & registration':<25} ${result['title_reg_fees']:>10,.2f}")
    print(f"  {'Doc fee':<25} ${result['doc_fee']:>10,.2f}")
    print(f"  {'-'*47}")
    print(f"  {'OTD TOTAL':<25} ${result['otd_total']:>10,.2f}")

    print("\n  Common add-ons to DECLINE:")
    for name, lo, hi, advice in COMMON_ADDONS[:4]:
        print(f"    - {name} (${lo}-${hi}): {advice}")

    return result


# ── 4. Dealer Outreach ───────────────────────────────────────────────────────

def draft_outreach(listing: dict, buyer: dict):
    header("STEP 4: Dealer Outreach Template")
    vehicle = f"{listing['year']} {listing['make']} {listing['model']} {listing['trim']}"
    stock = listing.get("stock_number") or "N/A"

    email = f"""  Subject: Inquiry - {vehicle} (Stock #{stock})

  Hi,

  I'm interested in the {vehicle} listed at ${listing['asking_price']:,}
  (Stock #{stock}). I'm a serious, pre-approved buyer ready to purchase
  this week.

  Could you please provide your best out-the-door price including all
  taxes, fees, and registration for {buyer['state']}? I'm comparing
  offers from several dealers in the area.

  I'd also appreciate confirmation that the vehicle has no undisclosed
  damage and that the CARFAX is clean.

  Thank you,
  {buyer['name']}"""

    print("  EMAIL TEMPLATE:")
    print(email)

    print("\n  TEXT/SMS TEMPLATE:")
    print(f"  Hi, I'm interested in your {vehicle} (Stock #{stock}).")
    print(f"  What's your best OTD price for {buyer['state']}? Comparing offers this week. Thanks!")

    print("\n  PHONE SCRIPT:")
    print(f"  \"Hi, I'm calling about the {vehicle}, stock number {stock}.")
    print(f"   I'm a pre-approved buyer comparing a few options this week.")
    print(f"   What's the best out-the-door price you can offer for a {buyer['state']} buyer?\"")


# ── 5. Negotiation Strategy ──────────────────────────────────────────────────

def negotiation_strategy(listing: dict):
    header("STEP 5: Negotiation Strategy")
    vehicle = f"{listing['year']} {listing['make']} {listing['model']} {listing['trim']}"
    key = vehicle
    vals = MOCK_VALUATIONS.get(key, {"kbb_fair": 0, "edmunds": 0, "nada_clean": 0})

    asking = listing["asking_price"]
    avg_market = (vals["kbb_fair"] + vals["edmunds"] + vals["nada_clean"]) / 3
    days = listing["days_on_market"]

    # Determine aggressiveness based on days on market
    if days > 30:
        discount = 0.08
        urgency = "LOW (sitting 30+ days - dealer motivated)"
    elif days > 14:
        discount = 0.05
        urgency = "MEDIUM"
    else:
        discount = 0.03
        urgency = "HIGH (fresh listing - less room)"

    anchor_offer = round(avg_market * (1 - discount), -2)
    walkaway = round(avg_market * 1.02, -2)

    print(f"  Vehicle:          {vehicle}")
    print(f"  Asking price:     ${asking:,}")
    print(f"  Days on market:   {days}  (Urgency: {urgency})")
    print(f"\n  Market Values:")
    print(f"    KBB Fair:       ${vals['kbb_fair']:,}")
    print(f"    Edmunds:        ${vals['edmunds']:,}")
    print(f"    NADA Clean:     ${vals['nada_clean']:,}")
    print(f"    Average:        ${avg_market:,.0f}")
    print(f"\n  Recommended Strategy:")
    print(f"    Opening offer:  ${anchor_offer:,.0f}  ({discount*100:.0f}% below market avg)")
    print(f"    Target price:   ${avg_market:,.0f}")
    print(f"    Walk-away at:   ${walkaway:,.0f}  (2% above market)")
    print(f"\n  Talking Points:")
    if days > 20:
        print(f"    - Vehicle has been listed {days} days - mention this")
    print(f"    - Reference KBB/Edmunds values to justify offer")
    print(f"    - Mention competing offers from other dealers")
    print(f"    - Be ready to walk away - another deal will come")

    return {"anchor": anchor_offer, "target": avg_market, "walkaway": walkaway}


# ── 6. Decision Tracker ──────────────────────────────────────────────────────

def decision_tracker(listings: list, strategies: dict):
    header("STEP 6: Decision Tracker")

    fmt = "{:<26} {:>8} {:>9} {:>9} {:>10} {:<10} {}"
    print(fmt.format("Vehicle", "Asking", "Offer", "Target", "OTD Est.", "Status", "Notes"))
    print("-" * 100)

    rows = []
    for c in listings:
        vehicle = f"{c['year']} {c['make']} {c['model']} {c['trim']}"
        key = vehicle
        vals = MOCK_VALUATIONS.get(key, {})
        avg = (vals.get("kbb_fair", 0) + vals.get("edmunds", 0) + vals.get("nada_clean", 0)) / 3
        offer = round(avg * 0.95, -2) if avg else c["asking_price"]

        otd_est = calc_otd(avg, "TX", local_tax_rate=0.02, doc_fee=150)["otd_total"] if avg else 0

        if c["deal_rating"] == "Great Deal":
            status = "PRIORITY"
            notes = f"Great deal, {c['days_on_market']}d on market"
        elif c["deal_rating"] == "Good Deal":
            status = "Pending"
            notes = f"Good deal, {c['source']}"
        else:
            status = "Review"
            notes = f"Fair deal - needs CARFAX check"

        print(fmt.format(
            vehicle, f"${c['asking_price']:,}", f"${offer:,.0f}",
            f"${avg:,.0f}", f"${otd_est:,.0f}", status, notes,
        ))
        rows.append({"vehicle": vehicle, "offer": offer, "otd": otd_est, "status": status})

    # Final recommendation
    priority = [r for r in rows if r["status"] == "PRIORITY"]
    if priority:
        best = min(priority, key=lambda x: x["otd"])
        print(f"\n  RECOMMENDATION: Pursue {best['vehicle']} first")
        print(f"  Estimated OTD: ${best['otd']:,.0f} -- best value-to-cost ratio")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "#" * 70)
    print("#  BUY ME A CAR - Used Car Buying Assistant Demo")
    print("#  End-to-end: search -> CARFAX -> OTD -> outreach -> negotiate -> decide")
    print("#" * 70)

    # 1. Search
    listings = search_listings()

    # 2. CARFAX - clean report
    rating_clean = analyze_carfax(MOCK_CARFAX)

    # 2b. CARFAX - risky report
    rating_risky = analyze_carfax(MOCK_CARFAX_RISKY)

    # 3. OTD for top pick
    top_pick = listings[0]  # 2022 Civic EX
    otd = calculate_otd(top_pick, offer_price=23000, state="TX")

    # 4. Outreach
    draft_outreach(top_pick, BUYER_PROFILE)

    # 5. Negotiation
    strat = negotiation_strategy(top_pick)

    # Also show strategy for the best deal
    strat2 = negotiation_strategy(listings[1])  # Corolla - Great Deal, 32 days

    # 6. Decision tracker
    decision_tracker(listings, {})

    print(f"\n{'='*70}")
    print("  Demo complete. In production, Claude uses live data from listing")
    print("  sites, real CARFAX reports, and interactive negotiation tracking.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
