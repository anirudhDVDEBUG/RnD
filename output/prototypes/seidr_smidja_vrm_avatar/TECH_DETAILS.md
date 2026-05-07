# Technical Details: Seidr-Smidja

## What It Does

Seidr-Smidja is a Python tool that programmatically generates VRM-format 3D avatar files without requiring manual 3D modeling software. It exposes avatar creation through three interfaces (CLI, REST API, MCP) so that AI agents can autonomously produce VRM avatars from text descriptions. The tool handles mesh generation, UV mapping, material assignment, blendshape creation, spring bone configuration, and VRM metadata packaging into a single standards-compliant `.vrm` file.

VRM is a glTF-based format specifically designed for humanoid avatars, widely used in VRChat, VTube Studio, 3tene, and other virtual avatar platforms. Seidr-Smidja abstracts the complexity of VRM authoring into simple parameters an AI agent can reason about.

## Architecture

```
User/Agent Request
       |
       v
+------------------+
| Interface Layer  |  (CLI argparse / FastAPI / MCP stdio)
+------------------+
       |
       v
+------------------+
| Style Engine     |  Resolves presets (anime, cyberpunk, fantasy, etc.)
+------------------+
       |
       v
+------------------+
| Mesh Generator   |  Parametric humanoid mesh (vertices, faces, UVs)
+------------------+
       |
       v
+------------------+
| VRM Packager     |  Blendshapes, spring bones, materials, metadata
+------------------+
       |
       v
+------------------+
| glTF/VRM Export  |  Binary .vrm output (glTF 2.0 + VRM extensions)
+------------------+
```

### Key Files

| File | Purpose |
|------|---------|
| `seidr_smidja.py` | Main entry point, interface routing |
| `mesh_generator.py` | Parametric humanoid mesh creation |
| `vrm_packager.py` | VRM metadata, blendshapes, spring bones |
| `style_presets.py` | Named style configurations |
| `api_server.py` | FastAPI REST interface |
| `mcp_handler.py` | MCP protocol handler (stdio JSON-RPC) |

### Dependencies

- **numpy** -- mesh vertex/face computation
- **pygltflib** -- glTF 2.0 read/write (VRM is glTF-based)
- **fastapi + uvicorn** -- REST API mode
- **pillow** -- texture generation/manipulation

### Data Flow

1. Input parameters (style, hair, eyes, outfit, accessories) are resolved against style presets
2. Base humanoid mesh is generated parametrically (configurable vertex density)
3. Customization meshes (hair, clothing, accessories) are merged onto base
4. Blendshapes (facial expressions) are computed as vertex offsets from neutral pose
5. Spring bone chains are configured for physics-enabled elements (hair, clothing)
6. Materials and textures are assigned (cel-shading for anime styles)
7. VRM metadata (permissions, author, license) is written
8. Everything is packaged into a single binary `.vrm` (glTF + VRM extensions)

## Limitations

- **No AI image generation** -- does not use Stable Diffusion or similar; meshes are parametric/procedural
- **Limited customization depth** -- relies on preset components; cannot create arbitrary freeform shapes
- **No rigging editor** -- bone weights are automatic; fine-tuning requires external tools (Blender)
- **Texture quality** -- procedural textures are functional but not artist-grade
- **VRM 0.x only** -- does not yet support VRM 1.0 specification
- **No animation** -- generates static avatar; animation requires separate tools

## Why This Matters for Claude-Driven Products

| Use Case | Application |
|----------|-------------|
| **Agent Factories** | Agents can self-generate visual personas/avatars for customer-facing bots |
| **Marketing/Ad Creatives** | Rapidly produce branded virtual mascots or spokesperson avatars |
| **Voice AI** | Pair generated avatars with voice synthesis for VTuber-style presentations |
| **Lead-gen** | Create personalized avatar demos as interactive sales collateral |
| **Content Pipelines** | Automate avatar creation for virtual events, gaming, or social media content |

The key value is **removing the human-in-the-loop for 3D avatar creation** -- an agent can go from text description to deployable VRM file in a single tool call, enabling fully automated virtual identity pipelines.
