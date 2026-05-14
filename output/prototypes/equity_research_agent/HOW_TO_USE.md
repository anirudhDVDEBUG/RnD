# How to Use — Equity Research Agent

## Option A: Install as a Claude Code Skill (Recommended)

### 1. Clone the source repo

```bash
git clone https://github.com/prof-little-bear/cc-equity-research.git
```

### 2. Copy the skill into Claude's skills directory

```bash
mkdir -p ~/.claude/skills/equity_research_agent
cp cc-equity-research/SKILL.md ~/.claude/skills/equity_research_agent/SKILL.md
```

The repo ships 24 analysis skills. To install the full bundle:

```bash
cp -r cc-equity-research/skills/* ~/.claude/skills/
```

### 3. Trigger phrases

Once the skill is installed, Claude Code activates it automatically when you say things like:

- "Analyze NVDA stock and give me a research report"
- "Run a DCF valuation on Microsoft"
- "Screen for undervalued mid-cap tech stocks"
- "Compare AMD vs NVDA financials"
- "Review Tesla's 10-K and summarize key risks"

No special prefix needed — Claude matches the intent to the skill.

### 4. Personalization

Append your investor level to any request:

- `"...beginner level"` — plain-language, defines terms, big-picture focus
- `"...intermediate level"` — standard research format (default)
- `"...advanced level"` — full quant detail, sensitivity tables

---

## Option B: Run the Standalone Demo

### Prerequisites

- Python 3.8+

### Install & Run

```bash
cd equity_research_agent/
bash run.sh
```

No dependencies to install — the demo uses only Python stdlib.

### CLI Usage

```bash
# Full report for a single ticker
python3 equity_research.py NVDA

# Set investor level
python3 equity_research.py AAPL --level beginner

# Quantitative screen across all tickers
python3 equity_research.py --screen

# Compare multiple tickers
python3 equity_research.py --compare NVDA AAPL
```

---

## First 60 Seconds

```
$ python3 equity_research.py NVDA --level intermediate

============================================================
  EQUITY RESEARCH REPORT — NVDA
  NVIDIA Corporation
  Sector: Technology | Industry: Semiconductors
  Price: $135.40 | Market Cap: $3,320B
============================================================

  Income Statement Analysis
------------------------------------------------------------
        Metric        FY2024        FY2025       FY2026E
        Revenue ($M)  26,974        60,922       130,497
        Rev Growth    —             125.9%       114.2%
        Gross Margin  56.9%         63.5%        65.0%
        ...

  DCF Valuation (5-Year, 3-Scenario)
------------------------------------------------------------
        Scenario  FCF Growth  Price Target   Upside
        Bear      5.0%        $117.50        -13.2%
        Base      12.0%       $195.65        44.5%
        Bull      20.0%       $316.82        134.0%

  Executive Summary
------------------------------------------------------------
  Rating:        BUY
  Price Target:  $195.65 (Base case)
  Upside:        44.5%
```

Output appears instantly — mock data, no network calls.

---

## MCP Data Server (Optional)

The source repo includes a financial-data MCP server for live data. To enable it, add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "equity-data": {
      "command": "python3",
      "args": ["/path/to/cc-equity-research/mcp_server/server.py"],
      "env": {
        "FINANCIAL_DATA_API_KEY": "your-key-here"
      }
    }
  }
}
```

This replaces mock data with live financials from the configured data provider. See the source repo README for supported providers.
