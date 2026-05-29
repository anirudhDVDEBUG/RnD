# Technical Details

## What It Does

TradingAgents-CN-lite is a lightweight multi-agent framework that orchestrates specialized AI agents through a LangGraph directed graph to analyze stocks across three markets: A-share (China), Hong Kong, and US. Each agent has a distinct role — fetching market data, performing technical analysis, evaluating fundamentals, gauging sentiment, assessing risk, and making a final trading recommendation. The agents communicate through a shared state graph, with each node's output feeding into downstream nodes.

Unlike monolithic "ask the LLM for stock advice" approaches, this framework decomposes the analysis into structured, auditable steps. Each agent can use a different LLM or prompt strategy, and the graph topology ensures all analyses complete before the decision agent synthesizes them.

## Architecture

```
                    +-----------------+
                    | MarketDataAgent |
                    +--------+--------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v---+  +------v------+  +----v--------+
     | Technical   |  | Fundamental |  | Sentiment   |
     | Analyst     |  | Analyst     |  | Agent       |
     +--------+---+  +------+------+  +----+--------+
              |              |              |
              +--------------+--------------+
                             |
                    +--------v--------+
                    | RiskManagement  |
                    +--------+--------+
                             |
                    +--------v--------+
                    | TradingDecision |
                    +-----------------+
```

### Key Files (real repo)

| File | Purpose |
|------|---------|
| `tradingagents/graph.py` | LangGraph workflow definition, node wiring |
| `tradingagents/agents/` | Individual agent implementations (one per file) |
| `tradingagents/data/` | Market data fetchers (akshare, yfinance, tushare) |
| `tradingagents/config.py` | LLM provider config, risk parameters |
| `main.py` | CLI entry point |

### Key Files (this demo)

| File | Purpose |
|------|---------|
| `trading_agents.py` | All 6 agents + graph orchestration + mock data (single file) |
| `run.sh` | One-command demo runner |

### Data Flow

1. **MarketDataAgent** fetches OHLCV history + fundamentals + news headlines for a ticker
2. Three analyst agents run in parallel on that data:
   - **TechnicalAnalystAgent**: SMA crossovers, RSI, trend detection
   - **FundamentalAnalystAgent**: PE, PB, margins, growth, dividend yield
   - **SentimentAgent**: NLP keyword scoring on news headlines
3. **RiskManagementAgent** computes volatility and position sizing from price history + analyst scores
4. **TradingDecisionAgent** combines all scores into a weighted composite -> BUY/HOLD/SELL

### Dependencies (real framework)

- **langgraph / langchain** - Agent orchestration and LLM abstraction
- **akshare** - A-share and HK market data (free, no API key)
- **yfinance** - US market data
- **openai / anthropic** - LLM backends for agent reasoning
- **pandas / numpy** - Data manipulation

### Model Calls

In the real framework, each analyst agent makes 1-2 LLM calls per stock (prompt with data -> structured analysis). A full run for one ticker typically uses ~4-6 LLM calls. The demo replaces these with deterministic scoring logic to show the same data flow without API costs.

## Limitations

- **Not a trading system** — produces analysis reports, not executable orders. No broker integration.
- **No real-time streaming** — batch analysis only; designed for end-of-day or on-demand use.
- **Data source constraints** — akshare is free but rate-limited; tushare requires a token. US data via yfinance has known gaps.
- **LLM dependency** — agent quality is only as good as the underlying model. Cheap models produce shallow analysis.
- **No backtesting** — cannot evaluate historical accuracy of recommendations.
- **Single-stock focus** — analyzes one ticker at a time; no portfolio-level optimization or correlation analysis.
- **Chinese language bias** — prompts and some outputs are in Chinese by default; needs prompt customization for English-only use.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | Clean example of multi-agent LangGraph orchestration with parallel branches — directly transferable to non-finance agent pipelines |
| **Lead-gen / marketing** | The architecture pattern (data fetch -> multi-analyst -> risk -> decision) maps to lead scoring: data enrichment -> qualification agents -> risk scoring -> routing |
| **Claude skill ecosystem** | Demonstrates how a domain-specific skill can wrap a complex multi-agent framework behind simple trigger phrases |
| **Voice AI** | Decision agent output is concise and structured enough to feed directly into voice summaries ("Your portfolio check: Moutai is a buy, Tesla is a sell") |
| **Prompt engineering** | Each agent has a focused system prompt — good template for decomposing complex tasks into specialized sub-agents |
