# Technical Details: Ansys AEDT MCP Server

## What It Does

The `ansys-aedt-mcp` server exposes Ansys Electronics Desktop (AEDT) simulation capabilities as MCP tools that Claude can invoke. It wraps [PyAEDT](https://aedt.docs.pyansys.com/) -- Ansys's official Python automation library -- behind the Model Context Protocol, letting an LLM create projects, build 3D geometry, assign materials and boundaries, configure solvers, run simulations, and extract results through structured tool calls instead of manual GUI interaction or scripting.

The server supports four AEDT solver applications: **HFSS** (3D electromagnetic), **Maxwell** (electromagnetic/electromechanical), **Q3D Extractor** (parasitic RLC extraction), and **Icepak** (thermal/fluid flow). A typical workflow is: create project -> create design -> build geometry -> assign excitations -> configure setup/sweep -> analyze -> extract results.

## Architecture

```
Claude Desktop / Claude Code
       |
       | MCP JSON-RPC (stdio transport)
       v
 ┌─────────────────────┐
 │  ansys-aedt-mcp      │   server.py (FastMCP-based)
 │  MCP Server           │   - Tool definitions
 │                       │   - Input validation
 │                       │   - JSON-RPC handler
 └───────┬───────────────┘
         |
         | PyAEDT API calls
         v
 ┌─────────────────────┐
 │  PyAEDT              │   Python automation library
 │  (pyaedt package)     │   - AEDT COM/gRPC bridge
 │                       │   - Geometry, materials, mesh
 │                       │   - Solver control, post-proc
 └───────┬───────────────┘
         |
         | COM / gRPC
         v
 ┌─────────────────────┐
 │  Ansys AEDT Desktop  │   Licensed commercial solver
 │  (HFSS, Maxwell,     │   - Finite element solver
 │   Q3D, Icepak)       │   - Mesh generation
 │                       │   - Results database
 └─────────────────────┘
```

### Key Files (upstream repo)

| File | Role |
|------|------|
| `server.py` | MCP server entry point; registers tools, handles JSON-RPC |
| `pyaedt` (dependency) | Ansys-maintained Python library that drives AEDT |
| `pyproject.toml` | Dependencies: `mcp`, `pyaedt` |

### Data Flow

1. Claude sends a `tools/call` JSON-RPC request (e.g., `aedt_create_box` with position/dimensions/material).
2. The MCP server deserializes the arguments and calls the corresponding PyAEDT method.
3. PyAEDT translates the call into AEDT's COM or gRPC API, which controls the running AEDT desktop instance.
4. AEDT performs the operation (creates geometry, runs solver, etc.).
5. PyAEDT returns the result; the server serializes it back as MCP tool output.

### Dependencies

- **Runtime:** Python 3.9+, `pyaedt` (pulls in numpy, matplotlib, etc.), `mcp` (MCP SDK)
- **Required:** Ansys AEDT 2023 R2+ with valid license (HFSS/Maxwell/Q3D/Icepak)
- **Platform:** Windows primary (AEDT is Windows-native); Linux with AEDT Linux builds
- **Demo only:** Python 3.9+ standard library (no external packages)

## Limitations

- **Requires Ansys AEDT license.** This is a commercial product; the MCP server is the bridge, not a replacement. No simulation runs without a licensed AEDT installation.
- **Windows-centric.** AEDT's COM automation works best on Windows. Linux support exists but is less common in practice.
- **Solver scope.** Covers HFSS, Maxwell, Q3D, Icepak. Does not support Mechanical, Fluent, or other Ansys workbench tools.
- **No geometry import.** The current tool set creates primitive shapes (boxes, cylinders). Complex CAD imports (STEP, SAT) would require additional tool implementations.
- **Single-session.** Manages one AEDT desktop session at a time. Parallel multi-project orchestration is not built in.
- **No real-time streaming.** Simulation progress (mesh adaptation passes, convergence) is reported after completion, not streamed live.

## Why This Matters for Claude-Driven Products

**Agent factories / engineering automation:** This is a concrete example of giving Claude control over a heavyweight commercial simulation tool. The same MCP pattern can wrap any desktop engineering application (MATLAB, SolidWorks, Cadence) to create AI-driven design automation agents.

**Lead-gen for simulation services:** A consulting firm could deploy Claude with this MCP server as a front-end: prospects describe their antenna/motor/PCB problem in natural language, Claude sets up and runs a preliminary simulation, and the firm delivers results as a lead-qualification step.

**Parametric design exploration:** Claude can loop over design variables (patch width, substrate thickness, feed position), run hundreds of simulations, and identify optimal configurations -- turning conversational AI into an automated design-of-experiments engine.

**Training and education:** Engineering students and junior engineers can describe what they want to simulate in plain English instead of learning AEDT's complex GUI, lowering the barrier to electromagnetic simulation.
