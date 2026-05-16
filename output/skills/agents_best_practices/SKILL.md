---
name: agents_best_practices
description: |
  Provider-neutral best practices for building AI agents, agentic workflows, and prompt engineering.
  Applies to Claude Code, Codex, and other agentic harnesses.
  Trigger: user asks about agent design patterns, agentic workflow best practices,
  prompt engineering for agents, multi-agent architectures, or MCP integration patterns.
---

# Agents Best Practices

Provider-neutral skill for agent design, agentic workflows, and prompt engineering best practices. Works across Claude Code, Codex, and other agentic harnesses.

## When to use

- "What are best practices for building AI agents?"
- "How should I structure an agentic workflow?"
- "Help me design a multi-agent system"
- "What prompt engineering patterns work best for agents?"
- "How do I integrate MCP servers into my agent architecture?"

## How to use

### 1. Agent Design Principles

- **Single Responsibility**: Each agent should have one clear purpose. Avoid monolithic agents that try to do everything.
- **Composability**: Design agents as modular building blocks that can be composed into larger workflows.
- **Fail Gracefully**: Agents should handle errors, timeouts, and unexpected inputs without crashing the pipeline.
- **Observability**: Log decisions, tool calls, and reasoning steps so workflows can be debugged and audited.

### 2. Agentic Workflow Patterns

- **Sequential Pipeline**: Chain agents in a linear sequence where each agent's output feeds the next. Best for deterministic, ordered tasks.
- **Parallel Fan-Out**: Dispatch independent subtasks to multiple agents simultaneously, then aggregate results. Use when subtasks are independent.
- **Router/Dispatcher**: A coordinator agent routes tasks to specialized sub-agents based on the input type or intent.
- **Iterative Refinement**: An agent produces output, a reviewer agent evaluates it, and the cycle repeats until quality thresholds are met.
- **Human-in-the-Loop**: Insert approval checkpoints at critical decision points to maintain human oversight.

### 3. Prompt Engineering for Agents

- **Be Explicit About Role and Constraints**: Define what the agent can and cannot do upfront.
- **Structured Output**: Request JSON or structured formats when the output will be consumed by another agent or system.
- **Few-Shot Examples**: Provide concrete examples of expected input/output pairs for complex tasks.
- **Chain-of-Thought**: Encourage step-by-step reasoning for tasks requiring analysis or decision-making.
- **Guard Rails**: Include explicit instructions about safety boundaries, forbidden actions, and escalation paths.

### 4. Cross-Platform Compatibility

- **Provider-Neutral Prompts**: Write prompts that work across different LLM providers. Avoid provider-specific syntax in core logic.
- **Skill Portability**: Structure skills with clear YAML frontmatter, trigger conditions, and self-contained instructions so they work in Claude Code, Codex, or other harnesses.
- **MCP Integration**: Use the Model Context Protocol for tool access. Design MCP servers with clean interfaces and minimal coupling to the agent logic.

### 5. Quality & Safety

- **Input Validation**: Validate inputs at agent boundaries before processing.
- **Output Verification**: Check agent outputs against expected schemas or constraints before passing downstream.
- **Rate Limiting & Cost Control**: Set budgets for token usage and API calls per workflow run.
- **Idempotency**: Design agent actions to be safely retryable without side effects.
- **Audit Trail**: Maintain a log of all agent decisions and actions for accountability.

### 6. Practical Steps

1. Define the workflow goal and break it into discrete agent responsibilities.
2. Choose the right workflow pattern (sequential, parallel, router, iterative).
3. Write provider-neutral prompts with clear role definitions and constraints.
4. Implement tool access via MCP where possible for clean separation of concerns.
5. Add observability (logging, tracing) and error handling at each agent boundary.
6. Test with diverse inputs and edge cases before deploying.
7. Monitor production runs and iterate on prompt/agent design based on failure modes.

## References

- Source: [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) — Provider-neutral Agent Skill for Codex, Claude Code, and agentic harness design.
- Topics: agent-skill, agentic-workflows, prompt-engineering, best-practices, cross-platform, MCP
