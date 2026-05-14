---
name: equity_research_agent
description: |
  Turn Claude Code into an equity-research agent that performs comprehensive stock analysis including fundamental analysis, valuation modeling, financial statement analysis, SEC filing review, and quantitative screening.

  Triggers:
  - User asks to analyze a stock or equity
  - User requests financial statement analysis or valuation
  - User wants SEC filing review or earnings analysis
  - User asks for investment research or stock screening
  - User requests DCF, comparable analysis, or ratio analysis
---

# Equity Research Agent

A comprehensive equity-research skill that enables deep financial analysis, valuation modeling, and investment research workflows.

## When to use

- "Analyze AAPL stock and give me a research report"
- "Run a DCF valuation on Microsoft"
- "Review Tesla's latest 10-K filing and summarize key risks"
- "Screen for undervalued mid-cap tech stocks"
- "Compare the financial health of AMD vs NVDA"

## How to use

### Step 1: Define the Research Scope

Identify the ticker symbol(s) and the type of analysis needed:
- **Fundamental Analysis**: Revenue trends, margins, growth rates, competitive positioning
- **Valuation**: DCF modeling, comparable company analysis, precedent transactions
- **Financial Statement Analysis**: Income statement, balance sheet, cash flow deep-dives
- **SEC Filing Review**: 10-K, 10-Q, 8-K, proxy statement analysis
- **Quantitative Screening**: Ratio-based filtering, factor scoring, sector comparisons

### Step 2: Gather Financial Data

Use available data sources (MCP financial data server or web search) to collect:
- Historical financial statements (3-5 years minimum)
- Current market data (price, market cap, volume)
- SEC filings and earnings transcripts
- Industry benchmarks and peer comparisons

### Step 3: Perform Analysis

Execute the relevant analysis modules:

1. **Income Statement Analysis** — Revenue growth, margin trends, operating leverage
2. **Balance Sheet Analysis** — Asset quality, leverage ratios, working capital
3. **Cash Flow Analysis** — FCF generation, capex intensity, cash conversion
4. **Ratio Analysis** — P/E, EV/EBITDA, P/FCF, ROE, ROIC
5. **DCF Valuation** — Project future cash flows, determine WACC, calculate intrinsic value
6. **Comparable Analysis** — Identify peers, normalize metrics, derive relative valuation
7. **Risk Assessment** — Identify key risks from filings, concentration, regulatory exposure
8. **Catalyst Identification** — Upcoming earnings, product launches, macro factors

### Step 4: Synthesize and Report

Produce a structured research output:
- **Executive Summary**: Bull/bear thesis in 2-3 sentences
- **Key Metrics Table**: Critical financial data at a glance
- **Valuation Range**: Low/base/high scenario with methodology
- **Risk Factors**: Top 3-5 risks with probability assessment
- **Recommendation**: Rating with price target and time horizon

### Personalization Layer

Adapt output to the investor's level:
- **Beginner**: Plain-language explanations, define financial terms, focus on big picture
- **Intermediate**: Standard research format, moderate technical depth
- **Advanced**: Full quantitative detail, sensitivity tables, factor decomposition

## Analysis Capabilities

| Category | Skills |
|----------|--------|
| Fundamental | Revenue analysis, margin analysis, growth modeling, competitive moat |
| Valuation | DCF, comps, sum-of-parts, dividend discount, residual income |
| Filings | 10-K review, 10-Q review, proxy analysis, insider transactions |
| Quantitative | Factor screening, ratio scoring, sector rotation, momentum signals |
| Risk | Concentration risk, leverage risk, regulatory risk, macro sensitivity |
| Synthesis | Research reports, investment memos, earnings previews, peer rankings |

## Important Notes

- Always disclose that this is AI-generated analysis, not professional financial advice
- Use the most recent available data; flag when data may be stale
- Present ranges and scenarios rather than single-point estimates
- Clearly state assumptions underlying any valuation model
- Flag when information is unavailable rather than speculating
