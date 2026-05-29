#!/usr/bin/env python3
"""
demo.py — End-to-end demonstration of prompt_cache_analyzer.
Runs against three mock agent configs and shows before/after optimization.
No API keys required.
"""

import json
from prompt_cache_analyzer import analyze, optimize_config, format_report, estimate_tokens

# ── Mock configs representing real-world agent setups ──────────────────────

CLAUDE_CODE_CONFIG = {
    "harness": "claude_code",
    "system_prompt": (
        "You are Claude, an AI assistant made by Anthropic. You are running inside Claude Code, "
        "an agentic coding tool. Current time: {timestamp}. Session ID: {session_id}.\n\n"
        "# CLAUDE.md\n"
        "This project uses Python 3.12, pytest for testing, and ruff for linting.\n"
        "Always run tests before committing. Use type hints for all public functions.\n"
        "The main entry point is src/main.py. Database models are in src/models/.\n\n"
        "# Tool Definitions\n"
        "You have access to the following tools:\n"
        "- Read: Read files from the filesystem\n"
        "- Write: Write files to the filesystem\n"
        "- Edit: Edit existing files with diffs\n"
        "- Bash: Execute shell commands\n"
        "- Grep: Search file contents\n"
        "- Glob: Find files by pattern\n"
        "- Agent: Delegate to sub-agents\n"
        "- TodoWrite: Manage task lists\n\n"
        "Each tool has specific parameters and usage guidelines. "
        "Prefer dedicated tools over shell commands. "
        "Use Edit for modifications, Write for new files only.\n"
    ),
    "tools": [
        {"name": "Read", "description": "Read file contents", "parameters": {"file_path": "string"}},
        {"name": "Write", "description": "Write file contents", "parameters": {"file_path": "string", "content": "string"}},
        {"name": "Edit", "description": "Edit with diffs", "parameters": {"file_path": "string", "changes": "array"}},
        {"name": "Bash", "description": "Run shell commands", "parameters": {"command": "string"}},
        {"name": "Grep", "description": "Search contents", "parameters": {"pattern": "string", "path": "string"}},
    ],
    "messages": [
        {"role": "system", "content": "Additional context: working directory is /home/user/project"},
        {"role": "user", "content": "Fix the login bug in auth.py"},
        {"role": "assistant", "content": "I'll look at auth.py to understand the issue."},
        {"role": "user", "content": "Also add input validation"},
    ],
}

AIDER_CONFIG = {
    "harness": "aider",
    "system_prompt": (
        "You are an expert software engineer. Act as a coding partner.\n"
        "Follow the user's instructions carefully. Request ID: {request_id}.\n"
        "Always reply with complete file contents using the SEARCH/REPLACE format.\n"
        "Do not explain unless asked. Focus on correct, working code.\n"
    ),
    "repo_map": (
        "src/main.py: main entry point, imports app from flask\n"
        "src/models.py: SQLAlchemy models - User, Post, Comment\n"
        "src/routes/auth.py: login, logout, register endpoints\n"
        "src/routes/api.py: REST API endpoints for posts and comments\n"
        "src/templates/: Jinja2 templates for the web UI\n"
        "tests/test_auth.py: authentication tests\n"
        "tests/test_api.py: API endpoint tests\n"
        "requirements.txt: flask, sqlalchemy, pytest, gunicorn\n"
    ),
    "messages": [
        {"role": "user", "content": "Add rate limiting to the API endpoints"},
        {"role": "assistant", "content": "I'll add Flask-Limiter to the API routes."},
        {"role": "user", "content": "Use redis as the backend for rate limiting"},
    ],
}

GENERIC_AGENT_CONFIG = {
    "harness": "generic",
    "system_prompt": (
        "You are a helpful coding assistant. Generated at: {timestamp}.\n"
        "You write clean, well-tested Python code.\n"
    ),
    "messages": [
        {"role": "user", "content": "Write a function to parse CSV files"},
        {"role": "system", "content": "Remember: always handle encoding errors gracefully."},
        {"role": "assistant", "content": "Here's a CSV parser..."},
        {"role": "user", "content": "Add support for TSV files too"},
    ],
}

# ── Run the demo ───────────────────────────────────────────────────────────

def run_demo():
    configs = [
        ("Claude Code", CLAUDE_CODE_CONFIG),
        ("Aider", AIDER_CONFIG),
        ("Generic Agent", GENERIC_AGENT_CONFIG),
    ]

    print()
    print("=" * 60)
    print("  PROMPT CACHE SKILLS — Demo")
    print("  Analyzing 3 agent configurations for cache issues...")
    print("=" * 60)

    for name, config in configs:
        print(f"\n{'─'*60}")
        print(f"  Analyzing: {name}")
        print(f"{'─'*60}")

        # Analyze
        result = analyze(config)
        print(format_report(result))

        # Optimize
        print(f"\n  Applying optimizations...")
        patched = optimize_config(config, harness=config.get("harness", "generic"))

        # Re-analyze patched config
        patched_result = analyze(patched)
        moved = patched.get("_dynamic_elements_moved", [])

        print(f"  Moved {len(moved)} dynamic element(s) out of cached prefix.")
        if moved:
            for elem in moved:
                print(f"    - Removed: {elem}")

        print(f"\n  AFTER optimization:")
        print(f"    Issues remaining: {len(patched_result.issues)}")
        print(f"    Estimated savings: {patched_result.estimated_savings_pct:.0f}%")

        # Cost simulation
        total = result.total_tokens
        cacheable = patched_result.cache_eligible_tokens
        uncached_cost = total * 3.0 / 1_000_000  # $3/MTok input (Claude 3.5 Sonnet)
        cache_write_cost = cacheable * 3.75 / 1_000_000  # 1.25x for cache write
        cache_read_cost = cacheable * 0.30 / 1_000_000   # 0.1x for cache read
        remaining_cost = (total - cacheable) * 3.0 / 1_000_000
        cached_cost = cache_read_cost + remaining_cost  # after first turn

        print(f"\n  Cost estimate (per turn, Claude 3.5 Sonnet pricing):")
        print(f"    Without caching:  ${uncached_cost*1000:.4f} per 1K turns")
        print(f"    With caching:     ${cached_cost*1000:.4f} per 1K turns  (after warm-up)")
        if uncached_cost > 0:
            pct = (1 - cached_cost / uncached_cost) * 100
            print(f"    Savings:          {pct:.0f}%")

    # Summary
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    print("  Prompt caching reduces input token costs by up to 90% on")
    print("  cache hits. The key rules:")
    print("    1. Keep the prompt prefix stable (no timestamps/IDs)")
    print("    2. Order: system -> tools -> history -> new user msg")
    print("    3. Add cache_control breakpoints at key boundaries")
    print("    4. Ensure prefix exceeds 1,024 tokens minimum")
    print("    5. Keep requests frequent (< 5 min apart) to stay warm")
    print(f"{'='*60}")
    print()


if __name__ == "__main__":
    run_demo()
