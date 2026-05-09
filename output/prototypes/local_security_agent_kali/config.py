"""Configuration for the local security agent."""

import os

# LM Studio endpoint (OpenAI-compatible)
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:1234/v1")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "lm-studio")
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen2.5-7b")
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.3"))

# Agent settings
MAX_STEPS = int(os.environ.get("MAX_STEPS", "10"))
TOOL_TIMEOUT = int(os.environ.get("TOOL_TIMEOUT", "300"))

# Mock mode — set to "1" to run without LM Studio / real tools
MOCK_MODE = os.environ.get("MOCK_MODE", "0") == "1"
