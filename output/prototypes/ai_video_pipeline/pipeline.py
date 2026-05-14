"""
AI Video Pipeline — script → images → voiceover → video.

Uses Groq (LLM), Pexels (images), Edge-TTS (voiceover), MoviePy (assembly).
Set MOCK=1 to run without API keys using synthetic data.
"""

import os
import sys
import json
import asyncio
import textwrap
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MOCK = os.getenv("MOCK", "0") == "1"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Step 1: Script generation (Groq LLM or mock)
# ---------------------------------------------------------------------------

def generate_script(topic: str, num_scenes: int = 3) -> list[dict]:
    """Return list of dicts with 'narration' and 'visual' keys."""
    if MOCK:
        print(f"[MOCK] Generating {num_scenes}-scene script for: {topic}")
        scenes = []
        mock_data = [
            {"narration": f"Welcome to our exploration of {topic}. This fascinating subject is reshaping how we think about the future.",
             "visual": f"{topic} futuristic concept"},
            {"narration": f"Experts predict that {topic} will transform industries ranging from healthcare to transportation within the next decade.",
             "visual": f"{topic} technology innovation"},
            {"narration": f"In conclusion, {topic} represents one of the most exciting frontiers of human progress. The journey has only just begun.",
             "visual": f"{topic} future vision"},
        ]
        for i in range(min(num_scenes, len(mock_data))):
            scenes.append(mock_data[i])
        return scenes

    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[{
            "role": "user",
            "content": (
                f"Write a {num_scenes}-scene video script about '{topic}'. "
                f"Return a JSON object with a 'scenes' key containing an array of objects, "
                f"each with 'narration' (spoken text) and 'visual' (image search query) keys."
            ),
        }],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)["scenes"]


# ---------------------------------------------------------------------------
# Step 2: Image sourcing (Pexels or mock)
# ---------------------------------------------------------------------------

def fetch_image(query: str, output_path: Path) -> Path:
    """Download a stock image from Pexels, or generate a placeholder."""
    if MOCK:
        print(f"[MOCK] Creating placeholder image for: {query}")
        _create_placeholder_image(query, output_path)
        return output_path

    import requests
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    resp = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": 1},
    )
    resp.raise_for_status()
    photos = resp.json().get("photos", [])
    if not photos:
        print(f"[WARN] No Pexels results for '{query}', using placeholder")
        _create_placeholder_image(query, output_path)
        return output_path
    img_url = photos[0]["src"]["large2x"]
    img_data = requests.get(img_url).content
    with open(output_path, "wb") as f:
        f.write(img_data)
    return output_path


def _create_placeholder_image(text: str, output_path: Path, size=(1920, 1080)):
    """Generate a colored placeholder image with text."""
    from PIL import Image, ImageDraw, ImageFont
    import hashlib

    h = int(hashlib.md5(text.encode()).hexdigest()[:6], 16)
    r, g, b = (h >> 16) & 0xFF, (h >> 8) & 0xFF, h & 0xFF
    # Ensure readable contrast — darken the base colour
    bg = (r // 3 + 30, g // 3 + 30, b // 3 + 30)

    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except (OSError, IOError):
        font = ImageFont.load_default()

    wrapped = textwrap.fill(text, width=30)
    bbox = draw.textbbox((0, 0), wrapped, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size[0] - tw) // 2
    y = (size[1] - th) // 2
    draw.text((x, y), wrapped, fill=(255, 255, 255), font=font)
    img.save(output_path, "JPEG", quality=85)


# ---------------------------------------------------------------------------
# Step 3: Voiceover (Edge-TTS or mock)
# ---------------------------------------------------------------------------

async def generate_voiceover(text: str, output_path: Path, voice: str = "en-US-AriaNeural"):
    """Generate TTS audio file."""
    if MOCK:
        print(f"[MOCK] Generating silent audio for scene ({len(text)} chars)")
        _create_silent_audio(output_path, duration=max(3, len(text) / 15))
        return output_path

    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))
    return output_path


def _create_silent_audio(output_path: Path, duration: float = 5.0, sr: int = 22050):
    """Write a short silent WAV file as placeholder audio."""
    import wave
    import struct
    n_frames = int(sr * duration)
    with wave.open(str(output_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        # Write silence (zeros)
        wf.writeframes(struct.pack(f"<{n_frames}h", *([0] * n_frames)))


# ---------------------------------------------------------------------------
# Step 4: Video assembly (MoviePy)
# ---------------------------------------------------------------------------

def assemble_video(scenes: list[dict], output_path: Path):
    """Combine images + audio into a single MP4."""
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

    clips = []
    for i, scene in enumerate(scenes):
        audio_file = OUTPUT_DIR / f"audio_{i}.wav"
        image_file = OUTPUT_DIR / f"image_{i}.jpg"

        audio = AudioFileClip(str(audio_file))
        image = (
            ImageClip(str(image_file))
            .set_duration(audio.duration)
            .resize(height=720)
            .set_audio(audio)
        )
        clips.append(image)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger="bar",
    )
    final.close()
    for c in clips:
        c.close()
    print(f"\nVideo saved to: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(topic: str, num_scenes: int = 3):
    print(f"=== AI Video Pipeline ===")
    print(f"Topic: {topic}")
    print(f"Scenes: {num_scenes}")
    print(f"Mode: {'MOCK (no API keys)' if MOCK else 'LIVE'}")
    print()

    # 1. Generate script
    print("--- Step 1: Script Generation ---")
    scenes = generate_script(topic, num_scenes)
    for i, s in enumerate(scenes):
        print(f"  Scene {i+1}: {s['narration'][:80]}...")
    print()

    # 2. Fetch images
    print("--- Step 2: Image Sourcing ---")
    for i, scene in enumerate(scenes):
        fetch_image(scene["visual"], OUTPUT_DIR / f"image_{i}.jpg")
    print()

    # 3. Generate voiceover
    print("--- Step 3: Voiceover Generation ---")
    for i, scene in enumerate(scenes):
        asyncio.run(generate_voiceover(scene["narration"], OUTPUT_DIR / f"audio_{i}.wav"))
    print()

    # 4. Assemble video
    print("--- Step 4: Video Assembly ---")
    output_file = OUTPUT_DIR / "final_video.mp4"
    assemble_video(scenes, output_file)

    # Summary
    print(f"\n=== Pipeline Complete ===")
    print(f"Output directory: {OUTPUT_DIR}/")
    for f in sorted(OUTPUT_DIR.iterdir()):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name:30s} {size_kb:8.1f} KB")


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of Artificial Intelligence"
    num_scenes = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    run(topic, num_scenes)
