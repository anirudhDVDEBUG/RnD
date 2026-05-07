# Seidr-Smidja: AI-Agent-Driven VRM Avatar Generator

**TL;DR:** Seidr-Smidja lets AI agents (Claude Code, Hermes, OpenClaw) generate complete VRM avatars for VRChat/VTubing via CLI, API, or MCP -- no manual 3D modeling required.

## Headline Result

```
$ python seidr_smidja.py --create --style cyberpunk --name "NeonKitsune"
[OK] Generated VRM avatar: output/NeonKitsune.vrm (2.4 MB)
     - 12,847 vertices, 8 blendshapes, 24 spring bones
     - Compatible with: VRChat, VTube Studio, 3tene
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install, configure, and run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, data flow, limitations

## Source

- Repository: https://github.com/hrabanazviking/Seidr-Smidja
- Interfaces: CLI, REST API, MCP Server
- Language: Python
