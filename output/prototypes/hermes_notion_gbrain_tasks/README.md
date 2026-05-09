# Hermes Notion GBrain — Natural Language Task Manager

**TL;DR:** Send a WhatsApp or Slack message like *"Add a task to review the Q3 report by Friday"* and it gets parsed, enriched with relevant knowledge from GBrain, and created as a structured Notion page — automatically.

## Headline Result

```
📱 WhatsApp: "Add a task to review the Q3 report by Friday"
  → NLP Parse: intent=create, priority=medium, due=2026-05-15
  → GBrain:   context="Company reports follow Q-template format..." (85% match)
  → Notion:   Page created with title, priority, due date, tags, and knowledge callout
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, and run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **Source:** [mantenasud/hermes-notion-gbrain](https://github.com/mantenasud/hermes-notion-gbrain)
