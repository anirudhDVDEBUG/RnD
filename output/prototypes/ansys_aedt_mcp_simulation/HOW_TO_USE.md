# How to Use: Ansys AEDT MCP Simulation

## Option A: MCP Server (connect Claude Desktop to live Ansys AEDT)

### Prerequisites

- **Ansys Electronics Desktop 2023 R2+** installed and licensed
- **Python 3.9+**
- **uv** (recommended) or pip

### Install

```bash
git clone https://github.com/LaplaceYoung/ansys-aedt-mcp.git
cd ansys-aedt-mcp
uv sync          # or: pip install -e .
```

### Configure Claude Desktop

Add this to `~/.claude.json` (or `claude_desktop_config.json`), inside the `mcpServers` block:

```json
{
  "mcpServers": {
    "ansys-aedt": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/ansys-aedt-mcp", "run", "server.py"]
    }
  }
}
```

If using pip instead of uv:

```json
{
  "mcpServers": {
    "ansys-aedt": {
      "command": "python",
      "args": ["/absolute/path/to/ansys-aedt-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop after saving. The AEDT tools will appear in Claude's tool list.

---

## Option B: Claude Code Skill

### Install the Skill

```bash
mkdir -p ~/.claude/skills/ansys_aedt_mcp_simulation
cp SKILL.md ~/.claude/skills/ansys_aedt_mcp_simulation/SKILL.md
```

### Trigger Phrases

The skill activates when you say things like:

- "Set up MCP server for Ansys AEDT simulation automation"
- "Run an HFSS electromagnetic simulation with Claude"
- "Automate Maxwell or Q3D design workflows via MCP"
- "Create parametric sweeps and reports in Ansys AEDT"
- "Use PyAEDT with Claude for Icepak thermal simulation"

---

## First 60 Seconds

### 1. Run the mock demo (no Ansys needed)

```bash
bash run.sh
```

**Input:** None -- the demo runs a complete patch antenna workflow automatically.

**Output:** You'll see every MCP tool call with JSON request/response, ending with an ASCII S11 plot showing a resonance dip at 2.4 GHz with ~-27 dB return loss.

### 2. With real Ansys AEDT

After configuring the MCP server, open Claude Desktop and type:

> "Create a 2.4 GHz patch antenna in HFSS and plot S11"

Claude will:
1. Create an AEDT project and HFSS design
2. Build ground plane, substrate, and patch geometry
3. Assign a lumped port excitation
4. Set up analysis at 2.4 GHz with a 1-4 GHz frequency sweep
5. Run the simulation
6. Extract and display S-parameter results

Each step is a separate MCP tool call that you can watch in Claude's tool-use panel.

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `aedt_create_project` | Create a new AEDT project |
| `aedt_create_design` | Create HFSS / Maxwell / Q3D / Icepak design |
| `aedt_create_box` | Create 3D box geometry |
| `aedt_create_cylinder` | Create 3D cylinder geometry |
| `aedt_assign_excitation` | Assign WavePort or LumpedPort |
| `aedt_create_setup` | Configure analysis setup |
| `aedt_create_frequency_sweep` | Add frequency sweep to setup |
| `aedt_analyze` | Run the simulation |
| `aedt_get_s_parameters` | Extract S-parameter results |
