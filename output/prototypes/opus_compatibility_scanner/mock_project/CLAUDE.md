# CLAUDE.md — Example project config (intentionally contains 4.6 patterns)

## Model Configuration
This project uses claude-opus-4-6 as the primary model.
Fallback model: claude-opus-4-6-20250115

## Custom Instructions
When generating code, always include type annotations.
Use the contextWindow of 1000000 tokens for large files.

## Subagent Configuration
For code review tasks, delegate_to a specialized agent.
Set agent_prompt to focus on security analysis.
Set max_agent_turns to 10 for complex reviews.

## Permissions
The project uses allow_bash for shell commands.
Set allow_edit for file modifications.
