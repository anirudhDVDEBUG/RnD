# How to Use — Director SKILL

## This is a Claude Code Skill

It augments Claude Code's behavior when you ask about filmmaking, shot lists, or video prompts. No server, no API keys.

## Install the Skill

### Option A: Global install (all projects)

```bash
mkdir -p ~/.claude/skills/director-skill-ai-filmmaking
cp SKILL.md ~/.claude/skills/director-skill-ai-filmmaking/SKILL.md
```

### Option B: Per-project install

```bash
mkdir -p .claude/skills/director-skill-ai-filmmaking
cp SKILL.md .claude/skills/director-skill-ai-filmmaking/SKILL.md
```

### Option C: Clone from source

```bash
git clone https://github.com/wuwangzhang1216/DirectorSKILL.git
cp DirectorSKILL/SKILL.md ~/.claude/skills/director-skill-ai-filmmaking/SKILL.md
```

After copying, restart Claude Code. The skill is active immediately.

## Trigger Phrases

Say any of these to Claude Code and the skill activates:

| Phrase | What happens |
|---|---|
| "create a shot list" | Generates numbered shots with type, movement, duration |
| "generate keyframe prompts" | Produces image-gen prompts per shot |
| "director style overlay" | Applies a specific director's visual language |
| "cinematic video prompt" | Creates Runway/Kling/Veo-ready prompts |
| "storyboard this scene" | Full pipeline: shots + keyframes + video prompts |

## Available Directors

Spielberg, Kubrick, Wong Kar-wai, Nolan, Villeneuve, Wes Anderson, Tarkovsky, David Lynch, Park Chan-wook, Ridley Scott.

## First 60 Seconds

**1. Install the skill** (Option A above — 10 seconds).

**2. Open Claude Code and type:**

```
Create a shot list for this scene in the style of Kubrick:
A child opens a mysterious door at the end of a long symmetrical hallway in a grand hotel.
```

**3. Claude responds with:**

- A 5-shot numbered sequence (EWS → CU → WS etc.) with camera movement, duration, and director notes
- Keyframe prompts you can paste into Midjourney/DALL-E/Flux
- Video prompts formatted for Runway Gen-3/4, Kling, or Google Veo

**4. Iterate:**

```
Switch to Wong Kar-wai style and format the video prompts for Kling
```

## Standalone Demo (no Claude Code needed)

```bash
bash run.sh
```

Runs three demo scenes (Tarkovsky, Wong Kar-wai, Kubrick) and prints formatted output. Zero dependencies beyond Python 3.

### Custom scene:

```bash
python3 director_skill.py "A woman dances alone in an empty ballroom" "wes_anderson" "runway"
```

### JSON export:

```bash
python3 director_skill.py --json
```
