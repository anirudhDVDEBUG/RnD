# DeepSeek Loop Agent

**A Claude-Code-shaped agent loop powered by the DeepSeek API** — built-in tools (file read/write, bash, grep, glob), permission modes, cron scheduling, and streaming SdkMessage events. Drop-in alternative LLM backend for agent workflows.

## Headline Result

```
$ deepseek-loop --allow-all "Analyze this codebase"
>> Tool: glob(*.py)         → found 5 files
>> Tool: file_read(tools.py) → read 15 lines
>> Tool: bash(python3 --version) → Python 3.12.0

## Codebase Summary
This project implements a Claude-Code-shaped agent loop over DeepSeek...
(Agent completed in 4 turns, 3 tool calls)
```

Run `bash run.sh` for a full offline demo — no API key required.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **Source:** [github.com/v9ai/deepseek-loop](https://github.com/v9ai/deepseek-loop) (Rust original)
