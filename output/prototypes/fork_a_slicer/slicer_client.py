"""
Slicer Client — Simulates the OrcaSlicer fork side.

Connects to the Bambu Bridge via JSON-RPC over a Unix socket
and performs printer discovery, status checks, and job submission.
"""

import json
import socket
import sys
import time

SOCKET_PATH = "/tmp/bambu_bridge.sock"


def rpc_call(method, params=None, timeout=10):
    """Send a JSON-RPC 2.0 request to the bridge and return the result."""
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1,
    }
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect(SOCKET_PATH)
    sock.sendall(json.dumps(request).encode("utf-8"))
    data = sock.recv(65536)
    sock.close()
    return json.loads(data.decode("utf-8"))


def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def run_demo():
    """Run the full slicer-side demo sequence."""

    # Step 1: Bridge info
    print_separator("STEP 1: Query Bridge Info")
    resp = rpc_call("get_bridge_info")
    info = resp["result"]
    print(f"  Bridge Version : {info['bridge_version']}")
    print(f"  Architecture   : {info['architecture']}")
    print(f"  Protocol       : {info['protocol']}")
    print(f"  Transport      : {info['transport']}")
    print(f"  Bridge PID     : {info['pid']}")
    print(f"  Methods        : {', '.join(info['supported_methods'])}")

    # Step 2: Discover printers
    print_separator("STEP 2: Discover Bambu Lab Printers")
    resp = rpc_call("discover_printers")
    printers = resp["result"]["printers"]
    scan_ms = resp["result"]["scan_duration_ms"]
    print(f"  Discovery method: {resp['result']['discovery_method']}")
    print(f"  Scan duration   : {scan_ms}ms")
    print(f"  Found {len(printers)} printer(s):\n")
    for p in printers:
        print(f"    [{p['model']:12s}] {p['name']}")
        print(f"                  ID: {p['id']}  IP: {p['ip']}")

    # Step 3: Get detailed status for each printer
    print_separator("STEP 3: Printer Status Details")
    idle_printer_id = None
    for p in printers:
        resp = rpc_call("get_printer_status", {"printer_id": p["id"]})
        status = resp["result"]
        print(f"\n  {status['name']} ({status['model']})")
        print(f"    Status      : {status['status'].upper()}")
        print(f"    Firmware    : {status['firmware']}")
        print(f"    Nozzle Temp : {status['nozzle_temp']}C")
        print(f"    Bed Temp    : {status['bed_temp']}C")
        print(f"    Filament    : {status['filament']}")
        if status["status"] == "printing":
            print(f"    Progress    : {status.get('print_progress', '?')}%")
            print(f"    File        : {status.get('current_file', '?')}")
            print(f"    Remaining   : {status.get('remaining_time_min', '?')} min")
        elif status["status"] == "idle":
            idle_printer_id = status["id"]

    # Step 4: Submit a print job to an idle printer
    print_separator("STEP 4: Submit Print Job")
    if idle_printer_id:
        resp = rpc_call("submit_print_job", {
            "printer_id": idle_printer_id,
            "gcode_file": "fulu_test_cube_0.2mm_PLA.3mf",
        })
        if "result" in resp:
            job = resp["result"]
            print(f"  Job ID        : {job['job_id']}")
            print(f"  Printer       : {job['printer_id']}")
            print(f"  File          : {job['file']}")
            print(f"  Status        : {job['status']}")
            print(f"  Est. Time     : {job['estimated_time_min']} min")
            print(f"  Message       : {job['message']}")
        else:
            print(f"  Error: {resp.get('error', {}).get('message', 'Unknown error')}")
    else:
        print("  No idle printers available for job submission.")

    # Step 5: Try submitting to a busy printer (error handling demo)
    print_separator("STEP 5: Error Handling — Submit to Busy Printer")
    busy_printer = next(
        (p for p in printers if rpc_call("get_printer_status", {"printer_id": p["id"]})["result"]["status"] == "printing"),
        None,
    )
    if busy_printer:
        resp = rpc_call("submit_print_job", {
            "printer_id": busy_printer["id"],
            "gcode_file": "test.gcode",
        })
        if "error" in resp:
            print(f"  Expected error : {resp['error']['message']}")
            print(f"  Error code     : {resp['error']['code']}")
        else:
            print(f"  Unexpectedly succeeded: {resp}")
    else:
        print("  (No busy printers to test error handling)")

    # Summary
    print_separator("DEMO COMPLETE")
    print("  The FULU-Foundation process isolation bridge works as follows:")
    print("  1. Bridge runs as a SEPARATE PROCESS (own PID, own memory)")
    print("  2. Slicer communicates via JSON-RPC over Unix domain socket")
    print("  3. No proprietary Bambu code inside the slicer process")
    print("  4. Bridge handles all Bambu Connect protocol details")
    print("  5. Clean separation = stability + legal clarity\n")


if __name__ == "__main__":
    run_demo()
