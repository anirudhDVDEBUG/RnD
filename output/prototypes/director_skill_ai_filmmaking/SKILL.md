---
name: Director SKILL — AI Filmmaking
description: |
  Claude Code skill for AI filmmaking — generates shot lists, keyframe prompts, and video prompts with 10 director-style overlays (Spielberg, Kubrick, Wong Kar-wai, Nolan, Villeneuve, Wes Anderson, Tarkovsky, David Lynch, Park Chan-wook, Ridley Scott). Designed for use with AI video tools like Runway, Kling, and Veo.
  Triggers:
    - "create a shot list"
    - "generate keyframe prompts"
    - "director style overlay"
    - "cinematic video prompt"
    - "storyboard this scene"
---

# Director SKILL — AI Filmmaking

A Claude Code skill that transforms scene descriptions into professional cinematic shot lists, keyframe prompts, and AI video generation prompts — all styled through the lens of iconic film directors.

## When to use

- "Create a shot list for my scene"
- "Generate keyframe prompts in the style of Kubrick"
- "Storyboard this scene with cinematic direction"
- "Write video prompts for Runway / Kling / Veo"
- "Apply a Spielberg director overlay to these shots"

## How to use

### Step 1: Describe your scene

Provide a scene description — it can be a brief concept, a screenplay excerpt, or a narrative paragraph. Include details about setting, characters, mood, and action.

### Step 2: Choose a director style (optional)

Select from 10 available director-style overlays that shape the visual language of your output:

| Director | Signature Style |
|---|---|
| **Steven Spielberg** | Emotional close-ups, golden-hour lighting, awe-inspiring reveals |
| **Stanley Kubrick** | Symmetrical compositions, one-point perspective, cold precision |
| **Wong Kar-wai** | Saturated neons, step-printed motion blur, longing and intimacy |
| **Christopher Nolan** | IMAX-scale compositions, cross-cut timelines, practical grandeur |
| **Denis Villeneuve** | Vast negative space, slow-reveal wide shots, desaturated palette |
| **Wes Anderson** | Centered framing, pastel palette, dollhouse planimetric compositions |
| **Andrei Tarkovsky** | Long takes, natural elements (water, fire, wind), spiritual atmosphere |
| **David Lynch** | Surreal juxtaposition, uncanny lighting, dreamlike discontinuity |
| **Park Chan-wook** | Baroque framing, bold color contrast, visceral choreography |
| **Ridley Scott** | Smoke and atmosphere, backlit silhouettes, layered industrial detail |

If no director is specified, a neutral cinematic style is used.

### Step 3: Generate outputs

The skill produces three structured outputs:

1. **Shot List** — A numbered sequence of shots with shot type (wide, medium, close-up, etc.), camera movement, subject action, and duration estimate.

2. **Keyframe Prompts** — Detailed image generation prompts for each key moment, incorporating the selected director's visual language — including lens choice, lighting, color grade, and composition.

3. **Video Prompts** — Ready-to-paste prompts optimized for AI video generation tools (Runway Gen-3/4, Kling, Google Veo). Each prompt includes motion description, camera behavior, and transition notes.

### Step 4: Iterate and refine

- Ask to adjust pacing, add/remove shots, or switch director styles
- Request prompts formatted for a specific platform (e.g., "format for Kling" or "optimize for Veo")
- Combine multiple director styles for a hybrid look

## Example

**Input:**
> A lone astronaut discovers a garden growing inside an abandoned space station. Style: Tarkovsky.

**Shot List (excerpt):**
1. EWS — Slow drift past the derelict station exterior, debris floating in silence. 8s.
2. MS — Astronaut's gloved hand pushes open an airlock door, revealing green light spilling through. 5s.
3. WS — Interior cathedral of overgrown vines and flowers under broken skylights, dust motes in shafts of light. 10s.

**Keyframe Prompt (excerpt):**
> Wide shot interior of abandoned space station overtaken by lush green garden, broken skylights casting god rays through floating dust particles, vines climbing corroded metal walls, single astronaut in weathered spacesuit standing in awe, Tarkovsky-inspired long contemplative composition, natural diffused lighting, 35mm film grain, muted earth tones with vivid greens, spiritual atmosphere.

**Video Prompt (excerpt, Runway-optimized):**
> Slow dolly forward through overgrown space station interior, camera drifts past hanging vines and blooming flowers growing from cracked metal panels, dust particles float through shafts of natural light from broken ceiling, astronaut figure in mid-ground turns slowly to face camera, ambient atmospheric haze, cinematic 24fps, smooth continuous motion.

## References

- Source: [wuwangzhang1216/DirectorSKILL](https://github.com/wuwangzhang1216/DirectorSKILL)
- Compatible with: Runway, Kling, Google Veo, and other AI video generation platforms
