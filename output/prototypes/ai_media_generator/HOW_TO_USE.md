# How to Use — AI Media Prompt Generator

## Install the Claude Code Skill

This is a **Claude Code Skill** (not an MCP server). Installation means dropping a `SKILL.md` file into the skills directory.

### Step 1 — Clone the source

```bash
git clone https://github.com/Hao0321/ai-media-generator.git
```

### Step 2 — Copy the skill file

```bash
mkdir -p ~/.claude/skills/ai_media_generator
cp ai-media-generator/SKILL.md ~/.claude/skills/ai_media_generator/SKILL.md
```

That's it. No `pip install`, no `npm install`, no API keys. The skill is pure prompt instructions that Claude reads at activation time.

### Step 3 — Verify

Open Claude Code and type any trigger phrase (see below). Claude should respond with a platform-optimized prompt.

## Trigger Phrases

Say any of these in Claude Code to activate the skill:

| Phrase | What happens |
|--------|-------------|
| `generate AI image` | Crafts an image prompt for your chosen platform |
| `create video prompt` | Builds a video prompt with camera/motion direction |
| `AI media` | General media prompt generation |
| `midjourney prompt` | Midjourney-specific syntax with --ar, --v, --s flags |
| `sora prompt` | Sora-optimized video scene description |
| `kling prompt` | Kling video prompt with motion controls |
| `veo prompt` | Google Veo cinematic video prompt |
| `flux prompt` | Flux image prompt with natural language |
| `seedance prompt` | Seedance motion/dance video prompt |
| `suno prompt` | Suno music prompt with genre, mood, lyrics |
| `music prompt` | General music generation prompt |
| `generative prompt` | Any generative AI platform |

## First 60 Seconds

**1. Install** (10 seconds):
```bash
mkdir -p ~/.claude/skills/ai_media_generator
curl -o ~/.claude/skills/ai_media_generator/SKILL.md \
  https://raw.githubusercontent.com/Hao0321/ai-media-generator/main/SKILL.md
```

**2. Open Claude Code** and type:
```
Generate a Midjourney prompt for a luxury perfume bottle on black marble
```

**3. Claude responds** with something like:
```
medium close-up of an elegant crystal perfume bottle on polished black marble,
dark studio with single spotlight, rim lighting with warm amber highlights,
Kodak Portra 400 color grading, shot on 100mm macro lens, luxurious and
sophisticated atmosphere, style: high-end commercial photography
--ar 4:5 --v 6.1 --s 800 --q 1

Negative: blurry, deformed, low quality, watermark, text, logo, oversaturated
```

**4. Iterate**: "Make it more dramatic" / "Switch to Flux" / "Add a reflection"

**5. Execute**: Claude can open the platform in your browser and paste the prompt.

## Running the Local Demo

No Claude Code needed — see the prompt engine in action:

```bash
bash run.sh
```

This generates 6 demo prompts (image, video, music) across different platforms with zero API keys.
