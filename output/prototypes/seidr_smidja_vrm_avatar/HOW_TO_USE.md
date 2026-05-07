# How to Use Seidr-Smidja

## Install

```bash
git clone https://github.com/hrabanazviking/Seidr-Smidja.git
cd Seidr-Smidja
pip install -r requirements.txt
```

## As a Claude Skill

Drop the skill folder into your skills directory:

```bash
cp -r skill/ ~/.claude/skills/seidr_smidja_vrm_avatar/
```

**Trigger phrases:**
- "Create a VRM avatar"
- "Make me a VTuber avatar"
- "Generate a 3D anime character for VRChat"
- "Use Seidr-Smidja to build an avatar"
- "I need an avatar for VTubing"

## As an MCP Server

Add this to your `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "seidr-smidja": {
      "command": "python",
      "args": ["/path/to/Seidr-Smidja/seidr_smidja.py", "--mcp"],
      "env": {}
    }
  }
}
```

Replace `/path/to/Seidr-Smidja/` with your actual clone location.

## CLI Usage

```bash
# Basic generation
python seidr_smidja.py --create --style anime --name "MyAvatar"

# With detailed customization
python seidr_smidja.py --create \
  --style cyberpunk \
  --name "NeonKitsune" \
  --hair spiky_long \
  --eyes heterochromia \
  --outfit jacket_techwear \
  --accessories fox_ears,visor

# Start the REST API server
python seidr_smidja.py --serve --port 8080
```

## First 60 Seconds

```bash
# 1. Run the demo (uses mock generation, no GPU required)
bash run.sh

# Expected output:
# [INIT] Seidr-Smidja VRM Generator v0.3.0
# [STYLE] Applying style preset: cyberpunk
# [MESH] Generating base mesh... 12,847 vertices
# [BLEND] Creating blendshapes: neutral, joy, angry, sorrow, fun, surprised, blink_l, blink_r
# [BONE] Configuring spring bones: 24 chains (hair, clothing, accessories)
# [META] Writing VRM metadata (title, author, permissions)
# [EXPORT] Avatar saved: output/demo_avatar.vrm (2.4 MB)
# [DONE] VRM avatar ready for VRChat / VTube Studio / 3tene

# 2. Inspect the output
python seidr_smidja.py --inspect output/demo_avatar.vrm
```

## API Mode (for integration)

```bash
# Start server
python seidr_smidja.py --serve --port 8080

# Create avatar via HTTP
curl -X POST http://localhost:8080/create \
  -H "Content-Type: application/json" \
  -d '{"name": "TestAvatar", "style": "anime", "hair": "twin_tails"}'
```

Response:
```json
{
  "status": "success",
  "file": "output/TestAvatar.vrm",
  "stats": {
    "vertices": 12847,
    "blendshapes": 8,
    "spring_bones": 24
  }
}
```
