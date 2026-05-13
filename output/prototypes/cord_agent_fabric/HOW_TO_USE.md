# How to Use Cord Agent Fabric

## 1. Install the real Cord

Cord is written in Rust. You need the Rust toolchain (`rustup`).

```bash
# Install Rust if you don't have it
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone and build Cord
git clone https://github.com/fosenai/cord.git
cd cord
cargo build --release

# Binary lands in target/release/cord
./target/release/cord --help
```

## 2. Set up as a Claude Code Skill

Cord ships as a Claude Code **skill**. Drop the skill folder:

```bash
mkdir -p ~/.claude/skills/cord_agent_fabric
# Copy SKILL.md into that directory
cp SKILL.md ~/.claude/skills/cord_agent_fabric/SKILL.md
```

**Trigger phrases** that activate the skill:

- "Set up Cord for distributed agent discovery"
- "I want my MCP servers discoverable across machines"
- "Connect multiple AI agents in a mesh network"
- "Use semantic search to find LLM backends on my network"
- "Configure Cord for multi-agent orchestration"

Any mention of **Cord**, **distributed agent mesh**, **agent discovery**, **multi-agent orchestration across machines**, or **semantic service discovery for MCP servers** will also trigger it.

## 3. Run the local demo (no API keys)

```bash
bash run.sh
```

This runs a Python simulation of Cord's core loop — registering services, building a peer mesh, and running semantic discovery queries. Output is printed to the terminal and exported to `cord_mesh_state.json`.

## 4. First 60 seconds

**Input** — run `bash run.sh`:

```
$ bash run.sh
=== Cord Agent Fabric — Demo ===

Running cord_demo.py ...

════════════════════════════════════════════════════════════════
  Cord Agent Fabric — Local Simulator
════════════════════════════════════════════════════════════════
```

**What happens next:**

1. **8 services register** — MCP servers, LLM backends, and autonomous agents across 5 simulated peers.
2. **5 semantic queries run** — each returns the top-3 matches with similarity scores rendered as bar charts.
3. **Mesh state exports** to `cord_mesh_state.json`.

**Output** (excerpt):

```
▸ Step 3 — Semantic discovery queries

  Query: "I need a tool that can read and write files on the filesystem"
    1. fs-tools-mcp [mcp-server] on dev-box
       ████████████████████████████░░ 91.23%
    2. git-mcp [mcp-server] on dev-box
       ██████████░░░░░░░░░░░░░░░░░░░░ 31.47%
    3. codegen-llama [llm-backend] on gpu-node-1
       ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 12.85%
```

**Output file** — `cord_mesh_state.json`:

```json
{
  "mesh": {
    "peers": [ ... ],
    "services": [ ... ],
    "total_peers": 5,
    "total_services": 8
  }
}
```

## 5. Using real Cord (once installed)

```bash
# Register an MCP server
cord register --name "my-mcp-server" \
  --type mcp-server \
  --endpoint "http://localhost:3000" \
  --description "MCP server providing file system and git tools"

# Discover services by describing what you need
cord discover "I need a tool that can read and write files"

# Join a peer mesh
cord join --peer 192.168.1.10:7946

# List everything in the mesh
cord list
```
