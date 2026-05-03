# AGENTS.md — Subagent definitions

## Code Review Agent
- subagent_type: code_review
- subagent_model: claude-opus-4-6
- agent_prompt: "Review code for bugs, security issues, and style violations."
- max_agent_turns: 5

## Documentation Agent
- subagent_type: documentation
- agent_prompt: "Generate comprehensive documentation."
