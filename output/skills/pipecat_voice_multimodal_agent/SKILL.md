---
name: pipecat_voice_multimodal_agent
description: |
  Build real-time voice and multimodal conversational AI agents using the Pipecat framework.
  TRIGGER: user wants to build a voice bot, real-time conversational AI, voice assistant,
  multimodal agent pipeline, or mentions pipecat.
---

# Pipecat Voice & Multimodal Agent

Build real-time voice and multimodal conversational AI applications using the open-source Pipecat framework.

## When to use

- "Build a voice assistant using pipecat"
- "Create a real-time conversational AI bot"
- "Set up a multimodal agent with speech-to-text and TTS"
- "How do I create a voice pipeline with pipecat?"
- "Build a phone call bot with AI responses"

## How to use

### 1. Install Pipecat

```bash
pip install pipecat-ai
# Install with specific service extras as needed:
pip install "pipecat-ai[daily,openai,deepgram,cartesia,silero]"
```

### 2. Core Concepts

Pipecat uses a **pipeline** architecture with **frames** flowing through **processors**:

- **Frames**: Units of data (audio, text, images) that flow through the pipeline
- **Processors/Services**: Transform frames (STT, LLM, TTS, transport)
- **Pipeline**: Connects processors in sequence to build a conversation flow
- **Transport**: Handles real-time audio/video I/O (e.g., Daily.co WebRTC, WebSocket)

### 3. Basic Voice Agent Example

```python
import asyncio
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.transports.services.daily import DailyTransport, DailyParams
from pipecat.services.openai import OpenAILLMService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext

async def main():
    # Transport (WebRTC via Daily)
    transport = DailyTransport(
        room_url="YOUR_DAILY_ROOM_URL",
        token="YOUR_TOKEN",
        bot_name="My Bot",
        params=DailyParams(audio_out_enabled=True)
    )

    # Speech-to-Text
    stt = DeepgramSTTService(api_key="YOUR_DEEPGRAM_KEY")

    # LLM
    llm = OpenAILLMService(api_key="YOUR_OPENAI_KEY", model="gpt-4o")

    # Text-to-Speech
    tts = CartesiaTTSService(
        api_key="YOUR_CARTESIA_KEY",
        voice_id="YOUR_VOICE_ID"
    )

    # Conversation context
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    context = OpenAILLMContext(messages)
    context_aggregator = llm.create_context_aggregator(context)

    # Build pipeline
    pipeline = Pipeline([
        transport.input(),
        stt,
        context_aggregator.user(),
        llm,
        tts,
        transport.output(),
        context_aggregator.assistant()
    ])

    # Run
    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))
    runner = PipelineRunner()

    @transport.event_handler("on_first_participant_joined")
    async def on_joined(transport, participant):
        await task.queue_frames([context_aggregator.user().get_context_frame()])

    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Key Services & Integrations

| Category | Services |
|----------|----------|
| **Transport** | Daily (WebRTC), WebSocket, Local |
| **STT** | Deepgram, Whisper, Azure, AssemblyAI, Gladia |
| **LLM** | OpenAI, Anthropic, Google Gemini, Together, Fireworks |
| **TTS** | Cartesia, ElevenLabs, Azure, PlayHT, LMNT, XTTS |
| **Image** | DALL-E, Fal, Stability |
| **Vision** | OpenAI Vision, Google Gemini, Moondream |

### 5. Advanced Patterns

- **Function calling**: Register tools on the LLM service for agentic behavior
- **Interruptions**: Set `allow_interruptions=True` in PipelineParams for natural conversation
- **VAD (Voice Activity Detection)**: Use Silero VAD for accurate speech detection
- **Multi-modal**: Combine vision + voice for camera-aware assistants
- **Telephony**: Integrate with Twilio or Daily SIP for phone bots

### 6. Project Structure

```
my-voice-bot/
├── bot.py              # Main pipeline definition
├── requirements.txt    # pipecat-ai[daily,openai,deepgram,cartesia,silero]
├── .env                # API keys
└── runner.py           # Optional: HTTP server to spawn bots
```

## References

- **Repository**: https://github.com/pipecat-ai/pipecat
- **Documentation**: https://docs.pipecat.ai
- **Examples**: https://github.com/pipecat-ai/pipecat/tree/main/examples
