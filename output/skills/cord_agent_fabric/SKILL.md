---
name: cord_agent_fabric
description: |
  Set up and use Cord — a distributed agent fabric for LLMs, MCP servers, and AI agents.
  Enables discovery of any LLM CLI / HTTP backend / MCP server across machines via
  natural-language semantic search. Built in Rust.
  TRIGGER: user mentions Cord, distributed agent mesh, agent discovery, multi-agent
  orchestration across machines, or semantic service discovery for MCP servers.
---

# Cord Agent Fabric

Set up and operate **Cord**, a distributed agent fabric that lets LLMs, MCP servers, and AI agents discover and communicate with each other across machines using natural-language semantic search.

## When to use

- "Set up Cord for distributed agent discovery"
- "I want my MCP servers discoverable across machines"
- "Connect multiple AI agents in a mesh network"
- "Use semantic search to find LLM backends on my network"
- "Configure Cord for multi-agent orchestration"

## How to use

### 1. Install Cord

Cord is built in Rust. Install from the GitHub repository:

```bash
# Clone the repository
git clone https://github.com/fosenai/cord.git
cd cord

# Build from source (requires Rust toolchain)
cargo build --release

# Or install directly
cargo install --path .
```

### 2. Register services

Register your LLM backends, MCP servers, or AI agents with Cord so they become discoverable:

```bash
# Register an MCP server with a natural-language description
cord register --name "my-mcp-server" \
  --type mcp-server \
  --endpoint "http://localhost:3000" \
  --description "MCP server providing file system and git tools"

# Register an LLM backend
cord register --name "local-llm" \
  --type llm-backend \
  --endpoint "http://gpu-node:8080" \
  --description "Local LLaMA model for code generation"
```

### 3. Discover services via semantic search

Cord uses natural-language semantic search to find registered services:

```bash
# Find services by describing what you need
cord discover "I need a tool that can read and write files"
cord discover "code generation model with GPU acceleration"
cord discover "agent that handles database operations"
```

### 4. Multi-machine mesh

Cord operates as a decentralized mesh — agents on different machines can discover each other without a central registry:

```bash
# Join an existing Cord network
cord join --peer <peer-address>

# List all discovered peers and services
cord list
```

### 5. Integration with Claude Code

When working on projects that use Cord:

1. Check for a `cord.toml` or Cord configuration file in the project root
2. Use `cord list` to see available services in the mesh
3. Use `cord discover` with natural-language queries to find relevant agents/servers
4. Register new services as needed for the project's agent architecture

### Key features

- **Semantic discovery**: Find services using natural language, not just exact names
- **Decentralized mesh**: No central registry; peers discover each other directly
- **Multi-protocol**: Supports LLM CLI tools, HTTP backends, and MCP servers
- **Built in Rust**: Fast, reliable, low resource usage
- **Agent orchestration**: Coordinate multiple AI agents across distributed infrastructure

## References

- **Repository**: https://github.com/fosenai/cord
- **Topics**: agent-mesh, distributed-agents, service-discovery, mcp-server, multi-agent, agent-orchestration, decentralized
