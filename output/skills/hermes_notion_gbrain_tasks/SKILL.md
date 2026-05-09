---
name: hermes_notion_gbrain_tasks
description: |
  Set up natural language task management via WhatsApp/Slack → Notion with GBrain knowledge enrichment.
  Triggers: hermes notion, whatsapp task management, notion task bot, gbrain knowledge enrichment, natural language tasks notion
---

# Hermes Notion GBrain Task Manager

Natural language task management that routes messages from WhatsApp or Slack into Notion, with automatic GBrain knowledge enrichment.

## When to use

- "Set up a WhatsApp bot that creates Notion tasks from natural language"
- "Build a Slack-to-Notion task management pipeline with AI enrichment"
- "Configure Hermes agent for natural language task capture into Notion"
- "Integrate GBrain knowledge base with Notion task management"
- "Create a conversational task manager that syncs to Notion"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/mantenasud/hermes-notion-gbrain.git
cd hermes-notion-gbrain
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file with the required credentials:

```bash
# Notion Integration
NOTION_API_KEY=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id

# GBrain (knowledge enrichment)
GBRAIN_API_KEY=your_gbrain_api_key

# Messaging platform (WhatsApp/Slack)
# Configure the relevant webhook endpoints and tokens
```

### 3. Set up Notion integration

1. Go to [Notion Developers](https://developers.notion.com/) and create a new integration
2. Share your target Notion database with the integration
3. Copy the integration token and database ID into your `.env`

### 4. Configure messaging channel

- **WhatsApp**: Set up a WhatsApp Business API webhook pointing to your server endpoint
- **Slack**: Create a Slack app with event subscriptions and point to your server endpoint

### 5. Run the agent

```bash
python main.py
```

### Architecture overview

```
User (WhatsApp/Slack)
  → Hermes Agent (NLP parsing)
    → GBrain (knowledge enrichment)
      → Notion API (task creation/update)
```

The Hermes agent receives natural language messages, parses task intent (create, update, list, complete), enriches tasks with relevant knowledge from GBrain, and manages them in a Notion database.

### Key features

- **Natural language input**: Send messages like "Add a task to review the Q3 report by Friday" and it creates structured Notion entries
- **GBrain enrichment**: Automatically attaches relevant knowledge context to tasks
- **Multi-channel**: Works with both WhatsApp and Slack as input channels
- **Task lifecycle**: Create, update, complete, and list tasks via conversation

## References

- Source repository: [mantenasud/hermes-notion-gbrain](https://github.com/mantenasud/hermes-notion-gbrain)
- Topics: ai-agent, gbrain, hermes, notion, task-management, whatsapp-bot
- Language: Python
