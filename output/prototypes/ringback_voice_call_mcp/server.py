#!/usr/bin/env python3
"""
Ringback Voice Call MCP Server (Demo/Mock Mode)

A Model Context Protocol server that lets AI agents place live voice calls
to your phone using SIP/pjsua2 + whisper.cpp + Linphone.

This demo version simulates the full call flow without requiring actual
SIP infrastructure, making it easy to evaluate the concept.
"""

import json
import sys
import os
import time
import random
import threading
from datetime import datetime


# ---------------------------------------------------------------------------
# Simulated SIP / TTS / STT backends
# ---------------------------------------------------------------------------

class MockSIPClient:
    """Simulates pjsua2 SIP call lifecycle."""

    def __init__(self, username: str, password: str, domain: str):
        self.username = username
        self.domain = domain
        self.registered = False
        self.active_call = None

    def register(self) -> dict:
        self.registered = True
        return {
            "status": "registered",
            "account": f"sip:{self.username}@{self.domain}",
            "transport": "UDP",
        }

    def place_call(self, target: str, message: str) -> dict:
        """Simulate placing a SIP call and speaking a TTS message."""
        call_id = f"call-{int(time.time())}-{random.randint(1000,9999)}"
        self.active_call = call_id
        return {
            "call_id": call_id,
            "target": target,
            "status": "ringing",
            "codec": "PCMU/8000",
            "message_queued": message,
        }

    def wait_for_answer(self) -> dict:
        """Simulate callee answering."""
        return {
            "call_id": self.active_call,
            "status": "answered",
            "duration_ring_ms": random.randint(2000, 6000),
        }

    def speak_tts(self, text: str) -> dict:
        """Simulate TTS playback into the call audio channel."""
        word_count = len(text.split())
        duration_ms = word_count * 280  # ~280ms per word
        return {
            "call_id": self.active_call,
            "tts_engine": "piper-tts",
            "text_length": len(text),
            "estimated_duration_ms": duration_ms,
            "status": "spoken",
        }

    def listen_stt(self, timeout_s: int = 15) -> dict:
        """Simulate whisper.cpp transcription of callee speech."""
        mock_responses = [
            "Got it, I'll take a look right away.",
            "Thanks for the heads up. Can you send me the logs?",
            "Okay, let me check the dashboard.",
            "I'm on it. Give me five minutes.",
            "Acknowledged. Please escalate if it's not fixed in an hour.",
        ]
        return {
            "call_id": self.active_call,
            "stt_engine": "whisper.cpp",
            "model": "base.en",
            "transcription": random.choice(mock_responses),
            "confidence": round(random.uniform(0.88, 0.99), 2),
            "duration_ms": random.randint(1500, 5000),
        }

    def hangup(self) -> dict:
        call_id = self.active_call
        self.active_call = None
        return {"call_id": call_id, "status": "hung_up"}


class MockNotifier:
    """Simulates tiered alert backends (ntfy, Pushover)."""

    def send_ntfy(self, topic: str, message: str, priority: str) -> dict:
        return {
            "backend": "ntfy",
            "topic": topic,
            "priority": priority,
            "status": "delivered",
            "timestamp": datetime.now().isoformat(),
        }

    def send_pushover(self, user_key: str, message: str, priority: int) -> dict:
        return {
            "backend": "pushover",
            "priority": priority,
            "status": "delivered",
            "timestamp": datetime.now().isoformat(),
        }


# ---------------------------------------------------------------------------
# MCP Protocol Handler
# ---------------------------------------------------------------------------

class RingbackMCPServer:
    """
    JSON-RPC 2.0 stdio MCP server exposing Ringback voice-call tools.
    """

    def __init__(self):
        sip_user = os.environ.get("SIP_USERNAME", "demo_user")
        sip_pass = os.environ.get("SIP_PASSWORD", "demo_pass")
        sip_domain = os.environ.get("SIP_DOMAIN", "localhost")
        self.call_target = os.environ.get("CALL_TARGET", f"sip:phone@{sip_domain}")

        self.sip = MockSIPClient(sip_user, sip_pass, sip_domain)
        self.notifier = MockNotifier()
        self.sip.register()

    # -- Tool definitions ----------------------------------------------------

    TOOLS = [
        {
            "name": "ringback_call",
            "description": (
                "Place a live voice call to the configured phone number. "
                "The agent's message is spoken aloud via TTS, and the callee's "
                "response is transcribed back via whisper.cpp."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to speak to the callee.",
                    },
                    "wait_for_response": {
                        "type": "boolean",
                        "description": "Whether to wait for a spoken response.",
                        "default": True,
                    },
                },
                "required": ["message"],
            },
        },
        {
            "name": "ringback_tiered_alert",
            "description": (
                "Send a tiered alert: first a push notification (ntfy/Pushover), "
                "then escalate to a voice call if the user doesn't acknowledge "
                "within the timeout."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Alert message content.",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "description": "Alert priority level.",
                        "default": "medium",
                    },
                    "escalate_to_call": {
                        "type": "boolean",
                        "description": "Whether to escalate to voice call.",
                        "default": True,
                    },
                },
                "required": ["message"],
            },
        },
        {
            "name": "ringback_status",
            "description": "Check the current SIP registration and call status.",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
    ]

    # -- Tool handlers -------------------------------------------------------

    def handle_call(self, args: dict) -> dict:
        message = args["message"]
        wait = args.get("wait_for_response", True)

        call_result = self.sip.place_call(self.call_target, message)
        answer_result = self.sip.wait_for_answer()
        tts_result = self.sip.speak_tts(message)

        result = {
            "call": call_result,
            "answer": answer_result,
            "tts": tts_result,
        }

        if wait:
            stt_result = self.sip.listen_stt()
            result["response"] = stt_result

        hangup_result = self.sip.hangup()
        result["hangup"] = hangup_result
        return result

    def handle_tiered_alert(self, args: dict) -> dict:
        message = args["message"]
        priority = args.get("priority", "medium")
        escalate = args.get("escalate_to_call", True)

        steps = []

        # Step 1: Push notification via ntfy
        ntfy_result = self.notifier.send_ntfy("ringback-alerts", message, priority)
        steps.append({"step": 1, "action": "ntfy_push", "result": ntfy_result})

        # Step 2: Pushover if medium+
        if priority in ("medium", "high", "critical"):
            pushover_priority = {"medium": 0, "high": 1, "critical": 2}[priority]
            po_result = self.notifier.send_pushover("user_key", message, pushover_priority)
            steps.append({"step": 2, "action": "pushover", "result": po_result})

        # Step 3: Escalate to call if critical or requested
        if escalate and priority in ("high", "critical"):
            call_result = self.handle_call({"message": message, "wait_for_response": True})
            steps.append({"step": 3, "action": "voice_call_escalation", "result": call_result})

        return {"alert_priority": priority, "escalation_steps": steps}

    def handle_status(self, _args: dict) -> dict:
        return {
            "sip_registered": self.sip.registered,
            "account": f"sip:{self.sip.username}@{self.sip.domain}",
            "call_target": self.call_target,
            "active_call": self.sip.active_call,
            "backends": ["ntfy", "pushover", "pjsua2-sip"],
        }

    # -- MCP JSON-RPC dispatch -----------------------------------------------

    def handle_request(self, request: dict) -> dict:
        method = request.get("method", "")
        req_id = request.get("id")
        params = request.get("params", {})

        if method == "initialize":
            return self._ok(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": "ringback-voice-call-mcp",
                    "version": "0.1.0",
                },
            })

        if method == "notifications/initialized":
            return None  # notification, no response

        if method == "tools/list":
            return self._ok(req_id, {"tools": self.TOOLS})

        if method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            handler = {
                "ringback_call": self.handle_call,
                "ringback_tiered_alert": self.handle_tiered_alert,
                "ringback_status": self.handle_status,
            }.get(tool_name)

            if not handler:
                return self._error(req_id, -32601, f"Unknown tool: {tool_name}")

            result = handler(tool_args)
            return self._ok(req_id, {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
            })

        return self._error(req_id, -32601, f"Unknown method: {method}")

    def _ok(self, req_id, result):
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def _error(self, req_id, code, message):
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    # -- stdio loop ----------------------------------------------------------

    def run(self):
        """Read JSON-RPC messages from stdin, write responses to stdout."""
        sys.stderr.write("[ringback-mcp] Server started (demo mode)\n")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                continue

            response = self.handle_request(request)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    server = RingbackMCPServer()
    server.run()
