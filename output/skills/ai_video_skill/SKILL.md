---
name: AI Video Skill
description: |
  End-to-end AI video generation across 6 models (Seedance 2.0, Kling, Wan, Veo, OmniHuman) with a self-improving quality-control loop.
  Triggers: "generate a video", "text to video", "image to video", "create video from prompt", "video generation with AI"
---

# AI Video Skill

Generate AI videos end-to-end using multiple state-of-the-art models with an integrated quality-control feedback loop that learns and improves over time.

## When to use

- "Generate a video from this text prompt"
- "Convert this image to a video using Seedance"
- "Create a text-to-video clip with Kling"
- "Generate a video and evaluate its quality"
- "Make an AI video of a person talking using OmniHuman"

## Supported Models

| Model | Type | Best For |
|-------|------|----------|
| **Seedance 2.0** | Text-to-video, Image-to-video | High-quality motion, dance/movement |
| **Kling** | Text-to-video, Image-to-video | General-purpose video generation |
| **Wan** | Text-to-video | Creative/artistic video generation |
| **Veo** | Text-to-video | Photorealistic video generation |
| **OmniHuman** | Image-to-video | Human animation, talking heads |

## How to use

### 1. Setup

Ensure the required API keys are configured as environment variables for the model providers you intend to use. Check the project's configuration files for the specific variable names required by each provider.

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Generate a Video

Choose a model and generation mode based on your needs:

- **Text-to-video**: Provide a text prompt describing the desired video.
- **Image-to-video**: Provide a source image plus an optional motion/style prompt.

The skill will:
1. Parse your prompt and select the appropriate model (or use the one you specify).
2. Submit the generation request to the provider API.
3. Poll for completion and download the result.
4. Run the **quality-control loop** — evaluate the output against criteria (motion coherence, prompt adherence, visual fidelity).
5. If quality falls below threshold, automatically refine the prompt and re-generate (self-improving loop).
6. Return the final video file path.

### 3. Quality-Control Loop

The skill includes a self-improving feedback mechanism:
- Each generated video is scored on multiple quality dimensions.
- If the score is below the acceptance threshold, the skill rewrites the prompt incorporating lessons from the failure.
- History of successful prompt patterns is retained to improve future generations.
- This loop runs up to a configurable maximum number of iterations.

### 4. Model Selection Tips

- Use **Seedance 2.0** for dynamic movement and dance sequences.
- Use **Kling** for versatile general-purpose generation.
- Use **OmniHuman** when animating a still photo of a person.
- Use **Veo** for photorealistic output.
- Use **Wan** for stylized or artistic content.

## References

- Source repository: [0xadvait/ai-video-skill](https://github.com/0xadvait/ai-video-skill)
- Topics: ai-video, claude-code, claude-skill, generative-ai, image-to-video, seedance, text-to-video, video-generation
