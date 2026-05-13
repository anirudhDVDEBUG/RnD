#!/usr/bin/env python3
"""
Fork-a-Slicer Demo — Orchestrates the full process-isolation demo.

Starts the Bambu Bridge in a subprocess, then runs the slicer client
against it, demonstrating the FULU-Foundation architecture end-to-end.
"""

import os
import signal
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOCKET_PATH = "/tmp/bambu_bridge.sock"


def cleanup(bridge_proc):
    """Terminate the bridge process and clean up the socket."""
    if bridge_proc and bridge_proc.poll() is None:
        bridge_proc.terminate()
        bridge_proc.wait(timeout=5)
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)


def main():
    print("=" * 60)
    print("  Fork-a-Slicer: FULU-Foundation Process Isolation Demo")
    print("=" * 60)
    print()
    print("This demo shows how a forked OrcaSlicer communicates with")
    print("Bambu Lab printers through a process-isolated JSON-RPC bridge.")
    print()

    # Clean up any stale socket
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    # Start the bridge as a separate process
    print("[main] Starting Bambu Connect Bridge (separate process)...")
    bridge_proc = subprocess.Popen(
        [sys.executable, os.path.join(SCRIPT_DIR, "bambu_bridge.py")],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    # Wait for the bridge socket to become available
    for i in range(30):
        if os.path.exists(SOCKET_PATH):
            break
        time.sleep(0.1)
    else:
        print("[main] ERROR: Bridge socket did not appear. Exiting.")
        cleanup(bridge_proc)
        sys.exit(1)

    print(f"[main] Bridge is ready. Slicer PID={os.getpid()}, Bridge PID={bridge_proc.pid}")
    print(f"[main] Two separate processes communicating via {SOCKET_PATH}")
    print()

    # Run the slicer client
    try:
        slicer_proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "slicer_client.py")],
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        print("[main] Slicer client timed out.")
    finally:
        cleanup(bridge_proc)

    print("[main] Bridge process terminated. Demo finished.")


if __name__ == "__main__":
    main()
