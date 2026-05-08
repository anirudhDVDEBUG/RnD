# Technical Details

## What It Does

OpenAI's Realtime API provides a persistent WebSocket connection for speech-to-speech AI interactions. Unlike the standard Chat Completions API (which handles text), the Realtime API accepts streaming PCM16 audio input and returns streaming audio + text output simultaneously. The models (`gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`) can reason over spoken content before responding, enabling voice agents that understand context, translate between languages, and call external functions — all with sub-second latency.

This prototype implements the complete client-server event protocol locally using a mock server, demonstrating every major feature without requiring an API key or network access.

## Architecture

### Files

| File | Role |
|---|---|
| `mock_server.js` | WebSocket server that mimics the OpenAI Realtime API event protocol |
| `client.js` | Realtime API client demonstrating 5 features end-to-end |
| `run_demo.js` | Orchestrator — starts server, runs client, exits cleanly |
| `run.sh` | Entry point — installs deps and runs the demo |
| `package.json` | Single dependency: `ws` (WebSocket library) |

### Data Flow

```
┌─────────┐   WebSocket    ┌──────────────┐
│ client.js│ ──────────────→│ mock_server.js│
│          │                │              │
│ 1. Open  │←── session.    │ Creates      │
│          │    created     │ session obj   │
│          │                │              │
│ 2. Send  │──→ session.    │ Updates      │
│   config │    update      │ config       │
│          │←── session.    │              │
│          │    updated     │              │
│          │                │              │
│ 3. Send  │──→ input_audio │ Buffers      │
│   audio  │    _buffer.    │ audio data   │
│   chunks │    append      │              │
│          │                │              │
│ 4. Commit│──→ input_audio │ Processes    │
│   buffer │    _buffer.    │ (VAD + model)│
│          │    commit      │              │
│          │                │              │
│ 5. Recv  │←── response.   │ Streams back │
│   stream │    audio_      │ transcript + │
│          │    transcript. │ audio deltas │
│          │    delta       │              │
│          │←── response.   │              │
│          │    audio.delta │              │
│          │←── response.   │              │
│          │    done        │              │
└─────────┘                └──────────────┘
```

### Key Event Types

| Client → Server | Description |
|---|---|
| `session.update` | Configure voice, modalities, tools, transcription |
| `input_audio_buffer.append` | Stream base64 PCM16 audio chunks |
| `input_audio_buffer.commit` | Signal end of speech (or rely on server VAD) |
| `response.create` | Manually trigger a response |

| Server → Client | Description |
|---|---|
| `session.created` | Session established with ID and config |
| `response.audio_transcript.delta` | Streamed transcript word-by-word |
| `response.audio.delta` | Streamed audio (base64 PCM16) |
| `response.function_call_arguments.done` | Tool call with parsed arguments |
| `response.done` | Response complete with usage stats |

### Dependencies

- **`ws`** (v8.16+) — WebSocket client/server for Node.js. Zero transitive dependencies.
- **Node.js 18+** — For stable WebSocket and Buffer APIs.

No other dependencies. No build step. No bundler.

## Limitations

- **Mock only**: The mock server returns canned responses; it does not run speech recognition or synthesis. Replace `ws://localhost:8765` with `wss://api.openai.com/v1/realtime` and add auth headers for real usage.
- **No real audio I/O**: The demo sends synthetic PCM16 buffers. A production app would capture microphone input via Web Audio API or `node-record-lpcm16`.
- **No speaker output**: Received audio deltas are measured but not played. A production client would pipe them to a speaker/audio sink.
- **Single-turn flow**: Each demo step is sequential. Real conversations would overlap input/output with continuous VAD-driven turns.
- **No error recovery**: The demo doesn't handle reconnection, rate limits, or partial failures.
- **Auth headers not wired**: Connecting to the real API requires adding `Authorization` and `OpenAI-Beta` headers to the WebSocket handshake — shown in SKILL.md but not in this mock-targeting client.

## Why This Matters

### For voice AI products
The Realtime API eliminates the traditional STT → LLM → TTS pipeline, replacing three API calls with a single streaming connection. This cuts latency from 2-4 seconds to under 500ms, which is the threshold for natural conversation.

### For Claude-driven agent factories
Voice is the next frontier for AI agents. A Claude-based orchestrator could use OpenAI's Realtime API as a voice frontend while routing complex reasoning to Claude. The function-calling capability means the voice model can trigger Claude-powered tools mid-conversation.

### For marketing and lead-gen
Voice bots that respond in real-time with natural speech convert better than text chatbots. The translation feature enables multilingual lead capture without separate models per language.

### Competitive context
This API launched alongside OpenAI's push into voice intelligence (May 2025). The models can now reason over speech — not just transcribe-then-think — which is a qualitative leap over previous voice APIs. Understanding this protocol is essential for anyone building in the voice AI space.

## References

- [Advancing voice intelligence with new models in the API](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api)
- [OpenAI Realtime API Guide](https://platform.openai.com/docs/guides/realtime)
- [OpenAI Realtime API Reference](https://platform.openai.com/docs/api-reference/realtime)
