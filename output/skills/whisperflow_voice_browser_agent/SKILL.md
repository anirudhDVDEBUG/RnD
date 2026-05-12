---
name: whisperflow_voice_browser_agent
description: |
  Build a voice-first autonomous browser agent using Whisper STT, GPT-4o Vision, and Playwright.
  TRIGGER: user wants voice-controlled browser automation, speech-to-action web tasks,
  self-healing web agents, or autonomous browsing with voice commands.
---

# Whisperflow Voice Browser Agent

An autonomous voice-first agent that executes complex web tasks. Powered by GPT-4o Vision, Playwright, and Whisper. Features self-healing navigation, adaptive memory, and multi-persona experts.

## When to use

- "Build a voice-controlled browser automation agent"
- "Create an autonomous web agent that takes voice commands"
- "Set up a self-healing browser bot with speech input"
- "I want a Jarvis-like assistant that browses the web for me"
- "Build a Playwright agent with Whisper voice input and vision"

## How to use

### 1. Project Setup

Create the project structure:

```
whisperflow/
├── main.py              # Entry point and orchestrator
├── voice_input.py       # Whisper STT voice capture
├── browser_agent.py     # Playwright browser automation
├── vision_analyzer.py   # GPT-4o Vision screenshot analysis
├── memory_store.py      # Adaptive memory for self-healing
├── expert_personas.py   # Multi-persona expert routing
├── requirements.txt
└── .env
```

### 2. Install Dependencies

```bash
pip install openai playwright sounddevice numpy pydantic python-dotenv
python -m playwright install chromium
```

**requirements.txt:**
```
openai>=1.30.0
playwright>=1.44.0
sounddevice>=0.4.6
numpy>=1.26.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### 3. Voice Input with Whisper

```python
# voice_input.py
import sounddevice as sd
import numpy as np
import tempfile
import wave
from openai import OpenAI

class VoiceInput:
    def __init__(self, client: OpenAI, sample_rate=16000, silence_threshold=500, silence_duration=1.5):
        self.client = client
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

    def record_until_silence(self) -> str:
        """Record audio until silence is detected, then transcribe with Whisper."""
        print("Listening... (speak now)")
        frames = []
        silent_chunks = 0
        chunk_size = int(self.sample_rate * 0.1)
        max_silent = int(self.silence_duration / 0.1)

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
            while True:
                data, _ = stream.read(chunk_size)
                frames.append(data.copy())
                amplitude = np.abs(data).mean()
                if amplitude < self.silence_threshold:
                    silent_chunks += 1
                else:
                    silent_chunks = 0
                if silent_chunks >= max_silent and len(frames) > max_silent:
                    break

        audio_data = np.concatenate(frames)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, 'wb') as wf:
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
```

### 4. Browser Agent with Playwright

```python
# browser_agent.py
import base64
from playwright.async_api import async_playwright, Page, Browser

class BrowserAgent:
    def __init__(self):
        self.browser: Browser | None = None
        self.page: Page | None = None
        self.playwright = None

    async def start(self, headless=False):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def navigate(self, url: str):
        await self.page.goto(url, wait_until="domcontentloaded", timeout=15000)

    async def screenshot_base64(self) -> str:
        img_bytes = await self.page.screenshot(full_page=False)
        return base64.b64encode(img_bytes).decode()

    async def execute_action(self, action: dict):
        """Execute a parsed action on the page."""
        act = action.get("action")
        selector = action.get("selector", "")
        value = action.get("value", "")

        try:
            if act == "click":
                await self.page.click(selector, timeout=5000)
            elif act == "type":
                await self.page.fill(selector, value)
            elif act == "navigate":
                await self.navigate(value)
            elif act == "scroll_down":
                await self.page.evaluate("window.scrollBy(0, 500)")
            elif act == "scroll_up":
                await self.page.evaluate("window.scrollBy(0, -500)")
            elif act == "wait":
                await self.page.wait_for_timeout(int(value) if value else 2000)
            elif act == "press":
                await self.page.keyboard.press(value)
            return True
        except Exception as e:
            print(f"Action failed: {e}")
            return False

    async def get_page_context(self) -> str:
        """Extract visible text and interactive elements."""
        return await self.page.evaluate("""() => {
            const els = document.querySelectorAll('a, button, input, select, textarea, [role=button]');
            const items = Array.from(els).slice(0, 50).map(el => ({
                tag: el.tagName, text: el.innerText?.slice(0, 80),
                id: el.id, name: el.name, type: el.type,
                href: el.href, placeholder: el.placeholder
            }));
            return JSON.stringify({ title: document.title, url: location.href, elements: items });
        }""")

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
```

### 5. GPT-4o Vision Analyzer

```python
# vision_analyzer.py
from openai import OpenAI
import json

class VisionAnalyzer:
    def __init__(self, client: OpenAI):
        self.client = client

    def analyze_and_plan(self, screenshot_b64: str, page_context: str,
                         user_goal: str, memory_hints: str = "") -> list[dict]:
        """Analyze a screenshot + DOM context and return a list of actions."""
        system = """You are an autonomous browser agent. Given a screenshot, page context,
and user goal, return a JSON array of actions to take. Each action is an object with:
- "action": one of click, type, navigate, scroll_down, scroll_up, wait, press, done
- "selector": CSS selector (for click/type)
- "value": text to type, URL to navigate, or key to press
- "reasoning": brief explanation

If the goal is complete, return [{"action": "done", "reasoning": "..."}].
Return ONLY valid JSON."""

        user_msg = f"Goal: {user_goal}\nPage context: {page_context}"
        if memory_hints:
            user_msg += f"\nPast experience hints: {memory_hints}"

        resp = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": [
                    {"type": "text", "text": user_msg},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{screenshot_b64}", "detail": "high"
                    }}
                ]}
            ],
            max_tokens=1500
        )
        text = resp.choices[0].message.content.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)
```

### 6. Adaptive Memory for Self-Healing

```python
# memory_store.py
import json
from pathlib import Path

class MemoryStore:
    def __init__(self, path="memory.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {"successes": [], "failures": [], "selector_map": {}}

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2))

    def record_success(self, domain: str, action: dict):
        self.data["successes"].append({"domain": domain, **action})
        if action.get("selector"):
            key = f"{domain}:{action.get('reasoning', '')[:40]}"
            self.data["selector_map"][key] = action["selector"]
        self.save()

    def record_failure(self, domain: str, action: dict, error: str):
        self.data["failures"].append({"domain": domain, "error": error, **action})
        self.save()

    def get_hints(self, domain: str) -> str:
        failures = [f for f in self.data["failures"] if f.get("domain") == domain][-5:]
        successes = [s for s in self.data["successes"] if s.get("domain") == domain][-5:]
        hints = ""
        if failures:
            hints += "Recent failures: " + json.dumps(failures) + "\n"
        if successes:
            hints += "Recent successes: " + json.dumps(successes)
        return hints
```

### 7. Main Orchestrator

```python
# main.py
import asyncio
from urllib.parse import urlparse
from dotenv import load_dotenv
from openai import OpenAI
from voice_input import VoiceInput
from browser_agent import BrowserAgent
from vision_analyzer import VisionAnalyzer
from memory_store import MemoryStore

load_dotenv()

MAX_STEPS = 20

async def run():
    client = OpenAI()
    voice = VoiceInput(client)
    analyzer = VisionAnalyzer(client)
    memory = MemoryStore()
    browser = BrowserAgent()
    await browser.start(headless=False)
    await browser.navigate("https://www.google.com")

    print("Whisperflow ready. Say your command or 'quit' to exit.")

    while True:
        command = voice.record_until_silence()
        if command.lower().strip() in ("quit", "exit", "stop"):
            break

        domain = urlparse(browser.page.url).netloc
        for step in range(MAX_STEPS):
            screenshot = await browser.screenshot_base64()
            context = await browser.get_page_context()
            hints = memory.get_hints(domain)

            actions = analyzer.analyze_and_plan(screenshot, context, command, hints)
            print(f"Step {step+1}: {len(actions)} action(s) planned")

            done = False
            for action in actions:
                if action.get("action") == "done":
                    print(f"Task complete: {action.get('reasoning')}")
                    done = True
                    break

                print(f"  -> {action.get('action')}: {action.get('selector', '')} {action.get('value', '')}")
                success = await browser.execute_action(action)
                domain = urlparse(browser.page.url).netloc

                if success:
                    memory.record_success(domain, action)
                else:
                    memory.record_failure(domain, action, "execution_failed")

                await browser.page.wait_for_timeout(800)

            if done:
                break
        else:
            print("Max steps reached.")

        print("Ready for next command...")

    await browser.close()
    print("Goodbye.")

if __name__ == "__main__":
    asyncio.run(run())
```

### 8. Environment Configuration

**.env:**
```
OPENAI_API_KEY=sk-your-key-here
```

### 9. Run

```bash
python main.py
```

Speak a command like "Search for the latest AI news on Google" and watch the agent navigate autonomously.

## Key Architecture Concepts

- **Voice-first loop**: Whisper STT captures commands → GPT-4o Vision plans actions → Playwright executes
- **Self-healing**: Failed selectors are recorded in memory; the vision model receives failure hints to choose alternative selectors on retry
- **Adaptive memory**: Success/failure patterns per domain persist across sessions so the agent learns from past runs
- **Multi-step autonomy**: The agent loops screenshot→analyze→act until the goal is complete or max steps reached

## References

- Source: [adriansanthosh77-dev/Whisperflowactions](https://github.com/adriansanthosh77-dev/Whisperflowactions)
- [Playwright Python docs](https://playwright.dev/python/)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [GPT-4o Vision](https://platform.openai.com/docs/guides/vision)
