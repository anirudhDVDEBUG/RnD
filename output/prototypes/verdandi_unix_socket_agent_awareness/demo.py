#!/usr/bin/env python3
"""
Verdandi Demo — End-to-end demonstration.

Spins up the hub + 3 simulated AI agents in-process, each publishing
state updates, receiving peer awareness, and demonstrating self-healing
when one agent disconnects.

No external API keys or services required.
"""

import os
import sys
import time
import threading

from verdandi_hub import VerdandiHub
from verdandi_agent import VerdandiAgent

SOCKET_PATH = "/tmp/verdandi_demo.sock"
os.environ["VERDANDI_SOCKET"] = SOCKET_PATH

SEPARATOR = "=" * 60


def section(title: str):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR, flush=True)


def run_demo():
    # ---- Phase 1: Start the Hub ----
    section("PHASE 1: Starting Verdandi Hub (central nervous system)")
    hub = VerdandiHub(SOCKET_PATH)
    hub.start()

    # Run hub in background thread
    hub_thread = threading.Thread(target=_hub_loop, args=(hub,), daemon=True)
    hub_thread.start()
    time.sleep(0.3)

    # ---- Phase 2: Connect agents ----
    section("PHASE 2: Connecting 3 AI agent instances")
    agents = []
    agent_configs = [
        ("planner", {"role": "planner", "goal": "decompose user request", "load": 0.3}),
        ("researcher", {"role": "researcher", "goal": "gather information", "load": 0.6}),
        ("writer", {"role": "writer", "goal": "draft final output", "load": 0.1}),
    ]

    for agent_id, initial_state in agent_configs:
        a = VerdandiAgent(agent_id, SOCKET_PATH)
        if a.connect():
            agents.append((a, initial_state))
        time.sleep(0.15)

    # Drain initial registration messages
    for a, _ in agents:
        a.poll(0.2)

    # ---- Phase 3: Publish initial states ----
    section("PHASE 3: Agents publishing initial state (cross-instance awareness)")
    for a, state in agents:
        a.publish_state(state)
        time.sleep(0.15)

    # Let broadcasts propagate
    time.sleep(0.3)
    for a, _ in agents:
        a.poll(0.2)

    # ---- Phase 4: Show awareness ----
    section("PHASE 4: Each agent's awareness of its peers")
    for a, _ in agents:
        a.query_world()
        time.sleep(0.15)
        a.poll(0.3)
        print(f"\n  [{a.agent_id}] knows about peers: {list(a.peers.keys())}")
        for pid, pstate in a.peers.items():
            if pid != a.agent_id:
                print(f"    -> {pid}: {pstate}")
    print(flush=True)

    # ---- Phase 5: State update propagation ----
    section("PHASE 5: Real-time state update propagation")
    planner = agents[0][0]
    planner.publish_state({"role": "planner", "goal": "decompose user request", "load": 0.9, "status": "busy"})
    time.sleep(0.3)

    for a, _ in agents[1:]:
        msgs = a.poll(0.3)
        for m in msgs:
            if m.get("type") == "peer_update":
                print(f"  [{a.agent_id}] saw planner go busy: load={m['state'].get('load')}, status={m['state'].get('status')}")

    # ---- Phase 6: Self-healing ----
    section("PHASE 6: Self-healing — agent disconnects, hub recovers")
    researcher = agents[1][0]
    print(f"  Disconnecting '{researcher.agent_id}'...")
    researcher.disconnect()
    time.sleep(0.5)

    # Hub should have auto-cleaned
    print(f"  Hub state store now has: {list(hub.state_store.keys())}")
    print(f"  Hub active connections: {len(hub.clients)}")

    # Remaining agents can still query
    writer = agents[2][0]
    writer.query_world()
    time.sleep(0.3)
    writer.poll(0.3)
    print(f"  [{writer.agent_id}] peers after self-heal: {list(writer.peers.keys())}")

    # ---- Phase 7: Reconnection ----
    section("PHASE 7: Self-healing reconnection")
    researcher2 = VerdandiAgent("researcher", SOCKET_PATH)
    if researcher2.connect():
        researcher2.publish_state({"role": "researcher", "goal": "re-joined after recovery", "load": 0.2})
        time.sleep(0.3)
        researcher2.poll(0.3)
        print(f"  [{researcher2.agent_id}] reconnected and re-registered")
        print(f"  Hub state store now has: {list(hub.state_store.keys())}")
        agents[1] = (researcher2, {})

    # ---- Phase 8: Heartbeat ----
    section("PHASE 8: Heartbeat keep-alive")
    for a, _ in agents:
        if a.running:
            a.send_heartbeat()
            time.sleep(0.1)
            msgs = a.poll(0.2)
            acks = [m for m in msgs if m.get("type") == "heartbeat_ack"]
            print(f"  [{a.agent_id}] heartbeat ack received: {bool(acks)}")

    # ---- Cleanup ----
    section("DEMO COMPLETE")
    print("  Verdandi enables real-time cross-instance awareness via Unix sockets.")
    print("  Key capabilities demonstrated:")
    print("    - Hub-and-spoke architecture with Unix domain sockets")
    print("    - Agent registration and world-state synchronization")
    print("    - Real-time state broadcast to all peers")
    print("    - Self-healing on disconnect (auto-cleanup + reconnection)")
    print("    - Heartbeat keep-alive mechanism")
    print(f"\n  Socket path used: {SOCKET_PATH}")
    print()

    for a, _ in agents:
        if a.running:
            a.disconnect()
    hub.stop()


def _hub_loop(hub: VerdandiHub):
    while hub.run_once(timeout=0.2):
        pass


if __name__ == "__main__":
    run_demo()
