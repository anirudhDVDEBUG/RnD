# How to Use OpenSquilla

## Install

### Option A — pip (when published)

```bash
pip install opensquilla
```

### Option B — from source

```bash
git clone https://github.com/OpenSquilla/opensquilla.git
cd opensquilla
pip install -e .
```

### Option C — this prototype (no install needed)

```bash
bash run.sh
```

Requires only Python 3.8+ and stdlib. No external packages.

---

## As a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/opensquilla_token_efficient_agent
cp SKILL.md ~/.claude/skills/opensquilla_token_efficient_agent/SKILL.md
```

### Trigger phrases

- "Set up an OpenSquilla agent"
- "I want a token-efficient AI agent"
- "Help me configure opensquilla with MCP"
- "Build an agent that optimizes token usage"
- "Use opensquilla for agent memory and skills"

---

## MCP Server Integration

If you use OpenSquilla with MCP-connected tools, add servers to `~/.claude.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

OpenSquilla's `MCPConfig` class generates this JSON programmatically — see the demo output.

---

## First 60 Seconds

### 1. Run the demo

```bash
bash run.sh
```

### 2. What you see

```
========================================================
  OpenSquilla — Token-Efficient AI Agent Demo
========================================================

1) PROMPT COMPRESSION
  Original  (  89 tok): I would like you to please summarize the following document about quar...
  Compressed(  32 tok): summarize the following document about quarterly earnings for the fisc...
  Savings: 64.0%  |  Intelligence density: 0.36

2) SKILL-BASED ARCHITECTURE
  Prompt: Please summarize the quarterly report on cloud infrastructure spending
  Result: [Skill:summarize] Summary (9 words input): summarize the quarterly...
  Tokens: 17 -> 16 (5.9% saved)

3) AGENT MEMORY
  Stored 3 memory entries: ['user_name', 'project', 'preference']
  Query: What project am I working on?
  Response: [Agent 'memory_agent'] ... Context: [memory:user_name] Alice; ...

4) MCP SERVER CONFIGURATION
  Generated ~/.claude.json mcpServers config:
  { "mcpServers": { "filesystem": { ... }, "github": { ... } } }

5) TOKEN BUDGET COMPARISON
  Original prompt: 89 tokens
    Budget    Compressed   Savings   Density
        32            32    64.0%     0.36
        64            64    28.1%     0.719
       128            89     0.0%     1.0
       256            89     0.0%     1.0
```

### 3. Integrate into your own code

```python
from opensquilla_agent import Agent, Skill

@Skill(name="lead_score", description="Score a lead from CRM data")
def lead_score(text: str) -> str:
    # your scoring logic here
    return "Score: 85/100"

agent = Agent(
    name="sales_agent",
    token_budget=2048,
    memory_enabled=True,
    memory_path="./sales_memory",
    skills=[lead_score],
)

result = agent.run("lead_score this prospect: Acme Corp, 500 employees, SaaS")
print(result)
```
