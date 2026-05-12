"""Cognitive engine: multi-step reasoning via Gemini or mock."""
import random

MOCK_RESPONSES = {
    "default": [
        "I've analyzed the situation step by step. {context_note}Based on my reasoning, here's what I recommend: break the problem into smaller components, address each systematically, and validate results.",
        "After careful consideration and multi-step analysis, {context_note}I believe the optimal approach involves identifying key constraints first, then exploring solution paths that satisfy all requirements.",
        "Running cognitive analysis... {context_note}My reasoning chain suggests we should prioritize the most impactful factors and work outward from there. I've stored this insight for future reference.",
    ],
    "memory": [
        "I recall our previous discussions. {context_note}Building on that context, I can provide a more informed perspective now.",
    ],
    "plan": [
        "Let me decompose this into actionable steps: 1) Define the objective clearly, 2) Identify required resources, 3) Execute in priority order, 4) Validate each milestone. {context_note}",
    ],
    "security": [
        "From a defensive security perspective, {context_note}I recommend: audit access controls, monitor for anomalies, keep systems patched, and maintain incident response procedures.",
    ],
}


class CognitiveEngine:
    def __init__(self, memory_manager, api_key: str = ""):
        self.memory = memory_manager
        self.api_key = api_key
        self.use_api = bool(api_key)
        self.model = None
        if self.use_api:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-pro")
            except ImportError:
                self.use_api = False

    def think(self, user_input: str) -> str:
        context = self.memory.get_relevant_context(user_input)
        if self.use_api and self.model:
            return self._think_api(user_input, context)
        return self._think_mock(user_input, context)

    def _think_api(self, user_input: str, context: str) -> str:
        prompt = (
            f"You are FRIDAY, an autonomous cognitive AI operating system.\n"
            f"Context from memory: {context}\n"
            f"User: {user_input}\n"
            f"Reason step-by-step, then respond concisely."
        )
        response = self.model.generate_content(prompt)
        result = response.text
        self.memory.store(user_input, result)
        return result

    def _think_mock(self, user_input: str, context: str) -> str:
        lower = user_input.lower()
        context_note = ""
        if "(no" not in context:
            context_note = "Drawing on prior context, "

        if any(w in lower for w in ["plan", "step", "how to", "decompose"]):
            pool = MOCK_RESPONSES["plan"]
        elif any(w in lower for w in ["security", "scan", "defend", "threat"]):
            pool = MOCK_RESPONSES["security"]
        elif any(w in lower for w in ["remember", "recall", "previous"]):
            pool = MOCK_RESPONSES["memory"]
        else:
            pool = MOCK_RESPONSES["default"]

        result = random.choice(pool).format(context_note=context_note)
        self.memory.store(user_input, result)
        return result

    def self_reflect(self) -> str:
        stats = self.memory.get_stats()
        return (
            f"Self-reflection: {stats['total_memories']} memories stored, "
            f"{stats['session_memories']} this session. "
            f"Cognitive engine: {'Gemini API' if self.use_api else 'mock mode'}."
        )
