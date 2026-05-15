---
name: video_production_toolkit
description: |
  Video production toolkit with 13 skills for transcription, translation, dubbing, multicam editing, subtitles, reframing, and WeChat publishing. Uses ffmpeg and Whisper for processing.
  Triggers: transcribe video, translate video, dub video, add subtitles, multicam edit, reframe video, publish to WeChat, video production pipeline, generate subtitles from audio, create dubbed version
---

# Video Production Toolkit

A comprehensive set of video production skills covering the full pipeline from transcription to publishing. Based on [jianshuo/claude-skills](https://github.com/jianshuo/claude-skills).

## When to use

- "Transcribe this video and generate subtitles"
- "Translate and dub this video into Chinese/English"
- "Create a multicam edit from these video files"
- "Reframe this video for vertical/portrait format"
- "Publish this video to WeChat with subtitles"

## How to use

### Prerequisites

Ensure the following are installed:

```bash
# ffmpeg for video/audio processing
brew install ffmpeg   # macOS
sudo apt install ffmpeg  # Linux

# Python dependencies
pip install openai-whisper   # For transcription
pip install deep-translator  # For translation
pip install pydub             # For audio manipulation
```

### Available Skills

1. **Transcribe** - Extract speech from video/audio files using Whisper. Outputs SRT/VTT subtitle files.
2. **Translate** - Translate subtitle files or transcriptions between languages.
3. **Dub** - Generate dubbed audio tracks in target languages and merge with original video.
4. **Subtitles** - Burn subtitles into video or generate standalone subtitle files (SRT, VTT, ASS).
5. **Multicam** - Combine multiple camera angles into a single multicam edit with automatic or manual switching.
6. **Reframe** - Reframe horizontal (16:9) video to vertical (9:16) or square (1:1) for social platforms.
7. **WeChat Publishing** - Prepare and format video content for WeChat article or video channel publishing.

### Steps

1. **Transcribe a video:**
   ```
   Transcribe the video at ./input/talk.mp4 and output subtitles as SRT
   ```
   The agent will use Whisper to detect speech, generate timestamps, and write an SRT file.

2. **Translate subtitles:**
   ```
   Translate ./output/talk.srt from English to Chinese
   ```
   Produces a translated subtitle file preserving original timing.

3. **Dub a video:**
   ```
   Dub ./input/talk.mp4 into Mandarin Chinese
   ```
   Generates synthesized speech in the target language and mixes it with the original video.

4. **Add subtitles to video:**
   ```
   Burn Chinese subtitles from ./output/talk_zh.srt into ./input/talk.mp4
   ```
   Uses ffmpeg to hardcode subtitles into the video file.

5. **Multicam edit:**
   ```
   Create a multicam edit from camera1.mp4, camera2.mp4, and camera3.mp4
   ```
   Synchronizes and combines multiple camera angles.

6. **Reframe for social media:**
   ```
   Reframe ./input/talk.mp4 to 9:16 vertical format for TikTok
   ```
   Intelligently crops and reframes video to target aspect ratio using speaker/subject detection.

7. **Publish to WeChat:**
   ```
   Prepare ./input/talk.mp4 for WeChat publishing with Chinese subtitles
   ```
   Formats video and generates metadata suitable for WeChat channels.

### Key ffmpeg patterns used

```bash
# Burn subtitles into video
ffmpeg -i input.mp4 -vf subtitles=subs.srt output.mp4

# Extract audio for transcription
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav

# Reframe to vertical (9:16)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih" -c:a copy output_vertical.mp4

# Merge dubbed audio with video
ffmpeg -i video.mp4 -i dubbed_audio.wav -c:v copy -map 0:v -map 1:a output.mp4
```

## References

- Source repository: [jianshuo/claude-skills](https://github.com/jianshuo/claude-skills)
- [ffmpeg documentation](https://ffmpeg.org/documentation.html)
- [OpenAI Whisper](https://github.com/openai/whisper)
