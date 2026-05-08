# How to Use

## Installation

```bash
# Clone or navigate to this directory
cd openai_realtime_voice_models

# Install dependencies (only `ws` WebSocket library)
npm install

# Run the full demo (mock server + client)
bash run.sh
```

**Requirements:** Node.js 18+ (uses native `WebSocket` events via the `ws` package).

## This is a Claude Code SKILL

### Where to install

```bash
mkdir -p ~/.claude/skills/openai_realtime_voice_models
cp SKILL.md ~/.claude/skills/openai_realtime_voice_models/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code and the skill activates:

- "Build a voice assistant using OpenAI's Realtime API"
- "Add live speech translation to my app"
- "Set up real-time speech-to-speech with reasoning capabilities"
- "Transcribe audio using OpenAI's latest voice models"
- "Create a multilingual voice interface with OpenAI"

Keywords: `openai realtime api`, `voice intelligence`, `speech-to-speech`, `realtime voice model`, `voice translation api`

## First 60 Seconds

### Input

```bash
bash run.sh
```

### Output

```
=== Installing dependencies ===
added 1 package in 0.5s

=== Running OpenAI Realtime Voice API Demo ===

[Mock Realtime API] Listening on ws://localhost:8765
[Mock Realtime API] Simulating model: gpt-4o-realtime-preview

────────────────────────────────────────────────────────────
  OpenAI Realtime Voice API — Interactive Demo
────────────────────────────────────────────────────────────
  Endpoint : ws://localhost:8765
  Model    : gpt-4o-realtime-preview
────────────────────────────────────────────────────────────

STEP 1: Session Created
  [00:00.001] Session ID: sess_1715100000000
  [00:00.001] Model: gpt-4o-realtime-preview

STEP 2: Configure Session (voice + transcription)
  [00:00.002] Voice: alloy
  [00:00.002] Transcription: enabled (whisper-1)
  [00:00.002] Turn detection: server_vad

STEP 3: Stream Audio & Get Response
  [00:00.003] Sending: 3 audio chunks (simulated speech)
  [00:00.004] Input transcription: "User said something interesting."
  [00:00.004] Response transcript: "Hello, how can I help you today?"
  [00:00.004] Audio received: 15680 bytes PCM16

STEP 4: Translation Mode (English → Spanish)
  [00:00.005] Mode: Translation (EN → ES)
  [00:00.006] Translated output: "Traduccion en tiempo real completada."

STEP 5: Function Calling (Voice Agent)
  [00:00.007] Tools registered: get_weather
  [00:00.008] Function called: get_weather({"location":"San Francisco"})
  [00:00.008] Agent response: "The weather in San Francisco is..."

────────────────────────────────────────────────────────────
  SUMMARY
────────────────────────────────────────────────────────────
  Features demonstrated:
    1. WebSocket session lifecycle (create → configure → use)
    2. Streaming audio input with server-side VAD
    3. Real-time speech transcription (Whisper)
    4. Speech-to-speech translation (EN → ES)
    5. Voice-triggered function calling (tool use)

  To use with real OpenAI API:
    export OPENAI_API_KEY=sk-...
    export REALTIME_API_URL=wss://api.openai.com/v1/realtime
────────────────────────────────────────────────────────────
```

## Connecting to the Real OpenAI API

```bash
export OPENAI_API_KEY=sk-your-key-here
export REALTIME_API_URL=wss://api.openai.com/v1/realtime
export REALTIME_MODEL=gpt-4o-realtime-preview
node client.js
```

Note: The real API requires WebSocket headers (`Authorization`, `OpenAI-Beta`) which the `ws` library supports. The client would need a small modification to add auth headers — see the SKILL.md for the exact header format.

## Model Selection

| Model | Use case | Pricing tier |
|---|---|---|
| `gpt-4o-realtime-preview` | Full voice reasoning, function calling, complex tasks | Higher |
| `gpt-4o-mini-realtime-preview` | Cost-efficient voice tasks, simple Q&A | Lower |
