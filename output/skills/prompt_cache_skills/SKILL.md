---
name: prompt_cache_skills
description: |
  Drop-in prompt-caching patches for LLM agent harnesses. Analyzes your agent setup and applies prompt-cache optimizations to reduce token usage and API costs.
  Triggers: prompt caching, token optimization, reduce API costs, cache prompts, optimize LLM tokens
---

# Prompt Cache Skills

Drop-in prompt-caching fixes for the LLM agent harness you use. Point your AI coding agent at this skill and it ships the patches to optimize token usage through prompt caching.

## When to use

- "Optimize my agent's prompt caching to reduce token costs"
- "Apply prompt-cache patches to my Claude Code / Aider / Cline setup"
- "Reduce API token usage in my LLM agent pipeline"
- "Set up prompt caching for my coding agent harness"
- "Fix prompt caching configuration for my AI assistant"

## How to use

1. **Identify the agent harness**: Determine which LLM agent harness is in use (Claude Code, Aider, Cline, Roo Code, OpenCode, or custom).

2. **Audit current caching behavior**: Review the current prompt/system message configuration to identify where cache breakpoints are missing or suboptimal. Look for:
   - System prompts that change unnecessarily between turns (busting the cache)
   - Long static context (tool definitions, instructions) not marked for caching
   - Conversation history structures that prevent prefix caching

3. **Apply prompt-cache optimizations**:
   - **Static prefix stabilization**: Ensure system prompts and tool definitions are placed in a stable prefix that doesn't change between requests, enabling Anthropic's automatic prompt caching.
   - **Breakpoint insertion**: For APIs that support explicit cache control (e.g., Anthropic's `cache_control` parameter), add `ephemeral` breakpoints at optimal positions — typically after the system prompt, after tool definitions, and at the end of prior conversation context.
   - **Message ordering**: Restructure message arrays so cacheable content comes first (system → tools → cached history → new user message).
   - **Minimize cache-busting**: Remove dynamic elements (timestamps, random IDs, changing metadata) from cached prefixes. Move them to the non-cached tail of the prompt.

4. **Validate the fix**: After applying patches, verify caching is active by checking API response headers for `cache_creation_input_tokens` and `cache_read_input_tokens` fields. A successful cache hit shows `cache_read_input_tokens > 0` on subsequent requests.

5. **Supported agent harnesses**:
   - **Claude Code**: Optimize CLAUDE.md and system prompt structures
   - **Aider**: Patch prompt construction in aider's coder modules
   - **Cline / Roo Code**: Fix system prompt templates for cache stability
   - **OpenCode**: Adjust prompt assembly pipeline
   - **Custom agents**: Apply the same prefix-stabilization and breakpoint patterns to any Anthropic API or OpenAI-compatible integration

## Key principles

- **Stable prefixes**: The first N tokens of your prompt must be identical across requests for caching to activate. Even a single token change invalidates the cache.
- **Minimum cache size**: Anthropic requires at least 1,024 tokens (Claude 3.5) or 2,048 tokens (Claude 3 Opus) in the cached prefix for caching to engage.
- **Cache lifetime**: Cached prefixes have a 5-minute TTL and are extended on cache hits. Frequent requests keep the cache warm.
- **Cost savings**: Cache reads cost 90% less than re-processing the same tokens. For agents with large system prompts and tool definitions, this can reduce costs by 50-80%.

## References

- Source repository: [OnlyTerp/prompt-cache-skills](https://github.com/OnlyTerp/prompt-cache-skills)
- [Anthropic Prompt Caching documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- Supports: Claude Code, Aider, Cline, Roo Code, OpenCode, and custom LLM agent setups
