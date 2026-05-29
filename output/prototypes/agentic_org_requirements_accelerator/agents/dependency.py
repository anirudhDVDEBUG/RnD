"""Dependency Mapping Agent: Identify dependencies, conflicts, and gaps."""

from typing import Dict, List, Tuple
from intake import Requirement

# Keyword groups that indicate related requirements
DEPENDENCY_GROUPS = {
    "auth": ["login", "authentication", "token", "session", "permission", "admin"],
    "payment": ["checkout", "payment", "stripe", "paypal", "apple pay", "cart", "order"],
    "data": ["database", "encrypted", "data", "storage", "cache", "analytics"],
    "ui": ["dashboard", "page", "search", "filter", "seo", "a/b test"],
    "infra": ["microservice", "ci/cd", "deploy", "pipeline", "concurrent", "response time"],
    "notification": ["email", "notification", "abandoned cart", "promotion"],
}

CONFLICT_PATTERNS = [
    (["real-time", "sub-200ms"], ["batch", "async"]),
    (["monolith"], ["microservice"]),
]


def _classify(req: Requirement) -> List[str]:
    groups = []
    text_lower = req.text.lower()
    for group, keywords in DEPENDENCY_GROUPS.items():
        if any(kw in text_lower for kw in keywords):
            groups.append(group)
    return groups or ["uncategorized"]


def _find_dependencies(requirements: List[Requirement]) -> List[Dict]:
    classified: Dict[str, List[str]] = {}
    for req in requirements:
        for group in _classify(req):
            classified.setdefault(group, []).append(req.id)

    deps = []
    for group, req_ids in classified.items():
        if len(req_ids) > 1:
            for i in range(len(req_ids)):
                for j in range(i + 1, len(req_ids)):
                    deps.append({
                        "from": req_ids[i],
                        "to": req_ids[j],
                        "type": "related",
                        "group": group,
                        "reason": f"Both requirements touch the '{group}' domain",
                    })

    # Add infra dependencies: non-functional reqs are prerequisites
    infra_reqs = [r.id for r in requirements if r.domain in ("non-functional", "technical")]
    func_reqs = [r.id for r in requirements if r.domain == "functional"]
    for ir in infra_reqs[:2]:  # top 2 infra reqs block functional work
        for fr in func_reqs[:3]:  # first 3 functional reqs
            deps.append({
                "from": ir,
                "to": fr,
                "type": "blocks",
                "group": "infra-prerequisite",
                "reason": "Infrastructure requirement should be in place before functional delivery",
            })

    return deps


def _find_conflicts(requirements: List[Requirement]) -> List[Dict]:
    conflicts = []
    for i, r1 in enumerate(requirements):
        for r2 in requirements[i + 1:]:
            t1, t2 = r1.text.lower(), r2.text.lower()
            for group_a, group_b in CONFLICT_PATTERNS:
                a_in_1 = any(k in t1 for k in group_a)
                b_in_2 = any(k in t2 for k in group_b)
                a_in_2 = any(k in t2 for k in group_a)
                b_in_1 = any(k in t1 for k in group_b)
                if (a_in_1 and b_in_2) or (a_in_2 and b_in_1):
                    conflicts.append({
                        "req_a": r1.id,
                        "req_b": r2.id,
                        "reason": f"Potential tension between '{r1.text[:40]}...' and '{r2.text[:40]}...'",
                    })
    return conflicts


def _find_gaps(requirements: List[Requirement]) -> List[Dict]:
    """Detect common missing requirements."""
    gaps = []
    texts = " ".join(r.text.lower() for r in requirements)

    gap_checks = [
        ("authentication", "No explicit authentication/authorization requirement found"),
        ("backup", "No data backup or disaster recovery requirement found"),
        ("accessibility", "No accessibility (WCAG) requirement found"),
        ("logging", "No logging or monitoring requirement found"),
        ("rate limit", "No rate limiting or abuse prevention requirement found"),
    ]

    for keyword, message in gap_checks:
        if keyword not in texts:
            gaps.append({"type": "missing", "message": message, "severity": "warning"})

    return gaps


def run(requirements: List[Requirement]) -> Dict:
    return {
        "dependencies": _find_dependencies(requirements),
        "conflicts": _find_conflicts(requirements),
        "gaps": _find_gaps(requirements),
    }
