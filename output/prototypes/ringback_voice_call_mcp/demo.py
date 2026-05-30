#!/usr/bin/env python3
"""
Ringback Voice Call MCP — Interactive Demo

Simulates the full agent → phone call flow without requiring SIP
infrastructure. Exercises all three MCP tools and prints formatted output.
"""

import json
import sys
import os
import subprocess
import textwrap

DIVIDER = "=" * 64
SUBDIV = "-" * 48

def send_mcp(proc, method: str, params: dict = None, req_id: int = 1) -> dict:
    """Send a JSON-RPC request to the MCP server and read the response."""
    request = {"jsonrpc": "2.0", "id": req_id, "method": method}
    if params:
        request["params"] = params

    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()

    line = proc.stdout.readline().strip()
    if not line:
        return {}
    return json.loads(line)


def print_section(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def print_result(label: str, data: dict, indent: int = 2):
    print(f"\n  {label}:")
    print(SUBDIV)
    if "result" in data and "content" in data["result"]:
        for item in data["result"]["content"]:
            if item["type"] == "text":
                parsed = json.loads(item["text"])
                print(textwrap.indent(json.dumps(parsed, indent=2), "    "))
    elif "result" in data:
        print(textwrap.indent(json.dumps(data["result"], indent=2), "    "))
    else:
        print(textwrap.indent(json.dumps(data, indent=2), "    "))


def main():
    print(DIVIDER)
    print("  RINGBACK VOICE CALL MCP — Demo")
    print("  AI Agent → Phone Call via SIP (mock mode)")
    print(DIVIDER)

    # Start the MCP server as a subprocess
    server_path = os.path.join(os.path.dirname(__file__), "server.py")
    proc = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={
            **os.environ,
            "SIP_USERNAME": "agent",
            "SIP_PASSWORD": "secret",
            "SIP_DOMAIN": "sip.example.com",
            "CALL_TARGET": "sip:oncall-engineer@sip.example.com",
        },
    )

    req_id = 0

    # ── 1. Initialize ──────────────────────────────────────────────────
    print_section("1. MCP Initialization")
    req_id += 1
    resp = send_mcp(proc, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "demo-client", "version": "1.0"},
    }, req_id)
    print(f"\n  Server: {resp['result']['serverInfo']['name']} "
          f"v{resp['result']['serverInfo']['version']}")
    print(f"  Protocol: {resp['result']['protocolVersion']}")

    # Send initialized notification (no response expected)
    proc.stdin.write(json.dumps({
        "jsonrpc": "2.0", "method": "notifications/initialized"
    }) + "\n")
    proc.stdin.flush()

    # ── 2. List tools ──────────────────────────────────────────────────
    print_section("2. Available MCP Tools")
    req_id += 1
    resp = send_mcp(proc, "tools/list", {}, req_id)
    for tool in resp["result"]["tools"]:
        print(f"\n  * {tool['name']}")
        print(f"    {tool['description'][:80]}...")

    # ── 3. Check status ────────────────────────────────────────────────
    print_section("3. SIP Registration Status")
    req_id += 1
    resp = send_mcp(proc, "tools/call", {
        "name": "ringback_status", "arguments": {}
    }, req_id)
    print_result("Registration info", resp)

    # ── 4. Place a voice call ──────────────────────────────────────────
    print_section("4. Place a Voice Call")
    print("\n  Scenario: Agent detected a production deployment failure")
    print("  and needs to call the on-call engineer immediately.\n")

    req_id += 1
    resp = send_mcp(proc, "tools/call", {
        "name": "ringback_call",
        "arguments": {
            "message": (
                "Alert: Production deployment pipeline failed at stage 3. "
                "Error: container image build timeout after 300 seconds. "
                "The staging environment is unaffected. "
                "Please check the CI dashboard and acknowledge."
            ),
            "wait_for_response": True,
        },
    }, req_id)
    print_result("Call result", resp)

    # Extract the transcribed response for display
    result_data = json.loads(resp["result"]["content"][0]["text"])
    if "response" in result_data:
        print(f"\n  >> Callee said: \"{result_data['response']['transcription']}\"")
        print(f"     (confidence: {result_data['response']['confidence']}, "
              f"engine: {result_data['response']['stt_engine']})")

    # ── 5. Tiered alert (low → push only) ──────────────────────────────
    print_section("5. Tiered Alert — Low Priority (push only)")
    req_id += 1
    resp = send_mcp(proc, "tools/call", {
        "name": "ringback_tiered_alert",
        "arguments": {
            "message": "FYI: Nightly backup completed successfully.",
            "priority": "low",
            "escalate_to_call": False,
        },
    }, req_id)
    print_result("Alert result", resp)

    # ── 6. Tiered alert (critical → push + call) ──────────────────────
    print_section("6. Tiered Alert — Critical (push + voice call escalation)")
    print("\n  Scenario: Database replication lag exceeded 60s threshold.\n")

    req_id += 1
    resp = send_mcp(proc, "tools/call", {
        "name": "ringback_tiered_alert",
        "arguments": {
            "message": (
                "CRITICAL: Database replication lag is 62 seconds and rising. "
                "Primary node CPU at 94%. Immediate attention required."
            ),
            "priority": "critical",
            "escalate_to_call": True,
        },
    }, req_id)
    print_result("Escalation result", resp)

    # ── Summary ────────────────────────────────────────────────────────
    print_section("Demo Complete")
    print("""
  This demo exercised all three Ringback MCP tools:

    1. ringback_status    — Check SIP registration
    2. ringback_call      — Place a live voice call with TTS + STT
    3. ringback_tiered_alert — Push notification → voice call escalation

  In production, replace MockSIPClient with real pjsua2 bindings
  and point CALL_TARGET to your Linphone SIP address.

  See HOW_TO_USE.md for setup instructions.
""")

    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=5)


if __name__ == "__main__":
    main()
