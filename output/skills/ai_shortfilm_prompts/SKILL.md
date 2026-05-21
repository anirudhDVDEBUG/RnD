---
name: ai_shortfilm_prompts
description: |
  AI short film production skill — methodology, prompt engineering, and structured workflows for creating cinematic AI-generated short films using video generation models (Sora, Kling, Veo, Seedance, Jimeng). Based on the approach behind "Zombie Scavenger" by Mx-Shell.
  Triggers: ai short film, video generation prompts, cinematic AI video, shortfilm workflow, sora kling veo seedance prompts
---

# AI Short Film Prompts

A structured methodology and prompt engineering skill for producing AI-generated short films using state-of-the-art video generation models. Based on the production approach behind *Zombie Scavenger* by Mx-Shell.

## When to use

- "Help me plan and write prompts for an AI short film"
- "Generate cinematic video prompts for Sora / Kling / Veo / Seedance"
- "I want to create an AI-generated short film with a coherent narrative"
- "Write scene-by-scene video generation prompts for my story concept"
- "Help me produce a short film using AI video tools"

## How to use

### Phase 1: Story & Script Development

1. **Define the concept**: Establish genre, tone, setting, and core narrative arc. Keep the story concise — AI short films work best at 1-5 minutes.
2. **Write a beat sheet**: Break the story into 8-15 key narrative beats (setup, inciting incident, rising action, climax, resolution).
3. **Create a scene list**: Convert beats into discrete scenes, each 5-15 seconds of generated video. Note the target shot count.

### Phase 2: Visual Direction & Shot Design

4. **Establish visual style**: Define a consistent style guide — color palette, lighting mood, camera language, aspect ratio (16:9 for cinematic). Reference real cinematography terms (e.g., Dutch angle, rack focus, dolly zoom).
5. **Design character consistency**: Write detailed character descriptions (appearance, clothing, posture) to reuse across prompts for visual continuity.
6. **Plan shot types**: For each scene, specify shot type (wide establishing, medium, close-up, POV, over-the-shoulder) and camera movement (pan, tilt, tracking, static).

### Phase 3: Prompt Engineering for Video Generation

7. **Structure each prompt** with these components:
   - **Scene context**: Brief narrative context (not included in the generation prompt itself, but used for planning)
   - **Visual description**: Detailed, concrete imagery — what is visible in the frame
   - **Camera direction**: Shot type, movement, angle
   - **Lighting & atmosphere**: Time of day, weather, mood lighting
   - **Style modifiers**: Cinematic quality keywords tuned to the target model

8. **Model-specific optimization**:
   - **Sora**: Emphasize photorealistic detail, physical accuracy, and camera movement descriptions. Use natural language scene descriptions.
   - **Kling (Kuaishou)**: Strong with character motion and action sequences. Specify motion dynamics explicitly.
   - **Veo (Google)**: Excels at cinematic compositions. Leverage detailed cinematography language.
   - **Seedance (Seed)**: Good for stylized and dance/movement content. Describe rhythm and flow.
   - **Jimeng (ByteDance)**: Supports Chinese-language prompts. Strong with Asian aesthetic styles and character generation.

9. **Prompt template**:

```
[Shot type], [camera movement]. [Subject description] in [setting/environment].
[Action/motion description]. [Lighting conditions], [atmosphere/mood].
[Style keywords: cinematic, photorealistic, 4K, shallow depth of field, etc.]
```

**Example**:
```
Medium close-up, slow push-in. A weary survivor in a torn military jacket
crouches behind an overturned car in a deserted urban street. She peers
through a cracked car window, breath visible in the cold air. Overcast
daylight, muted desaturated tones, volumetric fog. Cinematic, photorealistic,
anamorphic lens flare, shallow depth of field, 4K.
```

### Phase 4: Production & Assembly

10. **Generate in batches**: Produce multiple variations of each shot and select the best takes.
11. **Maintain continuity**: Cross-reference character descriptions and environment details between shots.
12. **Sequence and edit**: Arrange generated clips following the beat sheet. Note where transitions (cuts, dissolves, fade-to-black) should occur.
13. **Audio direction**: Plan sound design, music cues, and any dialogue/voiceover to pair with the visual edit.

### Output Format

When generating prompts for the user, output a structured document:

```markdown
# [Film Title] — AI Video Generation Prompts

## Style Guide
- Visual style: [description]
- Color palette: [description]
- Aspect ratio: [16:9 / 9:16 / etc.]
- Target model: [Sora / Kling / Veo / Seedance / Jimeng]

## Character Reference
- [Character name]: [Detailed visual description]

## Scene [N]: [Scene Title]
**Narrative beat**: [What happens in the story]
**Duration**: [Estimated seconds]

### Shot [N.1]
- Type: [Shot type + camera movement]
- Prompt: [Full generation prompt]

### Shot [N.2]
- Type: [Shot type + camera movement]
- Prompt: [Full generation prompt]
```

## Tips

- Keep individual shots under 10 seconds for best quality across all models
- Use consistent character descriptions verbatim across all prompts for continuity
- Avoid abstract or metaphorical language — video models respond to concrete visual descriptions
- Specify what is IN the frame, not what is absent
- For action sequences, describe the motion frame-by-frame rather than summarizing
- Test prompts with cheaper/faster models first, then refine for hero shots on premium models
- Chinese-language prompts can be used directly with Jimeng and Kling for potentially better results

## References

- Source repository: https://github.com/jnMetaCode/ai-shortfilm-prompts
- Based on the production methodology behind *Zombie Scavenger* by Mx-Shell
- Supports: Sora, Kling, Veo, Seedance, Jimeng
