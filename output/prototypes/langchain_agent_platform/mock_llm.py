"""Mock LLM for demo purposes — no API key needed."""

from typing import Any, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.embeddings import Embeddings
import hashlib
import struct


# Canned responses keyed by substring matching
RESPONSES = {
    "decorators": (
        "Decorators are functions that modify the behavior of other functions or classes. "
        "They use the @decorator syntax and are commonly used for logging, authentication, "
        "caching, and access control. A decorator wraps a function, adding functionality "
        "before or after the original function executes."
    ),
    "42 * 17": "42 * 17 = 714",
    "calculator": "I'll calculate that for you. The answer is 714.",
    "langchain": (
        "LangChain is an agent engineering platform for composing LLMs, tools, and retrieval "
        "into production-ready applications. It provides LCEL for declarative chain composition, "
        "tool-calling agents, RAG pipelines, and structured output parsing."
    ),
    "inception": (
        '{"title": "Inception", "rating": 9, "summary": "A mind-bending thriller about '
        'dream infiltration, featuring stunning visuals and a complex narrative that keeps '
        'you questioning reality."}'
    ),
}


class MockChatModel(BaseChatModel):
    """A mock chat model that returns canned responses for demo purposes."""

    model_name: str = "mock-model"

    @property
    def _llm_type(self) -> str:
        return "mock-chat-model"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Get the last human message content
        last_msg = messages[-1].content.lower() if messages else ""

        # Find matching canned response
        response_text = "I understand your question. Here is a helpful response."
        for key, value in RESPONSES.items():
            if key in last_msg:
                response_text = value
                break

        message = AIMessage(content=response_text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])


class MockEmbeddings(Embeddings):
    """Deterministic fake embeddings for reproducible demos."""

    dimensions: int = 64

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)

    def _embed(self, text: str) -> List[float]:
        # Deterministic hash-based embedding
        h = hashlib.sha256(text.encode()).digest()
        # Convert bytes to floats in [-1, 1]
        floats = []
        for i in range(0, min(len(h), self.dimensions * 4), 4):
            val = struct.unpack("f", h[i : i + 4])[0]
            # Normalize to [-1, 1]
            floats.append(max(-1.0, min(1.0, val / 1e38)))
        # Pad if needed
        while len(floats) < self.dimensions:
            floats.append(0.0)
        return floats[: self.dimensions]
