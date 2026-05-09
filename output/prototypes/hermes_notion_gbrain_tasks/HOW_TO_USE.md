# How to Use: Hermes Notion GBrain Tasks

## Install (demo — no API keys needed)

```bash
cd hermes_notion_gbrain_tasks
bash run.sh
```

The demo runs entirely with mock data using Python stdlib. No pip install required for the demo.

## Install (full integration)

```bash
git clone https://github.com/mantenasud/hermes-notion-gbrain.git
cd hermes-notion-gbrain
pip install -r requirements.txt
```

Create a `.env` file:

```bash
NOTION_API_KEY=secret_xxxxxxxxxx
NOTION_DATABASE_ID=your_database_id
GBRAIN_API_KEY=your_gbrain_key
```

Then run:

```bash
python main.py
```

## Claude Skill Setup

This is packaged as a Claude Code skill. To install:

1. Copy the skill folder to `~/.claude/skills/hermes_notion_gbrain_tasks/`
2. The folder must contain a `SKILL.md` file

**Trigger phrases** that activate this skill:

- "hermes notion"
- "whatsapp task management"
- "notion task bot"
- "gbrain knowledge enrichment"
- "natural language tasks notion"

Example: *"Set up a WhatsApp bot that creates Notion tasks from natural language"*

## First 60 Seconds

**Input** (simulated WhatsApp messages):

```
"Add a task to review the Q3 report by Friday"
"Remind me to deploy the new API to staging in 3 days #dev"
"Schedule a meeting with the design team tomorrow #design"
"Show my tasks"
"Complete task review the Q3 report"
```

**Output:**

```
[1] 📱 WhatsApp: "Add a task to review the Q3 report by Friday"
  ├─ Intent: create (confidence: 90%)
  ├─ Title: review the Q3 report
  ├─ Priority: medium
  ├─ Due: 2026-05-15
  ├─ Tags: work
  ├─ GBrain Score: 85%
  ├─ Context: Company reports follow the Q-template format...
  ├─ Docs: Q3-Report-Template.docx, Revenue-Dashboard-Link
  └─ ✓ Task created: "review the Q3 report" (Priority: medium, Due: 2026-05-15)
     Notion Page ID: notion-0001

[6] 💬 Slack: "Show my tasks"
  └─ You have 5 task(s):
    [To Do] review the Q3 report | Priority: Medium | Due: 2026-05-15 | Tags: work
    [To Do] deploy the new API to staging | Priority: Medium | Due: 2026-05-12 | Tags: dev
    ...
```

## Notion Database Setup (for full integration)

1. Go to [developers.notion.com](https://developers.notion.com/) → Create integration
2. Share your target database with the integration
3. Required database columns: **Name** (title), **Status** (select), **Priority** (select), **Due Date** (date), **Tags** (multi-select)

## Messaging Channel Setup

- **WhatsApp**: Configure WhatsApp Business API webhook → your server's `/webhook/whatsapp` endpoint
- **Slack**: Create a Slack app with event subscriptions → your server's `/webhook/slack` endpoint
