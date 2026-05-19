# How to Use — Agent Design Patterns

## Install

```bash
# No dependencies — pure Python 3.8+
git clone <this-repo-or-copy-the-directory>
cd agent_design_patterns
```

To also get the original runnable patterns with real LLM code:

```bash
git clone https://github.com/huangjia2019/agent-design-patterns.git
cd agent-design-patterns
pip install -r requirements.txt  # if present
```

## As a Claude Skill

Drop the skill file so Claude Code auto-discovers it:

```bash
mkdir -p ~/.claude/skills/agent-design-patterns
cp SKILL.md ~/.claude/skills/agent-design-patterns/SKILL.md
```

**Trigger phrases** (say any of these to Claude Code):
- "Help me pick the right agent design pattern for my use case"
- "Architect a multi-agent system using established design patterns"
- "What agentic design patterns should I use for this workflow?"
- "Review my agent architecture against known design patterns"
- "Set up a project using agent design patterns from the 7x6 framework"

## First 60 Seconds

```bash
bash run.sh
```

**What you'll see** (truncated):

```
=== Agent Design Patterns — 7x6 Framework Demo ===

═══════════════════════════════════════════════════
1. THE 7x6 AGENT DESIGN PATTERN GRID
═══════════════════════════════════════════════════

Layer / Concern   Decomposition             Orchestration             Context Engineering       ...
--------------------------------------------------------------------------------------------------------------
Single Agent      Task Decomposition Agent  ReAct Loop                Prompt Chaining           ...
Multi-Agent       Divide and Conquer        Supervisor Orchestrator   Shared Blackboard         ...
Planning          Hierarchical Task Network Plan-Execute-Replan       Goal-Context Alignment    ...
...

═══════════════════════════════════════════════════
5. ARCHITECTURE PRESETS
═══════════════════════════════════════════════════

  Autonomous Agent: Single agent that plans, acts, and self-corrects.
    • Task Decomposition Agent (1,1)
    • ReAct Loop (1,2)
    • Tool Router (4,1)
    • Scratchpad Memory (5,3)
    • Retry with Reflection (1,5)
    • Self-Eval Gate (1,4)

  Research Agent: Deep-research agent with planning, retrieval, and human oversight.
    • Hierarchical Task Network (3,1)
    • Plan-Execute-Replan (3,2)
    ...
```

## Using the Python API

```python
from agent_patterns import PatternFramework

fw = PatternFramework()

# Search by use case
fw.recommend("I need a coding agent with error recovery")

# Get a specific pattern
p = fw.get("ReAct Loop")
print(p.summary, p.composable_with)

# Filter by layer or concern
fw.by_layer("Guardrails")
fw.by_concern("Human-in-the-Loop")

# Architecture presets
fw.architecture_for("autonomous_agent")
fw.architecture_for("research_agent")
fw.architecture_for("agent_swarm")
fw.architecture_for("production_pipeline")

# Full grid
print(fw.grid())
```
