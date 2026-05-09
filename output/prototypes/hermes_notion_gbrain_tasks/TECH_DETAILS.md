# Technical Details: Hermes Notion GBrain

## What It Does

Hermes is a conversational task management agent that accepts natural language messages from WhatsApp or Slack, parses them into structured task intents using regex-based NLP, enriches them with contextual knowledge from a GBrain knowledge base, and persists them as structured pages in a Notion database. It handles the full task lifecycle: create, update, complete, and list.

The agent acts as middleware between chat platforms (input) and Notion (storage), with GBrain providing an intelligence layer that automatically attaches relevant context, documents, and suggested assignees to each task.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  WhatsApp /  │────▶│  NLPParser   │────▶│   GBrain     │────▶│  Notion API  │
│  Slack       │     │  (intent,    │     │  Enricher    │     │  (create/    │
│  Webhook     │     │   priority,  │     │  (context,   │     │   update     │
│              │     │   due date,  │     │   docs,      │     │   pages)     │
│              │     │   tags)      │     │   assignees) │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `hermes_agent.py` | Core classes: `NLPParser`, `GBrainEnricher`, `NotionTaskManager`, `HermesAgent` |
| `demo.py` | End-to-end demo with 8 mock messages showing all intents |
| `run.sh` | Entry point — runs demo with no external dependencies |
| `requirements.txt` | Dependencies for full integration (requests, notion-client, python-dotenv) |

### Data Flow

1. **Message arrives** via webhook (WhatsApp Business API or Slack Events API)
2. **NLPParser.parse()** extracts intent (create/update/complete/list), title, priority (high/medium/low from keyword matching), due date (relative/absolute date parsing), and tags (hashtags + category inference)
3. **GBrainEnricher.enrich()** matches task keywords against a knowledge base, attaching context strings, related document links, and suggested assignees with a confidence score
4. **NotionTaskManager.create_task()** builds a Notion page object with properties (Name, Status, Priority, Due Date, Tags) and child blocks (GBrain callout, related docs list), then submits via the Notion API
5. **Reply** is sent back to the originating channel

### Dependencies

- **Python 3.10+** (uses `str | None` union syntax)
- `requests` — HTTP calls to Notion and GBrain APIs
- `notion-client` — Official Notion SDK for page/database operations
- `python-dotenv` — Environment variable management
- Demo uses only stdlib (re, json, datetime)

### Model Calls

The current implementation uses **regex-based NLP** (no LLM calls). The GBrain enrichment is a keyword-matching lookup. In a production setup, you'd replace `NLPParser` with an LLM call for intent classification and `GBrainEnricher` with the actual GBrain API for semantic knowledge retrieval.

## Limitations

- **No LLM-powered parsing**: Intent detection uses regex patterns, not a language model. Complex or ambiguous messages may be misclassified.
- **GBrain is mocked**: The demo uses a hardcoded knowledge base. Real GBrain integration requires an API key and network access.
- **No webhook server**: The demo simulates incoming messages. Production use requires running a web server (Flask/FastAPI) to receive webhooks.
- **No auth/multi-user**: No user authentication or multi-tenant support. Each instance manages a single Notion database.
- **English only**: NLP patterns are English-specific.
- **No message threading**: Each message is processed independently — no conversation context across messages.

## Why This Matters for Claude-Driven Products

- **Agent factories**: This is a clean pattern for building chat-to-database agents. Replace Notion with any CRM/project tool and you have a reusable agent template. Claude could replace the regex NLP layer for much better intent parsing.
- **Lead-gen / marketing**: A WhatsApp bot that captures tasks and enriches them with knowledge context is directly applicable to lead capture workflows — replace "task" with "lead" and GBrain with a company knowledge base.
- **Voice AI**: The NLP parsing layer could accept voice-to-text transcripts. The architecture (parse → enrich → store) maps cleanly to voice agent pipelines.
- **Knowledge-enriched workflows**: The GBrain enrichment pattern (auto-attach context from a knowledge base) is valuable for any agent that needs to augment user input with organizational knowledge before taking action.
