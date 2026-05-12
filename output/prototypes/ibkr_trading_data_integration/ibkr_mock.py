"""
Mock IBKR client that simulates the osauer/ibkr Go CLI responses.
Produces realistic account, positions, quotes, option chains, history,
market scans, and position-sizing output without requiring a live
Interactive Brokers gateway.
"""

import json
import random
import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

random.seed(42)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class AccountSummary:
    account_id: str
    net_liquidation: float
    equity_with_loan: float
    available_funds: float
    buying_power: float
    gross_position_value: float
    maint_margin_req: float
    currency: str = "USD"


@dataclass
class Position:
    symbol: str
    description: str
    quantity: int
    avg_cost: float
    market_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float
    asset_class: str = "STK"


@dataclass
class Quote:
    symbol: str
    last: float
    bid: float
    ask: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    change: float
    change_pct: float
    timestamp: str


@dataclass
class OptionLeg:
    contract_id: int
    symbol: str
    expiry: str
    strike: float
    right: str  # CALL / PUT
    bid: float
    ask: float
    last: float
    volume: int
    open_interest: int
    implied_vol: float
    delta: float
    gamma: float
    theta: float
    vega: float


@dataclass
class DailyBar:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass
class ScanResult:
    symbol: str
    last: float
    change_pct: float
    volume: int
    market_cap_b: float


@dataclass
class PositionSize:
    symbol: str
    account_equity: float
    risk_pct: float
    entry_price: float
    stop_price: float
    risk_per_share: float
    shares: int
    position_value: float
    risk_amount: float


# ---------------------------------------------------------------------------
# Mock data generators
# ---------------------------------------------------------------------------

SYMBOLS = {
    "AAPL": ("Apple Inc.", 227.50),
    "MSFT": ("Microsoft Corp.", 454.20),
    "NVDA": ("NVIDIA Corp.", 136.80),
    "AMZN": ("Amazon.com Inc.", 205.60),
    "TSLA": ("Tesla Inc.", 285.40),
    "SPY":  ("SPDR S&P 500 ETF", 592.10),
    "QQQ":  ("Invesco QQQ Trust", 518.30),
    "META": ("Meta Platforms Inc.", 625.90),
}


def mock_account() -> AccountSummary:
    nav = 487_250.00
    return AccountSummary(
        account_id="U1234567",
        net_liquidation=nav,
        equity_with_loan=nav + 12_400,
        available_funds=nav * 0.42,
        buying_power=nav * 1.68,
        gross_position_value=nav * 0.78,
        maint_margin_req=nav * 0.22,
    )


def mock_positions() -> List[Position]:
    holdings = [
        ("AAPL", 150, 178.30),
        ("NVDA", 200, 98.50),
        ("SPY",  50,  545.20),
        ("MSFT", 80,  410.00),
        ("TSLA", 60,  240.10),
    ]
    positions = []
    for sym, qty, avg in holdings:
        price = SYMBOLS[sym][1]
        mv = round(price * qty, 2)
        pnl = round((price - avg) * qty, 2)
        positions.append(Position(
            symbol=sym,
            description=SYMBOLS[sym][0],
            quantity=qty,
            avg_cost=avg,
            market_price=price,
            market_value=mv,
            unrealized_pnl=pnl,
            realized_pnl=round(random.uniform(-500, 2000), 2),
        ))
    return positions


def mock_quote(symbol: str) -> Quote:
    base = SYMBOLS.get(symbol, (symbol, 100.0))[1]
    noise = round(random.uniform(-0.5, 0.5), 2)
    last = round(base + noise, 2)
    prev_close = round(base - random.uniform(0.5, 3.0), 2)
    change = round(last - prev_close, 2)
    return Quote(
        symbol=symbol,
        last=last,
        bid=round(last - 0.02, 2),
        ask=round(last + 0.02, 2),
        open=round(base - random.uniform(-1, 2), 2),
        high=round(base + random.uniform(1, 4), 2),
        low=round(base - random.uniform(1, 4), 2),
        close=prev_close,
        volume=random.randint(5_000_000, 80_000_000),
        change=change,
        change_pct=round(change / prev_close * 100, 2),
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
    )


def mock_option_chain(symbol: str, num_strikes: int = 5) -> List[OptionLeg]:
    base = SYMBOLS.get(symbol, (symbol, 100.0))[1]
    expiry = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    chain = []
    strike_step = round(base * 0.02, 0)  # ~2% increments
    center = round(base / strike_step) * strike_step
    for i in range(-num_strikes // 2, num_strikes // 2 + 1):
        strike = center + i * strike_step
        for right in ("CALL", "PUT"):
            itm = (strike < base) if right == "CALL" else (strike > base)
            mid = max(0.10, round(abs(base - strike) * (0.7 if itm else 0.3)
                                  + random.uniform(0.5, 3.0), 2))
            iv = round(random.uniform(0.25, 0.65), 4)
            d = round(random.uniform(0.3, 0.8) * (1 if right == "CALL" else -1), 4)
            chain.append(OptionLeg(
                contract_id=random.randint(100000, 999999),
                symbol=symbol,
                expiry=expiry,
                strike=strike,
                right=right,
                bid=round(mid - 0.05, 2),
                ask=round(mid + 0.05, 2),
                last=mid,
                volume=random.randint(10, 5000),
                open_interest=random.randint(100, 50000),
                implied_vol=iv,
                delta=d,
                gamma=round(random.uniform(0.005, 0.05), 4),
                theta=round(-random.uniform(0.02, 0.15), 4),
                vega=round(random.uniform(0.05, 0.30), 4),
            ))
    return chain


def mock_daily_history(symbol: str, days: int = 20) -> List[DailyBar]:
    base = SYMBOLS.get(symbol, (symbol, 100.0))[1]
    price = base * 0.92
    bars = []
    for i in range(days):
        dt = datetime.date.today() - datetime.timedelta(days=days - i)
        o = round(price, 2)
        h = round(price + random.uniform(0.5, 4), 2)
        l = round(price - random.uniform(0.5, 4), 2)
        c = round(price + random.uniform(-2, 3), 2)
        price = c
        bars.append(DailyBar(
            date=dt.isoformat(),
            open=o, high=h, low=l, close=c,
            volume=random.randint(10_000_000, 120_000_000),
        ))
    return bars


def mock_market_scan(scan_type: str = "TOP_PERC_GAIN") -> List[ScanResult]:
    pool = list(SYMBOLS.keys())
    random.shuffle(pool)
    results = []
    for sym in pool[:6]:
        base = SYMBOLS[sym][1]
        chg = round(random.uniform(1.5, 9.8) * (1 if "GAIN" in scan_type else -1), 2)
        results.append(ScanResult(
            symbol=sym,
            last=round(base * (1 + chg / 100), 2),
            change_pct=chg,
            volume=random.randint(20_000_000, 150_000_000),
            market_cap_b=round(random.uniform(50, 3200), 1),
        ))
    results.sort(key=lambda r: abs(r.change_pct), reverse=True)
    return results


def mock_position_size(symbol: str, risk_pct: float = 2.0,
                       stop_distance: float = 5.0) -> PositionSize:
    acct = mock_account()
    price = SYMBOLS.get(symbol, (symbol, 100.0))[1]
    risk_amount = round(acct.net_liquidation * risk_pct / 100, 2)
    shares = int(risk_amount / stop_distance)
    return PositionSize(
        symbol=symbol,
        account_equity=acct.net_liquidation,
        risk_pct=risk_pct,
        entry_price=price,
        stop_price=round(price - stop_distance, 2),
        risk_per_share=stop_distance,
        shares=shares,
        position_value=round(shares * price, 2),
        risk_amount=risk_amount,
    )
