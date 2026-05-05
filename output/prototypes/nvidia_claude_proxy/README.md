# nvidia_claude_proxy

**Use Claude Code with free NVIDIA-hosted LLMs (DeepSeek, Kimi, MiniMax, GLM) by running a local proxy that translates Anthropic API requests into OpenAI-compatible format and forwards them to NVIDIA NIM.**

## Headline Result

```
$ bash run.sh
[PROXY] Started on http://localhost:8082
[PROXY] Translating Anthropic Messages API -> OpenAI Chat Completions
[REQUEST] model=claude-sonnet-4-20250514 -> nvidia/deepseek-r1
[RESPONSE] 200 OK | 847 tokens | 1.2s latency
[DASHBOARD] http://localhost:8082/dashboard — 3 requests, avg 1.1s
```

Zero-cost model access. Drop-in replacement for `ANTHROPIC_BASE_URL`.

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, configure, run in 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations
