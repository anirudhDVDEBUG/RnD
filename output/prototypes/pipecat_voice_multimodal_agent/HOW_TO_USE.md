# How to Use

## Run the Demo (no API keys)

```bash
cd pipecat_voice_multimodal_agent
bash run.sh
```

Requires only Python 3.10+. No pip install needed — the demo uses mock services to show the full pipeline architecture.

## Install Pipecat for Production

```bash
pip install "pipecat-ai[daily,openai,deepgram,cartesia,silero]"
```

Pick extras for the services you need:

| Extra | What it adds |
|-------|-------------|
| `daily` | WebRTC transport via Daily.co |
| `openai` | GPT-4o LLM service |
| `deepgram` | Deepgram Nova-2 STT |
| `cartesia` | Cartesia Sonic TTS |
| `silero` | Silero VAD for speech detection |
| `anthropic` | Claude as the LLM |
| `elevenlabs` | ElevenLabs TTS |

## Claude Code Skill Setup

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/pipecat_voice_multimodal_agent
cp SKILL.md ~/.claude/skills/pipecat_voice_multimodal_agent/SKILL.md
```

**Trigger phrases** that activate this skill:
- "Build a voice assistant using pipecat"
- "Create a real-time conversational AI bot"
- "Set up a multimodal agent with speech-to-text and TTS"
- "How do I create a voice pipeline with pipecat?"
- "Build a phone call bot with AI responses"

## First 60 Seconds

**Input:** Run `bash run.sh`

**Output:**
```
======================================================================
  PIPECAT VOICE PIPELINE DEMO (Mock Services)
  Demonstrates real-time voice AI architecture
======================================================================

  Pipeline:
    Audio In -> VAD (Silero-mock) -> STT (Deepgram-mock) -> LLM (GPT-4o-mock) -> TTS (Cartesia-mock) -> Audio Out

  Turn 1/5
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  User:      "Hello, I'd like to learn about voice AI pipelines."
  Assistant: "Hi there! I'm a voice AI assistant built with Pipecat..."
  Output:    [audio: 2.6s, 33 words]
  Latency:   450ms (simulated)
  ...
```

Then a Frame Inspector traces a single utterance through every pipeline stage with metadata.

## Going to Production

1. Get API keys: [Daily.co](https://daily.co), [Deepgram](https://deepgram.com), [OpenAI](https://platform.openai.com), [Cartesia](https://cartesia.ai)
2. Set environment variables:
   ```bash
   export DAILY_API_KEY=...
   export DEEPGRAM_API_KEY=...
   export OPENAI_API_KEY=...
   export CARTESIA_API_KEY=...
   ```
3. Replace mock services with real ones (see `mock_pipeline_demo.py` comments for the exact swap).

## Production Bot Template

```python
import asyncio, os
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.transports.services.daily import DailyTransport, DailyParams
from pipecat.services.openai import OpenAILLMService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext

async def main():
    transport = DailyTransport(
        room_url=os.getenv("DAILY_ROOM_URL"),
        token=os.getenv("DAILY_TOKEN"),
        bot_name="MyBot",
        params=DailyParams(audio_out_enabled=True)
    )
    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")
    tts = CartesiaTTSService(api_key=os.getenv("CARTESIA_API_KEY"), voice_id="your-voice-id")

    context = OpenAILLMContext([{"role": "system", "content": "You are a helpful assistant."}])
    ca = llm.create_context_aggregator(context)

    pipeline = Pipeline([
        transport.input(), stt, ca.user(), llm, tts, transport.output(), ca.assistant()
    ])

    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))
    runner = PipelineRunner()

    @transport.event_handler("on_first_participant_joined")
    async def on_joined(transport, participant):
        await task.queue_frames([ca.user().get_context_frame()])

    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(main())
```
