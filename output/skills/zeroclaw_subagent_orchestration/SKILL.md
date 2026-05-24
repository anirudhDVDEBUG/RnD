---
name: zeroclaw_subagent_orchestration
description: |
  Orchestrate multi-agent workflows using the ZeroClaw subagent pattern with Claude Code Router and MCP.
  Triggers: "orchestrate subagents", "zeroclaw routing", "multi-agent pipeline", "claude code router", "subagent orchestration", "MCP agent routing"
---

# ZeroClaw Subagent Orchestration

Orchestrate complex AI workflows by decomposing tasks into specialized subagents using the ZeroClaw pattern with Claude Code Router and MCP integration.

## When to use

- "Set up a multi-agent pipeline to handle this complex task"
- "Orchestrate subagents to break down and parallelize this workflow"
- "Route this task across specialized Claude agents using ZeroClaw"
- "Create a subagent orchestration with MCP tools for this project"
- "Build an agent router that delegates to specialized sub-agents"

## How to use

### 1. Define the Task Decomposition

Break the user's complex task into discrete, parallelizable subtasks. Each subtask maps to a specialized subagent.

```markdown
## Task Decomposition
- Subtask A: [Research / data gathering] → Research Agent
- Subtask B: [Code generation] → Code Agent  
- Subtask C: [Review / validation] → Review Agent
- Subtask D: [Integration / assembly] → Orchestrator Agent
```

### 2. Configure the Agent Router

Set up routing logic that dispatches subtasks to the appropriate subagent based on task type:

```python
# ZeroClaw Router Pattern
router_config = {
    "agents": {
        "research": {
            "role": "Gather information, search codebases, read documentation",
            "tools": ["Grep", "Glob", "Read", "WebFetch"],
            "subagent_type": "Explore"
        },
        "code": {
            "role": "Write, edit, and refactor code",
            "tools": ["Edit", "Write", "Bash"],
            "subagent_type": "Code"
        },
        "review": {
            "role": "Validate output, run tests, check quality",
            "tools": ["Bash", "Read", "Grep"],
            "subagent_type": "Review"
        }
    },
    "routing_strategy": "parallel_then_merge"  # or "sequential", "fan_out_fan_in"
}
```

### 3. Launch Subagents

Use the Claude Code Agent tool to spawn specialized subagents:

- **Explore agents** (`subagent_type=Explore`): For research, codebase analysis, and information gathering
- **Code agents** (`subagent_type=Code`): For implementation tasks that produce file changes
- **Review agents**: For validation, testing, and quality checks

Dispatch independent subtasks in parallel. Chain dependent subtasks sequentially, passing outputs as inputs.

### 4. Merge and Synthesize Results

Collect outputs from all subagents and synthesize into a unified result:

1. Gather all subagent outputs
2. Resolve any conflicts between parallel outputs
3. Validate the combined result against the original task requirements
4. Present the final integrated output to the user

### 5. MCP Integration (Optional)

Connect external tools via MCP servers to extend agent capabilities:

- Add domain-specific MCP servers for specialized data sources
- Configure MCP tool routing so each subagent has access to relevant external tools
- Use the Claude Code proxy pattern to manage MCP connections across subagents

## Architecture Overview

```
[User Task]
    |
    v
[Orchestrator / Router]
    |         |         |
    v         v         v
[Agent A] [Agent B] [Agent C]   (parallel execution)
    |         |         |
    v         v         v
[MCP Tools] [MCP Tools] [MCP Tools]  (optional)
    |         |         |
    +----+----+----+----+
         |
         v
  [Result Merger]
         |
         v
  [Final Output]
```

## Best Practices

- Keep each subagent focused on a single responsibility
- Use parallel execution for independent subtasks to maximize throughput
- Pass minimal, well-defined context to each subagent to reduce token usage
- Use the orchestrator to handle error recovery and retries
- Prefer `subagent_type=Explore` for read-only research to protect the main context window

## References

- Source: [muhammadqasimkalhoro94-blip/claude-zeroclaw-agentics](https://github.com/muhammadqasimkalhoro94-blip/claude-zeroclaw-agentics)
- Pattern: ZeroClaw Subagents 2026 — AI Orchestration with Claude Code Router & MCP
