# FRIDAY Technical Details

## What It Does

FRIDAY is a modular Python framework for building a local, autonomous AI assistant. It wires together five subsystems -- persistent memory, multi-step reasoning (via Google Gemini or mock), voice I/O, defensive security scanning, and task automation -- into a single orchestrator loop. The design mirrors the architecture of the [original FRIDAY project](https://github.com/subhansh-dev/Friday-Autonomous-Cognitive-AI-Operating-System) while making it runnable out of the box without API keys or audio hardware.

The core value proposition is the **memory-augmented reasoning loop**: every query and response is stored in a JSON memory file, and future queries retrieve relevant context via keyword overlap scoring before sending the prompt to the LLM. This gives the system a form of persistent, cross-session "learning."

## Architecture

```
friday/
  main.py                        # Orchestrator: demo + interactive REPL
  config.py                      # Env-based config (API key, paths)
  modules/
    memory/
      memory_manager.py          # JSON-backed persistent memory with keyword retrieval
    reasoning/
      cognitive_engine.py        # Gemini API or mock; context-injected prompts
    voice/
      voice_controller.py        # speech_recognition/pyttsx3 or text fallback
    cyber/
      scanner.py                 # Localhost port scan, system info (defensive only)
    automation/
      task_runner.py             # Named task queue with timing and error capture
  data/
    memory_store.json            # Persistent memory (created at runtime)
    logs/                        # Reserved for activity logs
```

### Data Flow

1. **Input** -- User speaks (via microphone) or types at the REPL.
2. **Memory retrieval** -- `MemoryManager.get_relevant_context()` scores all stored memories against the current query using word-overlap and returns the top-k.
3. **Reasoning** -- `CognitiveEngine.think()` builds a prompt with injected context, sends to Gemini (or mock), and returns the response.
4. **Storage** -- Query + response are appended to `memory_store.json` with a timestamp.
5. **Output** -- Response is spoken (TTS) or printed.
6. **Self-reflection** -- `self_reflect()` returns stats on memory count, session count, and engine mode.

### Dependencies

| Dependency | Required? | Purpose |
|---|---|---|
| Python 3.8+ | Yes | Runtime |
| `google-generativeai` | Optional | Live Gemini reasoning |
| `speechrecognition` | Optional | Speech-to-text |
| `pyttsx3` | Optional | Text-to-speech |
| `psutil` | Optional | Enhanced system monitoring |

Zero external dependencies for the demo/mock mode.

### Model Calls

- In live mode, `CognitiveEngine` calls `gemini-pro` via `google.generativeai`. Each call includes the system prompt, retrieved memory context, and the user query.
- In mock mode, responses are selected from categorized templates based on keyword matching (plan/security/memory/default).

## Limitations

- **Memory retrieval is keyword-based**, not semantic. Production use should swap in embedding-based similarity (e.g., sentence-transformers + FAISS).
- **No real autonomy** -- FRIDAY doesn't take actions without user input. It's a reasoning loop, not an agent with tool use.
- **Mock mode is deterministic-ish** -- useful for demos but not for evaluating reasoning quality.
- **Security scanning is localhost-only** -- by design. Scanning external targets requires explicit authorization.
- **No multi-model orchestration** -- single Gemini call per query, no chain-of-thought routing or model selection.
- **Voice requires audio hardware** -- headless servers fall back to text I/O automatically.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|---|---|
| **Agent factories** | FRIDAY's modular architecture (memory + reasoning + tools) mirrors the pattern needed for spawning specialized agents. The memory layer is directly reusable. |
| **Voice AI** | The voice module pattern (STT -> reasoning -> TTS) is the same pipeline used in voice-first products. Swap pyttsx3 for ElevenLabs or Whisper for production quality. |
| **Lead-gen / marketing** | The persistent memory + context injection pattern is how you build agents that remember prospect interactions across sessions. |
| **Defensive security** | The localhost scanner and system monitor patterns are building blocks for security-aware AI agents. |
| **Self-improving systems** | The self-reflection module demonstrates the feedback loop pattern: observe own state -> identify gaps -> adjust. Essential for agents that get better over time. |

The key takeaway: FRIDAY isn't a product -- it's a **pattern library** for memory-augmented, multi-modal AI agents. Each module can be extracted and composed into Claude-driven workflows.
