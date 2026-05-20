# datasette-llm: Add LLM Prompting to Any Datasette Instance

**TL;DR:** `datasette-llm` is a Datasette plugin that integrates Simon Willison's `llm` library, letting any Datasette instance answer natural-language questions about its data. Version 0.1a8 fixes a bug where the `llm_prompt_context()` hook silently dropped context from generator-based plugins.

**Headline result:** `bash run.sh` shows the before/after of the v0.1a8 fix -- a generator plugin's sample rows are lost in the broken version and fully collected in the fixed version, then a mock LLM generates working SQL from the complete context.

| File | What's inside |
|------|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install steps, Claude skill setup, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, hook system, limitations |
| [run.sh](run.sh) | End-to-end demo with mock data (no API keys needed) |
