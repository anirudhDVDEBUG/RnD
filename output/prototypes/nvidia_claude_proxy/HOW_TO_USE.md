# How to Use nvidia_claude_proxy

## Install

```bash
git clone https://github.com/Jeanrooy/nvidia-claude-proxy.git
cd nvidia-claude-proxy
pip install -r requirements.txt
```

Dependencies: `flask`, `requests`, `flask-cors` (Python 3.9+).

## Configure

1. Get a free NVIDIA NIM API key at https://build.nvidia.com (sign up, no credit card).
2. Export it:

```bash
export NVIDIA_API_KEY="nvapi-xxxxxxxxxxxxxxxxxxxx"
```

## Run the Proxy

```bash
python proxy.py
# Proxy starts on http://localhost:8082
```

## Point Claude Code at the Proxy

```bash
export ANTHROPIC_BASE_URL="http://localhost:8082"
claude  # now all requests route through the proxy to NVIDIA models
```

## This is a Claude Skill

Drop the skill file so Claude Code can self-activate:

```bash
mkdir -p ~/.claude/skills/nvidia_claude_proxy
cp SKILL.md ~/.claude/skills/nvidia_claude_proxy/SKILL.md
```

**Trigger phrases:**
- "Set up a proxy to use free NVIDIA models with Claude Code"
- "How do I use DeepSeek or Kimi through Claude's API format?"
- "Connect Claude Code to NVIDIA NIM free models"
- "Set up an Anthropic-to-OpenAI API proxy with analytics"

## First 60 Seconds

```bash
# Terminal 1 — start the proxy (mock mode, no key needed for demo)
bash run.sh

# Output:
# [PROXY] Mock mode — no NVIDIA_API_KEY set, using synthetic responses
# [PROXY] Listening on http://localhost:8082
# [TEST] POST /v1/messages {"model":"claude-sonnet-4-20250514","messages":[...]}
# [PROXY] Translated -> OpenAI format, target: nvidia/deepseek-r1
# [RESPONSE] 200 | tokens: 142 | latency: 0.3s
# [DASHBOARD] Stats: 1 request | avg latency 0.3s | models: deepseek-r1
```

```bash
# Terminal 2 — query the proxy like it's the Anthropic API
curl -X POST http://localhost:8082/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello, what model are you?"}]
  }'
```

Response (Anthropic Messages API format):
```json
{
  "id": "msg_proxy_001",
  "type": "message",
  "role": "assistant",
  "content": [{"type": "text", "text": "I am DeepSeek-R1, served via NVIDIA NIM."}],
  "model": "nvidia/deepseek-r1",
  "usage": {"input_tokens": 12, "output_tokens": 14}
}
```

## Model Mappings

| Claude Model Requested | NVIDIA NIM Model Used |
|---|---|
| claude-sonnet-4-20250514 | nvidia/deepseek-r1 |
| claude-haiku-4-5-20251001 | nvidia/glm-4 |
| claude-opus-4-20250514 | nvidia/kimi-k2 |
| (any other) | nvidia/minimax-01 |

## Analytics Dashboard

Open `http://localhost:8082/dashboard` in a browser to see:
- Request count and rate
- Average latency per model
- Token usage breakdown
- Error rate
