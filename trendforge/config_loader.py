"""Config loader — loads YAML configs and .env values."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"


def load_yaml(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_sources() -> dict[str, Any]:
    return load_yaml("sources.yaml")


def load_interests() -> dict[str, Any]:
    return load_yaml("interests.yaml")


def load_watched_repos() -> list[str]:
    data = load_yaml("watched_repos.yaml")
    return data.get("repos", []) or []


def load_dotenv() -> None:
    """Lightweight .env loader (no external dep)."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


# Email: hard-coded recipient per project spec.
DIGEST_RECIPIENT = "anirudh.royyuru@gmail.com"
