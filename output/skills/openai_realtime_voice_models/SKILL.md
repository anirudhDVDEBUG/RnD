---
name: openai_realtime_voice_models
description: |
  Build voice-powered applications using OpenAI's advanced Realtime API voice models (gpt-4o-mini-realtime, gpt-4o-realtime) that support speech-to-speech reasoning, live translation, and transcription.
  Triggers: openai realtime api, voice intelligence, speech-to-speech, realtime voice model, voice translation api
---

# OpenAI Realtime Voice Models

Build intelligent voice experiences using OpenAI's Realtime API with models that can reason over speech, translate between languages, and transcribe audio in real time.

## When to use

- "Build a voice assistant using OpenAI's Realtime API"
- "Add live speech translation to my app"
- "Set up real-time speech-to-speech with reasoning capabilities"
- "Transcribe audio using OpenAI's latest voice models"
- "Create a multilingual voice interface with OpenAI"

## How to use

### 1. Choose the right model

| Model | Best for |
|---|---|
| `gpt-4o-realtime-preview` | Full-featured voice with reasoning, function calling |
| `gpt-4o-mini-realtime-preview` | Cost-efficient real-time voice tasks |

### 2. Set up a Realtime API session

Connect via WebSocket to the Realtime API endpoint:

```javascript
const ws = new WebSocket(
  "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview",
  {
    headers: {
      "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
      "OpenAI-Beta": "realtime=v1",
    },
  }
);

ws.on("open", () => {
  // Configure the session
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      modalities: ["text", "audio"],
      voice: "alloy",
      input_audio_format: "pcm16",
      output_audio_format: "pcm16",
      turn_detection: { type: "server_vad" },
    },
  }));
});
```

### 3. Stream audio input

Send audio chunks as base64-encoded PCM16 data:

```javascript
ws.send(JSON.stringify({
  type: "input_audio_buffer.append",
  audio: base64AudioChunk,
}));
```

### 4. Handle responses

Listen for audio and transcript deltas:

```javascript
ws.on("message", (data) => {
  const event = JSON.parse(data);
  switch (event.type) {
    case "response.audio.delta":
      // Play back audio: event.delta (base64 PCM16)
      break;
    case "response.audio_transcript.delta":
      // Display transcript: event.delta
      break;
    case "response.done":
      // Response complete
      break;
  }
});
```

### 5. Enable translation or transcription

For **live translation**, set instructions in the session config:

```javascript
ws.send(JSON.stringify({
  type: "session.update",
  session: {
    instructions: "You are a real-time translator. Listen to the user's speech and translate it to Spanish, responding in spoken Spanish.",
    modalities: ["text", "audio"],
  },
}));
```

For **transcription**, use the `input_audio_transcription` config:

```javascript
ws.send(JSON.stringify({
  type: "session.update",
  session: {
    input_audio_transcription: { model: "whisper-1" },
  },
}));
```

### 6. Add function calling for voice agents

```javascript
ws.send(JSON.stringify({
  type: "session.update",
  session: {
    tools: [
      {
        type: "function",
        name: "get_weather",
        description: "Get current weather for a location",
        parameters: {
          type: "object",
          properties: {
            location: { type: "string" },
          },
          required: ["location"],
        },
      },
    ],
  },
}));
```

### Key considerations

- **Audio format**: Use PCM16 at 24kHz sample rate for best quality
- **Voice options**: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`
- **Turn detection**: Server-side VAD handles conversation turn-taking automatically
- **Reasoning**: The realtime models can reason over spoken content before responding, enabling more thoughtful voice interactions
- **Latency**: Responses stream back in real time with sub-second latency

## References

- [Advancing voice intelligence with new models in the API](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api)
- [OpenAI Realtime API Documentation](https://platform.openai.com/docs/guides/realtime)
- [OpenAI API Reference — Realtime](https://platform.openai.com/docs/api-reference/realtime)
