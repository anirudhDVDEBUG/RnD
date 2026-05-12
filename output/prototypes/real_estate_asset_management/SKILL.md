---
name: real_estate_asset_management
description: |
  Claude Code skill for real estate and private equity asset management — QARs, LP reporting, rent rolls, T-12 analysis, valuations, debt monitoring, and hold/sell/refi decisions.
  TRIGGER: user mentions real estate asset management, quarterly asset review, LP reporting, rent roll analysis, T-12 operating statement, property valuation, debt maturity monitoring, hold/sell/refi analysis, or commercial real estate portfolio management.
---

# Real Estate Asset Management

Structured workflows for commercial real estate and private equity asset management, covering quarterly reporting, financial analysis, valuation, debt monitoring, and disposition strategy.

## When to use

- "Prepare a quarterly asset review for this property portfolio"
- "Generate an LP report from these rent rolls and financials"
- "Run a T-12 analysis on this operating statement"
- "Evaluate hold vs. sell vs. refinance for this asset"
- "Monitor debt maturities and covenant compliance across the portfolio"

## How to use

1. **Quarterly Asset Review (QAR)**:
   - Collect property-level data: occupancy, rent roll, NOI, capex, leasing activity.
   - Compare actuals vs. budget and vs. prior quarter.
   - Flag properties with occupancy below target, rising expense ratios, or tenant credit issues.
   - Produce a summary with property scorecards and portfolio-level KPIs.

2. **LP Reporting**:
   - Aggregate fund-level metrics: IRR, equity multiple, DPI, TVPI.
   - Summarize capital account activity (contributions, distributions, NAV).
   - Include property-level updates with occupancy, NOI, and valuation changes.
   - Format for investor-ready delivery with executive summary and appendices.

3. **Rent Roll Analysis**:
   - Parse rent roll data: tenant names, suite/unit, SF, lease dates, base rent, escalations, reimbursements.
   - Calculate WALT (weighted average lease term), mark-to-market rent gap, and rollover exposure by year.
   - Identify concentration risk (single tenant > 20% of revenue).
   - Flag upcoming expirations within 12 months.

4. **T-12 Operating Statement Analysis**:
   - Organize trailing 12-month income and expenses.
   - Calculate effective gross income, operating expense ratio, and NOI.
   - Trend monthly variances and seasonality.
   - Normalize for non-recurring items (one-time capex, insurance claims).
   - Benchmark against market comps where available.

5. **Valuation**:
   - Apply cap rate to stabilized NOI for direct capitalization.
   - Build a discounted cash flow (DCF) with assumptions for rent growth, vacancy, capex reserves, and exit cap rate.
   - Cross-check with comparable sales (price per SF, price per unit).
   - Sensitize on cap rate (+/- 25-50 bps) and NOI scenarios.

6. **Debt Monitoring**:
   - Track loan balances, interest rates (fixed vs. floating), maturity dates, and extension options.
   - Calculate DSCR and LTV at current and stressed valuations.
   - Flag maturities within 12-24 months and covenant breaches.
   - Assess refinancing feasibility given current rate environment.

7. **Hold / Sell / Refi Decision Framework**:
   - Estimate remaining upside under hold scenario (lease-up, rent growth, value-add capex).
   - Model sale proceeds net of costs, taxes, and promote.
   - Compare refi proceeds and post-refi returns vs. redeployment alternatives.
   - Score each option on IRR, equity multiple, risk, and fund strategy alignment.
