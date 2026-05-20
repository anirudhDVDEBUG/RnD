---
name: datasette_llm_accountant
description: |
  Install, configure, and troubleshoot datasette-llm — a Datasette plugin that adds LLM prompting capabilities to Datasette instances using Simon Willison's LLM library.
  TRIGGER: user mentions datasette-llm, llm_prompt_context hook, Datasette LLM integration, or wants to add AI/LLM features to a Datasette instance.
---

# datasette-llm Integration Skill

A skill for working with `datasette-llm`, the Datasette plugin that integrates LLM prompting capabilities into Datasette.

## When to use

- "How do I add LLM prompting to my Datasette instance?"
- "Help me install and configure datasette-llm"
- "I'm getting an error with llm_prompt_context() not collecting responses"
- "Set up datasette-llm with my Datasette project"
- "Debug my datasette-llm plugin hook"

## How to use

### Installation

```bash
pip install datasette-llm
```

### Key Concepts

1. **datasette-llm** is a Datasette plugin that brings LLM capabilities (via Simon Willison's `llm` library) into Datasette.
2. It provides the `llm_prompt_context()` hook, which allows plugins to supply additional context to LLM prompts.
3. As of version **0.1a8**, a bug was fixed where `llm_prompt_context()` did not fully collect chains of responses (issue #7).

### Configuration Steps

1. Install datasette-llm into your Datasette environment:
   ```bash
   pip install datasette-llm
   ```

2. Ensure you have at least one LLM model plugin installed (e.g., `llm-claude-3`, `llm-gpt-4`):
   ```bash
   llm install llm-claude-3
   ```

3. Configure your LLM API keys:
   ```bash
   llm keys set anthropic
   ```

4. Start Datasette — the plugin will be auto-discovered:
   ```bash
   datasette serve mydb.db
   ```

### Using the llm_prompt_context() Hook

The `llm_prompt_context()` plugin hook allows other Datasette plugins to inject context into LLM prompts. If you are developing a plugin that supplies context:

```python
from datasette import hookimpl

@hookimpl
def llm_prompt_context(datasette, request):
    # Return additional context string or an iterable of context chunks
    return "Additional context for the LLM prompt."
```

**Important (v0.1a8 fix):** Ensure you are on version 0.1a8 or later if your hook returns chained/iterable responses, as earlier versions did not fully collect chains of responses.

### Troubleshooting

- **Incomplete context in prompts:** Upgrade to datasette-llm >= 0.1a8 to fix the chain collection bug.
- **Plugin not loading:** Verify installation with `datasette plugins` and check that datasette-llm appears in the list.

## References

- [datasette-llm 0.1a8 Release Notes](https://simonwillison.net/2026/May/19/datasette-llm/#atom-everything)
- [datasette-llm GitHub Repository](https://github.com/datasette/datasette-llm)
- [Bug fix: llm_prompt_context() chain collection — Issue #7](https://github.com/datasette/datasette-llm/issues/7)
