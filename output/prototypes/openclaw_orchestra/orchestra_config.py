"""
Orchestra configuration: define agent topologies as Python dicts or load from YAML.
"""

import os
import json

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


DEFAULT_TOPOLOGY = {
    "agents": [
        {
            "name": "backend-specialist",
            "workspace": "./workspaces/backend",
            "tools": ["code-edit", "test-runner", "git"],
            "prompt": "You handle backend API changes. Focus on data models, endpoints, and business logic.",
        },
        {
            "name": "frontend-specialist",
            "workspace": "./workspaces/frontend",
            "tools": ["code-edit", "browser-preview", "git"],
            "prompt": "You handle frontend UI changes. Focus on components, styling, and user interaction.",
        },
        {
            "name": "reviewer",
            "workspace": "./workspaces/review",
            "tools": ["code-read", "lint", "git"],
            "prompt": "You review code produced by other agents and provide feedback.",
        },
    ]
}


def load_config(path=None):
    """Load orchestra config from YAML/JSON file, or return default topology."""
    if path and os.path.exists(path):
        with open(path) as f:
            if path.endswith((".yaml", ".yml")) and HAS_YAML:
                return yaml.safe_load(f)
            else:
                return json.load(f)
    return DEFAULT_TOPOLOGY
