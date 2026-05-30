# How to Use Ringback Voice Call MCP

## Install (Demo Mode -- 30 seconds)

```bash
cd ringback_voice_call_mcp
bash run.sh
```

Demo mode uses Python stdlib only. No pip installs, no SIP server, no API keys.

## Install (Production Mode)

### 1. Clone the source repo

```bash
git clone https://github.com/mohitbadwal/ringback.git
cd ringback
pip install -r requirements.txt
```

### 2. Install system dependencies

- **pjsua2**: PJSIP Python bindings for SIP call handling
  ```bash
  # Ubuntu/Debian
  sudo apt install python3-pjsua2
  # macOS (build from source)
  brew install pjsip
  ```
- **whisper.cpp**: Local speech-to-text
  ```bash
  git clone https://github.com/ggerganov/whisper.cpp
  cd whisper.cpp && make
  ./models/download-ggml-model.sh base.en
  ```
- **Linphone**: Free SIP client on your phone ([linphone.org](https://www.linphone.org/))

### 3. Set up a SIP account

Register a free SIP account (e.g., [sip2sip.info](https://sip2sip.info)) or run a local SIP server (Opalvoip, Kamailio). Configure Linphone on your phone with the same SIP domain.

## MCP Server Configuration

Add this to `~/.claude.json` (or project `.mcp.json`):

```json
{
  "mcpServers": {
    "ringback": {
      "command": "python3",
      "args": ["/absolute/path/to/ringback/server.py"],
      "env": {
        "SIP_USERNAME": "your_sip_username",
        "SIP_PASSWORD": "your_sip_password",
        "SIP_DOMAIN": "your_sip_domain",
        "CALL_TARGET": "sip:your_phone@your_sip_domain"
      }
    }
  }
}
```

Replace the `env` values with your actual SIP credentials and the SIP URI of your Linphone app.

## Three MCP Tools

| Tool | What it does |
|------|-------------|
| `ringback_call` | Place a voice call, speak a message via TTS, optionally wait for spoken response (transcribed via whisper.cpp) |
| `ringback_tiered_alert` | Send push notification (ntfy/Pushover) first, escalate to voice call if priority is high/critical |
| `ringback_status` | Check SIP registration status, active calls, configured backends |

## First 60 Seconds

After adding the MCP config, restart Claude Code and try:

**Input (prompt to Claude):**
> "Call me on my phone and tell me the nightly build failed on the auth-service repo."

**What happens:**
1. Claude calls `ringback_call` with the message
2. Your phone rings via SIP/Linphone
3. TTS speaks: "The nightly build failed on the auth-service repo."
4. You respond verbally: "Okay, I'll check the logs."
5. whisper.cpp transcribes your response
6. Claude receives the transcription and continues the conversation

**Output (returned to Claude):**
```json
{
  "call": {
    "call_id": "call-1717012345-4821",
    "target": "sip:your_phone@your_domain",
    "status": "ringing"
  },
  "tts": {
    "tts_engine": "piper-tts",
    "status": "spoken",
    "estimated_duration_ms": 3080
  },
  "response": {
    "transcription": "Okay, I'll check the logs.",
    "confidence": 0.95,
    "stt_engine": "whisper.cpp"
  },
  "hangup": {
    "status": "hung_up"
  }
}
```

**Tiered alert input:**
> "Send me a critical alert about the database replication lag. Escalate to a phone call."

**What happens:**
1. ntfy push notification sent
2. Pushover notification sent (critical priority)
3. Voice call placed automatically as escalation
4. Full call flow (TTS + STT) executes

## Notification Backend Setup (Optional)

- **ntfy**: Self-hosted or use [ntfy.sh](https://ntfy.sh/). No account needed for public topics.
- **Pushover**: Get a user key at [pushover.net](https://pushover.net/) ($5 one-time).

These are optional -- the voice call works independently.
