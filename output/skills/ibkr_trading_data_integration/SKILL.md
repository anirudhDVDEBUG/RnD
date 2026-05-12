---
name: ibkr_trading_data_integration
description: |
  Integrate with Interactive Brokers (IBKR) for read-only market data and account information using the osauer/ibkr Go CLI, Claude Code plugin, and MCP server.
  TRIGGER: When the user wants to check brokerage account data, view stock/options positions, get real-time quotes, look up option chains, retrieve daily price history, run market scans, or calculate position sizes via Interactive Brokers.
---

# IBKR Trading Data Integration

Use this skill to access Interactive Brokers (IBKR) read-only account and market data through a Go-based CLI daemon with Claude Code plugin and MCP server support.

## When to use

- "Show me my Interactive Brokers positions and account summary"
- "Get a quote for AAPL and its option chain"
- "Run a market scan for top gainers on IBKR"
- "Pull daily price history for TSLA from Interactive Brokers"
- "Calculate fixed-fractional position size for a trade"

## How to use

### 1. Install the IBKR CLI + Daemon

Clone and build the Go project:

```bash
git clone https://github.com/osauer/ibkr.git
cd ibkr
go build -o ibkr .
```

Ensure the IBKR Client Portal Gateway or TWS is running and accessible, as the tool connects to the Interactive Brokers API.

### 2. Configure for Claude Code (Plugin)

The project includes a Claude Code plugin. Add the IBKR tool to your Claude Code configuration so that Claude can invoke IBKR commands directly. Refer to the repo's plugin setup instructions for the exact configuration path.

### 3. Configure for Claude Desktop (MCP Server)

For Claude Desktop, configure the MCP server in your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ibkr": {
      "command": "path/to/ibkr",
      "args": ["mcp"]
    }
  }
}
```

### 4. Available Features

All access is **read-only** (no order placement or modifications):

- **Account**: View account summary, balances, and margin information
- **Positions**: List current portfolio positions with P&L
- **Quotes**: Get real-time or delayed quotes for stocks, ETFs, and other instruments
- **Option Chains**: Look up available options with strikes, expirations, and Greeks
- **Daily History**: Retrieve historical daily OHLCV price data for any symbol
- **Market Scans**: Run predefined market scans (top gainers, losers, most active, etc.)
- **Fixed-Fractional Sizing**: Calculate position sizes based on risk percentage and stop-loss distance

### 5. Example Usage with Claude

Once configured, ask Claude naturally:

- "What are my current IBKR positions?"
- "Get me a quote for SPY"
- "Show the option chain for NVDA expiring next month"
- "Pull 1-year daily history for AMZN"
- "Scan for the most active stocks today"
- "Size a position for MSFT with 2% risk and a $5 stop"

The daemon must be running for Claude to access the data. All operations are safe and read-only -- no trades will be executed.

## References

- Source repository: [osauer/ibkr](https://github.com/osauer/ibkr)
- Tags: interactive-brokers, mcp-server, options-trading, finance, golang
