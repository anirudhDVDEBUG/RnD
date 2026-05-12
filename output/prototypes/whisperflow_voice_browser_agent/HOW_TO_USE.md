# How to Use WhisperFlow

## Option A: Mock demo (no dependencies)

```bash
bash run.sh
```

Requires only Python 3.10+. Simulates voice input, browser, and vision analysis with built-in mock data. Produces full visible output showing the agent loop.

## Option B: Live mode (real browser + voice + API)

### 1. Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

System-level audio libraries may be needed for `sounddevice`:
- **macOS:** `brew install portaudio`
- **Ubuntu:** `sudo apt install libportaudio2`
- **Windows:** included with pip install

### 2. Set environment

```bash
export OPENAI_API_KEY="sk-..."
export WHISPERFLOW_MOCK=0          # disable mock mode
export WHISPERFLOW_MAX_COMMANDS=10 # optional, default 5
```

### 3. Run

```bash
python3 main.py
```

Speak into your mic. The agent will transcribe your command, take a screenshot of the current browser page, plan actions using GPT-4o Vision, and execute them via Playwright.

## As a Claude Code Skill

Drop the skill definition into your skills directory:

```bash
mkdir -p ~/.claude/skills/whisperflow_voice_browser_agent
# Copy the SKILL.md file into that directory
cp SKILL.md ~/.claude/skills/whisperflow_voice_browser_agent/SKILL.md
```

**Trigger phrases that activate it:**
- "Build a voice-controlled browser automation agent"
- "Create an autonomous web agent that takes voice commands"
- "Set up a self-healing browser bot with speech input"
- "I want a Jarvis-like assistant that browses the web for me"
- "Build a Playwright agent with Whisper voice input and vision"

Claude will scaffold the full project using the patterns in this repo.

## First 60 seconds

```
$ bash run.sh

==> WhisperFlow Voice Browser Agent -- Demo

==> Running mock demo (no API keys / hardware required)...

============================================================
  WhisperFlow -- Voice-First Browser Agent
============================================================
  Mode: MOCK (no API keys / hardware required)

[mock-browser] Chromium launched (simulated)
[mock-browser] Navigated to https://news.ycombinator.com

--- Command 1/5 ---
[mock-voice] You said: Go to Hacker News and find the top story
[expert] Routing to: Navigator -- Specializes in URL routing...
[state] Page: Hacker News | URL: https://news.ycombinator.com
[plan] 1 action(s) planned
  [1/1] navigate -> OK

--- Command 2/5 ---
[mock-voice] You said: Search Google for 'best noise-canceling headphones 2026'
[expert] Routing to: Searcher -- Expert at filling search forms...
[plan] 4 action(s) planned
  [1/4] navigate -> OK
  [2/4] click -> OK
  [3/4] type -> OK
  [4/4] press -> OK

...

============================================================
  Session Summary
============================================================
  Commands processed: 5
  Memory entries:     8
  Successful actions: 8
  Failed actions:     0
============================================================

==> Demo complete.
```
