# How to Use

## Quick Demo (no keys needed)

```bash
bash run.sh
```

This runs a mock simulation showing all 5 message types (text, voice, image, file, RAG query) across WhatsApp and Telegram without any API keys.

## Full Installation

### Prerequisites

- Node.js 18+
- An Anthropic API key (`sk-ant-...`)
- For Telegram: a bot token from [@BotFather](https://t.me/BotFather)
- For WhatsApp: a phone number (you'll scan a QR code)

### Step 1: Clone the source repo

```bash
git clone https://github.com/ghanibot/Claude-Code-on-WhatsApp.git
cd Claude-Code-on-WhatsApp
npm install
```

On Termux (Android):

```bash
bash install.sh
```

### Step 2: Configure environment

Create a `.env` file:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
TELEGRAM_BOT_TOKEN=123456:ABC-your-telegram-token   # optional
```

### Step 3: Start the bot

```bash
node index.js
```

- **WhatsApp:** A QR code appears in the terminal. Scan it with WhatsApp to link.
- **Telegram:** Connects automatically using the bot token.

## Claude Code Skill Setup

This is also packaged as a Claude Code skill. To install:

1. Copy the skill folder:

```bash
mkdir -p ~/.claude/skills/claude_code_whatsapp_telegram_bot
cp SKILL.md ~/.claude/skills/claude_code_whatsapp_telegram_bot/SKILL.md
```

2. Trigger phrases that activate it:
   - "Set up a Claude bot on WhatsApp"
   - "Deploy a Claude agent on Telegram with voice and vision support"
   - "Build a mobile AI agent that runs on Android via Termux"
   - "Create a messaging bot with RAG and file analysis using Claude"
   - "Run Claude Code on WhatsApp with multi-tool reasoning"

## First 60 Seconds

After `bash run.sh`, you'll see output like:

```
--- Scenario 1: Text Message (WhatsApp) ---
  [WA] Alice: Hi! What can you do?
  [Bot]: Hello! I'm your Claude-powered assistant on this messaging platform.
         I can handle text, voice messages, images, and file uploads.

--- Scenario 3: Image/Vision Analysis (WhatsApp) ---
  [WA] Carol: [Photo: whiteboard.jpg]
  [Bot]: I can see a whiteboard with a system architecture diagram. It shows
         a microservices layout with 3 services: Auth, API Gateway, and
         Data Pipeline.

--- Scenario 4: File Upload + RAG Ingestion (Telegram) ---
  [TG] Dave: [File: q3-budget.pdf]
  [Bot]: File "q3-budget.pdf" has been ingested into your knowledge base.
  [TG] Dave: What's the marketing budget for Q3?
  [Bot]: Based on your uploaded documents, the budget allocation for Q3
         marketing is $45,000...
```

The demo exercises the full message handler pipeline: routing, tool selection, conversation history, and RAG ingestion -- all with mock data so you can evaluate the architecture before plugging in real keys.
