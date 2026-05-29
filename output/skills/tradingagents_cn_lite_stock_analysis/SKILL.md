---
name: TradingAgents CN Lite - Multi-Agent Stock Analysis
description: |
  Set up and run the TradingAgents-CN-lite multi-agent trading analysis framework for A-share, Hong Kong, and US stock markets using LangGraph.
  Triggers: stock analysis, trading agents, multi-agent trading, A-share analysis, financial market agents
---

# TradingAgents CN Lite - Multi-Agent Stock Analysis

A Claude Code skill for scaffolding and running the TradingAgents-CN-lite framework — a lightweight multi-agent trading analysis system supporting A-share (China), Hong Kong, and US stock markets.

## When to use

- "Set up a multi-agent stock analysis system for Chinese A-shares"
- "Build a trading analysis pipeline using LangGraph with multiple AI agents"
- "Analyze stocks across A-share, HK, and US markets with AI agents"
- "Create a lightweight financial trading agent framework with LangGraph"
- "Help me configure TradingAgents-CN-lite for stock market analysis"

## How to use

### 1. Clone and install the framework

```bash
git clone https://github.com/cy-Yin/TradingAgents-CN-lite.git
cd TradingAgents-CN-lite
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file or export the following variables for your chosen LLM provider:

```bash
# Choose one or more LLM backends (OpenAI-compatible, DeepSeek, Claude, etc.)
export OPENAI_API_KEY="your-openai-key"
# or
export ANTHROPIC_API_KEY="your-anthropic-key"
# or
export DEEPSEEK_API_KEY="your-deepseek-key"
```

### 3. Understand the architecture

The framework uses **LangGraph** to orchestrate multiple specialized agents in a trading analysis pipeline:

- **Market Data Agents** — Fetch real-time and historical data for A-share (via akshare/tushare), HK, and US markets
- **Analyst Agents** — Perform technical analysis, fundamental analysis, and sentiment analysis
- **Risk Management Agents** — Evaluate portfolio risk and position sizing
- **Trading Decision Agents** — Synthesize agent outputs into actionable buy/hold/sell recommendations

The multi-agent graph processes a stock ticker through these specialized roles, with each agent contributing its analysis before a final decision is made.

### 4. Run an analysis

```python
# Example: Analyze a stock using the multi-agent pipeline
from tradingagents import TradingAgentGraph

# Initialize the agent graph
graph = TradingAgentGraph(
    model="deepseek-chat",  # or "gpt-4", "claude-sonnet-4-20250514", etc.
    market="a-share"        # or "hk", "us"
)

# Run analysis on a specific stock
result = graph.run(ticker="600519")  # e.g., Kweichow Moutai
print(result)
```

### 5. Supported markets

| Market | Ticker Examples | Data Sources |
|--------|----------------|-------------|
| A-Share (China) | 600519, 000001 | akshare, tushare |
| Hong Kong | 00700, 09988 | akshare |
| US | AAPL, TSLA | yfinance, akshare |

### 6. Customization tips

- **Swap LLM providers**: The framework supports OpenAI, DeepSeek, Claude, and other OpenAI-compatible APIs
- **Add custom agents**: Extend the LangGraph workflow by adding new analyst nodes
- **Adjust risk parameters**: Configure risk tolerance and position sizing in the config
- **Use for research only**: This is an analysis tool — always apply independent judgment before making real trades

## References

- **Source repository**: [cy-Yin/TradingAgents-CN-lite](https://github.com/cy-Yin/TradingAgents-CN-lite)
- **Framework**: Built on [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
- **Key topics**: multi-agent, stock-analysis, trading, langgraph, finance, A-share, quant
