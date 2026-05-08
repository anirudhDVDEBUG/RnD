# OpenAI Realtime Voice Models — Prototype

**TL;DR:** OpenAI's Realtime API lets you build speech-to-speech voice applications with sub-second latency, live translation, real-time transcription, and voice-triggered function calling — all over a single WebSocket connection. This prototype demonstrates the full API flow locally with a mock server (no API key needed).

## Headline Result

```
STEP 4: Translation Mode (English → Spanish)
  [00:00.123] Mode: Translation (EN → ES)
  [00:00.456] Translated output: "Traduccion en tiempo real completada."

STEP 5: Function Calling (Voice Agent)
  [00:00.789] Function called: get_weather({"location":"San Francisco"})
```

**Five features in one WebSocket session** — streaming audio, VAD turn detection, Whisper transcription, live translation, and tool-use — running end-to-end in under 2 seconds.

## Quick Start

```bash
bash run.sh
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) — Setup, installation, trigger phrases, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations, relevance
