"""
Real Estate Asset Management — Core Analysis Engine

Performs QAR, T-12 analysis, rent roll analysis, valuation,
debt monitoring, and hold/sell/refi scoring.
"""

from datetime import datetime, date
from typing import Any

from portfolio_data import PORTFOLIO


def calc_walt(rent_roll: list[dict]) -> float:
    """Weighted Average Lease Term in years from today."""
    today = date.today()
    total_weighted = 0.0
    total_sf = 0.0
    for t in rent_roll:
        if t["lease_end"] is None or t["lease_end"] == "Rolling":
            continue
        end = datetime.strptime(t["lease_end"], "%Y-%m-%d").date()
        remaining_years = max((end - today).days / 365.25, 0)
        total_weighted += t["sf"] * remaining_years
        total_sf += t["sf"]
    return total_weighted / total_sf if total_sf > 0 else 0.0


def concentration_risk(rent_roll: list[dict]) -> list[dict]:
    """Identify tenants representing >20% of revenue."""
    total_rent = sum(t["annual_rent"] for t in rent_roll)
    if total_rent == 0:
        return []
    risks = []
    for t in rent_roll:
        pct = t["annual_rent"] / total_rent
        if pct > 0.20:
            risks.append({"tenant": t["tenant"], "pct_revenue": pct})
    return risks


def upcoming_expirations(rent_roll: list[dict], months: int = 12) -> list[dict]:
    """Leases expiring within N months."""
    today = date.today()
    results = []
    for t in rent_roll:
        if t["lease_end"] is None or t["lease_end"] == "Rolling":
            continue
        end = datetime.strptime(t["lease_end"], "%Y-%m-%d").date()
        days_remaining = (end - today).days
        if 0 < days_remaining <= months * 30:
            results.append({"tenant": t["tenant"], "sf": t["sf"], "expires": t["lease_end"]})
    return results


def t12_analysis(prop: dict) -> dict:
    """Trailing 12-month operating analysis."""
    noi_list = prop["t12_monthly_noi"]
    rev_list = prop["t12_monthly_revenue"]
    opex_list = prop["t12_monthly_opex"]
    total_noi = sum(noi_list)
    total_rev = sum(rev_list)
    total_opex = sum(opex_list)
    opex_ratio = total_opex / total_rev if total_rev else 0
    return {
        "annual_noi": total_noi,
        "annual_revenue": total_rev,
        "annual_opex": total_opex,
        "opex_ratio": opex_ratio,
        "avg_monthly_noi": total_noi / 12,
        "noi_trend": "Stable" if max(noi_list) - min(noi_list) < 30_000 else "Volatile",
    }


def valuation(prop: dict, exit_cap_rate: float = None) -> dict:
    """Direct cap and sensitivity analysis."""
    t12 = t12_analysis(prop)
    base_cap = prop["cap_rate_acquisition"]
    if exit_cap_rate is None:
        exit_cap_rate = base_cap + 0.005  # assume 50bps expansion
    direct_cap_value = t12["annual_noi"] / base_cap
    scenarios = {}
    for delta in [-0.005, 0, 0.005, 0.01]:
        cap = base_cap + delta
        scenarios[f"{cap*100:.1f}%"] = t12["annual_noi"] / cap
    return {
        "direct_cap_value": direct_cap_value,
        "implied_cap_current": t12["annual_noi"] / prop["acquisition_price"] if prop["acquisition_price"] else 0,
        "sensitivity": scenarios,
    }


def debt_analysis(prop: dict) -> dict:
    """Debt metrics and risk flags."""
    debt = prop["debt"]
    t12 = t12_analysis(prop)
    val = valuation(prop)
    dscr = t12["annual_noi"] / debt["annual_debt_service"] if debt["annual_debt_service"] else 0
    ltv = debt["balance"] / val["direct_cap_value"] if val["direct_cap_value"] else 0
    maturity = datetime.strptime(debt["maturity"], "%Y-%m-%d").date()
    months_to_maturity = (maturity - date.today()).days / 30

    flags = []
    if months_to_maturity <= 24:
        flags.append(f"Maturity in {months_to_maturity:.0f} months")
    if dscr < 1.25:
        flags.append(f"DSCR below 1.25x ({dscr:.2f}x)")
    if ltv > 0.70:
        flags.append(f"LTV above 70% ({ltv:.0%})")

    return {
        "balance": debt["balance"],
        "rate": debt["rate"],
        "rate_type": debt["rate_type"],
        "maturity": debt["maturity"],
        "dscr": dscr,
        "ltv": ltv,
        "months_to_maturity": months_to_maturity,
        "flags": flags,
    }


def hold_sell_refi_score(prop: dict) -> dict:
    """Score hold/sell/refi options."""
    t12 = t12_analysis(prop)
    val = valuation(prop)
    debt_info = debt_analysis(prop)
    walt = calc_walt(prop["rent_roll"])

    # Hold score: lease-up runway + below-market rents
    hold_score = 0
    if prop["occupancy"] < prop["occupancy_budget"]:
        hold_score += 3  # upside from lease-up
    if prop.get("market_rent_psf") and any(
        t["rent_psf"] < prop["market_rent_psf"] * 0.9
        for t in prop["rent_roll"] if t["rent_psf"] > 0
    ):
        hold_score += 2  # mark-to-market upside
    if prop["capex_spent"] < prop["capex_budget"] * 0.5:
        hold_score += 2  # value-add capex still deploying

    # Sell score: stabilized, compressed cap rate, short WALT
    sell_score = 0
    if prop["occupancy"] >= prop["occupancy_budget"]:
        sell_score += 3
    if walt < 3.0:
        sell_score += 2  # rollover risk makes sell attractive
    if val["direct_cap_value"] > prop["acquisition_price"] * 1.15:
        sell_score += 2  # meaningful appreciation

    # Refi score: near-term maturity, rate savings possible
    refi_score = 0
    if debt_info["months_to_maturity"] <= 24:
        refi_score += 4
    if debt_info["rate"] > 0.055:
        refi_score += 2  # potential rate improvement
    if debt_info["dscr"] > 1.40:
        refi_score += 1  # strong coverage supports refi

    scores = {"Hold": hold_score, "Sell": sell_score, "Refi": refi_score}
    recommendation = max(scores, key=scores.get)

    return {
        "scores": scores,
        "recommendation": recommendation,
        "rationale": _rationale(recommendation, prop, debt_info, val),
    }


def _rationale(rec: str, prop: dict, debt_info: dict, val: dict) -> str:
    if rec == "Hold":
        return f"Lease-up/value-add runway remains; occupancy at {prop['occupancy']:.0%} vs {prop['occupancy_budget']:.0%} target."
    elif rec == "Sell":
        gain = val["direct_cap_value"] - prop["acquisition_price"]
        return f"Stabilized asset with ${gain/1e6:.1f}M unrealized gain; cap rate compression opportunity."
    else:
        return f"Debt matures in {debt_info['months_to_maturity']:.0f} months; refinance to extend and improve terms."


def portfolio_summary() -> dict:
    """Generate fund-level portfolio summary."""
    props = PORTFOLIO["properties"]
    total_sf = sum(p["sf"] or 0 for p in props)
    total_units = sum(p["units"] or 0 for p in props)
    total_debt = sum(p["debt"]["balance"] for p in props)
    weighted_occ = sum(
        p["occupancy"] * (p["sf"] or (p["units"] * 900))
        for p in props
    ) / sum(p["sf"] or (p["units"] * 900) for p in props)
    avg_cap = sum(p["cap_rate_acquisition"] for p in props) / len(props)

    return {
        "fund_name": PORTFOLIO["fund_name"],
        "num_properties": len(props),
        "total_sf": total_sf,
        "total_units": total_units,
        "portfolio_occupancy": weighted_occ,
        "weighted_avg_cap_rate": avg_cap,
        "total_debt": total_debt,
        "total_equity_deployed": PORTFOLIO["total_equity_deployed"],
    }


def run_full_analysis():
    """Run complete portfolio analysis and print report."""
    print("=" * 70)
    print("  QUARTERLY ASSET REVIEW — " + PORTFOLIO["fund_name"])
    print("  Generated:", date.today().isoformat())
    print("=" * 70)

    # Portfolio Summary
    summary = portfolio_summary()
    print("\n## PORTFOLIO SUMMARY")
    print(f"  Total Assets:          {summary['num_properties']} properties")
    print(f"  Total SF:              {summary['total_sf']:,.0f} SF | {summary['total_units']} units")
    print(f"  Portfolio Occupancy:   {summary['portfolio_occupancy']:.1%}")
    print(f"  Wtd Avg Cap Rate:      {summary['weighted_avg_cap_rate']:.2%}")
    print(f"  Total Debt:            ${summary['total_debt']:,.0f}")
    print(f"  Equity Deployed:       ${summary['total_equity_deployed']:,.0f}")

    # Per-property analysis
    for prop in PORTFOLIO["properties"]:
        print("\n" + "-" * 70)
        print(f"  PROPERTY SCORECARD: {prop['name']}")
        print(f"  {prop['type']} | {prop['location']}")
        print("-" * 70)

        # T-12
        t12 = t12_analysis(prop)
        print(f"\n  T-12 Operating Performance:")
        print(f"    Annual NOI:          ${t12['annual_noi']:,.0f}")
        print(f"    Annual Revenue:      ${t12['annual_revenue']:,.0f}")
        print(f"    OpEx Ratio:          {t12['opex_ratio']:.1%}")
        print(f"    NOI Trend:           {t12['noi_trend']}")

        # Occupancy
        noi_var = (prop["in_place_noi"] - prop["budget_noi"]) / prop["budget_noi"]
        print(f"\n  Occupancy & NOI:")
        print(f"    Occupancy:           {prop['occupancy']:.0%} (budget: {prop['occupancy_budget']:.0%})")
        print(f"    In-Place NOI:        ${prop['in_place_noi']:,.0f} (vs budget: {noi_var:+.1%})")

        # Rent Roll
        walt_val = calc_walt(prop["rent_roll"])
        conc = concentration_risk(prop["rent_roll"])
        expiring = upcoming_expirations(prop["rent_roll"])
        print(f"\n  Rent Roll:")
        print(f"    WALT:                {walt_val:.1f} years")
        if conc:
            for c in conc:
                print(f"    Concentration Risk:  {c['tenant']} ({c['pct_revenue']:.0%} of revenue)")
        if expiring:
            for e in expiring:
                print(f"    Expiring Soon:       {e['tenant']} — {e['sf']:,} SF (exp {e['expires']})")
        else:
            print(f"    Expirations <12mo:   None")

        # Valuation
        val = valuation(prop)
        print(f"\n  Valuation:")
        print(f"    Direct Cap Value:    ${val['direct_cap_value']:,.0f}")
        print(f"    Implied Cap (T-12):  {val['implied_cap_current']:.2%}")
        print(f"    Sensitivity:")
        for cap_str, value in val["sensitivity"].items():
            print(f"      Cap {cap_str}:       ${value:,.0f}")

        # Debt
        di = debt_analysis(prop)
        print(f"\n  Debt:")
        print(f"    Balance:             ${di['balance']:,.0f}")
        print(f"    Rate:                {di['rate']:.2%} ({di['rate_type']})")
        print(f"    Maturity:            {di['maturity']}")
        print(f"    DSCR:                {di['dscr']:.2f}x")
        print(f"    LTV:                 {di['ltv']:.1%}")
        if di["flags"]:
            for f in di["flags"]:
                print(f"    ** FLAG: {f}")

        # Hold/Sell/Refi
        hsr = hold_sell_refi_score(prop)
        print(f"\n  Hold / Sell / Refi:")
        print(f"    Scores:  Hold={hsr['scores']['Hold']}  Sell={hsr['scores']['Sell']}  Refi={hsr['scores']['Refi']}")
        print(f"    >> RECOMMENDATION:   {hsr['recommendation']}")
        print(f"       {hsr['rationale']}")

    # Summary recommendations
    print("\n" + "=" * 70)
    print("  RECOMMENDED ACTIONS")
    print("=" * 70)
    for prop in PORTFOLIO["properties"]:
        hsr = hold_sell_refi_score(prop)
        print(f"  {prop['name']:30s} -> {hsr['recommendation']:6s} | {hsr['rationale']}")

    print("\n" + "=" * 70)
    print("  END OF QUARTERLY ASSET REVIEW")
    print("=" * 70)


if __name__ == "__main__":
    run_full_analysis()
