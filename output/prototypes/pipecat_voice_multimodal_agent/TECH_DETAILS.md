# Technical Details

## What Pipecat Does

Pipecat is an open-source Python framework for building real-time voice and multimodal conversational AI agents. It provides a pipeline abstraction where typed data units ("frames") flow through a sequence of processors — STT, LLM, TTS, vision, and transport services. The framework handles the hard parts of real-time AI: streaming audio over WebRTC, managing conversation context, supporting interruptions (barge-in), and coordinating multiple async services with sub-500ms end-to-end latency.

The project has 14k+ GitHub stars and is gaining ~100/day. It's backed by Daily.co (the WebRTC company) and has production deployments handling voice bots, phone agents, and multimodal assistants.

## Architecture

```
User's mic                                              User's speaker
    |                                                        ^
    v                                                        |
[Transport Input] -> [VAD] -> [STT] -> [LLM] -> [TTS] -> [Transport Output]
    (Daily WebRTC)   (Silero)  (Deepgram) (GPT-4o) (Cartesia)  (Daily WebRTC)
                                  |
                          [Context Aggregator]
                          (manages chat history)
```

### Key Files in pipecat-ai/pipecat

| Path | Purpose |
|------|---------|
| `src/pipecat/pipeline/pipeline.py` | Core pipeline that chains processors |
| `src/pipecat/pipeline/runner.py` | Runs pipeline tasks, manages lifecycle |
| `src/pipecat/frames/frames.py` | Frame type definitions (audio, text, image, control) |
| `src/pipecat/services/` | STT/LLM/TTS service integrations |
| `src/pipecat/transports/` | WebRTC (Daily), WebSocket, local transport |
| `src/pipecat/processors/aggregators/` | Context management for LLM conversations |

### Data Flow

1. **Transport** receives raw audio from WebRTC/WebSocket
2. **VAD** (Voice Activity Detection) detects speech segments
3. **STT** converts audio frames to text transcription frames
4. **Context Aggregator** appends user text to conversation history
5. **LLM** generates response text from conversation context
6. **TTS** converts response text to audio frames
7. **Transport** streams audio back to the user
8. **Context Aggregator** records assistant response in history

### Dependencies

- **Runtime:** Python 3.10+, asyncio-based
- **Transport:** `daily-python` (WebRTC), or `websockets`
- **Services:** Each provider requires its own SDK + API key
- **VAD:** `silero-vad` (PyTorch-based, runs locally)

### Model Calls

In a typical pipeline, each user turn makes:
- 1 STT API call (streaming, Deepgram/Whisper)
- 1 LLM API call (streaming, OpenAI/Anthropic/Gemini)
- 1 TTS API call (streaming, Cartesia/ElevenLabs)

All calls are streaming — responses start before the full input is processed.

## Limitations

- **Transport lock-in:** WebRTC transport is tightly coupled to Daily.co. Self-hosted WebRTC requires a Daily account or writing a custom transport.
- **Python only:** No official Node.js/TypeScript SDK (though there's a separate `pipecat-js` client library).
- **Latency floor:** End-to-end latency depends on the slowest service in the chain. STT and TTS each add 100-300ms.
- **No built-in telephony:** Phone call support requires integrating Twilio or Daily SIP separately.
- **Cost:** Real-time voice AI requires paid APIs for STT, LLM, and TTS. A single conversation can cost $0.05-0.50 depending on services and duration.
- **No offline mode:** All AI services require network connectivity (except local Whisper/XTTS).

## Why It Matters for Claude-Driven Products

**Voice AI agents:** Pipecat supports Anthropic Claude as a drop-in LLM. Build voice assistants powered by Claude with `pip install "pipecat-ai[anthropic]"` — same pipeline, just swap `OpenAILLMService` for `AnthropicLLMService`.

**Agent factories:** Pipecat's modular pipeline maps directly to agent factory patterns — define a pipeline template, parameterize the system prompt and services, and spawn instances per customer/use-case.

**Lead-gen & phone bots:** Combine with Twilio/Daily SIP for outbound/inbound phone agents. The interruption handling and context management are production-ready for sales qualification and support triage.

**Multimodal:** Vision processors (OpenAI Vision, Gemini) can be added to the pipeline for camera-aware agents — useful for product demos, visual Q&A, and interactive marketing experiences.
