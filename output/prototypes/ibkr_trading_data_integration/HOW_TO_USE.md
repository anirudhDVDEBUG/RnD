# How to Use — IBKR Trading Data Integration

## Prerequisites

- **Go 1.21+** (to build the CLI)
- **Interactive Brokers account** with Client Portal Gateway or TWS running
- **Claude Code** (for plugin mode) or **Claude Desktop** (for MCP mode)

---

## 1. Install the IBKR CLI + Daemon

```bash
git clone https://github.com/osauer/ibkr.git
cd ibkr
go build -o ibkr .
# Verify:
./ibkr --help
```

The binary connects to the IBKR Client Portal Gateway API (default `https://localhost:5000`). Make sure the gateway is running and authenticated before using the CLI.

---

## 2a. Configure as a Claude Code Plugin

The repo ships a Claude Code plugin definition. Add the tool to your Claude Code settings so Claude can call IBKR commands directly. From the repo root:

```bash
# The plugin is defined in the repo — check the repo README for the
# exact path, typically something like:
claude plugin add ./claude-code-plugin.json
```

Trigger phrases that activate the skill:

- "Show me my IBKR positions"
- "Get a quote for AAPL"
- "Run a market scan for top gainers"
- "Pull daily history for TSLA"
- "Size a position for MSFT with 2% risk"

## 2b. Configure as a Claude Code Skill

Drop the skill file so Claude Code auto-discovers it:

```bash
mkdir -p ~/.claude/skills/ibkr_trading_data_integration
cp SKILL.md ~/.claude/skills/ibkr_trading_data_integration/SKILL.md
```

Same trigger phrases as above apply.

## 2c. Configure as an MCP Server (Claude Desktop)

Add this to your `~/.claude.json` under the `mcpServers` block:

```json
{
  "mcpServers": {
    "ibkr": {
      "command": "/absolute/path/to/ibkr",
      "args": ["mcp"],
      "env": {}
    }
  }
}
```

Replace `/absolute/path/to/ibkr` with the actual path to the compiled binary. Restart Claude Desktop after editing.

---

## 3. First 60 Seconds

Once the daemon is running and Claude is configured:

**Input (type into Claude):**
```
What are my current IBKR positions and account summary?
```

**Output (Claude responds with):**
```
Account U1234567 — Net Liquidation: $487,250.00

Positions:
  AAPL   150 shares  avg $178.30  mkt $227.50  P&L +$7,380.00
  NVDA   200 shares  avg  $98.50  mkt $136.80  P&L +$7,660.00
  SPY     50 shares  avg $545.20  mkt $592.10  P&L +$2,345.00
  ...
```

**Try next:**
```
Get a quote for NVDA and show its option chain expiring next month
```

```
Scan for the most active stocks today on IBKR
```

```
Size a position for AMZN with 1.5% risk and a $8 stop
```

---

## 4. Running the Mock Demo (No Broker Required)

To evaluate the data shapes without a live IBKR connection:

```bash
cd ibkr_trading_data_integration/
bash run.sh
```

This runs `demo.py` with mock data that mirrors the exact JSON structures the real CLI produces. No API keys or broker gateway needed.

---

## Key Notes

- **All access is read-only.** No orders are placed, no positions modified.
- The daemon must be running for live data. Without it, you get connection errors.
- Market data availability depends on your IBKR subscription (delayed vs. real-time).
- Option chains require options market data permissions on your IBKR account.
