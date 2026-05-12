---
name: friday_cognitive_ai_os
description: |
  Build an autonomous cognitive AI operating system inspired by FRIDAY — featuring memory, reasoning, voice interaction, cybersecurity tools, and self-improvement capabilities. Runs locally using Python and the Gemini API.
  Triggers: autonomous AI OS, cognitive AI system, FRIDAY-style assistant, local AI operating system, voice + memory + reasoning agent
---

# FRIDAY-Style Autonomous Cognitive AI Operating System

Build a local, autonomous cognitive AI operating system inspired by [FRIDAY](https://github.com/subhansh-dev/Friday-Autonomous-Cognitive-AI-Operating-System). FRIDAY combines memory, reasoning, voice interaction, cybersecurity, and self-improvement into a unified AI assistant that runs entirely on your machine.

## When to use

- "Build an autonomous AI assistant with memory and reasoning"
- "Create a local cognitive AI operating system like FRIDAY or JARVIS"
- "Set up a voice-controlled AI agent with cybersecurity tools"
- "Build a self-improving AI system with persistent memory"
- "Create a Python-based AI OS with voice, reasoning, and automation"

## How to use

### 1. Project Setup

Create the project structure with core modules:

```
friday/
  main.py                  # Entry point and orchestrator
  config.py                # API keys, settings
  requirements.txt         # Dependencies
  modules/
    memory/
      short_term.py        # Session-based memory
      long_term.py         # Persistent memory (JSON/SQLite)
      memory_manager.py    # Memory retrieval and consolidation
    reasoning/
      cognitive_engine.py  # Multi-step reasoning via Gemini API
      planner.py           # Task decomposition and planning
      self_reflect.py      # Self-evaluation and improvement
    voice/
      listener.py          # Speech-to-text (speech_recognition)
      speaker.py           # Text-to-speech (pyttsx3/gTTS)
      voice_controller.py  # Voice command routing
    cyber/
      scanner.py           # Network/port scanning (authorized targets only)
      monitor.py           # System monitoring and alerts
      defense.py           # Defensive security utilities
    automation/
      system_ops.py        # OS-level automation (file ops, process mgmt)
      task_runner.py       # Scheduled and triggered task execution
  data/
    memory_store.json      # Persistent memory storage
    logs/                  # Activity and reasoning logs
```

### 2. Install Dependencies

```bash
pip install google-generativeai speechrecognition pyttsx3 psutil requests rich
```

### 3. Configure the Gemini API

```python
# config.py
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-api-key-here")
MEMORY_FILE = "data/memory_store.json"
LOG_DIR = "data/logs/"
```

### 4. Build the Cognitive Engine

The reasoning module uses Gemini for multi-step thinking:

```python
# modules/reasoning/cognitive_engine.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class CognitiveEngine:
    def __init__(self, memory_manager):
        self.model = genai.GenerativeModel("gemini-pro")
        self.memory = memory_manager

    def think(self, user_input: str) -> str:
        context = self.memory.get_relevant_context(user_input)
        prompt = f"""You are FRIDAY, an autonomous cognitive AI.
Context from memory: {context}
User: {user_input}
Reason step-by-step, then respond."""
        response = self.model.generate_content(prompt)
        self.memory.store(user_input, response.text)
        return response.text
```

### 5. Implement Persistent Memory

```python
# modules/memory/memory_manager.py
import json
from pathlib import Path

class MemoryManager:
    def __init__(self, memory_file: str):
        self.memory_file = Path(memory_file)
        self.memories = self._load()

    def _load(self) -> list:
        if self.memory_file.exists():
            return json.loads(self.memory_file.read_text())
        return []

    def store(self, query: str, response: str):
        self.memories.append({"query": query, "response": response})
        self.memory_file.write_text(json.dumps(self.memories, indent=2))

    def get_relevant_context(self, query: str, k: int = 5) -> str:
        # Simple keyword matching; upgrade to embeddings for production
        scored = []
        for m in self.memories:
            overlap = len(set(query.lower().split()) & set(m["query"].lower().split()))
            scored.append((overlap, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        return "\n".join(f"Q: {m['query']} A: {m['response']}" for _, m in scored[:k])
```

### 6. Add Voice Interaction

```python
# modules/voice/voice_controller.py
import speech_recognition as sr
import pyttsx3

class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self) -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return self.recognizer.recognize_google(audio)

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
```

### 7. Wire Up the Main Loop

```python
# main.py
from modules.memory.memory_manager import MemoryManager
from modules.reasoning.cognitive_engine import CognitiveEngine
from modules.voice.voice_controller import VoiceController
from config import MEMORY_FILE

def main():
    memory = MemoryManager(MEMORY_FILE)
    brain = CognitiveEngine(memory)
    voice = VoiceController()

    voice.speak("FRIDAY online. How can I help?")
    while True:
        try:
            user_input = voice.listen()
            if "shutdown" in user_input.lower():
                voice.speak("Shutting down. Goodbye.")
                break
            response = brain.think(user_input)
            voice.speak(response)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### Key Design Principles

- **Local-first**: All processing runs on your machine; only API calls go external
- **Modular architecture**: Each capability is a separate module that can be developed independently
- **Persistent memory**: Conversations and learned context survive across sessions
- **Self-improvement**: The reasoning engine can reflect on past interactions to improve responses
- **Authorized security only**: Cybersecurity tools must only target systems you own or have explicit permission to test

## References

- Source repository: [subhansh-dev/Friday-Autonomous-Cognitive-AI-Operating-System](https://github.com/subhansh-dev/Friday-Autonomous-Cognitive-AI-Operating-System)
- [Google Gemini API docs](https://ai.google.dev/docs)
- [SpeechRecognition library](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 text-to-speech](https://pypi.org/project/pyttsx3/)
