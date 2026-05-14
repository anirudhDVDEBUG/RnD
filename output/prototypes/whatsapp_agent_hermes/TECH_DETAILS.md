# Technical Details

## What it does

The Andorina WhatsApp Agent for Hermes is a Python-based automation layer that wraps WhatsApp Web via browser automation (Selenium/WebDriver). It runs as a skill inside the Hermes agent framework, giving an AI agent the ability to send texts, voice notes, and files through a user's WhatsApp account -- on a schedule or on demand. Contact lookup is backed by the Google People API, so the agent can resolve names to phone numbers without manual input.

The key insight is that WhatsApp has no official bot API for personal accounts. Andorina works around this by driving a headless Chrome session against WhatsApp Web, simulating the same clicks and keystrokes a human user would make.

## Architecture

```
Hermes Agent Framework
  └── HermesWhatsAppAgent (skill entry point)
        ├── WhatsAppSession        # Selenium browser automation
        │     ├── authenticate()   # QR code scan flow
        │     ├── send_text()      # DOM interaction: find chat, type, send
        │     ├── send_voice_note()# Upload .ogg audio
        │     └── send_file()      # Attach & send file via clip icon
        ├── MessageScheduler       # Time-based queue, processes due messages
        ├── VoiceNoteGenerator     # TTS via gTTS -> .ogg conversion via pydub
        └── ContactBook            # Google People API wrapper for contact search
```

### Key files (this prototype)

| File | Purpose |
|---|---|
| `whatsapp_agent.py` | Core classes: agent, session, scheduler, contacts, TTS |
| `demo.py` | End-to-end demo exercising all features with mock data |
| `run.sh` | One-command runner |
| `requirements.txt` | Dependencies (stdlib-only for demo; real deps commented) |

### Data flow

1. Hermes receives a user intent (e.g., "send Alice the Q3 report")
2. `HermesWhatsAppAgent.search_contacts("Alice")` resolves to `+1-555-0101`
3. For text: `WhatsAppSession.send_text()` navigates WhatsApp Web DOM
4. For voice: `VoiceNoteGenerator.generate()` produces `.ogg`, then `send_voice_note()` uploads it
5. For scheduled sends: `MessageScheduler` queues the message and fires when due
6. All actions are logged for audit/replay

### Dependencies (real agent)

- **selenium / webdriver-manager** -- browser automation for WhatsApp Web
- **gTTS** -- Google Text-to-Speech for voice note generation
- **pydub** -- audio format conversion (MP3 -> OGG Opus)
- **google-api-python-client / google-auth-oauthlib** -- Google Contacts search
- **schedule** -- cron-like task scheduling

## Limitations

- **No official API**: relies on WhatsApp Web DOM scraping, which breaks when WhatsApp updates their frontend. Fragile by nature.
- **Single session**: one WhatsApp account per agent instance. No multi-account support.
- **No incoming messages**: this is send-only. It cannot read or respond to incoming WhatsApp messages.
- **QR code auth**: requires a one-time manual QR scan (or session cookie persistence). Cannot fully automate initial setup.
- **Linux only**: designed for Linux with Chrome/Chromium. macOS/Windows support is untested.
- **Rate limits**: WhatsApp may flag accounts that send too many automated messages. No built-in rate limiting or anti-ban logic.
- **No E2E encryption handling**: operates at the WhatsApp Web UI layer, not the protocol layer.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Lead-gen / Sales** | Auto-send follow-ups, share proposals, schedule check-ins with prospects via WhatsApp -- the most-used messaging app globally (2B+ users). |
| **Marketing** | Broadcast promotional voice notes or file attachments to segmented contact lists on a schedule. |
| **Agent factories** | Demonstrates the pattern of wrapping a consumer app (WhatsApp) as a tool for an AI agent. The same architecture applies to Telegram, Slack, SMS, or email. |
| **Voice AI** | The TTS -> voice note pipeline is a lightweight way to deliver AI-generated audio to end users without building a custom app. |

The core pattern -- browser automation as an agent tool -- is reusable. If you can drive a browser, any web app becomes an agent capability.
