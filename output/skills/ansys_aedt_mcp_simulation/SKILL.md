---
name: ansys_aedt_mcp_simulation
description: |
  Set up and use the ansys-aedt-mcp MCP server for Ansys Electronics Desktop (AEDT) automation with Claude.
  Enables electromagnetic simulation workflows using PyAEDT, HFSS, Maxwell, Q3D, Icepak, native AEDT APIs, reports, sweeps, and simulation management.

  TRIGGER: User wants to automate Ansys AEDT, run HFSS/Maxwell/Q3D/Icepak simulations via MCP, set up electromagnetic simulation workflows, use PyAEDT with Claude, or configure the ansys-aedt-mcp server.
---

# Ansys AEDT MCP Simulation Skill

Automate Ansys Electronics Desktop (AEDT) simulations through the `ansys-aedt-mcp` MCP server, enabling AI-driven electromagnetic simulation workflows with Claude.

## When to use

- "Set up MCP server for Ansys AEDT simulation automation"
- "Run an HFSS electromagnetic simulation with Claude"
- "Automate Maxwell or Q3D design workflows via MCP"
- "Create parametric sweeps and reports in Ansys AEDT"
- "Use PyAEDT with Claude for Icepak thermal simulation"

## How to use

### 1. Prerequisites

- **Ansys Electronics Desktop (AEDT)** installed (2023 R2 or later recommended)
- **Python 3.9+** with `pyaedt` installed
- **uv** package manager (recommended) or pip

### 2. Install the MCP Server

```bash
# Clone the repository
git clone https://github.com/LaplaceYoung/ansys-aedt-mcp.git
cd ansys-aedt-mcp

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 3. Configure for Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ansys-aedt": {
      "command": "uv",
      "args": ["--directory", "/path/to/ansys-aedt-mcp", "run", "server.py"]
    }
  }
}
```

Or if using pip:

```json
{
  "mcpServers": {
    "ansys-aedt": {
      "command": "python",
      "args": ["/path/to/ansys-aedt-mcp/server.py"]
    }
  }
}
```

### 4. Supported Simulation Tools

The MCP server provides tools for these AEDT applications:

- **HFSS** — 3D electromagnetic field simulation (antennas, RF components, signal integrity)
- **Maxwell** — Electromagnetic and electromechanical simulation (motors, transformers, actuators)
- **Q3D Extractor** — Parasitic extraction (RLC parameters for PCB/package designs)
- **Icepak** — Thermal/fluid flow simulation for electronics cooling

### 5. Key Capabilities

- **Project Management**: Create, open, save, and manage AEDT projects and designs
- **Geometry & Materials**: Create 3D objects, assign materials, define boundaries and excitations
- **Simulation Setup**: Configure analysis setups, frequency sweeps, mesh operations
- **Parametric Sweeps**: Define design variables and run parametric studies
- **Reports & Post-processing**: Generate S-parameter plots, field overlays, and export results
- **Native AEDT API Access**: Direct access to AEDT scripting APIs via PyAEDT

### 6. Example Workflow

Once configured, ask Claude to:

1. "Create a new HFSS project with a patch antenna at 2.4 GHz"
2. "Set up a frequency sweep from 1 GHz to 4 GHz"
3. "Run the simulation and plot S11 results"
4. "Optimize the antenna dimensions for best return loss"

## References

- **Repository**: [LaplaceYoung/ansys-aedt-mcp](https://github.com/LaplaceYoung/ansys-aedt-mcp)
- **PyAEDT Documentation**: [PyAEDT Docs](https://aedt.docs.pyansys.com/)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)
