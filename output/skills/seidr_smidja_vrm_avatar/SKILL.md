---
name: seidr_smidja_vrm_avatar
description: |
  Create VRM avatars (anime-style 3D avatars for VRChat, VTubing, etc.) using the Seidr-Smidja tool via CLI, API, or MCP.
  TRIGGER when: user wants to create a VRM avatar, generate a 3D anime avatar, make a VTuber model, create a VRChat avatar, or use Seidr-Smidja.
  DO NOT TRIGGER when: user is working with 2D images, non-avatar 3D models, or unrelated avatar systems.
---

# When to use

Use this skill when:
- "Create a VRM avatar" or "make me a VTuber avatar"
- "Generate a 3D anime character for VRChat"
- "Use Seidr-Smidja to build an avatar"
- "I need an avatar for VTubing/VRChat"
- "Set up avatar generation pipeline with AI agents"

# How to use

## Overview

Seidr-Smidja enables AI agents (Claude Code, Hermes Agent, OpenClaw, etc.) to create VRM-format 3D avatars through fully automated agent-driven processes. VRM avatars are used for VRChat, VTubing, and other virtual avatar applications.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/hrabanazviking/Seidr-Smidja.git
   cd Seidr-Smidja
   ```

2. Install dependencies (Python-based):
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the tool for your preferred interface (CLI, API, or MCP).

## Usage Modes

### CLI Mode
Run avatar generation directly from the command line:
```bash
python seidr_smidja.py --create --style <style> --output <output_path.vrm>
```

### API Mode
Start the API server and send requests programmatically:
```bash
python seidr_smidja.py --serve
```

### MCP Mode
Register as an MCP server for use with Claude Code or other MCP-compatible agents. Add to your MCP configuration:
```json
{
  "mcpServers": {
    "seidr-smidja": {
      "command": "python",
      "args": ["path/to/seidr_smidja.py", "--mcp"]
    }
  }
}
```

## Workflow

1. **Define avatar characteristics** - Specify style, body type, hair, clothing, accessories
2. **Generate the 3D model** - The tool creates the base mesh and applies customizations
3. **Apply VRM metadata** - Adds expression blendshapes, spring bones, and VRM-specific data
4. **Export** - Outputs a standards-compliant .vrm file ready for use

## Key Features

- Fully agent-driven (no manual 3D modeling required)
- Outputs standard VRM format compatible with VRChat, VTube Studio, etc.
- Supports CLI, REST API, and MCP interfaces
- Works with multiple AI agent frameworks (Claude Code, Hermes, OpenClaw)

# References

- Repository: https://github.com/hrabanazviking/Seidr-Smidja
- VRM specification: https://vrm.dev/en/
- Language: Python
- License: See repository for details
