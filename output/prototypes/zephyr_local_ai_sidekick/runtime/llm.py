"""Mock local LLM orchestration layer.

Simulates a local model inference pipeline (e.g. llama.cpp / Ollama)
so the demo runs without any real model or API key.
"""

import time
import random

MOCK_RESPONSES = {
    "greeting": "Hello! I'm Zephyr, your local-first AI sidekick. How can I help?",
    "summarize": "Here's a concise summary of the provided content, highlighting the key points and action items.",
    "code_review": "I've reviewed the code. It looks clean overall. Consider adding error handling around the DB call on line 42.",
    "rag_answer": "Based on the retrieved documents, the answer is: {context}",
    "fallback": "I understand your request. Let me think about that using my local reasoning capabilities.",
}

_THINKING_PHRASES = [
    "Reasoning locally...",
    "Consulting local model...",
    "Processing with on-device inference...",
]


class LocalLLM:
    """Simulates a local LLM with latency and token counting."""

    def __init__(self, model_name: str = "mock-7b-q4"):
        self.model_name = model_name
        self.total_tokens = 0

    def generate(self, prompt: str, context: str = "") -> dict:
        thinking = random.choice(_THINKING_PHRASES)
        time.sleep(random.uniform(0.05, 0.15))  # simulate inference

        # Pick a response based on keywords
        lower = prompt.lower()
        if any(w in lower for w in ("hello", "hi", "hey")):
            text = MOCK_RESPONSES["greeting"]
        elif "summar" in lower:
            text = MOCK_RESPONSES["summarize"]
        elif "review" in lower or "code" in lower:
            text = MOCK_RESPONSES["code_review"]
        elif context:
            text = MOCK_RESPONSES["rag_answer"].format(
                context=context[:120] + "..." if len(context) > 120 else context
            )
        else:
            text = MOCK_RESPONSES["fallback"]

        tokens_used = len(prompt.split()) + len(text.split())
        self.total_tokens += tokens_used

        return {
            "model": self.model_name,
            "thinking": thinking,
            "response": text,
            "tokens": tokens_used,
            "total_tokens": self.total_tokens,
        }
