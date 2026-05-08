"""
Parloa-style Voice Service Agent — core engine.

Implements a dialogue-flow-driven agent with mock STT/TTS, LLM orchestration,
and backend tool calling for customer service scenarios.
"""

import json
import random
import time
import yaml
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Turn:
    role: str          # "customer" or "agent"
    text: str
    intent: Optional[str] = None
    tool_used: Optional[str] = None
    confidence: float = 1.0
    latency_ms: float = 0.0


@dataclass
class ConversationMetrics:
    turns: int = 0
    intents_detected: int = 0
    tools_invoked: int = 0
    escalations: int = 0
    avg_latency_ms: float = 0.0
    resolved: bool = False
    total_latency_ms: float = 0.0

    def record_turn(self, latency_ms: float):
        self.turns += 1
        self.total_latency_ms += latency_ms
        self.avg_latency_ms = self.total_latency_ms / self.turns


# ---------------------------------------------------------------------------
# Mock STT / TTS
# ---------------------------------------------------------------------------

class MockSTT:
    """Simulates speech-to-text with realistic latency."""

    def transcribe(self, audio_input: str) -> tuple[str, float]:
        latency = random.uniform(50, 150)
        return audio_input, latency  # pass-through for simulation


class MockTTS:
    """Simulates text-to-speech with realistic latency."""

    def synthesize(self, text: str) -> tuple[str, float]:
        latency = random.uniform(80, 200)
        return f"[AUDIO] {text}", latency


# ---------------------------------------------------------------------------
# Backend Tools (mock CRM / KB / ticketing)
# ---------------------------------------------------------------------------

MOCK_ACCOUNTS = {
    "ACC-1001": {"name": "Jane Doe", "plan": "Premium", "balance": 142.50, "status": "active"},
    "ACC-1002": {"name": "John Smith", "plan": "Basic", "balance": 0.00, "status": "active"},
    "ACC-1003": {"name": "Alice Wang", "plan": "Enterprise", "balance": 1280.00, "status": "suspended"},
}

MOCK_KB = {
    "password_reset": "To reset your password, visit Settings > Security > Reset Password, or click the link in your confirmation email.",
    "billing_cycle": "Billing occurs on the 1st of each month. Changes mid-cycle are prorated.",
    "api_limits": "Free tier: 1K req/day. Basic: 10K. Premium: 100K. Enterprise: unlimited.",
    "outage_info": "We experienced a brief outage on 2026-05-06 affecting EU-West. All services restored.",
}

MOCK_TICKETS = {}
_ticket_counter = 3000


class BackendTools:
    """Simulated backend systems the agent can call."""

    def lookup_account(self, account_id: str) -> dict:
        if account_id in MOCK_ACCOUNTS:
            return {"status": "found", "account": MOCK_ACCOUNTS[account_id]}
        return {"status": "not_found", "error": f"No account {account_id}"}

    def get_invoice(self, account_id: str) -> dict:
        acct = MOCK_ACCOUNTS.get(account_id)
        if not acct:
            return {"status": "not_found"}
        return {
            "status": "ok",
            "invoice": {
                "account": account_id,
                "amount": acct["balance"],
                "due_date": "2026-06-01",
                "plan": acct["plan"],
            },
        }

    def search_kb(self, query: str) -> dict:
        query_lower = query.lower()
        for key, answer in MOCK_KB.items():
            if key.replace("_", " ") in query_lower or any(w in query_lower for w in key.split("_")):
                return {"status": "found", "article": key, "content": answer}
        return {"status": "no_match", "suggestion": "Try rephrasing or contact a specialist."}

    def create_ticket(self, subject: str, description: str) -> dict:
        global _ticket_counter
        _ticket_counter += 1
        tid = f"TKT-{_ticket_counter}"
        MOCK_TICKETS[tid] = {"subject": subject, "description": description, "state": "open"}
        return {"status": "created", "ticket_id": tid}

    def check_ticket_status(self, ticket_id: str) -> dict:
        if ticket_id in MOCK_TICKETS:
            return {"status": "ok", "ticket": MOCK_TICKETS[ticket_id]}
        return {"status": "not_found"}


# ---------------------------------------------------------------------------
# Intent Detection (keyword-based mock, would be LLM in production)
# ---------------------------------------------------------------------------

INTENT_KEYWORDS = {
    "billing": ["bill", "invoice", "charge", "payment", "balance", "price", "cost", "plan"],
    "technical": ["error", "bug", "broken", "not working", "issue", "outage", "down", "crash", "password", "reset", "api", "limit"],
    "account": ["account", "profile", "suspend", "cancel", "upgrade"],
    "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
    "farewell": ["bye", "goodbye", "thanks", "thank you", "that's all"],
}


def detect_intent(text: str) -> tuple[str, float]:
    text_lower = text.lower()
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[intent] = score
    if not scores:
        return "unknown", 0.3
    best = max(scores, key=scores.get)
    confidence = min(1.0, scores[best] / 3.0)
    return best, round(confidence, 2)


# ---------------------------------------------------------------------------
# Agent Core
# ---------------------------------------------------------------------------

class VoiceServiceAgent:
    """
    Orchestrates an end-to-end voice service conversation.

    Pipeline: STT -> Intent Detection -> Flow Router -> Tool Use -> Response Gen -> TTS
    """

    def __init__(self, flows_path: str = "flows.yaml", persona: Optional[dict] = None):
        self.stt = MockSTT()
        self.tts = MockTTS()
        self.tools = BackendTools()
        self.flows = self._load_flows(flows_path)
        self.persona = persona or {
            "name": "Nova",
            "tone": "friendly and professional",
            "language": "en",
        }
        self.history: list[Turn] = []
        self.metrics = ConversationMetrics()
        self.current_flow: Optional[str] = None
        self.context: dict = {}  # conversation context (extracted entities, etc.)
        self.unresolved_attempts = 0

    def _load_flows(self, path: str) -> dict:
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            return data.get("flows", {})
        except FileNotFoundError:
            return self._default_flows()

    @staticmethod
    def _default_flows() -> dict:
        return {
            "greeting": {"transitions": {"billing": "billing_flow", "technical": "tech_support_flow", "account": "account_flow"}},
            "billing_flow": {"tools": ["lookup_account", "get_invoice"], "escalation_threshold": 0.7},
            "tech_support_flow": {"tools": ["search_kb", "create_ticket", "check_ticket_status"], "escalation_threshold": 0.7, "max_attempts": 3},
            "account_flow": {"tools": ["lookup_account"], "escalation_threshold": 0.7},
        }

    def process_input(self, customer_text: str) -> Turn:
        """Full pipeline: STT -> detect intent -> route -> act -> respond -> TTS."""
        t0 = time.perf_counter()

        # STT
        transcribed, stt_lat = self.stt.transcribe(customer_text)

        # Record customer turn
        intent, confidence = detect_intent(transcribed)
        self.history.append(Turn(role="customer", text=transcribed, intent=intent, confidence=confidence))
        self.metrics.intents_detected += 1

        # Route to flow
        response_text, tool_used = self._route_and_act(intent, confidence, transcribed)

        # TTS
        audio_out, tts_lat = self.tts.synthesize(response_text)

        total_lat = (time.perf_counter() - t0) * 1000 + stt_lat + tts_lat
        self.metrics.record_turn(total_lat)

        agent_turn = Turn(
            role="agent",
            text=response_text,
            intent=intent,
            tool_used=tool_used,
            confidence=confidence,
            latency_ms=round(total_lat, 1),
        )
        self.history.append(agent_turn)
        return agent_turn

    def _route_and_act(self, intent: str, confidence: float, text: str) -> tuple[str, Optional[str]]:
        # Farewell
        if intent == "farewell":
            self.metrics.resolved = True
            return f"Thank you for contacting us! If you need anything else, don't hesitate to call back. Have a great day!", None

        # Greeting
        if intent == "greeting" and self.current_flow is None:
            self.current_flow = "greeting"
            return (
                f"Hello! I'm {self.persona['name']}, your virtual assistant. "
                f"I can help with billing, technical issues, or account questions. How can I assist you today?"
            ), None

        # Check escalation
        flow_config = self.flows.get(self.current_flow or "", {})
        threshold = flow_config.get("escalation_threshold", 0.7)
        max_attempts = flow_config.get("max_attempts", 3)

        if confidence < threshold and intent == "unknown":
            self.unresolved_attempts += 1
            if self.unresolved_attempts >= max_attempts:
                self.metrics.escalations += 1
                return "I want to make sure you get the best help. Let me transfer you to a specialist who can assist further. Please hold.", None
            return "I'm not quite sure I understood. Could you rephrase your question? I can help with billing, technical support, or account management.", None

        # Route to specific flow
        self.unresolved_attempts = 0
        if intent == "billing":
            self.current_flow = "billing_flow"
            return self._handle_billing(text)
        elif intent == "technical":
            self.current_flow = "tech_support_flow"
            return self._handle_tech_support(text)
        elif intent == "account":
            self.current_flow = "account_flow"
            return self._handle_account(text)
        else:
            return "I can help with billing, technical support, or account inquiries. Which area do you need help with?", None

    def _extract_account_id(self, text: str) -> Optional[str]:
        """Try to find an account ID in the text or context."""
        import re
        match = re.search(r'ACC-\d+', text, re.IGNORECASE)
        if match:
            aid = match.group(0).upper()
            self.context["account_id"] = aid
            return aid
        return self.context.get("account_id")

    def _handle_billing(self, text: str) -> tuple[str, Optional[str]]:
        account_id = self._extract_account_id(text)
        if not account_id:
            # Try with a default for demo
            account_id = "ACC-1001"
            self.context["account_id"] = account_id

        if any(w in text.lower() for w in ["invoice", "bill", "charge"]):
            result = self.tools.get_invoice(account_id)
            self.metrics.tools_invoked += 1
            if result["status"] == "ok":
                inv = result["invoice"]
                return (
                    f"I found your invoice. Your {inv['plan']} plan has a balance of "
                    f"${inv['amount']:.2f}, due on {inv['due_date']}. "
                    f"Would you like to make a payment or have any other questions?"
                ), "get_invoice"

        result = self.tools.lookup_account(account_id)
        self.metrics.tools_invoked += 1
        if result["status"] == "found":
            acct = result["account"]
            return (
                f"I've pulled up the account for {acct['name']}. "
                f"You're on the {acct['plan']} plan with a balance of ${acct['balance']:.2f}. "
                f"How can I help with your billing today?"
            ), "lookup_account"
        return "I wasn't able to locate that account. Could you provide your account ID?", "lookup_account"

    def _handle_tech_support(self, text: str) -> tuple[str, Optional[str]]:
        # Search knowledge base first
        kb_result = self.tools.search_kb(text)
        self.metrics.tools_invoked += 1
        if kb_result["status"] == "found":
            return (
                f"I found an article that should help: {kb_result['content']} "
                f"Does this resolve your issue?"
            ), "search_kb"

        # Create a ticket if KB didn't help
        ticket = self.tools.create_ticket(
            subject="Customer reported issue",
            description=text,
        )
        self.metrics.tools_invoked += 1
        return (
            f"I've created support ticket {ticket['ticket_id']} for your issue. "
            f"Our team will investigate and follow up within 24 hours. "
            f"Is there anything else I can help with?"
        ), "create_ticket"

    def _handle_account(self, text: str) -> tuple[str, Optional[str]]:
        account_id = self._extract_account_id(text)
        if not account_id:
            account_id = "ACC-1001"
            self.context["account_id"] = account_id

        result = self.tools.lookup_account(account_id)
        self.metrics.tools_invoked += 1
        if result["status"] == "found":
            acct = result["account"]
            return (
                f"Your account ({account_id}) is currently {acct['status']} on the {acct['plan']} plan. "
                f"Would you like to upgrade, modify, or cancel your account?"
            ), "lookup_account"
        return "I couldn't find that account. Could you verify your account ID?", "lookup_account"

    def get_summary(self) -> dict:
        return {
            "persona": self.persona["name"],
            "total_turns": self.metrics.turns,
            "intents_detected": self.metrics.intents_detected,
            "tools_invoked": self.metrics.tools_invoked,
            "escalations": self.metrics.escalations,
            "avg_latency_ms": round(self.metrics.avg_latency_ms, 1),
            "resolved": self.metrics.resolved,
        }
