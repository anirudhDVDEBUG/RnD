"""Specialist node — generates structured clinical recommendations from RAG context.

In production this calls the on-premises LLM. Here we use template-based generation.
"""

from .state import AgentState


def specialist_node(state: AgentState) -> AgentState:
    """Generate a structured OncoCoT recommendation from retrieved guidelines."""
    if not state.rag_documents:
        state.specialist_output = ""
        state.log("Specialist: no RAG documents — skipping")
        return state

    top_doc = state.rag_documents[0]
    supporting = state.rag_documents[1:] if len(state.rag_documents) > 1 else []

    # Build structured OncoCoT output
    sections = []
    sections.append(f"## Clinical Recommendation (Tier {state.selected_tier})")
    sections.append("")
    sections.append(f"**Primary Guideline:** {top_doc['title']}")
    sections.append(f"**Guideline ID:** {top_doc['id']}")
    sections.append("")
    sections.append("### Recommendation")
    sections.append(top_doc["content"])
    sections.append("")

    if supporting:
        sections.append("### Supporting Evidence")
        for i, doc in enumerate(supporting, 1):
            sections.append(f"{i}. [{doc['id']}] {doc['title']}")
            sections.append(f"   {doc['content'][:200]}...")
            sections.append("")

    sections.append("### Clinical Notes")
    sections.append(f"- Complexity Score: {state.complexity_score:.2f}")
    sections.append(f"- RAG Confidence: {state.rag_confidence:.3f}")
    sections.append(f"- Model Tier: {state.selected_tier}")
    sections.append(f"- Documents Retrieved: {len(state.rag_documents)}")
    sections.append("")
    sections.append("*This is a decision-support tool. All recommendations require "
                     "physician review before clinical action.*")

    state.specialist_output = "\n".join(sections)
    state.log("Specialist: generated structured recommendation")
    return state
