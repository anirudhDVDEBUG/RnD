"""
Mock codebase structure representing a typical SaaS application.
Used by the pipeline to demonstrate file-mapping and code generation.
"""

CODEBASE = {
    "src/api/routes.py": {
        "description": "API route definitions",
        "functions": ["get_analytics", "post_webhook", "search_items", "create_api_key", "rate_limit_middleware"],
        "lines": 340,
    },
    "src/api/middleware.py": {
        "description": "Request middleware (auth, rate limiting, logging)",
        "functions": ["check_rate_limit", "authenticate_request", "log_request"],
        "lines": 180,
    },
    "src/services/analytics.py": {
        "description": "Analytics data aggregation and retrieval",
        "functions": ["get_dashboard_data", "aggregate_metrics", "format_report"],
        "lines": 220,
    },
    "src/services/webhooks.py": {
        "description": "Webhook delivery and management",
        "functions": ["deliver_webhook", "register_endpoint", "validate_payload"],
        "lines": 150,
    },
    "src/services/search.py": {
        "description": "Search indexing and query execution",
        "functions": ["index_item", "delete_from_index", "execute_search", "invalidate_cache"],
        "lines": 280,
    },
    "src/models/api_key.py": {
        "description": "API key model and permission scopes",
        "functions": ["ApiKey", "generate_key", "validate_key"],
        "lines": 90,
    },
    "src/exporters/__init__.py": {
        "description": "Data export utilities (currently empty)",
        "functions": [],
        "lines": 5,
    },
    "tests/test_analytics.py": {
        "description": "Tests for analytics service",
        "functions": ["test_get_dashboard_data", "test_aggregate_metrics"],
        "lines": 120,
    },
    "tests/test_webhooks.py": {
        "description": "Tests for webhook service",
        "functions": ["test_deliver_webhook", "test_register_endpoint"],
        "lines": 95,
    },
    "tests/test_search.py": {
        "description": "Tests for search service",
        "functions": ["test_index_item", "test_execute_search"],
        "lines": 110,
    },
    "tests/test_api_keys.py": {
        "description": "Tests for API key management",
        "functions": ["test_generate_key", "test_validate_key"],
        "lines": 75,
    },
}

# Mapping from request keywords to relevant codebase areas
KEYWORD_FILE_MAP = {
    "csv": ["src/services/analytics.py", "src/exporters/__init__.py", "src/api/routes.py"],
    "export": ["src/services/analytics.py", "src/exporters/__init__.py", "src/api/routes.py"],
    "dashboard": ["src/services/analytics.py", "src/api/routes.py"],
    "analytics": ["src/services/analytics.py", "tests/test_analytics.py"],
    "webhook": ["src/services/webhooks.py", "src/api/routes.py", "tests/test_webhooks.py"],
    "retry": ["src/services/webhooks.py"],
    "backoff": ["src/services/webhooks.py"],
    "search": ["src/services/search.py", "tests/test_search.py"],
    "delete": ["src/services/search.py", "src/api/routes.py"],
    "cache": ["src/services/search.py"],
    "index": ["src/services/search.py"],
    "api key": ["src/models/api_key.py", "src/api/middleware.py", "tests/test_api_keys.py"],
    "rbac": ["src/models/api_key.py", "src/api/middleware.py"],
    "permission": ["src/models/api_key.py", "src/api/middleware.py"],
    "role": ["src/models/api_key.py", "src/api/middleware.py"],
    "rate limit": ["src/api/middleware.py", "src/api/routes.py"],
    "429": ["src/api/middleware.py"],
    "500": ["src/api/middleware.py", "src/api/routes.py"],
}
