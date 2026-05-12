#!/usr/bin/env python3
"""
End-to-end demo of the IBKR Trading Data Integration.

Exercises every feature the osauer/ibkr tool exposes — account summary,
positions, quotes, option chains, daily history, market scans, and
fixed-fractional position sizing — using deterministic mock data so it
runs without an IBKR gateway.
"""

import json
from dataclasses import asdict
from ibkr_mock import (
    mock_account,
    mock_positions,
    mock_quote,
    mock_option_chain,
    mock_daily_history,
    mock_market_scan,
    mock_position_size,
)

DIVIDER = "=" * 72


def section(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def pp(obj):
    """Pretty-print a dataclass or list of dataclasses."""
    if isinstance(obj, list):
        print(json.dumps([asdict(o) for o in obj], indent=2))
    else:
        print(json.dumps(asdict(obj), indent=2))


def main():
    print("IBKR Trading Data Integration — Mock Demo")
    print("Simulates osauer/ibkr CLI output for all supported features.\n")

    # 1. Account summary
    section("1. Account Summary")
    acct = mock_account()
    pp(acct)

    # 2. Positions
    section("2. Portfolio Positions")
    positions = mock_positions()
    pp(positions)
    total_pnl = sum(p.unrealized_pnl for p in positions)
    print(f"\n  Total unrealized P&L: ${total_pnl:,.2f}")

    # 3. Real-time quotes
    section("3. Real-Time Quotes")
    for sym in ["AAPL", "NVDA", "SPY"]:
        q = mock_quote(sym)
        direction = "+" if q.change >= 0 else ""
        print(f"  {q.symbol:6s}  ${q.last:>9.2f}  {direction}{q.change:>6.2f}"
              f"  ({direction}{q.change_pct}%)  vol {q.volume:>12,}")

    # 4. Option chain
    section("4. Option Chain — NVDA (next monthly)")
    chain = mock_option_chain("NVDA", num_strikes=5)
    print(f"  {'Strike':>8}  {'Right':5}  {'Bid':>7}  {'Ask':>7}  "
          f"{'IV':>6}  {'Delta':>7}  {'OI':>7}")
    print(f"  {'-'*8}  {'-'*5}  {'-'*7}  {'-'*7}  {'-'*6}  {'-'*7}  {'-'*7}")
    for leg in chain[:12]:  # show first 12 legs
        print(f"  {leg.strike:>8.0f}  {leg.right:5}  {leg.bid:>7.2f}  "
              f"{leg.ask:>7.2f}  {leg.implied_vol:>5.1%}  {leg.delta:>7.4f}  "
              f"{leg.open_interest:>7,}")

    # 5. Daily price history
    section("5. Daily Price History — TSLA (last 20 days)")
    history = mock_daily_history("TSLA", days=20)
    print(f"  {'Date':>12}  {'Open':>8}  {'High':>8}  {'Low':>8}  "
          f"{'Close':>8}  {'Volume':>14}")
    for bar in history[-10:]:  # show last 10 bars
        print(f"  {bar.date}  {bar.open:>8.2f}  {bar.high:>8.2f}  "
              f"{bar.low:>8.2f}  {bar.close:>8.2f}  {bar.volume:>14,}")
    print(f"  ... showing last 10 of {len(history)} bars")

    # 6. Market scan
    section("6. Market Scan — Top % Gainers")
    scan = mock_market_scan("TOP_PERC_GAIN")
    print(f"  {'Symbol':6}  {'Last':>9}  {'Chg%':>7}  {'Volume':>14}  {'MktCap($B)':>10}")
    for r in scan:
        print(f"  {r.symbol:6}  ${r.last:>8.2f}  +{r.change_pct:>5.2f}%  "
              f"{r.volume:>14,}  {r.market_cap_b:>10.1f}")

    # 7. Position sizing
    section("7. Fixed-Fractional Position Sizing")
    sizing = mock_position_size("MSFT", risk_pct=2.0, stop_distance=5.0)
    pp(sizing)
    print(f"\n  -> Buy {sizing.shares} shares of {sizing.symbol} "
          f"@ ${sizing.entry_price:.2f}")
    print(f"     Stop @ ${sizing.stop_price:.2f}  |  "
          f"Risking ${sizing.risk_amount:,.2f} ({sizing.risk_pct}% of equity)")

    print(f"\n{DIVIDER}")
    print("  Demo complete. All 7 IBKR features exercised successfully.")
    print(DIVIDER)


if __name__ == "__main__":
    main()
