"""Specification Writer Agent: Generate technical specs from requirements."""

from typing import Dict, List
from intake import Requirement

TECH_STACK_HINTS = {
    "search": {"service": "Search Service", "tech": "Elasticsearch / Typesense", "api": "GET /api/v1/products/search"},
    "checkout": {"service": "Payment Service", "tech": "Stripe SDK + PayPal REST API", "api": "POST /api/v1/orders/checkout"},
    "payment": {"service": "Payment Service", "tech": "Stripe SDK + PayPal REST API", "api": "POST /api/v1/payments"},
    "recommendation": {"service": "Recommendation Service", "tech": "Collaborative filtering / embeddings", "api": "GET /api/v1/recommendations"},
    "dashboard": {"service": "Admin Service", "tech": "React + REST API", "api": "GET /api/v1/admin/dashboard"},
    "inventory": {"service": "Inventory Service", "tech": "PostgreSQL + event sourcing", "api": "GET /api/v1/inventory"},
    "encrypted": {"service": "Security Layer", "tech": "AWS KMS / Vault", "api": "N/A (infrastructure)"},
    "concurrent": {"service": "Platform Infrastructure", "tech": "Kubernetes HPA + Redis cache", "api": "N/A (infrastructure)"},
    "microservice": {"service": "Platform Infrastructure", "tech": "Docker + Kubernetes + Istio", "api": "N/A (infrastructure)"},
    "ci/cd": {"service": "DevOps Pipeline", "tech": "GitHub Actions + ArgoCD", "api": "N/A (infrastructure)"},
    "a/b test": {"service": "Experimentation Service", "tech": "Feature flags (LaunchDarkly / custom)", "api": "GET /api/v1/experiments"},
    "seo": {"service": "Frontend SSR", "tech": "Next.js + structured data (JSON-LD)", "api": "N/A (frontend)"},
    "email": {"service": "Notification Service", "tech": "SendGrid / SES + job queue", "api": "POST /api/v1/notifications"},
    "analytics": {"service": "Analytics Service", "tech": "ClickHouse + Grafana", "api": "GET /api/v1/analytics"},
}


def _match_tech(text: str) -> Dict:
    text_lower = text.lower()
    for keyword, stack in TECH_STACK_HINTS.items():
        if keyword in text_lower:
            return stack
    return {"service": "Core Service", "tech": "To be determined", "api": "TBD"}


def run(requirements: List[Requirement]) -> List[Dict]:
    specs = []
    for req in requirements:
        tech = _match_tech(req.text)
        specs.append({
            "requirement_id": req.id,
            "title": req.text,
            "source": req.source,
            "service": tech["service"],
            "suggested_tech": tech["tech"],
            "api_endpoint": tech["api"],
            "data_model_notes": _data_notes(req),
            "testing_strategy": _test_strategy(req),
            "definition_of_done": [
                "Implementation matches acceptance criteria",
                "Unit test coverage >= 80%",
                "API documentation updated",
                "Code reviewed and approved",
            ],
        })
    return specs


def _data_notes(req: Requirement) -> str:
    text = req.text.lower()
    if "product" in text:
        return "Products table with full-text index; consider denormalized search index"
    if "order" in text or "checkout" in text or "payment" in text:
        return "Orders table with payment_status enum; idempotency keys for payment ops"
    if "user" in text or "admin" in text:
        return "Users table with role-based access; audit log for admin actions"
    if "analytics" in text or "metric" in text:
        return "Time-series data store; pre-aggregated rollups for dashboard queries"
    return "Schema to be designed during implementation spike"


def _test_strategy(req: Requirement) -> str:
    if req.domain == "non-functional":
        return "Load testing (k6/Locust), security scanning (OWASP ZAP), chaos engineering"
    if req.domain == "technical":
        return "Integration tests, infrastructure-as-code validation, deployment smoke tests"
    return "Unit tests + integration tests + E2E tests for critical paths"
