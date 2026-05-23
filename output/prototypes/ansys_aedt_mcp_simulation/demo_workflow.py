#!/usr/bin/env python3
"""
Demo: Full HFSS Patch Antenna Simulation Workflow via MCP

Walks through the complete workflow that Claude would execute when a user
asks: "Create a 2.4 GHz patch antenna in HFSS and simulate it."

No Ansys AEDT installation required -- uses mock session to show the
exact MCP tool calls, JSON-RPC messages, and simulation results.
"""

import json
import sys
from mock_aedt_server import MockMCPServer, format_jsonrpc

DIVIDER = "=" * 70


def print_step(num: int, title: str):
    print(f"\n{DIVIDER}")
    print(f"  Step {num}: {title}")
    print(DIVIDER)


def call(server: MockMCPServer, tool_name: str, arguments: dict, req_id: int):
    """Simulate an MCP tools/call request and print the exchange."""
    request = format_jsonrpc("tools/call", {"name": tool_name, "arguments": arguments}, req_id)
    print(f"\n  >> MCP Request:")
    print(f"     Tool: {tool_name}")
    print(f"     Args: {json.dumps(arguments, indent=6).replace(chr(10), chr(10) + '     ')}")

    result = server.handle_request("tools/call", {"name": tool_name, "arguments": arguments})
    text = result["content"][0]["text"]
    parsed = json.loads(text)
    print(f"\n  << MCP Response:")
    print(f"     {json.dumps(parsed, indent=6).replace(chr(10), chr(10) + '     ')}")
    return parsed


def render_s11_ascii(freqs: list, values: list):
    """Render a simple ASCII plot of S11 vs frequency."""
    print(f"\n  S11 (dB) vs Frequency (GHz)")
    print(f"  {'─' * 56}")

    min_v = min(values)
    max_v = max(values)
    rows = 16
    cols = 50

    # Build grid
    grid = [[" "] * cols for _ in range(rows)]
    for i, v in enumerate(values):
        col = int((i / (len(values) - 1)) * (cols - 1))
        row = int((1 - (v - min_v) / (max_v - min_v + 1e-9)) * (rows - 1))
        row = max(0, min(rows - 1, row))
        grid[row][col] = "*"

    for r in range(rows):
        db_label = max_v - r * (max_v - min_v) / (rows - 1)
        print(f"  {db_label:7.1f} |{''.join(grid[r])}|")

    print(f"          {'─' * cols}")
    print(f"          {freqs[0]:.1f}" + " " * (cols - 8) + f"{freqs[-1]:.1f} GHz")


def main():
    print("\n" + DIVIDER)
    print("  ANSYS AEDT MCP SERVER -- DEMO WORKFLOW")
    print("  Simulating a 2.4 GHz Microstrip Patch Antenna in HFSS")
    print(DIVIDER)

    server = MockMCPServer()
    req_id = 0

    # ── Initialize ──
    print_step(0, "Initialize MCP Connection")
    init_result = server.handle_request("initialize", {})
    print(f"\n  Server: {init_result['serverInfo']['name']} v{init_result['serverInfo']['version']}")
    print(f"  Protocol: {init_result['protocolVersion']}")

    # ── List Tools ──
    print_step(1, "List Available Tools")
    tools_result = server.handle_request("tools/list", {})
    print(f"\n  {len(tools_result['tools'])} tools available:")
    for t in tools_result["tools"]:
        print(f"    - {t['name']}: {t['description']}")

    # ── Create Project ──
    print_step(2, "Create AEDT Project")
    req_id += 1
    call(server, "aedt_create_project", {"name": "PatchAntenna_2p4GHz"}, req_id)

    # ── Create HFSS Design ──
    print_step(3, "Create HFSS Design")
    req_id += 1
    call(server, "aedt_create_design", {
        "project": "PatchAntenna_2p4GHz",
        "design_name": "PatchDesign1",
        "design_type": "HFSS",
    }, req_id)

    # ── Build Geometry ──
    print_step(4, "Build Antenna Geometry")

    # Ground plane
    req_id += 1
    print("\n  4a. Ground Plane (copper, 60x60 mm)")
    call(server, "aedt_create_box", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "position": [-30, -30, 0],
        "dimensions": [60, 60, 0.035],
        "name": "GroundPlane",
        "material": "copper",
    }, req_id)

    # Substrate
    req_id += 1
    print("\n  4b. Substrate (FR4, 60x60x1.6 mm)")
    call(server, "aedt_create_box", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "position": [-30, -30, 0.035],
        "dimensions": [60, 60, 1.6],
        "name": "Substrate",
        "material": "FR4_epoxy",
    }, req_id)

    # Patch
    req_id += 1
    print("\n  4c. Radiating Patch (copper, 28.5x37 mm)")
    call(server, "aedt_create_box", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "position": [-14.25, -18.5, 1.635],
        "dimensions": [28.5, 37, 0.035],
        "name": "Patch",
        "material": "copper",
    }, req_id)

    # Feed pin
    req_id += 1
    print("\n  4d. Coaxial Feed Pin")
    call(server, "aedt_create_cylinder", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "center": [-5.0, 0, 0.035],
        "radius": 0.65,
        "height": 1.6,
        "axis": "Z",
        "name": "FeedPin",
        "material": "copper",
    }, req_id)

    # ── Assign Excitation ──
    print_step(5, "Assign Lumped Port Excitation")
    req_id += 1
    call(server, "aedt_assign_excitation", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "port_name": "Port1",
        "face_id": 12,
        "exc_type": "LumpedPort",
    }, req_id)

    # ── Setup ──
    print_step(6, "Create Analysis Setup (2.4 GHz, 15 passes)")
    req_id += 1
    call(server, "aedt_create_setup", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "setup_name": "Setup1",
        "frequency": "2.4GHz",
        "max_passes": 15,
    }, req_id)

    # ── Frequency Sweep ──
    print_step(7, "Add Frequency Sweep (1-4 GHz, 10 MHz step)")
    req_id += 1
    call(server, "aedt_create_frequency_sweep", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "setup_name": "Setup1",
        "start": "1GHz",
        "stop": "4GHz",
        "step": "10MHz",
        "sweep_type": "Interpolating",
    }, req_id)

    # ── Analyze ──
    print_step(8, "Run Simulation")
    req_id += 1
    result = call(server, "aedt_analyze", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "setup_name": "Setup1",
    }, req_id)

    # ── Extract Results ──
    print_step(9, "Extract S11 Results & Plot")
    req_id += 1
    s_data = call(server, "aedt_get_s_parameters", {
        "project": "PatchAntenna_2p4GHz",
        "design": "PatchDesign1",
        "setup_name": "Setup1",
        "parameter": "S(1,1)",
        "freq_start": 1.0,
        "freq_stop": 4.0,
        "num_points": 31,
    }, req_id)

    # ── ASCII Plot ──
    print_step(10, "S11 Return Loss Plot")
    render_s11_ascii(s_data["frequencies_ghz"], s_data["values_db"])
    print(f"\n  Resonance: {s_data['min_freq_ghz']} GHz")
    print(f"  Return Loss: {s_data['min_value_db']} dB")

    # ── Summary ──
    print(f"\n{DIVIDER}")
    print("  WORKFLOW COMPLETE")
    print(DIVIDER)
    print(f"""
  This demo walked through the full MCP tool-call sequence that Claude
  executes when automating an HFSS patch antenna simulation:

    1. Project & design creation
    2. 3D geometry (ground, substrate, patch, feed)
    3. Port excitation assignment
    4. Analysis setup + frequency sweep
    5. Simulation solve
    6. S-parameter extraction & visualization

  With the real ansys-aedt-mcp server connected to Ansys AEDT, each of
  these tool calls drives PyAEDT to control the live AEDT session.

  To use with Claude Desktop, add the MCP server config shown in
  HOW_TO_USE.md and ask:
    "Create a 2.4 GHz patch antenna in HFSS and plot S11"
""")


if __name__ == "__main__":
    main()
