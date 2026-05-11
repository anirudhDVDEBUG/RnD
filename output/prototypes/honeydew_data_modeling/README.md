# Honeydew Data Modeling — Semantic Layer for AI Agents

**TL;DR:** Honeydew's MCP plugin gives AI coding agents (Claude Code, Cursor, Copilot) direct access to a shared semantic data layer — entities, metrics, and business-logic-aware SQL generation — so analysts and engineers query *meaning*, not raw tables.

## Headline result

```
> "Give me total revenue and order count by region"

SELECT
  customers.region,
  SUM(orders.total_amount)  AS total_revenue,
  COUNT(DISTINCT orders.order_id)  AS order_count
FROM customers JOIN orders
GROUP BY customers.region
```

One natural-language request, one semantically correct query — no tribal knowledge about joins or column names required.

## Quick links

| Doc | What you'll find |
|-----|-----------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, configure MCP, first-60-seconds walkthrough |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, product-builder angle |

## Run the demo (no API key needed)

```bash
bash run.sh
```
