# TradingAgents CN Lite - Multi-Agent Stock Analysis

Multi-agent trading analysis framework that runs specialized AI agents (market data, technical, fundamental, sentiment, risk, decision) through a LangGraph-style pipeline to produce buy/hold/sell recommendations for A-share, Hong Kong, and US stocks. This demo uses mock data so you can evaluate the architecture instantly.

## Headline Result

```
Ticker     Name                   Action       Conf       Risk     Score
------------------------------------------------------------------------
600519     Kweichow Moutai        BUY          moderate   medium   2
000001     Ping An Bank           STRONG BUY   high       low      5
00700      Tencent Holdings       HOLD         low        medium   0
09988      Alibaba Group          BUY          moderate   medium   2
AAPL       Apple Inc.             HOLD         low        medium   -1
TSLA       Tesla Inc.             SELL         moderate   high     -2
```

Run `bash run.sh` to reproduce this output (no API keys needed).

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** - Install the real framework, configure as a Claude skill, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** - Architecture, data flow, limitations, relevance to Claude-driven products
