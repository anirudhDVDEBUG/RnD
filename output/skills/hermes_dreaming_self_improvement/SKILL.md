---
name: hermes_dreaming_self_improvement
description: |
  Staged self-improvement engine for Hermes-style memory, skill, and fact updates with explicit review and apply/discard gates.
  Triggers: agent memory updates, self-improvement cycle, dreaming process, staged skill updates, review gate workflow
---

# Hermes Dreaming – Staged Self-Improvement Engine

A skill for running staged self-improvement cycles that propose updates to an agent's memory, skills, and facts — with explicit human review gates before any changes are applied.

## When to use

- "Run a dreaming cycle to improve agent memory and skills"
- "Stage self-improvement updates for review before applying"
- "Update my agent's facts and knowledge with review gates"
- "Run Hermes-style memory consolidation and skill refinement"
- "Propose skill and fact updates, then let me approve or discard"

## How to use

### 1. Install hermes-dreaming

```bash
# Clone the repository
git clone https://github.com/asimons81/hermes-dreaming.git
cd hermes-dreaming

# Install dependencies
pip install -e .
```

### 2. Run a dreaming cycle

The engine operates in staged phases:

1. **Propose** – The agent analyzes recent interactions and proposes updates to memory entries, skills, or facts.
2. **Review** – Proposed changes are surfaced for human review. Each proposal can be inspected individually.
3. **Apply or Discard** – Approved proposals are applied; rejected ones are discarded. Nothing changes without explicit approval.

```bash
# Run the dreaming process (proposes updates)
python -m hermes_dreaming dream

# Review staged proposals
python -m hermes_dreaming review

# Apply approved changes
python -m hermes_dreaming apply

# Discard rejected changes
python -m hermes_dreaming discard
```

### 3. MCP Server mode

Hermes Dreaming can also run as an MCP server, exposing its capabilities as tools for AI agents:

```json
{
  "mcpServers": {
    "hermes-dreaming": {
      "command": "python",
      "args": ["-m", "hermes_dreaming", "serve"]
    }
  }
}
```

### 4. Key concepts

- **Memory updates**: Consolidate, merge, or prune agent memory entries based on patterns observed across sessions.
- **Skill updates**: Propose new skills or refine existing ones based on recurring tasks or newly learned capabilities.
- **Fact updates**: Add, correct, or remove factual knowledge the agent maintains.
- **Review gates**: Every proposed change goes through an explicit approve/discard gate — no silent mutations.

### 5. Integration with Claude Code

Add the MCP server to your Claude Code configuration to let Claude propose self-improvement updates during coding sessions. Review and approve changes at your own pace.

## References

- **Source repository**: https://github.com/asimons81/hermes-dreaming
- **Topics**: ai-agents, cli, mcp, memory, open-source, python, self-improvement
- **Language**: Python
