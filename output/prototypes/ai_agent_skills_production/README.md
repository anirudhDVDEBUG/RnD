# AI Agent Skills for Production-Grade Applications

**TL;DR**: A Python framework for building self-contained, reusable AI agent skills that work across Claude, Codex, and Cursor. Each skill follows a BaseSkill pattern with validation, error handling, and a standard result envelope.

## Headline Result

```
$ bash run.sh
Registered Skills:
  - web_scraper v1.0.0: Extract structured data from HTML content
  - text_summarizer v1.0.0: Summarize text using extractive sentence scoring
  - data_validator v1.0.0: Validate structured data against a schema definition

All 3 skills executed successfully without external API keys.
```

Three production-grade skills running end-to-end in under 1 second, zero external dependencies, ready for agent integration.

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) - Installation, setup, and first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) - Architecture, data flow, and limitations
- [Source repo](https://github.com/DevelopersGlobal/ai-agent-skills)
