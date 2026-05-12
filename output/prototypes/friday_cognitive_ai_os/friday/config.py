"""FRIDAY configuration."""
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "data", "memory_store.json")
LOG_DIR = os.path.join(os.path.dirname(__file__), "data", "logs")
MOCK_MODE = not GEMINI_API_KEY
