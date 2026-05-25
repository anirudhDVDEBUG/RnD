# Technical Details

## What It Does

This project wraps the Anthropic Claude API behind WhatsApp and Telegram message interfaces. Incoming messages (text, voice notes, images, files) are normalized by a `MessageHandler` class, converted into Claude API message format (including multimodal content blocks), and sent through a tool-use loop that can chain multiple tools (web search, calculation, RAG document retrieval) before returning a final response. The bot maintains per-user conversation history for contextual multi-turn dialogue.

The WhatsApp connection uses the Baileys library, which reverse-engineers the WhatsApp Web protocol -- no official Business API needed. Telegram uses the standard Telegraf bot framework. Both feed into the same `MessageHandler`, making the platform layer swappable.

## Architecture

```
WhatsApp (Baileys)  ──┐
                      ├──> MessageHandler ──> Claude API (tool-use loop)
Telegram (Telegraf) ──┘        │
                               ├── Voice: audio buffer -> transcription -> text
                               ├── Image: base64 encode -> vision content block
                               ├── File:  extract text -> RAG ingest or inline
                               └── Tools: web_search, calculate, rag_lookup
```

### Key Files

| File | Purpose |
|------|---------|
| `src/message-handler.js` | Core routing logic: message type detection, Claude API calls with tool-use loop, conversation history management |
| `src/mock-bot.js` | Demo script simulating 5 scenarios with mock Anthropic client and RAG store |
| `package.json` | Dependencies: Baileys, Telegraf, Anthropic SDK, pdf-parse, fluent-ffmpeg |
| `run.sh` | Entry point for zero-config demo |

### Data Flow

1. Platform adapter (Baileys/Telegraf) receives a message event
2. Message is classified by type (text/voice/image/file)
3. Content is normalized into Claude API content blocks
4. `_callWithToolLoop` sends to Claude with available tools
5. If Claude requests tool use, tools execute and results feed back (up to 5 iterations)
6. Final text response is sent back to the user via the originating platform

### Dependencies

- **@whiskeysockets/baileys** -- WhatsApp Web protocol client (no official API)
- **telegraf** -- Telegram Bot API framework
- **@anthropic-ai/sdk** -- Claude API client with tool use support
- **pdf-parse** -- Extract text from PDF uploads
- **fluent-ffmpeg** -- Audio format conversion for voice messages
- **dotenv** -- Environment variable management

### Model Calls

- Default model: `claude-sonnet-4-6-20250514`
- Max tokens: 4096 per response
- System prompt instructs concise messaging-style responses
- Tool-use loop allows up to 5 chained tool calls per message

## Limitations

- **WhatsApp via Baileys is unofficial.** It reverse-engineers WhatsApp Web and can break with WhatsApp updates. Accounts may be banned if flagged as automated. Not suitable for production commercial use without risk assessment.
- **No built-in speech-to-text.** Voice transcription requires an external STT service (e.g., Whisper API). The handler has a placeholder for this.
- **RAG is naive.** The included RAG store is a simple in-memory map. Production use needs a vector database (Pinecone, ChromaDB, pgvector).
- **No message queue or persistence.** Messages are processed synchronously; conversation history lives in memory and is lost on restart.
- **Single-instance only.** No clustering, load balancing, or horizontal scaling built in.
- **Termux constraints.** Running on Android means limited RAM, no GPU, and potential battery/network issues for long-running bots.

## Why It Matters

For teams building Claude-driven products:

- **Lead-gen / marketing bots:** Deploy a Claude agent directly in the channels where customers already are (WhatsApp has 2B+ users). No app install needed.
- **Agent factories:** The `MessageHandler` pattern (normalize input -> Claude tool loop -> platform-agnostic response) is reusable across any messaging platform. Add Slack, Discord, or SMS by writing a thin adapter.
- **Voice AI:** The voice-message pipeline (receive audio -> transcribe -> Claude -> respond) is a building block for voice-first AI agents.
- **Mobile-first deployment:** Termux support means you can prototype a Claude agent from an Android phone with zero cloud infrastructure.
- **RAG integration pattern:** The file-upload-to-RAG flow demonstrates how to give Claude access to user-specific documents in a conversational interface.
