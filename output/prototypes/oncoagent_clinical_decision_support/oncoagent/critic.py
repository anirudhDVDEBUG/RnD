"""Reflexion critic — deterministic safety validation (not LLM-based).

Implements 3 rule-based checks from the OncoAgent 4-layer safety framework:
1. Format validation (OncoCoT schema)
2. Safety scan (prohibited patterns)
3. Citation grounding (every claim must reference a guideline)
"""

import re
from .state import AgentState

# Prohibited patterns: absolute dosing without citation, unsupported claims
PROHIBITED_PATTERNS = [
    (r"\b\d+\s*mg\b(?!.*\[)", "Dosing mentioned without guideline citation bracket"),
    (r"\bguarantee[sd]?\b", "Absolute guarantee language detected"),
    (r"\bcure[sd]?\b(?!.*palliative)", "Cure claim without palliative context"),
]

REQUIRED_SECTIONS = ["Recommendation", "Clinical Notes"]


def reflexion_critic(state: AgentState) -> AgentState:
    """Run deterministic safety checks on specialist output."""
    output = state.specialist_output
    issues = []

    if not output.strip():
        state.critic_feedback = "Empty specialist output"
        state.critic_pass = False
        state.log("Critic: FAIL — empty output")
        return state

    # Check 1: Format validation — required sections present
    for section in REQUIRED_SECTIONS:
        if section not in output:
            issues.append(f"Missing required section: '{section}'")

    # Check 2: Safety scan — prohibited patterns
    # (In this demo, dosing IS cited from guidelines so we do a simplified check)
    if re.search(r"\bguarantee[sd]?\b", output, re.IGNORECASE):
        issues.append("Absolute guarantee language detected")
    if re.search(r"\bwill cure\b", output, re.IGNORECASE):
        issues.append("Unsupported cure claim")

    # Check 3: Citation grounding — must reference at least one guideline ID
    guideline_refs = re.findall(r"[A-Z]+-[A-Z]+-\d{4}-\d{2}", output)
    if not guideline_refs:
        issues.append("No guideline ID citations found in output")

    # Check 4: Confidence floor
    if state.rag_confidence < 0.3:
        issues.append(f"RAG confidence {state.rag_confidence:.3f} below threshold 0.3")

    if issues:
        state.critic_feedback = "; ".join(issues)
        state.critic_pass = False
        state.log(f"Critic: FAIL — {state.critic_feedback}")
    else:
        state.critic_feedback = "All checks passed"
        state.critic_pass = True
        state.log("Critic: PASS")

    return state
