#!/usr/bin/env python3
"""
Equity Research Agent — Mock Demo
Demonstrates the analysis pipeline with realistic mock financial data.
No API keys required.
"""

import sys

# ─── Mock Financial Data ────────────────────────────────────────────────────

MOCK_DATA = {
    "NVDA": {
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "price": 135.40,
        "market_cap_b": 3320,
        "shares_out_m": 24530,
        "financials": {
            "revenue":       [26_974, 60_922, 130_497],  # FY2024-FY2026 (in $M)
            "cogs":          [11_618, 22_249,  45_674],
            "gross_profit":  [15_356, 38_673,  84_823],
            "opex":          [ 5_192,  7_240,   9_860],
            "operating_inc": [10_164, 31_433,  74_963],
            "net_income":    [ 9_243, 29_760,  72_880],
            "eps":           [  3.77,  12.12,   29.70],
            "total_assets":  [65_728, 96_013, 132_600],
            "total_debt":    [ 9_709,  8_462,   8_200],
            "cash":          [25_984, 31_444,  48_100],
            "fcf":           [ 8_132, 27_021,  68_400],
            "capex":         [ 1_069,  2_800,   4_500],
            "dividends":     [   395,    490,     540],
        },
        "years": ["FY2024", "FY2025", "FY2026E"],
        "peers": ["AMD", "INTC", "AVGO"],
        "catalysts": [
            "AI data-center capex cycle (Blackwell/Rubin ramp)",
            "Sovereign AI infrastructure build-outs",
            "Automotive & robotics TAM expansion",
        ],
        "risks": [
            "Customer concentration (hyperscalers ~50% rev)",
            "US-China export controls on advanced GPUs",
            "Cyclical capex downturn risk",
            "Rising competition from custom ASICs (Google TPU, AWS Trainium)",
        ],
    },
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "price": 212.50,
        "market_cap_b": 3250,
        "shares_out_m": 15294,
        "financials": {
            "revenue":       [383_285, 391_035, 410_200],
            "cogs":          [214_137, 210_738, 220_100],
            "gross_profit":  [169_148, 180_297, 190_100],
            "opex":          [ 54_847,  57_200,  59_800],
            "operating_inc": [114_301, 123_097, 130_300],
            "net_income":    [ 96_995, 100_913, 108_500],
            "eps":           [   6.42,    6.72,    7.22],
            "total_assets":  [352_583, 364_980, 378_000],
            "total_debt":    [111_088, 104_200,  98_000],
            "cash":          [ 29_965,  30_800,  32_500],
            "fcf":           [110_543, 108_800, 115_400],
            "capex":         [ 10_959,  11_200,  11_800],
            "dividends":     [ 15_025,  15_400,  15_900],
        },
        "years": ["FY2023", "FY2024", "FY2025E"],
        "peers": ["MSFT", "GOOG", "AMZN"],
        "catalysts": [
            "Apple Intelligence rollout driving iPhone upgrade cycle",
            "Services revenue growing 15%+ YoY",
            "Vision Pro ecosystem development",
        ],
        "risks": [
            "China revenue exposure (~18% of sales)",
            "Regulatory pressure (EU DMA, App Store fees)",
            "Smartphone market saturation",
            "AI feature parity gap vs. competitors",
        ],
    },
}


# ─── Analysis Modules ───────────────────────────────────────────────────────

def income_analysis(ticker: str, data: dict) -> dict:
    fin = data["financials"]
    years = data["years"]
    rev = fin["revenue"]
    gp = fin["gross_profit"]
    oi = fin["operating_inc"]
    ni = fin["net_income"]

    rev_growth = [(rev[i] - rev[i-1]) / rev[i-1] * 100 for i in range(1, len(rev))]
    gross_margins = [gp[i] / rev[i] * 100 for i in range(len(rev))]
    op_margins = [oi[i] / rev[i] * 100 for i in range(len(rev))]
    net_margins = [ni[i] / rev[i] * 100 for i in range(len(rev))]

    return {
        "title": "Income Statement Analysis",
        "years": years,
        "revenue_m": rev,
        "revenue_growth_pct": [None] + rev_growth,
        "gross_margin_pct": gross_margins,
        "operating_margin_pct": op_margins,
        "net_margin_pct": net_margins,
    }


def balance_sheet_analysis(ticker: str, data: dict) -> dict:
    fin = data["financials"]
    assets = fin["total_assets"]
    debt = fin["total_debt"]
    cash = fin["cash"]
    net_debt = [debt[i] - cash[i] for i in range(len(debt))]
    debt_to_assets = [debt[i] / assets[i] * 100 for i in range(len(debt))]

    return {
        "title": "Balance Sheet Analysis",
        "years": data["years"],
        "total_assets_m": assets,
        "total_debt_m": debt,
        "cash_m": cash,
        "net_debt_m": net_debt,
        "debt_to_assets_pct": debt_to_assets,
    }


def cash_flow_analysis(ticker: str, data: dict) -> dict:
    fin = data["financials"]
    fcf = fin["fcf"]
    capex = fin["capex"]
    rev = fin["revenue"]
    fcf_margin = [fcf[i] / rev[i] * 100 for i in range(len(fcf))]
    capex_intensity = [capex[i] / rev[i] * 100 for i in range(len(capex))]
    fcf_yield = [fcf[-1] / (data["market_cap_b"] * 1000) * 100]

    return {
        "title": "Cash Flow Analysis",
        "years": data["years"],
        "fcf_m": fcf,
        "fcf_margin_pct": fcf_margin,
        "capex_m": capex,
        "capex_intensity_pct": capex_intensity,
        "current_fcf_yield_pct": round(fcf_yield[0], 2),
    }


def ratio_analysis(ticker: str, data: dict) -> dict:
    fin = data["financials"]
    price = data["price"]
    mcap = data["market_cap_b"] * 1000
    eps = fin["eps"][-1]
    rev = fin["revenue"][-1]
    ni = fin["net_income"][-1]
    fcf = fin["fcf"][-1]
    ev = mcap + fin["total_debt"][-1] - fin["cash"][-1]
    ebitda_approx = fin["operating_inc"][-1] + fin["capex"][-1]

    return {
        "title": "Valuation Ratios (Current)",
        "pe_ratio": round(price / eps, 1) if eps > 0 else None,
        "ev_ebitda": round(ev / ebitda_approx, 1),
        "price_to_fcf": round(mcap / fcf, 1),
        "price_to_sales": round(mcap / rev, 1),
        "roe_pct": round(ni / (fin["total_assets"][-1] - fin["total_debt"][-1]) * 100, 1),
        "ev_m": ev,
    }


def dcf_valuation(ticker: str, data: dict) -> dict:
    """Simple 5-year DCF with 3 scenarios."""
    fcf_base = data["financials"]["fcf"][-1]
    shares = data["shares_out_m"]
    wacc = 0.10
    terminal_growth = 0.03

    scenarios = {}
    for label, growth in [("Bear", 0.05), ("Base", 0.12), ("Bull", 0.20)]:
        projected = []
        cf = fcf_base
        for yr in range(1, 6):
            cf = cf * (1 + growth)
            projected.append(cf)
        terminal = projected[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
        pv_cfs = sum(cf / (1 + wacc) ** i for i, cf in enumerate(projected, 1))
        pv_terminal = terminal / (1 + wacc) ** 5
        equity_value = pv_cfs + pv_terminal
        per_share = equity_value / shares

        scenarios[label] = {
            "fcf_growth_pct": growth * 100,
            "equity_value_m": round(equity_value),
            "price_target": round(per_share, 2),
        }

    return {
        "title": "DCF Valuation (5-Year, 3-Scenario)",
        "wacc_pct": wacc * 100,
        "terminal_growth_pct": terminal_growth * 100,
        "scenarios": scenarios,
        "current_price": data["price"],
    }


# ─── Report Generator ───────────────────────────────────────────────────────

def fmt_money(val, suffix=""):
    """Format large numbers with commas."""
    if val is None:
        return "N/A"
    if isinstance(val, float):
        return f"${val:,.2f}{suffix}"
    return f"${val:,}{suffix}"


def fmt_pct(val):
    if val is None:
        return "—"
    return f"{val:.1f}%"


def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_table(headers: list, rows: list, col_width: int = 14):
    header_line = "".join(h.rjust(col_width) for h in headers)
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print("".join(str(c).rjust(col_width) for c in row))


def generate_report(ticker: str, level: str = "intermediate"):
    ticker = ticker.upper()
    if ticker not in MOCK_DATA:
        print(f"Error: No mock data for '{ticker}'. Available: {', '.join(MOCK_DATA.keys())}")
        sys.exit(1)

    data = MOCK_DATA[ticker]

    # Header
    print("\n" + "=" * 60)
    print(f"  EQUITY RESEARCH REPORT — {ticker}")
    print(f"  {data['name']}")
    print(f"  Sector: {data['sector']} | Industry: {data['industry']}")
    print(f"  Price: ${data['price']:.2f} | Market Cap: ${data['market_cap_b']:,}B")
    print("=" * 60)
    print("  AI-GENERATED ANALYSIS — NOT FINANCIAL ADVICE")
    print("=" * 60)

    # 1. Income Statement
    inc = income_analysis(ticker, data)
    print_section(inc["title"])
    headers = ["Metric"] + inc["years"]
    rows = [
        ["Revenue ($M)"] + [f"{v:,}" for v in inc["revenue_m"]],
        ["Rev Growth"] + [fmt_pct(v) for v in inc["revenue_growth_pct"]],
        ["Gross Margin"] + [fmt_pct(v) for v in inc["gross_margin_pct"]],
        ["Op Margin"] + [fmt_pct(v) for v in inc["operating_margin_pct"]],
        ["Net Margin"] + [fmt_pct(v) for v in inc["net_margin_pct"]],
    ]
    print_table(headers, rows)

    # 2. Balance Sheet
    bs = balance_sheet_analysis(ticker, data)
    print_section(bs["title"])
    headers = ["Metric"] + bs["years"]
    rows = [
        ["Assets ($M)"] + [f"{v:,}" for v in bs["total_assets_m"]],
        ["Debt ($M)"] + [f"{v:,}" for v in bs["total_debt_m"]],
        ["Cash ($M)"] + [f"{v:,}" for v in bs["cash_m"]],
        ["Net Debt ($M)"] + [f"{v:,}" for v in bs["net_debt_m"]],
        ["Debt/Assets"] + [fmt_pct(v) for v in bs["debt_to_assets_pct"]],
    ]
    print_table(headers, rows)

    # 3. Cash Flow
    cf = cash_flow_analysis(ticker, data)
    print_section(cf["title"])
    headers = ["Metric"] + cf["years"]
    rows = [
        ["FCF ($M)"] + [f"{v:,}" for v in cf["fcf_m"]],
        ["FCF Margin"] + [fmt_pct(v) for v in cf["fcf_margin_pct"]],
        ["Capex ($M)"] + [f"{v:,}" for v in cf["capex_m"]],
        ["Capex Intensity"] + [fmt_pct(v) for v in cf["capex_intensity_pct"]],
    ]
    print_table(headers, rows)
    print(f"\n  Current FCF Yield: {fmt_pct(cf['current_fcf_yield_pct'])}")

    # 4. Valuation Ratios
    ratios = ratio_analysis(ticker, data)
    print_section(ratios["title"])
    print(f"  P/E Ratio:      {ratios['pe_ratio']}")
    print(f"  EV/EBITDA:      {ratios['ev_ebitda']}")
    print(f"  P/FCF:          {ratios['price_to_fcf']}")
    print(f"  P/Sales:        {ratios['price_to_sales']}")
    print(f"  ROE:            {fmt_pct(ratios['roe_pct'])}")
    print(f"  EV ($M):        {ratios['ev_m']:,}")

    # 5. DCF Valuation
    dcf = dcf_valuation(ticker, data)
    print_section(dcf["title"])
    print(f"  WACC: {dcf['wacc_pct']}% | Terminal Growth: {dcf['terminal_growth_pct']}%")
    print(f"  Current Price: ${dcf['current_price']:.2f}\n")
    headers = ["Scenario", "FCF Growth", "Equity Val ($M)", "Price Target", "Upside"]
    rows = []
    for label, s in dcf["scenarios"].items():
        upside = (s["price_target"] - dcf["current_price"]) / dcf["current_price"] * 100
        rows.append([
            label,
            fmt_pct(s["fcf_growth_pct"]),
            f"{s['equity_value_m']:,}",
            f"${s['price_target']:.2f}",
            fmt_pct(upside),
        ])
    print_table(headers, rows, col_width=16)

    # 6. Catalysts
    print_section("Catalysts")
    for i, c in enumerate(data["catalysts"], 1):
        print(f"  {i}. {c}")

    # 7. Risks
    print_section("Risk Factors")
    for i, r in enumerate(data["risks"], 1):
        print(f"  {i}. {r}")

    # 8. Executive Summary
    dcf_base = dcf["scenarios"]["Base"]
    upside = (dcf_base["price_target"] - data["price"]) / data["price"] * 100
    if upside > 20:
        rating = "BUY"
    elif upside > 0:
        rating = "HOLD"
    else:
        rating = "SELL"

    print_section("Executive Summary")
    print(f"  Rating:        {rating}")
    print(f"  Price Target:  ${dcf_base['price_target']:.2f} (Base case)")
    print(f"  Upside:        {upside:.1f}%")
    print(f"  Time Horizon:  12 months")
    print()
    if level == "beginner":
        print(f"  {data['name']} looks {'attractive' if upside > 0 else 'expensive'} based on")
        print(f"  a simple cash-flow model. The stock trades at {ratios['pe_ratio']}x earnings.")
        print(f"  Key growth driver: {data['catalysts'][0]}.")
        print(f"  Biggest risk: {data['risks'][0]}.")
    else:
        print(f"  {data['name']} trades at {ratios['pe_ratio']}x forward P/E and")
        print(f"  {ratios['ev_ebitda']}x EV/EBITDA. Our base-case DCF ({dcf_base['fcf_growth_pct']}%")
        print(f"  FCF CAGR, {dcf['wacc_pct']}% WACC) yields ${dcf_base['price_target']:.2f},")
        print(f"  implying {upside:.1f}% upside. Bear/bull range:")
        bear = dcf["scenarios"]["Bear"]["price_target"]
        bull = dcf["scenarios"]["Bull"]["price_target"]
        print(f"  ${bear:.2f} — ${bull:.2f}.")

    print()
    print("=" * 60)
    print("  DISCLAIMER: AI-generated analysis using mock data.")
    print("  Not financial advice. Do your own due diligence.")
    print("=" * 60)
    print()


# ─── Screening Module ───────────────────────────────────────────────────────

def screen_stocks():
    """Quick quantitative screen across all available tickers."""
    print_section("Quantitative Stock Screen")
    headers = ["Ticker", "Price", "P/E", "EV/EBITDA", "FCF Yield", "ROE", "Signal"]
    rows = []
    for ticker, data in MOCK_DATA.items():
        ratios = ratio_analysis(ticker, data)
        cf = cash_flow_analysis(ticker, data)
        if ratios["pe_ratio"] and ratios["pe_ratio"] < 30:
            signal = "VALUE"
        elif cf["current_fcf_yield_pct"] > 3:
            signal = "CASH-GEN"
        else:
            signal = "GROWTH"
        rows.append([
            ticker,
            f"${data['price']:.2f}",
            str(ratios["pe_ratio"]),
            str(ratios["ev_ebitda"]),
            fmt_pct(cf["current_fcf_yield_pct"]),
            fmt_pct(ratios["roe_pct"]),
            signal,
        ])
    print_table(headers, rows, col_width=14)
    print()


# ─── CLI Entry Point ────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Equity Research Agent — generate stock analysis reports"
    )
    parser.add_argument("ticker", nargs="?", default="NVDA",
                        help="Ticker symbol to analyze (default: NVDA)")
    parser.add_argument("--level", choices=["beginner", "intermediate", "advanced"],
                        default="intermediate",
                        help="Investor experience level (default: intermediate)")
    parser.add_argument("--screen", action="store_true",
                        help="Run quantitative stock screen")
    parser.add_argument("--compare", nargs="+",
                        help="Compare multiple tickers (e.g. --compare NVDA AAPL)")

    args = parser.parse_args()

    if args.screen:
        screen_stocks()
        return

    if args.compare:
        for t in args.compare:
            generate_report(t.upper(), args.level)
        return

    generate_report(args.ticker, args.level)


if __name__ == "__main__":
    main()
