# How to Use

## Quick demo (no credentials needed)

```bash
cd whatsapp_agent_hermes
bash run.sh
```

This runs the full agent lifecycle with mock data: authentication, contact search, text/voice/file sending, and scheduled delivery.

## Install the real Andorina agent

```bash
git clone https://github.com/AndorinaAI/Andorina-WhatsApp-Agent-for-Hermes.git
cd Andorina-WhatsApp-Agent-for-Hermes
pip install -r requirements.txt
```

Requirements (for the real agent, not the demo):
- Python 3.10+
- Chrome/Chromium (for Selenium-based WhatsApp Web automation)
- A WhatsApp account (scanned via QR code on first run)
- Google Cloud project with People API enabled (optional, for contact search)

## Claude Skill setup

This is a **Claude Code Skill**. To install:

```bash
mkdir -p ~/.claude/skills/whatsapp_agent_hermes
cp SKILL.md ~/.claude/skills/whatsapp_agent_hermes/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Set up a WhatsApp automation agent with Hermes"
- "I want to schedule WhatsApp messages automatically"
- "Help me configure Andorina WhatsApp bot"
- "Send voice notes and files via WhatsApp using AI"
- "Build an autonomous WhatsApp messaging agent"

## First 60 seconds

After `bash run.sh`, you'll see output like:

```
1. Authentication (simulated QR scan)
   [WhatsApp] QR code scanned (simulated). Authenticated.

2. Contact Search
   [Agent] Contact search 'vip' -> 3 results
     Bob Martinez           +1-555-0102   bob@example.com       labels=['work', 'vip']
     Eva Rossi              +1-555-0105   eva@example.com       labels=['personal', 'vip']
     Hiro Tanaka            +1-555-0108   hiro@example.com      labels=['work', 'vip']

3. Send Text Messages
   [WhatsApp] Text sent to +1-555-0101: Hi Alice, the Q3 report is ready...

4. Send Voice Notes (TTS)
   [TTS] Generated voice note: /tmp/whatsapp_voice_notes/note.ogg
   [WhatsApp] Voice note sent to +1-555-0105

5. Send Files from PC
   [WhatsApp] File sent to +1-555-0101: /tmp/whatsapp_demo_report.txt

6. Schedule Messages for Future Delivery
   [Scheduler] Queued text to +1-555-0103 at 2026-05-14T09:00:02
   Processed 3 scheduled message(s)

7. Final Agent Status
   {"authenticated": true, "scheduler": {"total": 3, "sent": 3}, "messages_sent": 7}
```

## Using the agent programmatically

```python
from whatsapp_agent import HermesWhatsAppAgent

agent = HermesWhatsAppAgent()
agent.initialize()

# Search contacts
contacts = agent.search_contacts("vip")

# Send a text
agent.send_message("+1-555-0101", "Meeting moved to 3pm")

# Send a voice note (auto TTS)
agent.send_voice("+1-555-0102", "Quick update: the deploy is live")

# Send a file
agent.send_file("+1-555-0103", "/path/to/report.pdf", "Q3 report")

# Schedule for later
agent.schedule_message("+1-555-0104", "Good morning!", delay_seconds=3600)
```
