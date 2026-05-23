# How to Use

## Install

```bash
git clone https://github.com/hikari0511/awesome-amazon-ec-skills.git
cd awesome-amazon-ec-skills

# This prototype (runs standalone with mock data):
pip install -r requirements.txt
```

Python 3.9+ required. No external API keys needed for the demo.

## As a Claude Code Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/awesome-amazon-ec-skills
cp SKILL.md ~/.claude/skills/awesome-amazon-ec-skills/SKILL.md
```

### Trigger Phrases

Claude will activate this skill when you say things like:

- "Help me optimize my Amazon listing"
- "Analyze competitor keywords on Amazon"
- "Find 1688 suppliers for my FBA product"
- "What's my Amazon PPC ACoS and how to improve it"
- "跨境电商选品分析"
- "Amazon SP-API integration"

## As an MCP Server (for SP-API integration)

If you have Amazon SP-API credentials, add this to `~/.claude.json`:

```json
{
  "mcpServers": {
    "amazon-ec": {
      "command": "python",
      "args": ["-m", "amazon_ec_mcp.server"],
      "env": {
        "SP_API_REFRESH_TOKEN": "<your-refresh-token>",
        "SP_API_CLIENT_ID": "<your-lwa-client-id>",
        "SP_API_CLIENT_SECRET": "<your-lwa-client-secret>",
        "SP_API_MARKETPLACE": "ATVPDKIKX0DER"
      }
    }
  }
}
```

Note: The MCP server requires valid SP-API credentials. The demo (`run.sh`) uses mock data and needs no credentials.

## First 60 Seconds

```bash
# 1. Run the full demo pipeline
bash run.sh

# 2. Try individual modules
python -m amazon_ec.listing_optimizer --asin B0EXAMPLE01
python -m amazon_ec.keyword_researcher --seed "insulated water bottle"
python -m amazon_ec.ppc_analyzer --campaign demo_campaign
python -m amazon_ec.sourcing_evaluator --product "stainless steel bottle"

# 3. Use with Claude Code (after installing skill)
# Just ask: "Optimize my Amazon listing for ASIN B0EXAMPLE01"
```

### Expected Output

Each module prints a structured report:

- **Listing Optimizer**: before/after scores, rewritten title & bullets, backend keyword suggestions
- **Keyword Researcher**: ranked keyword list with search volume estimates, relevance scores, competition level
- **PPC Analyzer**: campaign metrics, ACoS optimization recommendations, negative keyword candidates
- **Sourcing Evaluator**: supplier comparison table, landed cost breakdown, margin analysis
