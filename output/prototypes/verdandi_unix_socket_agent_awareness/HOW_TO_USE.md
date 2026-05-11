# How to Use Verdandi

## Install

Verdandi is pure Python (3.10+), no external dependencies.

```bash
# Clone the original project
git clone https://github.com/hrabanazviking/Verdandi.git
cd Verdandi
pip install -r requirements.txt   # empty — stdlib only

# Or use this demo directly
bash run.sh
```

## Claude Code Skill setup

This is packaged as a Claude Code skill. To install:

```bash
mkdir -p ~/.claude/skills/verdandi_unix_socket_agent_awareness
cp SKILL.md ~/.claude/skills/verdandi_unix_socket_agent_awareness/SKILL.md
```

**Trigger phrases** that activate the skill:

- "Set up real-time communication between multiple AI agent instances"
- "I need shared memory and awareness across AI processes using Unix sockets"
- "Configure a self-healing IPC layer for my AI agents on Linux"
- "Connect Hermes Agent instances so they share state in real-time"
- "Build an AI nervous system for cross-instance coordination"

## First 60 seconds

```bash
# 1. Run the self-contained demo (no API keys needed)
bash run.sh

# Output walks through 8 phases:
#   Phase 1: Hub starts on /tmp/verdandi_demo.sock
#   Phase 2: 3 agents connect
#   Phase 3: Each publishes its role/goal/load
#   Phase 4: Each agent sees all peers' state
#   Phase 5: Planner updates state -> others see it instantly
#   Phase 6: Researcher disconnects -> hub self-heals
#   Phase 7: Researcher reconnects automatically
#   Phase 8: Heartbeat keep-alive confirmed
```

## Using in your own code

### Start the hub (terminal 1)

```python
from verdandi_hub import VerdandiHub

hub = VerdandiHub("/tmp/verdandi.sock")
hub.serve_forever()
```

### Connect an agent (terminal 2+)

```python
from verdandi_agent import VerdandiAgent

agent = VerdandiAgent("my-agent-001")
agent.connect()

# Publish your state
agent.publish_state({"role": "researcher", "task": "gathering data", "load": 0.4})

# Poll for peer updates
while agent.running:
    messages = agent.poll(timeout=1.0)
    for msg in messages:
        if msg["type"] == "peer_update":
            print(f"Peer {msg['agent_id']} changed: {msg['state']}")
```

### Message protocol (JSON over newline-delimited stream)

| Direction | Type | Fields |
|-----------|------|--------|
| Agent -> Hub | `register` | `agent_id` |
| Agent -> Hub | `state_update` | `agent_id`, `state` (any dict) |
| Agent -> Hub | `heartbeat` | `agent_id` |
| Agent -> Hub | `query` | `agent_id` |
| Hub -> Agent | `world_state` | `agents` (full state map) |
| Hub -> Agent | `peer_update` | `agent_id`, `state` |
| Hub -> Agent | `heartbeat_ack` | `ts` |
| Hub -> Agent | `query_response` | `agents` |
