# How to Use — Honeydew Data Modeling Plugin

## Installation

### Option A: MCP server in Claude Code (recommended)

1. Clone the plugin repo:

```bash
git clone https://github.com/honeydew-ai/honeydew-ai-coding-agents-plugins.git
cd honeydew-ai-coding-agents-plugins
pip install -r requirements.txt   # installs honeydew-ai SDK + MCP deps
```

2. Add the MCP server to `~/.claude.json`:

```json
{
  "mcpServers": {
    "honeydew": {
      "command": "python",
      "args": [
        "-m", "honeydew_mcp_server"
      ],
      "cwd": "/path/to/honeydew-ai-coding-agents-plugins",
      "env": {
        "HONEYDEW_API_KEY": "your-api-key",
        "HONEYDEW_WORKSPACE": "your-workspace",
        "HONEYDEW_DOMAIN": "your-domain.honeydew.live"
      }
    }
  }
}
```

3. Restart Claude Code. The Honeydew tools should appear in the MCP tool list.

### Option B: Cursor / Copilot

Follow the plugin repo's README for IDE-specific setup. The same env vars apply.

### Option C: Standalone Python SDK

```bash
pip install honeydew-ai
```

```python
from honeydew import HoneydewClient

client = HoneydewClient(
    api_key="your-api-key",
    workspace="your-workspace",
    domain="your-domain.honeydew.live",
)
entities = client.list_entities()
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HONEYDEW_API_KEY` | Yes | API key from your Honeydew workspace settings |
| `HONEYDEW_WORKSPACE` | Yes | Workspace name |
| `HONEYDEW_DOMAIN` | Yes | Your Honeydew domain, e.g. `acme.honeydew.live` |

## First 60 seconds

After installing and configuring the MCP server:

**Input (in Claude Code):**
```
List all entities in the Honeydew semantic layer
```

**Output:**
```
Found 3 entities in workspace "ecommerce_analytics":

1. orders — All e-commerce orders placed on the platform
   Attributes: order_id, customer_id, order_date, status, total_amount, discount, channel
   Related to: customers, order_items

2. customers — Registered customer profiles
   Attributes: customer_id, email, signup_date, region, lifetime_value, segment

3. order_items — Line items within each order
   Attributes: item_id, order_id, product_name, category, quantity, unit_price
```

**Input:**
```
Generate SQL for total revenue by customer region
```

**Output:**
```sql
SELECT
  customers.region,
  SUM(orders.total_amount) AS total_revenue
FROM customers JOIN orders
GROUP BY customers.region
```

The SQL is generated from Honeydew's metric definitions — not hallucinated column names.

## Trigger phrases (if using as a Claude Skill)

Drop the skill folder into `~/.claude/skills/honeydew_data_modeling/` and these phrases will activate it:

- "Query the Honeydew semantic layer"
- "List entities and metrics in Honeydew"
- "Generate SQL using Honeydew"
- "Explore the data model in Honeydew"
- "What metrics are defined in Honeydew?"

## Running the local demo

```bash
bash run.sh
```

This runs the mock client (`honeydew_mock.py`) — no API key or network access required. It demonstrates entity exploration, metric browsing, and SQL generation with synthetic data.
