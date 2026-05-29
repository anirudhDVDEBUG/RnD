"""
TradingAgents CN Lite - Mock Multi-Agent Stock Analysis Demo

Demonstrates the multi-agent architecture of TradingAgents-CN-lite:
  Market Data Agent -> Analyst Agents -> Risk Agent -> Decision Agent

Uses mock data so no API keys or network access are needed.
"""

import json
import random
import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Mock market data
# ---------------------------------------------------------------------------

MOCK_STOCKS = {
    # A-Share
    "600519": {"name": "Kweichow Moutai", "market": "A-Share", "currency": "CNY",
               "price": 1685.00, "pe": 28.3, "pb": 9.1, "dividend_yield": 1.8,
               "sector": "Consumer Staples", "revenue_growth": 0.16, "net_margin": 0.52},
    "000001": {"name": "Ping An Bank", "market": "A-Share", "currency": "CNY",
               "price": 12.45, "pe": 5.2, "pb": 0.55, "dividend_yield": 5.6,
               "sector": "Financials", "revenue_growth": 0.03, "net_margin": 0.28},
    # Hong Kong
    "00700": {"name": "Tencent Holdings", "market": "HK", "currency": "HKD",
              "price": 415.60, "pe": 22.1, "pb": 4.8, "dividend_yield": 0.8,
              "sector": "Technology", "revenue_growth": 0.10, "net_margin": 0.30},
    "09988": {"name": "Alibaba Group", "market": "HK", "currency": "HKD",
              "price": 82.35, "pe": 10.5, "pb": 1.4, "dividend_yield": 2.5,
              "sector": "Technology", "revenue_growth": 0.08, "net_margin": 0.12},
    # US
    "AAPL":  {"name": "Apple Inc.", "market": "US", "currency": "USD",
              "price": 198.50, "pe": 31.2, "pb": 48.5, "dividend_yield": 0.5,
              "sector": "Technology", "revenue_growth": 0.05, "net_margin": 0.26},
    "TSLA":  {"name": "Tesla Inc.", "market": "US", "currency": "USD",
              "price": 255.30, "pe": 65.8, "pb": 14.2, "dividend_yield": 0.0,
              "sector": "Consumer Discretionary", "revenue_growth": 0.12, "net_margin": 0.11},
}

def _mock_price_history(base_price: float, days: int = 60) -> List[dict]:
    """Generate mock OHLCV history."""
    prices = []
    price = base_price * 0.92
    today = datetime.date.today()
    for i in range(days):
        change = random.uniform(-0.03, 0.035) * price
        o = round(price, 2)
        h = round(price + abs(change) * random.uniform(0.5, 1.5), 2)
        l = round(price - abs(change) * random.uniform(0.5, 1.5), 2)
        c = round(price + change, 2)
        vol = random.randint(500_000, 5_000_000)
        prices.append({"date": str(today - datetime.timedelta(days=days - i)),
                       "open": o, "high": h, "low": l, "close": c, "volume": vol})
        price = c
    return prices

def _mock_news(name: str) -> List[str]:
    templates = [
        f"{name} reports stronger-than-expected quarterly earnings.",
        f"Analysts upgrade {name} citing improving margins.",
        f"Regulatory scrutiny increases for {name}'s core business.",
        f"{name} announces strategic partnership in AI sector.",
        f"Institutional investors increase holdings in {name}.",
    ]
    return random.sample(templates, k=3)

# ---------------------------------------------------------------------------
# Agent definitions
# ---------------------------------------------------------------------------

@dataclass
class AgentOutput:
    agent: str
    analysis: str
    signals: Dict[str, object] = field(default_factory=dict)

class MarketDataAgent:
    """Fetches market data (mock)."""
    NAME = "MarketDataAgent"

    def run(self, ticker: str) -> AgentOutput:
        stock = MOCK_STOCKS.get(ticker)
        if not stock:
            return AgentOutput(self.NAME, f"Ticker {ticker} not found in database.",
                               {"error": True})
        history = _mock_price_history(stock["price"])
        last = history[-1]["close"]
        prev = history[-2]["close"]
        pct = (last - prev) / prev * 100
        sma20 = round(sum(h["close"] for h in history[-20:]) / 20, 2)
        sma60 = round(sum(h["close"] for h in history) / len(history), 2)
        return AgentOutput(
            self.NAME,
            f"Fetched {len(history)} days of data for {stock['name']} ({ticker}). "
            f"Latest close: {stock['currency']} {last:.2f} ({pct:+.2f}%). "
            f"SMA20={sma20}, SMA60={sma60}.",
            {"ticker": ticker, "name": stock["name"], "market": stock["market"],
             "currency": stock["currency"], "last_close": last,
             "sma20": sma20, "sma60": sma60, "history": history,
             "fundamentals": stock, "news": _mock_news(stock["name"])}
        )


class TechnicalAnalystAgent:
    """Performs technical analysis on price data."""
    NAME = "TechnicalAnalystAgent"

    def run(self, data: Dict) -> AgentOutput:
        if data.get("error"):
            return AgentOutput(self.NAME, "No data to analyze.", {"score": 0})
        last = data["last_close"]
        sma20 = data["sma20"]
        sma60 = data["sma60"]
        history = data["history"]

        # RSI (simplified 14-day)
        gains, losses = [], []
        for i in range(-14, 0):
            diff = history[i]["close"] - history[i - 1]["close"]
            gains.append(max(diff, 0))
            losses.append(max(-diff, 0))
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        rsi = 100 - (100 / (1 + avg_gain / max(avg_loss, 0.01)))

        trend = "bullish" if sma20 > sma60 else "bearish"
        momentum = "overbought" if rsi > 70 else ("oversold" if rsi < 30 else "neutral")
        score = 0
        score += 1 if trend == "bullish" else -1
        score += 1 if last > sma20 else -1
        score += 1 if momentum == "oversold" else (-1 if momentum == "overbought" else 0)

        return AgentOutput(
            self.NAME,
            f"Trend: {trend} (SMA20 {'>' if sma20 > sma60 else '<'} SMA60). "
            f"RSI(14)={rsi:.1f} -> {momentum}. Price {'above' if last > sma20 else 'below'} SMA20. "
            f"Technical score: {score}/3.",
            {"trend": trend, "rsi": round(rsi, 1), "momentum": momentum, "score": score}
        )


class FundamentalAnalystAgent:
    """Evaluates fundamentals: PE, PB, margins, growth."""
    NAME = "FundamentalAnalystAgent"

    def run(self, data: Dict) -> AgentOutput:
        if data.get("error"):
            return AgentOutput(self.NAME, "No data to analyze.", {"score": 0})
        f = data["fundamentals"]
        score = 0
        notes = []

        if f["pe"] < 15:
            score += 1; notes.append(f"Low PE ({f['pe']})")
        elif f["pe"] > 40:
            score -= 1; notes.append(f"High PE ({f['pe']})")
        else:
            notes.append(f"Moderate PE ({f['pe']})")

        if f["pb"] < 1.5:
            score += 1; notes.append(f"Low PB ({f['pb']})")
        elif f["pb"] > 10:
            score -= 1; notes.append(f"High PB ({f['pb']})")

        if f["revenue_growth"] > 0.10:
            score += 1; notes.append(f"Strong revenue growth ({f['revenue_growth']:.0%})")

        if f["net_margin"] > 0.20:
            score += 1; notes.append(f"Healthy net margin ({f['net_margin']:.0%})")

        if f["dividend_yield"] > 3.0:
            score += 1; notes.append(f"Attractive dividend yield ({f['dividend_yield']}%)")

        return AgentOutput(
            self.NAME,
            f"Fundamental analysis for {data['name']}: {'; '.join(notes)}. "
            f"Fundamental score: {score}/5.",
            {"score": score, "notes": notes}
        )


class SentimentAgent:
    """Analyzes news sentiment (mock NLP)."""
    NAME = "SentimentAgent"

    POSITIVE_WORDS = {"upgrade", "stronger", "partnership", "increase", "earnings"}
    NEGATIVE_WORDS = {"scrutiny", "regulatory", "decline", "warning", "downgrade"}

    def run(self, data: Dict) -> AgentOutput:
        if data.get("error"):
            return AgentOutput(self.NAME, "No data to analyze.", {"score": 0})
        news = data.get("news", [])
        pos = neg = 0
        for headline in news:
            words = set(headline.lower().split())
            pos += len(words & self.POSITIVE_WORDS)
            neg += len(words & self.NEGATIVE_WORDS)
        total = pos + neg or 1
        sentiment_score = round((pos - neg) / total, 2)
        label = "positive" if sentiment_score > 0.2 else ("negative" if sentiment_score < -0.2 else "neutral")
        return AgentOutput(
            self.NAME,
            f"Scanned {len(news)} headlines. Positive signals: {pos}, Negative: {neg}. "
            f"Sentiment: {label} (score={sentiment_score}).",
            {"sentiment": label, "score": sentiment_score, "headline_count": len(news)}
        )


class RiskManagementAgent:
    """Evaluates risk and suggests position sizing."""
    NAME = "RiskManagementAgent"

    def run(self, data: Dict, tech: Dict, fund: Dict, sent: Dict) -> AgentOutput:
        if data.get("error"):
            return AgentOutput(self.NAME, "No data.", {"risk_level": "unknown"})
        history = data["history"]
        returns = [(history[i]["close"] - history[i-1]["close"]) / history[i-1]["close"]
                    for i in range(1, len(history))]
        volatility = round((sum(r**2 for r in returns) / len(returns)) ** 0.5 * 100, 2)

        risk_score = 0
        if volatility > 3.0:
            risk_score += 2
        elif volatility > 1.5:
            risk_score += 1

        composite = tech.get("score", 0) + fund.get("score", 0)
        if composite < 0:
            risk_score += 1

        risk_level = "high" if risk_score >= 3 else ("medium" if risk_score >= 1 else "low")
        max_position = {
            "low": "5-8% of portfolio",
            "medium": "2-4% of portfolio",
            "high": "0-1% of portfolio"
        }[risk_level]

        return AgentOutput(
            self.NAME,
            f"Daily volatility: {volatility}%. Risk level: {risk_level}. "
            f"Recommended max position: {max_position}.",
            {"volatility": volatility, "risk_level": risk_level,
             "max_position": max_position, "risk_score": risk_score}
        )


class TradingDecisionAgent:
    """Synthesizes all agent outputs into a final recommendation."""
    NAME = "TradingDecisionAgent"

    def run(self, data: Dict, tech: Dict, fund: Dict, sent: Dict, risk: Dict) -> AgentOutput:
        if data.get("error"):
            return AgentOutput(self.NAME, "Cannot make decision — data error.",
                               {"action": "SKIP"})

        total_score = tech.get("score", 0) + fund.get("score", 0) + (
            1 if sent.get("score", 0) > 0.2 else (-1 if sent.get("score", 0) < -0.2 else 0))

        risk_level = risk.get("risk_level", "medium")
        if risk_level == "high":
            total_score -= 1

        if total_score >= 3:
            action, confidence = "STRONG BUY", "high"
        elif total_score >= 1:
            action, confidence = "BUY", "moderate"
        elif total_score >= -1:
            action, confidence = "HOLD", "low"
        elif total_score >= -3:
            action, confidence = "SELL", "moderate"
        else:
            action, confidence = "STRONG SELL", "high"

        return AgentOutput(
            self.NAME,
            f"RECOMMENDATION: {action} (confidence: {confidence}). "
            f"Composite score: {total_score}. Risk: {risk_level}. "
            f"Position sizing: {risk.get('max_position', 'N/A')}.",
            {"action": action, "confidence": confidence,
             "composite_score": total_score, "risk_level": risk_level}
        )


# ---------------------------------------------------------------------------
# Multi-Agent Graph (mirrors LangGraph orchestration)
# ---------------------------------------------------------------------------

class TradingAgentGraph:
    """
    Orchestrates the multi-agent pipeline:
      MarketData -> [Technical, Fundamental, Sentiment] (parallel) -> Risk -> Decision
    """

    def __init__(self, model: str = "mock", market: str = "all"):
        self.model = model
        self.market = market
        self.market_data = MarketDataAgent()
        self.technical = TechnicalAnalystAgent()
        self.fundamental = FundamentalAnalystAgent()
        self.sentiment = SentimentAgent()
        self.risk = RiskManagementAgent()
        self.decision = TradingDecisionAgent()

    def run(self, ticker: str, verbose: bool = True) -> Dict:
        steps: List[AgentOutput] = []

        # Step 1: Market data
        md = self.market_data.run(ticker)
        steps.append(md)
        if verbose:
            self._print_step(md)

        # Step 2: Parallel analysts
        tech = self.technical.run(md.signals)
        fund = self.fundamental.run(md.signals)
        sent = self.sentiment.run(md.signals)
        for a in (tech, fund, sent):
            steps.append(a)
            if verbose:
                self._print_step(a)

        # Step 3: Risk
        risk = self.risk.run(md.signals, tech.signals, fund.signals, sent.signals)
        steps.append(risk)
        if verbose:
            self._print_step(risk)

        # Step 4: Decision
        dec = self.decision.run(md.signals, tech.signals, fund.signals,
                                sent.signals, risk.signals)
        steps.append(dec)
        if verbose:
            self._print_step(dec, final=True)

        return {
            "ticker": ticker,
            "recommendation": dec.signals.get("action"),
            "confidence": dec.signals.get("confidence"),
            "composite_score": dec.signals.get("composite_score"),
            "risk_level": dec.signals.get("risk_level"),
            "steps": [{"agent": s.agent, "analysis": s.analysis} for s in steps],
        }

    @staticmethod
    def _print_step(output: AgentOutput, final: bool = False):
        sep = "=" if final else "-"
        print(f"\n{sep * 60}")
        prefix = ">>> FINAL" if final else "   "
        print(f"{prefix} [{output.agent}]")
        print(f"    {output.analysis}")
        if final:
            print(sep * 60)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    import sys
    random.seed(42)  # Reproducible demo output

    tickers = sys.argv[1:] if len(sys.argv) > 1 else list(MOCK_STOCKS.keys())

    print("=" * 60)
    print("  TradingAgents CN Lite - Multi-Agent Stock Analysis Demo")
    print("  (mock data — no API keys required)")
    print("=" * 60)

    graph = TradingAgentGraph()
    results = []

    for ticker in tickers:
        print(f"\n{'#' * 60}")
        print(f"  Analyzing: {ticker}")
        print(f"{'#' * 60}")
        result = graph.run(ticker)
        results.append(result)

    # Summary table
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"{'Ticker':<10} {'Name':<22} {'Action':<12} {'Conf':<10} {'Risk':<8} {'Score'}")
    print("-" * 72)
    for r in results:
        name = MOCK_STOCKS.get(r["ticker"], {}).get("name", "???")[:20]
        print(f"{r['ticker']:<10} {name:<22} {r['recommendation']:<12} "
              f"{r['confidence']:<10} {r['risk_level']:<8} {r['composite_score']}")
    print()


if __name__ == "__main__":
    main()
