"""Voice input module: captures audio and transcribes via Whisper (or mock)."""

import os
import tempfile
import wave

MOCK_MODE = os.environ.get("WHISPERFLOW_MOCK", "1") == "1"


class VoiceInput:
    """Record audio until silence, then transcribe with OpenAI Whisper."""

    def __init__(self, client=None, sample_rate=16000, silence_threshold=500, silence_duration=1.5):
        self.client = client
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

    def record_until_silence(self) -> str:
        if MOCK_MODE:
            return self._mock_transcribe()
        return self._real_transcribe()

    # -- mock path (no mic / no API key) ----------------------------------
    _mock_commands = [
        "Go to Hacker News and find the top story",
        "Search Google for 'best noise-canceling headphones 2026'",
        "Open Wikipedia and look up 'large language models'",
        "Scroll down and click the first link",
        "Go back and take a screenshot",
    ]
    _mock_idx = 0

    def _mock_transcribe(self) -> str:
        cmd = self._mock_commands[VoiceInput._mock_idx % len(self._mock_commands)]
        VoiceInput._mock_idx += 1
        print(f"[mock-voice] You said: {cmd}")
        return cmd

    # -- real path (requires mic + OPENAI_API_KEY) -------------------------
    def _real_transcribe(self) -> str:
        import sounddevice as sd  # noqa: delayed import
        import numpy as np

        print("Listening... (speak now)")
        frames = []
        silent_chunks = 0
        chunk_size = int(self.sample_rate * 0.1)
        max_silent = int(self.silence_duration / 0.1)

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="int16") as stream:
            while True:
                data, _ = stream.read(chunk_size)
                frames.append(data.copy())
                amplitude = abs(int(data.mean()))
                if amplitude < self.silence_threshold:
                    silent_chunks += 1
                else:
                    silent_chunks = 0
                if silent_chunks >= max_silent and len(frames) > max_silent:
                    break

        audio_data = __import__("numpy").concatenate(frames)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())
            with open(f.name, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file
                )
        print(f"You said: {transcript.text}")
        return transcript.text
