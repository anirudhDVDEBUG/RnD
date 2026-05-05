"""
Pipecat Pipeline Architecture Demo (Mock)

Demonstrates how Pipecat's frame-based pipeline works for voice/multimodal AI,
using mock services so no API keys are needed. Shows the exact same architecture
you'd use in production — just swap mock services for real ones.
"""

import asyncio
import time
import json
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ---------------------------------------------------------------------------
# Frames — the units of data flowing through the pipeline
# ---------------------------------------------------------------------------

class FrameType(Enum):
    AUDIO_RAW = "audio_raw"
    TRANSCRIPT = "transcript"
    LLM_TEXT = "llm_text"
    TTS_AUDIO = "tts_audio"
    SYSTEM = "system"


@dataclass
class Frame:
    type: FrameType
    data: Any
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)

    def __repr__(self):
        preview = str(self.data)[:60]
        return f"Frame({self.type.value}: {preview})"


# ---------------------------------------------------------------------------
# Processors — each transforms frames as they flow through
# ---------------------------------------------------------------------------

class Processor:
    """Base class for pipeline processors."""
    name: str = "base"

    async def process(self, frame: Frame) -> list[Frame]:
        return [frame]


class MockSTTService(Processor):
    """Simulates Speech-to-Text (like Deepgram, Whisper, etc.)."""
    name = "STT (Deepgram-mock)"

    SIMULATED_TRANSCRIPTS = [
        "Hello, I'd like to learn about voice AI pipelines.",
        "How does Pipecat handle real-time audio streaming?",
        "Can you explain the frame-based architecture?",
        "What TTS providers does Pipecat support?",
        "Thanks, that was really helpful!",
    ]

    def __init__(self):
        self._index = 0

    async def process(self, frame: Frame) -> list[Frame]:
        if frame.type != FrameType.AUDIO_RAW:
            return [frame]
        # Simulate STT latency
        await asyncio.sleep(0.15)
        transcript = self.SIMULATED_TRANSCRIPTS[self._index % len(self.SIMULATED_TRANSCRIPTS)]
        self._index += 1
        return [Frame(
            type=FrameType.TRANSCRIPT,
            data=transcript,
            metadata={"service": self.name, "confidence": 0.97}
        )]


class MockLLMService(Processor):
    """Simulates an LLM (like OpenAI GPT-4o, Claude, Gemini)."""
    name = "LLM (GPT-4o-mock)"

    RESPONSES = {
        "hello": "Hi there! I'm a voice AI assistant built with Pipecat. Pipecat is an open-source framework that lets you build real-time conversational AI with swappable STT, LLM, and TTS services.",
        "how does": "Pipecat streams audio in real-time using WebRTC via Daily.co. Audio frames flow through the pipeline: first STT converts speech to text, then the LLM generates a response, and finally TTS converts it back to speech — all in under 500ms.",
        "can you explain": "The frame-based architecture is Pipecat's core design. Data flows as typed frames through a pipeline of processors. Each processor transforms frames — STT turns audio into text, LLMs turn text into responses, TTS turns text into audio. This modular design lets you swap any component.",
        "what tts": "Pipecat supports Cartesia, ElevenLabs, Azure TTS, PlayHT, LMNT, and XTTS for text-to-speech. Each is a drop-in replacement — just change the service class and API key. Cartesia is popular for its low latency.",
        "thanks": "You're welcome! Check out github.com/pipecat-ai/pipecat for more examples. Happy building!",
    }

    def __init__(self, system_prompt: str = "You are a helpful voice assistant."):
        self.system_prompt = system_prompt
        self.context: list[dict] = [{"role": "system", "content": system_prompt}]

    async def process(self, frame: Frame) -> list[Frame]:
        if frame.type != FrameType.TRANSCRIPT:
            return [frame]

        user_text = frame.data.lower()
        self.context.append({"role": "user", "content": frame.data})

        # Match response based on keywords
        response = "I can help with voice AI pipelines, real-time audio, and the Pipecat framework. What would you like to know?"
        for key, resp in self.RESPONSES.items():
            if key in user_text:
                response = resp
                break

        self.context.append({"role": "assistant", "content": response})

        # Simulate LLM streaming latency
        await asyncio.sleep(0.2)
        return [Frame(
            type=FrameType.LLM_TEXT,
            data=response,
            metadata={"service": self.name, "tokens": len(response.split())}
        )]


class MockTTSService(Processor):
    """Simulates Text-to-Speech (like Cartesia, ElevenLabs, etc.)."""
    name = "TTS (Cartesia-mock)"

    async def process(self, frame: Frame) -> list[Frame]:
        if frame.type != FrameType.LLM_TEXT:
            return [frame]
        # Simulate TTS synthesis
        await asyncio.sleep(0.1)
        word_count = len(frame.data.split())
        duration_sec = word_count * 0.08  # ~75ms per word
        return [Frame(
            type=FrameType.TTS_AUDIO,
            data=f"[audio: {duration_sec:.1f}s, {word_count} words]",
            metadata={"service": self.name, "duration_sec": duration_sec, "sample_rate": 24000}
        )]


class MockVADService(Processor):
    """Simulates Voice Activity Detection (like Silero VAD)."""
    name = "VAD (Silero-mock)"

    async def process(self, frame: Frame) -> list[Frame]:
        if frame.type != FrameType.AUDIO_RAW:
            return [frame]
        # Simulate VAD check
        frame.metadata["vad_speech_detected"] = True
        frame.metadata["vad_confidence"] = 0.95
        return [frame]


# ---------------------------------------------------------------------------
# Pipeline — connects processors in sequence
# ---------------------------------------------------------------------------

class Pipeline:
    """Connects processors in sequence, passing frames through each."""

    def __init__(self, processors: list[Processor]):
        self.processors = processors

    async def push(self, frame: Frame) -> list[Frame]:
        frames = [frame]
        for proc in self.processors:
            next_frames = []
            for f in frames:
                result = await proc.process(f)
                next_frames.extend(result)
            frames = next_frames
        return frames


# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------

def print_header():
    print("=" * 70)
    print("  PIPECAT VOICE PIPELINE DEMO (Mock Services)")
    print("  Demonstrates real-time voice AI architecture")
    print("=" * 70)
    print()


def print_pipeline_diagram(processors: list[Processor]):
    names = [p.name for p in processors]
    print("  Pipeline:")
    print(f"    Audio In -> {' -> '.join(names)} -> Audio Out")
    print()


async def run_conversation():
    print_header()

    # Build pipeline — same structure as production Pipecat
    vad = MockVADService()
    stt = MockSTTService()
    llm = MockLLMService(
        system_prompt="You are a knowledgeable voice AI assistant that explains Pipecat concepts clearly."
    )
    tts = MockTTSService()

    pipeline = Pipeline([vad, stt, llm, tts])
    print_pipeline_diagram(pipeline.processors)

    # Simulate 5 conversation turns
    num_turns = 5
    total_latency = 0.0
    print("-" * 70)
    print("  CONVERSATION SIMULATION")
    print("-" * 70)

    for turn in range(num_turns):
        print(f"\n  Turn {turn + 1}/{num_turns}")
        print(f"  {'~' * 40}")

        # Create simulated audio input frame
        input_frame = Frame(
            type=FrameType.AUDIO_RAW,
            data=f"[raw audio chunk {turn + 1}: 16kHz, 16-bit PCM]",
            metadata={"sample_rate": 16000, "channels": 1}
        )

        start = time.time()
        output_frames = await pipeline.push(input_frame)
        latency = time.time() - start
        total_latency += latency

        # Show what happened at each stage
        for frame in output_frames:
            if frame.type == FrameType.TTS_AUDIO:
                # Reconstruct the conversation from context
                user_text = llm.context[-2]["content"] if len(llm.context) >= 2 else "..."
                assistant_text = llm.context[-1]["content"] if len(llm.context) >= 1 else "..."

                print(f"  User:      \"{user_text}\"")
                print(f"  Assistant: \"{assistant_text}\"")
                print(f"  Output:    {frame.data}")
                print(f"  Latency:   {latency * 1000:.0f}ms (simulated)")

    # Summary stats
    print(f"\n{'=' * 70}")
    print("  PIPELINE SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Turns completed:     {num_turns}")
    print(f"  Avg latency:         {(total_latency / num_turns) * 1000:.0f}ms (simulated)")
    print(f"  Pipeline stages:     {len(pipeline.processors)}")
    print(f"  Context messages:    {len(llm.context)}")
    print()

    # Show the services that would be swapped in production
    print("  Production service mapping:")
    print("  +-----------------+-------------------------+-------------------+")
    print("  | Stage           | Mock (this demo)        | Production        |")
    print("  +-----------------+-------------------------+-------------------+")
    print("  | Transport       | Simulated frames        | Daily WebRTC      |")
    print("  | VAD             | Silero-mock             | Silero VAD        |")
    print("  | STT             | Deepgram-mock           | Deepgram Nova-2   |")
    print("  | LLM             | GPT-4o-mock             | OpenAI / Claude   |")
    print("  | TTS             | Cartesia-mock           | Cartesia Sonic    |")
    print("  +-----------------+-------------------------+-------------------+")
    print()

    # Show what production code looks like
    print("  To go live, replace mock services with real ones:")
    print("    stt = DeepgramSTTService(api_key=os.getenv('DEEPGRAM_KEY'))")
    print("    llm = OpenAILLMService(api_key=os.getenv('OPENAI_KEY'), model='gpt-4o')")
    print("    tts = CartesiaTTSService(api_key=os.getenv('CARTESIA_KEY'))")
    print()
    return True


async def run_frame_inspector():
    """Shows detailed frame flow through the pipeline."""
    print(f"\n{'=' * 70}")
    print("  FRAME INSPECTOR — Trace a single utterance through the pipeline")
    print(f"{'=' * 70}\n")

    processors = [MockVADService(), MockSTTService(), MockLLMService(), MockTTSService()]

    input_frame = Frame(
        type=FrameType.AUDIO_RAW,
        data="[raw audio: 1.2s, 16kHz mono PCM]",
        metadata={"sample_rate": 16000, "channels": 1}
    )

    print(f"  INPUT:  {input_frame}")
    print(f"  Metadata: {json.dumps(input_frame.metadata, indent=2)}")
    print()

    frames = [input_frame]
    for i, proc in enumerate(processors):
        next_frames = []
        for f in frames:
            result = await proc.process(f)
            next_frames.extend(result)
        frames = next_frames

        print(f"  Stage {i + 1} [{proc.name}]:")
        for f in frames:
            print(f"    Output: {f}")
            print(f"    Metadata: {json.dumps(f.metadata, indent=2)}")
        print()

    print("  Each frame carries typed data + metadata through the pipeline.")
    print("  This is how Pipecat achieves modular, swappable AI services.\n")


async def main():
    await run_conversation()
    await run_frame_inspector()
    print("Demo complete. See HOW_TO_USE.md for production setup instructions.")


if __name__ == "__main__":
    asyncio.run(main())
