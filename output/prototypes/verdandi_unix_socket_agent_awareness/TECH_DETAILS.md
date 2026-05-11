# Technical Details

## What it does

Verdandi is a hub-and-spoke IPC daemon that provides real-time shared awareness between multiple AI agent processes running on the same host. The hub listens on a Unix domain socket; agents connect, register, publish JSON state updates, and receive broadcasts whenever any peer's state changes. The system self-heals: when an agent dies or disconnects, the hub removes its stale state and notifies remaining agents. Agents implement automatic reconnection.

The design trades network reach (Unix sockets are same-host only) for zero serialization overhead, no TCP handshake latency, and kernel-level access control via filesystem permissions.

## Architecture

```
             +-------------------+
             |   Verdandi Hub    |
             | (Unix socket srv) |
             +--------+----------+
                      |
         +------------+------------+
         |            |            |
    +----+----+  +----+----+  +----+----+
    | Agent A |  | Agent B |  | Agent C |
    | planner |  |researcher| | writer  |
    +---------+  +---------+  +---------+
```

### Key files

| File | Purpose |
|------|---------|
| `verdandi_hub.py` | Hub daemon — accepts connections, stores state, broadcasts updates, self-heals |
| `verdandi_agent.py` | Agent client — connects, publishes, polls, reconnects |
| `demo.py` | End-to-end demo exercising all 8 phases |
| `run.sh` | One-command entry point |

### Data flow

1. Agent connects to Unix socket, sends `register` message
2. Hub replies with `world_state` (all known agent states)
3. Agent publishes `state_update` — hub stores it and broadcasts `peer_update` to all other agents
4. Agents send periodic `heartbeat`; hub replies with `heartbeat_ack`
5. On disconnect, hub removes agent from state store (self-healing)

### Dependencies

**None** beyond Python 3.10+ stdlib: `socket`, `select`, `json`, `threading`, `os`, `time`.

### Model calls

Verdandi itself makes **zero** LLM/API calls. It is a transport layer. AI agents that connect to it are responsible for their own inference.

## Limitations

- **Same-host only**: Unix domain sockets do not cross machine boundaries. For multi-host coordination, you'd need TCP or a message broker.
- **No persistence**: State lives in memory. If the hub restarts, all state is lost. No WAL, no snapshots.
- **No authentication**: Any process with filesystem access to the socket can connect. Security relies on Unix file permissions.
- **No ordering guarantees**: Messages are delivered in FIFO order per connection, but there is no global sequence numbering or vector clocks.
- **Single hub**: No built-in clustering or hub failover. Single point of failure.
- **Linux/Unix only**: No Windows support (no `AF_UNIX` on older Windows, and the design assumes Unix filesystem semantics).

## Why it might matter for Claude-driven products

| Use case | How Verdandi fits |
|----------|-------------------|
| **Agent factories** | When spawning N Claude Code agents on one machine, Verdandi gives them shared awareness without a database. One agent can see that another is already working on a sub-task and avoid duplication. |
| **Lead-gen / marketing pipelines** | A multi-step pipeline (scrape -> enrich -> score -> email) can use Verdandi so each stage knows the pipeline's current throughput and back-pressure, enabling flow control without polling a DB. |
| **Ad creative generation** | Coordinator agent assigns creative briefs to worker agents; workers publish progress; coordinator detects stalls and reassigns — all via local sockets with sub-millisecond latency. |
| **Voice AI** | Real-time voice agents that need to share turn-taking state, user context, or escalation signals between concurrent sessions on the same server. |
| **Multi-agent orchestration** | Any scenario where 2+ Claude-powered processes need lightweight, zero-dependency coordination on a single host — Verdandi is simpler than Redis, faster than HTTP, and needs no infrastructure. |
