"""OncoAgent graph orchestrator — executes the 8-node pipeline.

Implements a lightweight state-machine that mirrors a LangGraph StateGraph
without requiring the langgraph dependency (keeping the demo self-contained).
"""

from .state import AgentState
from .redaction import redact_phi
from .router import complexity_router
from .rag import corrective_rag_pipeline
from .specialist import specialist_node
from .critic import reflexion_critic


def ingest_and_redact(state: AgentState) -> AgentState:
    """Layer 1 safety: strip PHI before any processing."""
    state.redacted_query = redact_phi(state.query)
    state.log(f"Ingestion: redacted query length {len(state.redacted_query)}")
    return state


def hitl_gate(state: AgentState) -> AgentState:
    """Human-in-the-loop gate — in production, pauses for physician review.
    In demo mode, auto-approves with a log entry."""
    state.log("HITL Gate: auto-approved (demo mode — would pause for physician review)")
    return state


def format_output(state: AgentState) -> AgentState:
    """Final formatting node."""
    state.final_output = state.specialist_output
    state.log("Formatter: output finalized")
    return state


def safe_refusal(state: AgentState) -> AgentState:
    """Fallback node — safe refusal when confidence is too low or critic fails."""
    state.final_output = (
        "## Unable to Provide Recommendation\n\n"
        "The system could not generate a sufficiently grounded recommendation "
        "for this query. This may be due to:\n"
        "- Insufficient matching guidelines in the knowledge base\n"
        "- Low retrieval confidence\n"
        "- Safety validation failure\n\n"
        f"**Critic feedback:** {state.critic_feedback}\n\n"
        "*Please consult a specialist oncologist directly for this case.*"
    )
    state.log(f"Fallback: safe refusal — {state.critic_feedback}")
    return state


def run_pipeline(query: str, patient_id: str = "DEMO-001") -> AgentState:
    """Execute the full OncoAgent pipeline.

    Graph topology:
        Router → Ingestion → Corrective RAG → Specialist ↔ Critic → HITL Gate → Formatter → END
                                                                ↓
                                                             Fallback → END
    """
    state = AgentState(patient_id=patient_id, query=query)
    state.log(f"Pipeline START — patient_id={patient_id}")

    # Node 1: Router
    state = complexity_router(state)

    # Node 2: Ingestion + PHI Redaction
    state = ingest_and_redact(state)

    # Node 3: Corrective RAG
    state = corrective_rag_pipeline(state)

    # Early exit if RAG found nothing
    if state.rag_confidence == 0.0:
        state = safe_refusal(state)
        state.log("Pipeline END (early — no evidence)")
        return state

    # Specialist ↔ Critic loop (with retry)
    while state.retry_count <= state.max_retries:
        # Node 4: Specialist
        state = specialist_node(state)

        # Node 5: Critic
        state = reflexion_critic(state)

        if state.critic_pass:
            break
        state.retry_count += 1
        state.log(f"Retry {state.retry_count}/{state.max_retries}")

    if not state.critic_pass:
        # Node 8: Fallback
        state = safe_refusal(state)
        state.log("Pipeline END (fallback)")
        return state

    # Node 6: HITL Gate
    state = hitl_gate(state)

    # Node 7: Formatter
    state = format_output(state)

    state.log("Pipeline END (success)")
    return state
