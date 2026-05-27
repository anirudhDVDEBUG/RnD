"""Mock policy documents and vendor interest mappings for demonstration."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PolicyDocument:
    title: str
    institution: str
    date: str
    excerpts: List[str]
    known_advisors: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class VendorProfile:
    name: str
    architecture: str
    key_constraints: List[str]
    lobbying_channels: List[str]
    preferred_framings: List[str]


VENDOR_PROFILES = [
    VendorProfile(
        name="Anthropic",
        architecture="Constitutional AI with RLHF",
        key_constraints=[
            "value alignment through training",
            "bounded autonomy",
            "transparency of reasoning",
            "human oversight requirements",
            "interpretability as safety",
        ],
        lobbying_channels=[
            "direct advisory to policymakers",
            "published safety research",
            "academic partnerships",
            "institutional relationships (Vatican, OECD)",
        ],
        preferred_framings=[
            "AI safety as existential priority",
            "alignment is a technical problem with technical solutions",
            "responsible scaling",
            "constitutional constraints as ethical architecture",
        ],
    ),
    VendorProfile(
        name="OpenAI",
        architecture="GPT-series with RLHF and moderation layers",
        key_constraints=[
            "content filtering",
            "usage policies",
            "iterative deployment",
            "red-teaming before release",
            "capability thresholds",
        ],
        lobbying_channels=[
            "government testimony",
            "media presence",
            "partnership with Microsoft",
            "safety board publications",
        ],
        preferred_framings=[
            "AGI benefits for all of humanity",
            "iterative deployment as responsible approach",
            "frontier model governance",
            "international coordination on AI safety",
        ],
    ),
    VendorProfile(
        name="Google DeepMind",
        architecture="Gemini multi-modal with safety filters",
        key_constraints=[
            "multi-modal integration",
            "search grounding",
            "factuality requirements",
            "enterprise compliance",
            "data provenance",
        ],
        lobbying_channels=[
            "standards bodies (ISO, NIST)",
            "academic funding",
            "government contracts",
            "industry consortia",
        ],
        preferred_framings=[
            "AI should be grounded in factual information",
            "multi-modal understanding as completeness",
            "enterprise-grade safety",
            "open ecosystem with guardrails",
        ],
    ),
    VendorProfile(
        name="Meta AI",
        architecture="Llama open-weight models",
        key_constraints=[
            "open weights distribution",
            "community-driven safety",
            "permissive licensing",
            "hardware democratization",
        ],
        lobbying_channels=[
            "open source community",
            "academic releases",
            "developer advocacy",
            "anti-regulation lobbying",
        ],
        preferred_framings=[
            "openness as safety",
            "democratized access prevents concentration",
            "community oversight over corporate oversight",
            "regulation stifles innovation",
        ],
    ),
]

POLICY_DOCUMENTS = [
    PolicyDocument(
        title="Magnifica Humanitas",
        institution="Vatican (Papal Encyclical)",
        date="2026-05",
        excerpts=[
            "Artificial intelligence must possess intrinsic value alignment, not merely behavioral compliance.",
            "The bounded autonomy of machine intelligence reflects the theological principle that freedom exists within divine order.",
            "Transparency of reasoning — the capacity for an artificial mind to show its work — constitutes a moral obligation, not merely a technical feature.",
            "Human oversight of artificial intelligence is not a constraint but a sacred trust.",
            "The interpretability of machine decisions mirrors the requirement for moral agents to examine their conscience.",
        ],
        known_advisors=["Christopher Olah (Anthropic co-founder)"],
        metadata={
            "context": "First papal encyclical specifically addressing AI ethics",
            "reception": "Widely praised by AI safety community; criticized by open-source advocates",
        },
    ),
    PolicyDocument(
        title="EU AI Act Amendment 2026.3 — Foundation Model Obligations",
        institution="European Parliament",
        date="2026-03",
        excerpts=[
            "Foundation model providers must demonstrate iterative safety testing prior to deployment.",
            "Models exceeding compute thresholds require mandatory red-team evaluation.",
            "Providers must maintain capability registries with defined escalation thresholds.",
            "Frontier models require international coordination before release.",
        ],
        known_advisors=["OpenAI policy team (testified March 2026)"],
        metadata={
            "context": "Amendment to original EU AI Act targeting frontier models",
            "reception": "Supported by incumbent labs; opposed by open-source community and startups",
        },
    ),
    PolicyDocument(
        title="NIST AI 600-2: Generative AI Safety Framework",
        institution="US National Institute of Standards and Technology",
        date="2026-01",
        excerpts=[
            "Generative AI systems should be grounded in verifiable factual information.",
            "Multi-modal AI systems present unique risks requiring integrated safety assessment.",
            "Enterprise deployment requires compliance with data provenance standards.",
            "AI outputs must be traceable to training data sources.",
        ],
        known_advisors=["Google DeepMind research staff (framework contributors)"],
        metadata={
            "context": "Extension of NIST AI RMF for generative models",
            "reception": "Adopted by federal agencies; industry compliance varies",
        },
    ),
]

# Keyword-to-vendor mapping for the demo analyzer
TERM_VENDOR_MAP = {
    "value alignment": "Anthropic",
    "constitutional": "Anthropic",
    "bounded autonomy": "Anthropic",
    "interpretability": "Anthropic",
    "transparency of reasoning": "Anthropic",
    "human oversight": "Anthropic",
    "responsible scaling": "Anthropic",
    "iterative deployment": "OpenAI",
    "iterative safety": "OpenAI",
    "red-team": "OpenAI",
    "capability threshold": "OpenAI",
    "frontier model": "OpenAI",
    "international coordination": "OpenAI",
    "content filtering": "OpenAI",
    "grounded in": "Google DeepMind",
    "factual information": "Google DeepMind",
    "multi-modal": "Google DeepMind",
    "data provenance": "Google DeepMind",
    "enterprise": "Google DeepMind",
    "traceable": "Google DeepMind",
    "open weights": "Meta AI",
    "democratize": "Meta AI",
    "community oversight": "Meta AI",
    "open source": "Meta AI",
    "permissive": "Meta AI",
}

STRATEGY_DEFINITIONS = {
    "Limitation Laundering": "Reframing technical constraints as ethical choices",
    "Safety Capture": "Defining 'safe AI' to match one's own architecture",
    "Standards Setting": "Getting your approach codified before competitors catch up",
    "Institutional Blessing": "Securing endorsement from trusted authorities (religious, academic, governmental)",
}
