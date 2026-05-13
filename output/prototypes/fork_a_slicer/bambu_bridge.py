"""
Bambu Connect Bridge — Process-isolated bridge that handles
Bambu Lab printer communication via a simulated proprietary protocol.

Runs as a separate process, exposes a JSON-RPC interface over a Unix socket.
"""

import json
import os
import socket
import sys
import threading
import time
import random
import signal

SOCKET_PATH = "/tmp/bambu_bridge.sock"

# Simulated Bambu Lab printers on the local network
MOCK_PRINTERS = [
    {
        "id": "01P00A2B0500123",
        "name": "BambuLab X1C - Workshop",
        "model": "X1 Carbon",
        "ip": "192.168.1.42",
        "firmware": "01.07.01.00",
        "status": "idle",
        "nozzle_temp": 25.0,
        "bed_temp": 25.0,
        "filament": "PLA Basic - White",
    },
    {
        "id": "01S00A3C0700456",
        "name": "BambuLab P1S - Office",
        "model": "P1S",
        "ip": "192.168.1.87",
        "firmware": "01.06.02.00",
        "status": "idle",
        "nozzle_temp": 24.5,
        "bed_temp": 24.5,
        "filament": "PETG HF - Black",
    },
    {
        "id": "01A00B4D0900789",
        "name": "BambuLab A1 - Prototyping",
        "model": "A1",
        "ip": "192.168.1.103",
        "firmware": "01.03.01.00",
        "status": "printing",
        "nozzle_temp": 215.0,
        "bed_temp": 60.0,
        "filament": "PLA Basic - Red",
        "print_progress": 47,
        "current_file": "benchy_v2.3mf",
        "remaining_time_min": 38,
    },
]


def handle_rpc(request_data):
    """Process a JSON-RPC 2.0 request and return a response."""
    try:
        req = json.loads(request_data)
    except json.JSONDecodeError:
        return json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": -32700, "message": "Parse error"},
            "id": None,
        })

    method = req.get("method", "")
    params = req.get("params", {})
    req_id = req.get("id", 1)

    if method == "discover_printers":
        # Simulate mDNS/SSDP network discovery delay
        time.sleep(0.3)
        result = {
            "printers": [
                {"id": p["id"], "name": p["name"], "model": p["model"], "ip": p["ip"]}
                for p in MOCK_PRINTERS
            ],
            "discovery_method": "ssdp+mdns",
            "scan_duration_ms": 312,
        }

    elif method == "get_printer_status":
        printer_id = params.get("printer_id")
        printer = next((p for p in MOCK_PRINTERS if p["id"] == printer_id), None)
        if not printer:
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32001, "message": f"Printer {printer_id} not found"},
                "id": req_id,
            })
        result = dict(printer)

    elif method == "submit_print_job":
        printer_id = params.get("printer_id")
        gcode_file = params.get("gcode_file", "unknown.gcode")
        printer = next((p for p in MOCK_PRINTERS if p["id"] == printer_id), None)
        if not printer:
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32001, "message": f"Printer {printer_id} not found"},
                "id": req_id,
            })
        if printer["status"] == "printing":
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32002, "message": "Printer is busy"},
                "id": req_id,
            })
        job_id = f"JOB-{random.randint(10000, 99999)}"
        result = {
            "job_id": job_id,
            "printer_id": printer_id,
            "file": gcode_file,
            "status": "queued",
            "estimated_time_min": random.randint(15, 180),
            "message": f"Print job {job_id} submitted to {printer['name']}",
        }

    elif method == "get_bridge_info":
        result = {
            "bridge_version": "0.1.0",
            "architecture": "FULU-Foundation",
            "protocol": "JSON-RPC 2.0",
            "transport": "Unix Domain Socket",
            "pid": os.getpid(),
            "uptime_seconds": 0,
            "supported_methods": [
                "discover_printers",
                "get_printer_status",
                "submit_print_job",
                "get_bridge_info",
            ],
        }

    else:
        return json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": f"Method not found: {method}"},
            "id": req_id,
        })

    return json.dumps({"jsonrpc": "2.0", "result": result, "id": req_id})


def run_bridge_server(ready_event=None):
    """Start the bridge as a Unix socket JSON-RPC server."""
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)
    server.settimeout(30)  # 30s timeout so bridge exits if idle

    print(f"[bridge] Bambu Connect Bridge started (PID {os.getpid()})")
    print(f"[bridge] Listening on {SOCKET_PATH}")
    print(f"[bridge] Architecture: FULU-Foundation / Process Isolation")

    if ready_event:
        ready_event.set()

    try:
        while True:
            try:
                conn, _ = server.accept()
            except socket.timeout:
                break
            data = conn.recv(65536)
            if data:
                response = handle_rpc(data.decode("utf-8"))
                conn.sendall(response.encode("utf-8"))
            conn.close()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.unlink(SOCKET_PATH)
        print("[bridge] Bridge shut down.")


if __name__ == "__main__":
    run_bridge_server()
