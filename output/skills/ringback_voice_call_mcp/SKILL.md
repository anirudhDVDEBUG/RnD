---
name: ringback_voice_call_mcp
description: |
  Set up Ringback MCP server so AI agents can make live voice calls to your phone using free self-hosted components (pjsua2 + whisper.cpp + Linphone). Supports interruptible voice calls and tiered alerts with no paid telephony or extra API keys.
  Triggers: voice call, phone call, ringback, MCP telephony, SIP call, VoIP agent, agent call phone, text-to-speech call, speech notification
---

# Ringback Voice Call MCP

Let your AI agent call your phone and talk to you — MCP servers for live, interruptible voice calls + tiered alerts, using free self-hosted pieces (pjsua2 + whisper.cpp + Linphone). No paid telephony, no extra API key.

## When to use

- "Set up voice calls from my AI agent to my phone"
- "I want Claude to call me when something important happens"
- "Configure Ringback MCP server for VoIP notifications"
- "Let my agent make a live phone call using SIP"
- "Set up self-hosted telephony for AI agent alerts"

## How to use

### Prerequisites

- Python 3.x
- [Linphone](https://www.linphone.org/) (free SIP client) installed on your phone
- pjsua2 (PJSIP Python bindings) for SIP call handling
- whisper.cpp for speech-to-text
- A local SIP server or SIP account for routing calls
- macOS or Linux environment

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohitbadwal/ringback.git
   cd ringback
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up pjsua2 and whisper.cpp** according to the project's documentation.

4. **Configure your SIP account** in the project configuration files so the MCP server can place calls to your Linphone client.

### MCP Server Configuration

Add the Ringback MCP server to your Claude Code configuration (`~/.claude/settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "ringback": {
      "command": "python",
      "args": ["path/to/ringback/server.py"],
      "env": {
        "SIP_USERNAME": "your_sip_username",
        "SIP_PASSWORD": "your_sip_password",
        "SIP_DOMAIN": "your_sip_domain",
        "CALL_TARGET": "sip:your_phone@domain"
      }
    }
  }
}
```

### Features

- **Live voice calls**: Agent initiates a real VoIP call to your phone via SIP/pjsua2
- **Interruptible**: You can speak back during the call; whisper.cpp transcribes your responses
- **Tiered alerts**: Supports escalation via ntfy and Pushover before making a call
- **Fully self-hosted**: No Twilio, no paid telephony APIs required
- **Text-to-speech**: Agent's messages are spoken aloud during the call

### Usage

Once configured, the MCP tools allow your agent to:
- Place a voice call to your phone with a spoken message
- Listen for your spoken response (transcribed via whisper.cpp)
- Send tiered notifications (push → call escalation)

Example agent prompt:
> "Call me on my phone and tell me the deployment failed, then wait for my response."

## References

- **Source repository**: [mohitbadwal/ringback](https://github.com/mohitbadwal/ringback)
- **Topics**: MCP, SIP, VoIP, telephony, text-to-speech, speech-to-text, voice-agent, Claude, Anthropic
- **Notification backends**: [ntfy](https://ntfy.sh/), [Pushover](https://pushover.net/)
