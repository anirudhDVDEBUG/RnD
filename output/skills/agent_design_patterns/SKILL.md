---
name: Agent Design Patterns
description: |
  Apply the 7×6 agent design pattern framework from "Designing AI Agents" (Manning) to architect agentic systems.
  Triggers: agent design patterns, agentic architecture, multi-agent patterns, agent framework design, context engineering patterns
---

# Agent Design Patterns

A skill for applying the 7×6 agent design pattern framework to architect robust agentic AI systems. Based on the open-source companion repo to *Designing AI Agents* (Manning) by Jia Huang, covering 28 verified patterns with runnable Python code.

## When to use

- "Help me pick the right agent design pattern for my use case"
- "Architect a multi-agent system using established design patterns"
- "What agentic design patterns should I use for this workflow?"
- "Set up a project using agent design patterns from the 7×6 framework"
- "Review my agent architecture against known design patterns"

## How to use

### 1. Understand the Framework

The 7×6 framework organizes 28 agent design patterns across two dimensions:

**7 Architectural Layers (rows):**
1. **Single Agent** — Core patterns for individual agent behavior
2. **Multi-Agent** — Coordination and communication between agents
3. **Planning** — Task decomposition and goal-oriented reasoning
4. **Tool Use** — Integration with external tools and APIs
5. **Memory** — Context management, retrieval, and persistence
6. **Guardrails** — Safety, validation, and constraint enforcement
7. **Harness** — Orchestration infrastructure (Claude Code, Aider, OpenHands, DeerFlow)

**6 Design Concerns (columns):**
1. Decomposition
2. Orchestration
3. Context Engineering
4. Evaluation
5. Error Recovery
6. Human-in-the-Loop

### 2. Clone and Explore the Pattern Library

```bash
git clone https://github.com/huangjia2019/agent-design-patterns.git
cd agent-design-patterns
pip install -r requirements.txt  # if provided
```

Each pattern sits at a coordinate in the 7×6 grid and includes:
- A runnable Python implementation
- Verified engineering slices from real agent frameworks (Claude Code, Aider, OpenHands, DeerFlow)
- Documentation explaining when and why to use the pattern

### 3. Select Patterns for Your Architecture

When designing an agentic system:

1. **Identify your layer**: Is this a single-agent, multi-agent, or orchestration problem?
2. **Identify your concern**: Do you need decomposition, context engineering, error recovery, etc.?
3. **Find the pattern** at that coordinate in the framework
4. **Study the reference implementation** in the repo
5. **Adapt the pattern** to your specific use case

### 4. Common Pattern Combinations

- **Autonomous Agent**: Single Agent + Planning + Tool Use + Memory
- **Agent Swarm**: Multi-Agent + Orchestration + Guardrails + Harness
- **Research Agent**: Planning + Context Engineering + Tool Use + Human-in-the-Loop
- **Production Pipeline**: Harness + Guardrails + Error Recovery + Evaluation

### 5. Apply Patterns in Code

```python
# Example: Browse pattern implementations
# Each pattern directory contains:
# - pattern implementation (.py)
# - README explaining the pattern
# - Test or demo script

# Navigate to a specific pattern:
# cd <layer>/<concern>/
# python main.py
```

## Key Principles

- **Patterns are composable**: Combine patterns from different coordinates for complex architectures
- **Context engineering is central**: How you manage context across agents determines system quality
- **Harness matters**: The orchestration layer (Claude Code, Aider, etc.) shapes which patterns are practical
- **Start simple**: Begin with single-agent patterns before adding multi-agent complexity

## References

- **Repository**: https://github.com/huangjia2019/agent-design-patterns
- **Book**: *Designing AI Agents* (Manning) by Jia Huang
- **Frameworks covered**: Claude Code, Aider, OpenHands, DeerFlow
