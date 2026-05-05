"""
nvidia_claude_proxy - Translates Anthropic Messages API to OpenAI format,
forwards to NVIDIA NIM free models.
"""

import os
import time
import json
import uuid

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MOCK_MODE = not NVIDIA_API_KEY

MODEL_MAP = {
    "claude-sonnet-4-20250514": "nvidia/deepseek-r1",
    "claude-3-5-sonnet-20241022": "nvidia/deepseek-r1",
    "claude-haiku-4-5-20251001": "nvidia/glm-4",
    "claude-3-haiku-20240307": "nvidia/glm-4",
    "claude-opus-4-20250514": "nvidia/kimi-k2",
    "claude-3-opus-20240229": "nvidia/kimi-k2",
}
DEFAULT_MODEL = "nvidia/minimax-01"

# In-memory analytics
stats = {"requests": [], "total": 0, "errors": 0}


def translate_request(anthropic_body):
    """Convert Anthropic Messages API body to OpenAI Chat Completions format."""
    messages = []

    # Handle system prompt
    system = anthropic_body.get("system", "")
    if system:
        messages.append({"role": "system", "content": system})

    # Convert messages
    for msg in anthropic_body.get("messages", []):
        role = msg.get("role", "user")
        content = msg.get("content", "")
        # Anthropic content can be a list of blocks or a string
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block["text"])
                elif isinstance(block, str):
                    text_parts.append(block)
            content = "\n".join(text_parts)
        messages.append({"role": role, "content": content})

    # Map model
    requested_model = anthropic_body.get("model", "")
    nvidia_model = MODEL_MAP.get(requested_model, DEFAULT_MODEL)

    return {
        "model": nvidia_model,
        "messages": messages,
        "max_tokens": anthropic_body.get("max_tokens", 1024),
        "temperature": anthropic_body.get("temperature", 0.7),
    }, nvidia_model


def translate_response(openai_response, nvidia_model):
    """Convert OpenAI Chat Completions response to Anthropic Messages format."""
    choice = openai_response.get("choices", [{}])[0]
    message = choice.get("message", {})
    usage = openai_response.get("usage", {})

    return {
        "id": f"msg_{uuid.uuid4().hex[:12]}",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": message.get("content", "")}],
        "model": nvidia_model,
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        },
    }


def mock_response(nvidia_model, messages):
    """Generate a mock response when no API key is set."""
    user_msg = ""
    for m in reversed(messages):
        if m["role"] == "user":
            user_msg = m["content"]
            break

    return {
        "choices": [
            {
                "message": {
                    "content": (
                        f"[Mock response from {nvidia_model}] "
                        f"You asked: '{user_msg[:80]}' — "
                        f"This is a simulated response demonstrating the proxy translation layer. "
                        f"In production, this would come from NVIDIA NIM."
                    )
                }
            }
        ],
        "usage": {"prompt_tokens": len(user_msg.split()), "completion_tokens": 42},
    }


@app.route("/v1/messages", methods=["POST"])
def messages():
    """Main proxy endpoint — accepts Anthropic format, returns Anthropic format."""
    start = time.time()
    body = request.get_json(force=True)

    openai_body, nvidia_model = translate_request(body)

    if MOCK_MODE:
        openai_resp = mock_response(nvidia_model, openai_body["messages"])
        status_code = 200
    else:
        import requests as http_requests

        resp = http_requests.post(
            NVIDIA_BASE_URL,
            json=openai_body,
            headers={
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=60,
        )
        status_code = resp.status_code
        if status_code != 200:
            stats["errors"] += 1
            return jsonify({"error": resp.text}), status_code
        openai_resp = resp.json()

    latency = time.time() - start
    anthropic_resp = translate_response(openai_resp, nvidia_model)

    # Record stats
    stats["total"] += 1
    stats["requests"].append(
        {
            "time": time.time(),
            "model": nvidia_model,
            "latency": round(latency, 3),
            "input_tokens": anthropic_resp["usage"]["input_tokens"],
            "output_tokens": anthropic_resp["usage"]["output_tokens"],
        }
    )
    # Keep only last 1000 entries
    if len(stats["requests"]) > 1000:
        stats["requests"] = stats["requests"][-500:]

    print(
        f"[REQUEST] {body.get('model','?')} -> {nvidia_model} | "
        f"{status_code} | {latency:.2f}s | "
        f"tokens: {anthropic_resp['usage']['input_tokens']}+{anthropic_resp['usage']['output_tokens']}"
    )

    return jsonify(anthropic_resp), 200


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Real-time analytics dashboard."""
    from dashboard import render_dashboard

    return render_dashboard(stats)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "mock_mode": MOCK_MODE, "total_requests": stats["total"]})


if __name__ == "__main__":
    mode = "MOCK (no NVIDIA_API_KEY)" if MOCK_MODE else "LIVE"
    print(f"[PROXY] nvidia_claude_proxy starting in {mode} mode")
    print(f"[PROXY] Listening on http://localhost:8082")
    print(f"[PROXY] Dashboard: http://localhost:8082/dashboard")
    app.run(host="0.0.0.0", port=8082, debug=False)
