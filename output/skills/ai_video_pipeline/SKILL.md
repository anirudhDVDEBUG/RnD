---
name: ai_video_pipeline
description: |
  AI-powered video generation pipeline that automates script writing, image sourcing, voiceover generation, and video assembly using Groq, Pexels, Edge-TTS, and MoviePy. 100% free stack.
  Triggers: generate video from text, automated video pipeline, text to video with voiceover, AI video creation, script to video automation
---

# AI Video Pipeline

Fully automated video generation pipeline: script → images → voiceover → final video. Uses Groq (LLM for script), Pexels (stock footage/images), Edge-TTS (text-to-speech), and MoviePy (video assembly).

## When to use

- "Generate a video from a topic or script automatically"
- "Build an automated text-to-video pipeline with voiceover"
- "Create a video generation workflow using free AI tools"
- "Set up a script-to-video automation with Groq, Pexels, and Edge-TTS"
- "Produce narrated videos from text prompts programmatically"

## How to use

### 1. Project Setup

```bash
# Clone or scaffold the project
mkdir ai-video-pipeline && cd ai-video-pipeline
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install groq moviepy edge-tts requests python-dotenv Pillow
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here
```

- **Groq API Key**: Get one free at https://console.groq.com
- **Pexels API Key**: Get one free at https://www.pexels.com/api/
- **Edge-TTS**: No API key needed (uses Microsoft Edge's free TTS)

### 3. Pipeline Architecture

The pipeline runs in four stages:

1. **Script Generation** — Groq LLM generates a video script from your topic/prompt, broken into scenes with narration text and visual descriptions.
2. **Image/Video Sourcing** — Pexels API fetches relevant stock images or video clips matching each scene's visual description.
3. **Voiceover Generation** — Edge-TTS converts each scene's narration text into audio files (multiple voice options available).
4. **Video Assembly** — MoviePy composites images/clips with audio narration, adds transitions, and renders the final MP4.

### 4. Build the Pipeline

```python
import os
from dotenv import load_dotenv
from groq import Groq
import edge_tts
import requests
from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
)

load_dotenv()

# Step 1: Generate script with Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_script(topic: str, num_scenes: int = 5) -> list[dict]:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Write a {num_scenes}-scene video script about '{topic}'. "
                       f"Return JSON array with objects having 'narration' and 'visual' keys."
        }],
        response_format={"type": "json_object"}
    )
    import json
    return json.loads(response.choices[0].message.content)["scenes"]

# Step 2: Fetch images from Pexels
def fetch_image(query: str, output_path: str) -> str:
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    resp = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": 1}
    )
    img_url = resp.json()["photos"][0]["src"]["large2x"]
    img_data = requests.get(img_url).content
    with open(output_path, "wb") as f:
        f.write(img_data)
    return output_path

# Step 3: Generate voiceover with Edge-TTS
async def generate_voiceover(text: str, output_path: str, voice: str = "en-US-AriaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

# Step 4: Assemble video with MoviePy
def assemble_video(scenes: list[dict], output_path: str = "output.mp4"):
    clips = []
    for i, scene in enumerate(scenes):
        audio = AudioFileClip(f"audio_{i}.mp3")
        image = ImageClip(f"image_{i}.jpg").set_duration(audio.duration)
        image = image.resize(height=1080).set_audio(audio)
        clips.append(image)
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=24)
```

### 5. Run the Pipeline

```python
import asyncio

topic = "The Future of Artificial Intelligence"
scenes = generate_script(topic)

for i, scene in enumerate(scenes):
    fetch_image(scene["visual"], f"image_{i}.jpg")
    asyncio.run(generate_voiceover(scene["narration"], f"audio_{i}.mp3"))

assemble_video(scenes)
print("Video generated: output.mp4")
```

### Key Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `voice` | `en-US-AriaNeural` | Edge-TTS voice (run `edge-tts --list-voices` for options) |
| `model` | `llama-3.3-70b-versatile` | Groq model for script generation |
| `fps` | `24` | Output video frame rate |
| `num_scenes` | `5` | Number of scenes in generated script |

### Tips

- Use `edge-tts --list-voices` to browse available voices and languages
- Pexels free tier allows 200 requests/hour — sufficient for most pipelines
- For longer videos, increase `num_scenes` and consider adding transitions between clips
- Add subtitles using MoviePy's `TextClip` for better engagement
- Groq's free tier provides fast inference — ideal for rapid script iteration

## References

- **Source Repository**: https://github.com/MYounus-Codes/ai-video-pipeline
- **Groq Console**: https://console.groq.com
- **Pexels API**: https://www.pexels.com/api/
- **Edge-TTS**: https://pypi.org/project/edge-tts/
- **MoviePy**: https://zulko.github.io/moviepy/
