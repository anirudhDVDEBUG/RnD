# mem0 -- Universal Memory Layer for AI Agents

**TL;DR:** mem0 gives any AI agent persistent, structured memory across sessions. It auto-extracts facts from conversations, deduplicates them, and retrieves relevant context via vector search -- turning stateless LLM calls into personalized, context-aware interactions.

## Headline Result

```
Added: "I prefer dark mode and Python over JavaScript."
  -> extracted: "Prefers dark mode"
  -> extracted: "Likes Python over JavaScript"

Search("testing frameworks", user_id="bob")
  -> "Uses pytest for testing" (score: 0.87)
```

One `pip install` + 5 lines of code = your agent remembers everything about each user.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install, configure, run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, data flow, limitations
- **[run.sh](run.sh)** -- `bash run.sh` for a fully offline demo (no API keys)
- **Source:** https://github.com/mem0ai/mem0 (+63 stars/day)
