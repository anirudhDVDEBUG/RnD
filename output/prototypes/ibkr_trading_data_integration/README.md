# IBKR Trading Data Integration

**Read-only access to Interactive Brokers account data, quotes, option chains, history, and market scans — via a Go CLI that doubles as a Claude Code plugin and MCP server.**

This prototype demonstrates all seven data features the [osauer/ibkr](https://github.com/osauer/ibkr) tool exposes, using deterministic mock data so you can evaluate the workflow without a live brokerage connection.

## Headline Result

```
$ bash run.sh
  AAPL    $227.50   +2.14  (+0.95%)  vol   42,317,890
  NVDA    $136.80   +1.68  (+1.24%)  vol   71,024,556
  SPY     $592.10   +0.93  (+0.16%)  vol   63,891,204

  -> Buy 1949 shares of MSFT @ $454.20
     Stop @ $449.20  |  Risking $9,745.00 (2.0% of equity)
```

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the real tool, configure Claude Code plugin or MCP server, first 60 seconds.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why this matters for Claude-driven products.
