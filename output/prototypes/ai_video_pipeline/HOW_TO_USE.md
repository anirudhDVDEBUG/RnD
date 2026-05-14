# How to Use — AI Video Pipeline

## Install

```bash
cd ai_video_pipeline
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

System requirement: `ffmpeg` must be installed (`apt install ffmpeg` / `brew install ffmpeg`).

## Configure API Keys (optional for mock mode)

Create `.env` in the project root:

```env
GROQ_API_KEY=gsk_...        # free at https://console.groq.com
PEXELS_API_KEY=...           # free at https://www.pexels.com/api/
```

Edge-TTS requires no API key.

## Run

### Mock mode (no keys)

```bash
MOCK=1 python3 pipeline.py "Quantum Computing" 3
# or simply:
bash run.sh
```

### Live mode

```bash
python3 pipeline.py "The History of Space Exploration" 5
```

### CLI Arguments

```
python3 pipeline.py <topic> [num_scenes]
```

| Arg | Default | Description |
|-----|---------|-------------|
| `topic` | "The Future of Artificial Intelligence" | Video subject |
| `num_scenes` | 3 | Number of scenes |

### Environment Variables

| Var | Default | Description |
|-----|---------|-------------|
| `MOCK` | `0` | Set to `1` to skip real API calls |
| `OUTPUT_DIR` | `output` | Where generated assets go |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model ID |

## First 60 Seconds

```
$ bash run.sh

=== AI Video Pipeline — Demo ===

Creating virtual environment...
Installing dependencies...

=== AI Video Pipeline ===
Topic: The Future of Artificial Intelligence
Scenes: 3
Mode: MOCK (no API keys)

--- Step 1: Script Generation ---
  Scene 1: Welcome to our exploration of The Future of Artificial Intelligence...
  Scene 2: Experts predict that The Future of Artificial Intelligence will trans...
  Scene 3: In conclusion, The Future of Artificial Intelligence represents one ...

--- Step 2: Image Sourcing ---
[MOCK] Creating placeholder image for: The Future of Artificial Intelligence futuristic concept
[MOCK] Creating placeholder image for: The Future of Artificial Intelligence technology innovation
[MOCK] Creating placeholder image for: The Future of Artificial Intelligence future vision

--- Step 3: Voiceover Generation ---
[MOCK] Generating silent audio for scene (136 chars)
[MOCK] Generating silent audio for scene (138 chars)
[MOCK] Generating silent audio for scene (143 chars)

--- Step 4: Video Assembly ---
Video saved to: output/final_video.mp4

=== Pipeline Complete ===
Output directory: output/
  audio_0.wav                       516.2 KB
  audio_1.wav                       541.0 KB
  audio_2.wav                       560.6 KB
  final_video.mp4                    <size> KB
  image_0.jpg                        <size> KB
  image_1.jpg                        <size> KB
  image_2.jpg                        <size> KB
```

Output: a playable `output/final_video.mp4` with colored placeholder slides and silent audio. In live mode, you get real Pexels imagery and Edge-TTS narration.

## Using as a Claude Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/ai_video_pipeline
cp SKILL.md ~/.claude/skills/ai_video_pipeline/SKILL.md
```

**Trigger phrases:**
- "Generate a video from a topic"
- "Build an automated text-to-video pipeline"
- "Create a video with voiceover from a script"
- "Set up script-to-video automation with Groq"

Claude will scaffold the pipeline code and walk you through API key setup.
