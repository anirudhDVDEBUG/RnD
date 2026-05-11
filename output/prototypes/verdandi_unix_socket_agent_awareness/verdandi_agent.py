#!/usr/bin/env python3
"""
Verdandi Agent — A node that connects to the Verdandi Hub.

Each agent registers itself, publishes state updates, receives
peer updates, and sends heartbeats.  Implements self-healing
reconnection on disconnect.
"""

import json
import os
import socket
import sys
import time
import threading

SOCKET_PATH = os.environ.get("VERDANDI_SOCKET", "/tmp/verdandi_demo.sock")
HEARTBEAT_INTERVAL = 2


class VerdandiAgent:
    def __init__(self, agent_id: str, socket_path: str = SOCKET_PATH):
        self.agent_id = agent_id
        self.socket_path = socket_path
        self.sock: socket.socket | None = None
        self.running = False
        self.peers: dict[str, dict] = {}
        self.on_peer_update = None  # callback(agent_id, state)
        self._recv_buffer = ""

    # ---- lifecycle ----

    def connect(self, retries: int = 5, delay: float = 0.3) -> bool:
        for attempt in range(retries):
            try:
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.connect(self.socket_path)
                self.sock.setblocking(False)
                self._send({"type": "register", "agent_id": self.agent_id})
                self._log("Connected to hub")
                self.running = True
                return True
            except (ConnectionRefusedError, FileNotFoundError, OSError):
                self._log(f"Connect attempt {attempt+1}/{retries} failed, retrying...")
                time.sleep(delay)
        self._log("Could not connect to hub")
        return False

    def disconnect(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        self._log("Disconnected")

    # ---- sending ----

    def publish_state(self, state: dict):
        self._send({
            "type": "state_update",
            "agent_id": self.agent_id,
            "state": state,
        })
        self._log("Published state", state=state)

    def send_heartbeat(self):
        self._send({"type": "heartbeat", "agent_id": self.agent_id})

    def query_world(self):
        self._send({"type": "query", "agent_id": self.agent_id})

    # ---- receiving ----

    def poll(self, timeout: float = 0.1) -> list[dict]:
        """Non-blocking receive. Returns list of parsed messages."""
        if not self.sock:
            return []
        import select as sel
        try:
            ready, _, _ = sel.select([self.sock], [], [], timeout)
        except (ValueError, OSError):
            return []
        if not ready:
            return []
        try:
            data = self.sock.recv(65536).decode()
            if not data:
                raise ConnectionResetError
            self._recv_buffer += data
        except (ConnectionResetError, BrokenPipeError, OSError):
            self._log("Lost connection to hub")
            self.running = False
            return []

        messages = []
        while "\n" in self._recv_buffer:
            line, self._recv_buffer = self._recv_buffer.split("\n", 1)
            if line.strip():
                try:
                    msg = json.loads(line)
                    messages.append(msg)
                    self._process(msg)
                except json.JSONDecodeError:
                    pass
        return messages

    def _process(self, msg: dict):
        kind = msg.get("type", "")
        if kind == "world_state":
            self.peers = msg.get("agents", {})
            self._log("Received world state", peers=list(self.peers.keys()))
        elif kind == "peer_update":
            peer_id = msg.get("agent_id", "?")
            state = msg.get("state", {})
            self.peers[peer_id] = state
            self._log(f"Peer update from {peer_id}", state=state)
            if self.on_peer_update:
                self.on_peer_update(peer_id, state)
        elif kind == "query_response":
            self.peers = msg.get("agents", {})
            self._log("Query response", peers=list(self.peers.keys()))
        elif kind == "heartbeat_ack":
            pass  # silent

    # ---- internals ----

    def _send(self, msg: dict):
        if not self.sock:
            return
        try:
            self.sock.sendall((json.dumps(msg) + "\n").encode())
        except (BrokenPipeError, OSError):
            self._log("Send failed — hub may be down")
            self.running = False

    def _log(self, event: str, **kw):
        extras = " ".join(f"{k}={v}" for k, v in kw.items())
        print(f"[AGENT:{self.agent_id}] {event}  {extras}", flush=True)
