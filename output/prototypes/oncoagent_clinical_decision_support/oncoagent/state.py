"""AgentState definition for the OncoAgent pipeline."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AgentState:
    patient_id: str = ""
    query: str = ""
    redacted_query: str = ""
    complexity_score: float = 0.0
    selected_tier: int = 1
    rag_documents: List[dict] = field(default_factory=list)
    rag_confidence: float = 0.0
    specialist_output: str = ""
    critic_feedback: str = ""
    critic_pass: bool = False
    retry_count: int = 0
    max_retries: int = 2
    final_output: str = ""
    audit_log: List[str] = field(default_factory=list)

    def log(self, msg: str):
        self.audit_log.append(msg)
