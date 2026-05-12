# WhisperFlow Voice Browser Agent

**Talk to your browser. It listens, sees, and acts.**

WhisperFlow is an autonomous voice-first agent that executes complex web tasks using Whisper for speech-to-text, GPT-4o Vision for screenshot understanding, and Playwright for browser control. It features self-healing navigation (remembers which selectors break and tries alternatives) and multi-persona expert routing.

## Headline result

```
You say: "Go to Hacker News and find the top story"
Agent:   navigates -> screenshots -> identifies links -> clicks top story -> reads content
         ...all hands-free, with automatic retry if the page layout changes.
```

## Quick start

```bash
bash run.sh        # mock demo, no API keys needed
```

**Next steps:** [HOW_TO_USE.md](HOW_TO_USE.md) | **Architecture:** [TECH_DETAILS.md](TECH_DETAILS.md)
