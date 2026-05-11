---
name: honeydew_data_modeling
description: |
  Integrate with Honeydew's semantic data layer to query, explore, and manage data models using AI coding agents.
  Triggers: honeydew, semantic layer, data modeling, metrics layer, analytics entities
---

# Honeydew Data Modeling Skill

Connect AI coding agents to [Honeydew](https://www.honeydew.ai/)'s semantic data layer for querying, exploring, and managing shared data models, entities, and metrics definitions.

## When to use

- "Query the Honeydew semantic layer for available entities and metrics"
- "Explore the data model in Honeydew and list available attributes"
- "Generate SQL using Honeydew's semantic definitions"
- "Connect to Honeydew and retrieve metric definitions for my analytics pipeline"
- "Use Honeydew to understand the business logic behind this data model"

## How to use

1. **Install the plugin**: Clone or install from the [honeydew-ai-coding-agents-plugins](https://github.com/honeydew-ai/honeydew-ai-coding-agents-plugins) repository following its setup instructions.

2. **Configure authentication**: Set up your Honeydew API credentials. Typically this involves setting environment variables:
   ```bash
   export HONEYDEW_API_KEY="your-api-key"
   export HONEYDEW_WORKSPACE="your-workspace"
   export HONEYDEW_DOMAIN="your-domain.honeydew.live"
   ```

3. **Explore available entities**: Use the plugin to list and inspect entities, metrics, and attributes defined in your Honeydew workspace's semantic layer.

4. **Query data models**: Leverage Honeydew's semantic definitions to generate correct, business-logic-aware SQL queries rather than writing raw SQL against underlying tables.

5. **Integrate into workflows**: Use the plugin within your AI coding agent (Claude Code, Cursor, Copilot, etc.) to bring semantic context into code generation, data pipeline development, and analytics engineering tasks.

## Key capabilities

- **Entity exploration**: Browse entities, attributes, and relationships in the semantic layer
- **Metrics retrieval**: Access pre-defined metric calculations and business logic
- **SQL generation**: Generate semantically correct SQL backed by Honeydew's shared definitions
- **Schema understanding**: Get context about data warehouse structure through the semantic layer

## References

- Source repository: [honeydew-ai/honeydew-ai-coding-agents-plugins](https://github.com/honeydew-ai/honeydew-ai-coding-agents-plugins)
- Honeydew platform: [honeydew.ai](https://www.honeydew.ai/)
- Listed in: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
