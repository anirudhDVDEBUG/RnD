---
name: verdandi_unix_socket_agent_awareness
description: |
  Set up Verdandi — a real-time cross-instance AI awareness system using Unix domain sockets.
  TRIGGER: user wants inter-agent communication, shared AI memory via sockets, self-healing agent networking, real-time cross-instance awareness, or AI nervous system setup on Linux/Unix.
---

# Verdandi: Unix Socket Agent Awareness

Verdandi (VERÐANDI — The Norn of Becoming) is a lightweight AI nervous system that enables real-time cross-instance awareness between AI agents via Unix domain sockets. It provides self-healing, self-correcting inter-process communication for AGI systems.

## When to use

- "Set up real-time communication between multiple AI agent instances"
- "I need shared memory and awareness across AI processes using Unix sockets"
- "Configure a self-healing IPC layer for my AI agents on Linux"
- "Connect Hermes Agent instances so they share state in real-time"
- "Build an AI nervous system for cross-instance coordination"

## How to use

### 1. Clone and install Verdandi

```bash
git clone https://github.com/hrabanazviking/Verdandi.git
cd Verdandi
pip install -r requirements.txt
```

### 2. Start the Verdandi daemon

Verdandi uses Unix domain sockets for low-latency, local IPC between agent instances:

```bash
python verdandi.py
```

The daemon creates a Unix socket (typically at `/tmp/verdandi.sock` or configured path) that AI agents connect to for real-time state sharing.

### 3. Connect AI agents

Each AI agent instance connects to the Verdandi socket to:
- **Broadcast state**: Share current context, goals, and observations
- **Receive updates**: Get real-time awareness of other instances' states
- **Self-heal**: Automatically recover from disconnections or failures

### 4. Integration with AI agents

Verdandi works with:
- **Hermes Agent** — primary integration target
- **Other AI agents** — any agent that can communicate via Unix domain sockets

### Key features

| Feature | Description |
|---------|-------------|
| Unix domain sockets | Low-latency local IPC, no network overhead |
| Self-healing | Automatic reconnection and state recovery |
| Self-correcting | Detects and resolves inconsistencies |
| Lightweight | Minimal resource footprint on any Linux/Unix system |
| Real-time awareness | Cross-instance state synchronization |

### Architecture notes

- **Transport**: Unix domain sockets (not TCP) — designed for same-host multi-agent coordination
- **Language**: Python
- **Platform**: Linux and Unix-based systems only (no Windows support)
- **Pattern**: Hub-and-spoke — Verdandi daemon is the central nervous system, agents are nodes

## References

- Source repository: https://github.com/hrabanazviking/Verdandi
- Related: [Hermes Agent](https://github.com/hrabanazviking) — AI agent designed to work with Verdandi
