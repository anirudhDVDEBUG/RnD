---
name: Claude Code WhatsApp & Telegram Bot
description: |
  Deploy a Claude Code agent on WhatsApp and Telegram with voice, vision, file analysis, RAG, and multi-tool reasoning. Runs on Termux (Android) or any Node.js environment.
  Triggers: whatsapp bot, telegram bot, claude whatsapp, mobile agent, termux claude, messaging bot claude
---

# Claude Code WhatsApp & Telegram Bot

Set up a Claude Code-powered agent accessible via WhatsApp and Telegram, featuring voice messages, image/vision analysis, file processing, RAG (Retrieval-Augmented Generation), and multi-tool reasoning. Designed to run on Termux (Android) or any Node.js server.

## When to use

- "Set up a Claude bot on WhatsApp"
- "Deploy a Claude agent on Telegram with voice and vision support"
- "Build a mobile AI agent that runs on Android via Termux"
- "Create a messaging bot with RAG and file analysis using Claude"
- "Run Claude Code on WhatsApp with multi-tool reasoning"

## How to use

### Prerequisites

- Node.js 18+ (or Termux on Android with Node.js installed)
- Anthropic API key
- For Telegram: a Telegram Bot Token from @BotFather
- For WhatsApp: a phone number to link via QR code (uses Baileys library)

### Step 1: Clone and install

```bash
git clone https://github.com/ghanibot/Claude-Code-on-WhatsApp.git
cd Claude-Code-on-WhatsApp
npm install
```

Or use the one-click installer if running on Termux:

```bash
bash install.sh
```

### Step 2: Configure environment

Create a `.env` file with your credentials:

```env
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=your_telegram_bot_token  # optional, for Telegram
```

### Step 3: Start the bot

```bash
node index.js
```

For WhatsApp, scan the QR code displayed in the terminal with your WhatsApp app. For Telegram, the bot will connect automatically using the bot token.

### Features

- **Voice messages**: Send voice notes and get AI-powered transcription and responses
- **Vision/Image analysis**: Send images for Claude to analyze and describe
- **File processing**: Upload documents (PDF, text, code files) for analysis
- **RAG**: Retrieval-Augmented Generation for context-aware responses from your documents
- **Multi-tool reasoning**: Claude can chain multiple tools together to solve complex tasks
- **Termux support**: Runs natively on Android devices via Termux

### Architecture

The bot uses:
- **Baileys** for WhatsApp Web API connection (no official API needed)
- **Telegraf/node-telegram-bot-api** for Telegram integration
- **Anthropic SDK** for Claude API calls
- **MCP servers** for extended tool capabilities

## References

- Source repository: [ghanibot/Claude-Code-on-WhatsApp](https://github.com/ghanibot/Claude-Code-on-WhatsApp)
- [Anthropic API documentation](https://docs.anthropic.com)
- [Baileys WhatsApp library](https://github.com/WhiskeySockets/Baileys)
