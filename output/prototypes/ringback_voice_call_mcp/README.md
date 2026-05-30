# Ringback Voice Call MCP

**Let your AI agent call your phone and talk to you** -- MCP servers for live, interruptible voice calls + tiered alerts, using free self-hosted pieces (pjsua2 + whisper.cpp + Linphone). No paid telephony, no extra API keys.

## Headline Result

```
Agent: "CRITICAL: Database replication lag is 62s and rising."
  → ntfy push sent ✓
  → Pushover alert sent ✓
  → SIP voice call placed to sip:oncall@sip.example.com ✓
  → TTS spoken into call ✓
  → Callee response transcribed: "I'm on it. Give me five minutes."
```

An AI agent that can **actually ring your phone**, speak a message aloud, listen to your reply, and bring the transcription back into the conversation -- all self-hosted, zero telephony costs.

## Quick Start

```bash
bash run.sh
```

No API keys or SIP setup needed -- the demo runs in mock mode and exercises all three MCP tools end-to-end.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install steps, MCP config JSON, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, data flow, limitations, why it matters

## Source

[mohitbadwal/ringback](https://github.com/mohitbadwal/ringback)
