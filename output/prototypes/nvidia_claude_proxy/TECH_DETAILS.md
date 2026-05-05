# Technical Details

## What It Does

nvidia_claude_proxy is a Flask-based HTTP server that accepts requests in Anthropic's Messages API format (`POST /v1/messages`) and translates them on-the-fly into OpenAI Chat Completions format (`POST /v1/chat/completions`), then forwards them to NVIDIA's NIM inference endpoints. Responses are translated back into Anthropic format before being returned to the caller. This lets any tool expecting the Anthropic API (notably Claude Code) use free NVIDIA-hosted models transparently.

The proxy also serves a lightweight analytics dashboard that tracks request volume, latency percentiles, token consumption, and model distribution in real time using in-memory counters.

## Architecture

```
Claude Code / curl
       |
       | Anthropic Messages API (POST /v1/messages)
       v
+------------------+
|   proxy.py       |  Flask app, single process
|  - translate_req |  Anthropic -> OpenAI format
|  - route_model   |  Map claude-* to nvidia/* model IDs
|  - translate_res |  OpenAI -> Anthropic format
|  - analytics     |  In-memory stats collector
+------------------+
       |
       | OpenAI Chat Completions API
       v
  NVIDIA NIM endpoint (https://integrate.api.nvidia.com/v1)
```

### Key Files

| File | Purpose |
|---|---|
| `proxy.py` | Main server: request translation, model routing, response mapping |
| `dashboard.py` | Analytics collector + HTML dashboard endpoint |
| `run.sh` | Demo runner with mock mode (no API key required) |

### Data Flow

1. Incoming request: extract `model`, `messages`, `max_tokens`, `system` from Anthropic format.
2. Model mapping: look up NVIDIA model ID from a static dict.
3. Message conversion: flatten Anthropic's `[{"role","content"}]` (where content can be a list of blocks) into OpenAI's simpler `{"role","content"}` strings. System prompt becomes a system message.
4. Forward to NVIDIA NIM with `Authorization: Bearer $NVIDIA_API_KEY`.
5. Response conversion: wrap OpenAI's `choices[0].message.content` back into Anthropic's `content: [{type:"text", text:...}]` envelope.
6. Record metrics (latency, tokens, status) in the analytics store.

### Dependencies

- **Flask** — HTTP server
- **requests** — outbound HTTP to NVIDIA
- **flask-cors** — allow browser dashboard access

No database, no background workers, no Docker required.

## Limitations

- **Streaming not supported**: The proxy does not translate Anthropic SSE streaming to/from OpenAI streaming. Requests with `stream: true` will be rejected or buffered.
- **Tool use / function calling**: Anthropic's tool_use blocks are not translated. Only plain text messages work.
- **Vision/images**: Multi-modal content blocks (images) are dropped during translation.
- **Rate limits**: NVIDIA NIM free tier has rate limits (~5 RPM for some models). The proxy does not retry or queue.
- **No auth on the proxy itself**: Anyone who can reach localhost:8082 can use your NVIDIA API key.
- **Single-process**: Not production-grade; meant for local dev use.

## Why It Matters

For teams building Claude-driven products (agent factories, lead-gen, ad creative pipelines):

- **Cost reduction during development**: Use free NVIDIA models for iteration/testing, switch to real Claude for production.
- **Model comparison**: A/B test Claude vs DeepSeek/Kimi quality by toggling `ANTHROPIC_BASE_URL`.
- **Fallback routing**: Could be extended to fall back to free models when Claude quota is exhausted.
- **Skill ecosystem proof**: Shows how Claude Code skills can integrate third-party inference without changing the client.
