# How to Use TradingAgents CN Lite

## Quick Demo (this repo)

```bash
bash run.sh
# Runs mock multi-agent analysis on 6 stocks across 3 markets
# No API keys, no installs — Python 3.8+ stdlib only
```

## Install the Real Framework

```bash
git clone https://github.com/cy-Yin/TradingAgents-CN-lite.git
cd TradingAgents-CN-lite
pip install -r requirements.txt
```

Set at least one LLM provider key:

```bash
export OPENAI_API_KEY="sk-..."       # GPT-4 / GPT-4o
# or
export DEEPSEEK_API_KEY="sk-..."     # DeepSeek-Chat (cheapest)
# or
export ANTHROPIC_API_KEY="sk-ant-..."  # Claude
```

## Use as a Claude Code Skill

1. Create the skill directory and drop the skill file:

```bash
mkdir -p ~/.claude/skills/tradingagents-cn-lite
cp SKILL.md ~/.claude/skills/tradingagents-cn-lite/SKILL.md
```

2. Trigger phrases that activate the skill:

| Phrase | What happens |
|--------|-------------|
| "Set up a multi-agent stock analysis system for Chinese A-shares" | Clones repo, installs deps, configures .env |
| "Analyze stocks across A-share, HK, and US markets with AI agents" | Runs the full LangGraph pipeline |
| "Build a trading analysis pipeline using LangGraph" | Scaffolds the multi-agent graph |
| "Help me configure TradingAgents-CN-lite" | Walks through env setup |

3. Claude will then clone the repo, install dependencies, and guide you through analysis.

## First 60 Seconds

**Input:**

```python
from tradingagents import TradingAgentGraph

graph = TradingAgentGraph(model="deepseek-chat", market="a-share")
result = graph.run(ticker="600519")  # Kweichow Moutai
```

**Output (abbreviated):**

```
[MarketDataAgent]     Fetched 60 days of data for Kweichow Moutai (600519).
                      Latest close: CNY 1712.45 (+0.38%). SMA20=1695.20, SMA60=1658.33.

[TechnicalAnalyst]    Trend: bullish (SMA20 > SMA60). RSI(14)=58.3 -> neutral.
                      Technical score: 1/3.

[FundamentalAnalyst]  Moderate PE (28.3); Strong revenue growth (16%);
                      Healthy net margin (52%). Fundamental score: 2/5.

[SentimentAgent]      Scanned 3 headlines. Positive: 3, Negative: 1.
                      Sentiment: positive (score=0.5).

[RiskManagement]      Daily volatility: 1.82%. Risk level: medium.
                      Recommended max position: 2-4% of portfolio.

[TradingDecision]     RECOMMENDATION: BUY (confidence: moderate).
                      Composite score: 2. Risk: medium.
```

Each agent contributes its specialized analysis, and the Decision Agent synthesizes everything into one actionable recommendation.

## Supported Markets

| Market | Example Tickers | Data Source (real framework) |
|--------|----------------|-----------------------------|
| A-Share (China) | 600519, 000001 | akshare, tushare |
| Hong Kong | 00700, 09988 | akshare |
| US | AAPL, TSLA | yfinance, akshare |

## Analyze a Single Ticker (this demo)

```bash
python3 trading_agents.py 600519
python3 trading_agents.py AAPL TSLA
```
