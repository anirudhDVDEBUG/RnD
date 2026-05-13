---
name: fork_a_slicer
description: |
  Step-by-step plans for forking OrcaSlicer and adding Bambu Lab printer support via a process isolation bridge, based on the FULU-Foundation architecture.
  Triggers: fork orcaslicer, bambu printer bridge, 3d printer slicer fork, process isolation slicer, FULU foundation slicer
---

# Fork-a-Slicer

AI-agent-driven workflow for forking OrcaSlicer and adding Bambu Lab printer support through a process isolation bridge. Based on the FULU-Foundation architecture.

## When to use

- "Help me fork OrcaSlicer and add Bambu printer support"
- "Set up a process isolation bridge for 3D printer communication"
- "Guide me through the FULU-Foundation architecture for slicer development"
- "I want to build a Bambu Connect bridge for OrcaSlicer"
- "Create a slicer fork with JSON-RPC printer networking"

## How to use

### 1. Clone and understand the plan repository

```bash
git clone https://github.com/danielcherubini/fork-a-slicer.git
cd fork-a-slicer
```

Review the step-by-step plans provided in the repository. These plans are designed to be consumed by an AI agent (like Claude Code or Gemini CLI) and followed interactively.

### 2. Fork OrcaSlicer

Follow the repository's phased plan to:
- Fork the OrcaSlicer repository
- Set up the build environment (supports Linux/ARM64)
- Understand the existing codebase structure

### 3. Implement the Process Isolation Bridge

The core architecture uses process isolation to safely bridge Bambu Lab printer communication:
- **Bridge layer**: A separate process that handles Bambu Connect protocol communication
- **JSON-RPC interface**: Clean inter-process communication between the slicer and the bridge
- **Printer networking**: Discovery and management of Bambu Lab printers on the local network

### 4. FULU-Foundation Architecture

The FULU-Foundation architecture provides:
- Clean separation between slicer UI/logic and printer communication
- Process isolation for stability and security
- Interoperability layer so the forked slicer can communicate with Bambu printers without embedding proprietary code

### 5. Build and Test

- Build the forked slicer with the bridge integration
- Test printer discovery and connectivity
- Validate print job submission through the bridge

## Key Concepts

- **OrcaSlicer**: Open-source 3D printing slicer (fork of BambuStudio/PrusaSlicer)
- **Bambu Connect**: Bambu Lab's printer communication protocol
- **Process Isolation Bridge**: Separate process handling proprietary protocol communication, connected via JSON-RPC
- **FULU-Foundation**: Architecture pattern for clean separation of concerns in slicer/printer interop

## References

- Source repository: https://github.com/danielcherubini/fork-a-slicer
- Topics: 3d-printing, ai-agent, arm64, bambu-connect, bambu-lab, bridge, claude-code, gemini-cli, interoperability, json-rpc, linux, open-source, orcaslicer, printer-networking, process-isolation, reverse-engineering
