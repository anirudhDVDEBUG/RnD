# Technical Details -- Ringback Voice Call MCP

## What It Does

Ringback is an MCP server that gives AI agents the ability to place real VoIP phone calls using entirely self-hosted, free components. When an agent invokes the `ringback_call` tool, the server registers with a SIP provider via pjsua2 (the Python bindings for PJSIP), dials the target phone running Linphone, plays text-to-speech audio into the call, and transcribes the callee's spoken response using whisper.cpp. The entire round-trip -- agent message in, human voice response out -- happens over a single SIP call with no paid telephony APIs.

The tiered alert system adds an escalation layer: low-priority messages go to push notifications (ntfy or Pushover), while high/critical alerts automatically escalate to a live voice call if the user doesn't acknowledge within a timeout window.

## Architecture

```
Claude Agent
    │
    ▼ (MCP JSON-RPC over stdio)
┌──────────────────────────┐
│  Ringback MCP Server     │
│  ┌────────────────────┐  │
│  │ ringback_call       │──┼──► pjsua2 (SIP) ──► Linphone (phone)
│  │ ringback_tiered_alert│──┼──► ntfy / Pushover (push)
│  │ ringback_status     │  │         │
│  └────────────────────┘  │         ▼
│                          │    piper-tts (speak)
│                          │    whisper.cpp (listen)
└──────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `server.py` | MCP server -- JSON-RPC handler, tool definitions, SIP/TTS/STT orchestration |
| `demo.py` | End-to-end demo exercising all three tools via subprocess |
| `run.sh` | One-command demo runner |

### Data Flow (voice call)

1. Agent sends `tools/call` with `ringback_call` and a text message
2. Server registers SIP account via pjsua2 (if not already registered)
3. Server places SIP INVITE to `CALL_TARGET`
4. On answer: piper-tts converts message text to PCM audio, streamed into the call
5. After TTS completes: whisper.cpp captures callee's microphone audio and transcribes it
6. Server returns JSON with call metadata + transcription to the agent
7. SIP BYE sent, call terminated

### Dependencies

| Component | Role | License |
|-----------|------|---------|
| **pjsua2** (PJSIP) | SIP call handling, codec negotiation, RTP media | GPL-2.0 |
| **whisper.cpp** | Local speech-to-text (no cloud API) | MIT |
| **piper-tts** | Local text-to-speech | MIT |
| **Linphone** | Free SIP client for iOS/Android/desktop | GPL-3.0 |
| **ntfy** | Push notification delivery | Apache-2.0 |
| **Pushover** | Push notification delivery (optional, $5 one-time) | Proprietary |

All core components are free and self-hostable. No Twilio, no Google Cloud Speech, no AWS Polly.

## Limitations

- **pjsua2 build complexity**: PJSIP Python bindings are notoriously difficult to build from source. Pre-built packages exist for Ubuntu (`python3-pjsua2`) but macOS/Windows require manual compilation.
- **Audio quality**: whisper.cpp transcription accuracy depends on call audio quality (codec, network jitter). SIP calls over lossy networks may produce lower-confidence transcriptions.
- **Single call at a time**: The current architecture handles one active call. Concurrent calls would need connection pooling.
- **No PSTN**: This calls SIP endpoints (Linphone), not regular phone numbers. Calling a landline/mobile requires a SIP-to-PSTN gateway (e.g., a VoIP provider with DID).
- **Latency**: TTS generation + SIP setup + whisper.cpp inference adds 3-8 seconds of round-trip latency before the agent gets a response.
- **No call recording/logging**: Calls are ephemeral. If you need audit trails, you'd need to add media recording.

## What It Does NOT Do

- Does not work with regular phone numbers out of the box (SIP only)
- Does not provide a web UI or dashboard
- Does not handle inbound calls (agent can't receive calls, only make them)
- Does not do real-time conversation (it's speak-then-listen, not full-duplex)
- Does not integrate with Twilio, Vonage, or any paid telephony API

## Why It Matters

**For Voice AI builders**: This is the missing "last mile" for agent-to-human communication. Most voice AI projects focus on inbound (human calls bot). Ringback flips it -- the agent initiates outbound calls. Combined with whisper.cpp for STT, it creates a closed-loop voice interaction without any cloud speech APIs.

**For agent factories / Claude-driven products**: Ringback turns any MCP-capable agent into an on-call notification system. A CI/CD monitoring agent can literally ring your phone at 3 AM when production is down, speak the error, and wait for your verbal instructions. This is a concrete differentiator over text-only alerting.

**For self-hosted / privacy-conscious deployments**: Everything runs locally. No audio leaves your network. No transcription data hits a cloud API. This matters for regulated industries (healthcare, finance) where call content may be sensitive.

**Cost advantage**: Twilio charges ~$0.013/min for voice calls + per-minute speech API costs. Ringback is $0/min after initial setup. For high-volume alerting or agent-to-team communication, the cost difference is significant.

## Source

[mohitbadwal/ringback](https://github.com/mohitbadwal/ringback)
