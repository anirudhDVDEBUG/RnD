"""Dual-tier complexity router — triages cases to Tier 1 (fast) or Tier 2 (deep reasoning)."""

from .state import AgentState

RARE_CANCERS = {
    "cholangiocarcinoma", "mesothelioma", "thymoma", "adrenocortical",
    "gastrointestinal_stromal", "neuroendocrine", "sarcoma",
}


def compute_complexity(case: dict) -> float:
    """Weighted complexity score (0.0 – 1.0) based on clinical features."""
    score = 0.0

    # Cancer type weighting
    cancer = case.get("cancer_type", "").lower()
    if cancer in RARE_CANCERS:
        score += 0.40
    elif cancer == "unknown_primary":
        score += 0.30

    # Stage weighting
    stage = case.get("stage", "").upper()
    if stage == "IV":
        score += 0.25
    elif stage == "III":
        score += 0.15

    # Mutation complexity
    mutations = case.get("mutations", [])
    if len(mutations) >= 2:
        score += 0.30
    elif len(mutations) == 1:
        score += 0.15

    # Prior treatment (recurrent/refractory cases are harder)
    if case.get("prior_treatment"):
        score += 0.10

    return min(score, 1.0)


def complexity_router(state: AgentState) -> AgentState:
    """Route to Tier 1 (< 0.5) or Tier 2 (>= 0.5)."""
    case = {
        "cancer_type": _extract_cancer_type(state.query),
        "stage": _extract_stage(state.query),
        "mutations": _extract_mutations(state.query),
        "prior_treatment": "prior" in state.query.lower() or "second-line" in state.query.lower(),
    }
    score = compute_complexity(case)
    tier = 2 if score >= 0.5 else 1
    state.complexity_score = score
    state.selected_tier = tier
    state.log(f"Router: complexity={score:.2f} → Tier {tier}")
    return state


def _extract_cancer_type(query: str) -> str:
    q = query.lower()
    for cancer in ["nsclc", "breast", "colorectal", "colon", "melanoma",
                    "pancreatic", "lung", "ovarian", "prostate",
                    *RARE_CANCERS]:
        if cancer in q:
            return cancer
    return "unknown"


def _extract_stage(query: str) -> str:
    q = query.upper()
    for stage in ["IV", "III", "II", "I"]:
        if f"STAGE {stage}" in q:
            return stage
    return ""


def _extract_mutations(query: str) -> list:
    q = query.lower()
    known = ["egfr", "alk", "braf", "kras", "her2", "brca", "ros1",
             "ntrk", "met", "ret", "pd-l1", "msi-h", "ras"]
    return [m for m in known if m in q]
