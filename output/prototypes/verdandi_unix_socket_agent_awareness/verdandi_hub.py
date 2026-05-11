#!/usr/bin/env python3
"""
Verdandi Hub — Central nervous system daemon.

Listens on a Unix domain socket and relays state updates between
connected AI agent instances.  Implements self-healing (auto-cleanup
of dead connections) and broadcast-based awareness sharing.
"""

import json
import os
import select
import socket
import sys
import time
import threading

SOCKET_PATH = os.environ.get("VERDANDI_SOCKET", "/tmp/verdandi_demo.sock")
HEARTBEAT_INTERVAL = 2  # seconds


class VerdandiHub:
    def __init__(self, socket_path: str = SOCKET_PATH):
        self.socket_path = socket_path
        self.server: socket.socket | None = None
        self.clients: dict[socket.socket, dict] = {}  # sock -> agent_info
        self.running = False
        self.state_store: dict[str, dict] = {}  # agent_id -> last_state

    # ---- lifecycle ----

    def start(self):
        self._cleanup_stale_socket()
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self.socket_path)
        self.server.listen(16)
        self.server.setblocking(False)
        self.running = True
        self._log("Hub listening", path=self.socket_path)

    def stop(self):
        self.running = False
        for c in list(self.clients):
            self._disconnect(c)
        if self.server:
            self.server.close()
        self._cleanup_stale_socket()
        self._log("Hub stopped")

    # ---- main loop ----

    def run_once(self, timeout: float = 0.5):
        """Process one select() cycle.  Returns False when stopped."""
        if not self.running:
            return False
        readable = [self.server] + list(self.clients)
        try:
            ready, _, _ = select.select(readable, [], [], timeout)
        except (ValueError, OSError):
            return self.running
        for sock in ready:
            if sock is self.server:
                self._accept()
            else:
                self._receive(sock)
        return self.running

    def serve_forever(self):
        self.start()
        try:
            while self.run_once():
                pass
        finally:
            self.stop()

    # ---- internals ----

    def _accept(self):
        try:
            conn, _ = self.server.accept()
            conn.setblocking(False)
            self.clients[conn] = {"connected_at": time.time()}
            self._log("Agent connected", total=len(self.clients))
        except OSError:
            pass

    def _receive(self, sock: socket.socket):
        try:
            raw = sock.recv(65536)
            if not raw:
                raise ConnectionResetError
            for line in raw.decode().strip().split("\n"):
                msg = json.loads(line)
                self._handle(sock, msg)
        except (ConnectionResetError, BrokenPipeError, OSError, json.JSONDecodeError):
            self._disconnect(sock)

    def _handle(self, sender: socket.socket, msg: dict):
        kind = msg.get("type", "")
        agent_id = msg.get("agent_id", "unknown")
        self.clients[sender]["agent_id"] = agent_id

        if kind == "register":
            self._log("Registered", agent=agent_id)
            # Send current world state to newcomer
            welcome = {"type": "world_state", "agents": self.state_store}
            self._send(sender, welcome)

        elif kind == "state_update":
            self.state_store[agent_id] = msg.get("state", {})
            self._log("State update", agent=agent_id, state=msg.get("state"))
            # Broadcast to all *other* agents
            broadcast = {"type": "peer_update", "agent_id": agent_id, "state": msg.get("state", {})}
            self._broadcast(broadcast, exclude=sender)

        elif kind == "heartbeat":
            self.clients[sender]["last_heartbeat"] = time.time()
            ack = {"type": "heartbeat_ack", "ts": time.time()}
            self._send(sender, ack)

        elif kind == "query":
            resp = {"type": "query_response", "agents": self.state_store}
            self._send(sender, resp)

    def _broadcast(self, msg: dict, exclude: socket.socket | None = None):
        for sock in list(self.clients):
            if sock is not exclude:
                self._send(sock, msg)

    def _send(self, sock: socket.socket, msg: dict):
        try:
            sock.sendall((json.dumps(msg) + "\n").encode())
        except (BrokenPipeError, OSError):
            self._disconnect(sock)

    def _disconnect(self, sock: socket.socket):
        info = self.clients.pop(sock, {})
        agent_id = info.get("agent_id", "?")
        try:
            sock.close()
        except OSError:
            pass
        # Self-healing: remove stale state
        self.state_store.pop(agent_id, None)
        self._log("Agent disconnected (self-healed)", agent=agent_id, remaining=len(self.clients))

    def _cleanup_stale_socket(self):
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

    @staticmethod
    def _log(event: str, **kw):
        extras = " ".join(f"{k}={v}" for k, v in kw.items())
        print(f"[HUB] {event}  {extras}", flush=True)


if __name__ == "__main__":
    hub = VerdandiHub()
    try:
        hub.serve_forever()
    except KeyboardInterrupt:
        hub.stop()
