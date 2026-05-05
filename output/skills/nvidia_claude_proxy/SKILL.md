---
name: nvidia_claude_proxy
description: |
  Set up a proxy server that translates Anthropic Claude API requests to OpenAI-compatible format, forwarding to NVIDIA NIM free models. Enables Claude Code to work with free NVIDIA-hosted LLMs (Kimi, MiniMax, GLM, DeepSeek). Includes a real-time analytics dashboard.
  TRIGGER when: user wants to use free NVIDIA models with Claude Code, set up an API proxy for Claude-to-OpenAI translation, connect Claude Code to NVIDIA NIM, use free LLMs like DeepSeek/Kimi/MiniMax through Claude interface, or set up a model proxy with analytics.
---

# nvidia_claude_proxy

Proxy server that translates Anthropic Claude API requests to OpenAI-compatible format, forwarding them to NVIDIA NIM free models. Use Claude Code with free NVIDIA-hosted LLMs.

## When to use

- "Set up a proxy to use free NVIDIA models with Claude Code"
- "How do I use DeepSeek or Kimi models through Claude's API format?"
- "I want to connect Claude Code to NVIDIA NIM free models"
- "Set up an Anthropic-to-OpenAI API proxy with analytics"
- "Use free LLMs with Claude Code via NVIDIA"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/Jeanrooy/nvidia-claude-proxy.git
cd nvidia-claude-proxy
pip install -r requirements.txt
```

### 2. Configure environment

Get a free NVIDIA NIM API key from https://build.nvidia.com and set it:

```bash
export NVIDIA_API_KEY="your-nvidia-nim-api-key"
```

### 3. Start the proxy server

```bash
python proxy.py
```

The proxy will start on a local port (default typically `http://localhost:8082`). It translates incoming Anthropic-format API requests into OpenAI-compatible format and forwards them to NVIDIA NIM endpoints.

### 4. Point Claude Code at the proxy

Configure Claude Code to use the proxy as its API base URL:

```bash
export ANTHROPIC_BASE_URL="http://localhost:8082"
```

Then run Claude Code normally — requests will be routed through the proxy to free NVIDIA-hosted models.

### 5. Available models

The proxy supports free NVIDIA NIM-hosted models including:
- **DeepSeek** variants
- **Kimi** (Moonshot AI)
- **MiniMax**
- **GLM** (ChatGLM)

Check the proxy's configuration or dashboard for the full list of available model mappings.

### 6. Analytics dashboard

The proxy includes a real-time analytics dashboard to monitor request volume, latency, token usage, and model distribution. Access it via the browser at the proxy's dashboard URL (typically shown in startup logs).

## Key features

- **API translation**: Converts Anthropic Messages API format to OpenAI Chat Completions format
- **Free models**: Access NVIDIA NIM-hosted LLMs at no cost
- **Dashboard**: Built-in real-time analytics for monitoring usage
- **Drop-in replacement**: Works with Claude Code by simply changing the base URL

## References

- Source repository: https://github.com/Jeanrooy/nvidia-claude-proxy
- NVIDIA NIM: https://build.nvidia.com
