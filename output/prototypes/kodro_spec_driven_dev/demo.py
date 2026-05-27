#!/usr/bin/env python3
"""
Kodro SDD Pipeline Demo
========================
Runs the full 6-phase spec-driven development pipeline on a sample spec
(user authentication with JWT) and prints the results.

No API keys required — everything runs locally.
"""

import json
import sys
import os
import textwrap

# Ensure the package is importable
sys.path.insert(0, os.path.dirname(__file__))

from kodro.pipeline import run_pipeline


SAMPLE_SPEC = {
    "name": "User Authentication Module",
    "purpose": (
        "JWT-based authentication service that handles user registration, "
        "login, token refresh, and session management for a REST API."
    ),
    "requirements": [
        {"id": "REQ-1", "text": "Users can register with email and password"},
        {"id": "REQ-2", "text": "Passwords are hashed with bcrypt before storage"},
        {"id": "REQ-3", "text": "Login returns a signed JWT access token (15min TTL)"},
        {"id": "REQ-4", "text": "Login returns a refresh token (7-day TTL)"},
        {"id": "REQ-5", "text": "Refresh endpoint issues a new access token given a valid refresh token"},
        {"id": "REQ-6", "text": "Protected routes reject requests without a valid JWT"},
        {"id": "REQ-7", "text": "Rate limit login to 5 attempts per minute per IP"},
    ],
    "data_models": [
        {
            "name": "User",
            "fields": {
                "id": "string",
                "email": "string",
                "password_hash": "string",
                "created_at": "string",
                "is_active": "boolean",
            },
        },
        {
            "name": "Token",
            "fields": {
                "token": "string",
                "user_id": "string",
                "expires_at": "string",
                "token_type": "string",
            },
        },
    ],
    "api_endpoints": [
        {"method": "POST", "path": "/auth/register", "description": "Register a new user"},
        {"method": "POST", "path": "/auth/login", "description": "Authenticate and get tokens"},
        {"method": "POST", "path": "/auth/refresh", "description": "Refresh access token"},
        {"method": "GET", "path": "/auth/me", "description": "Get current user profile"},
    ],
    "constraints": [
        "Passwords must be >= 8 characters",
        "JWT secret loaded from environment variable",
        "All endpoints return JSON",
        "Response time < 200ms for auth operations",
    ],
}


def print_section(title, content):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")
    print(content)


def main():
    print("=" * 60)
    print("  KODRO: Spec-Driven Development Demo")
    print("  Running 6-phase autonomous pipeline...")
    print("=" * 60)

    # Show the input spec
    print_section(
        "INPUT: Sample Specification (JWT Auth Module)",
        json.dumps(SAMPLE_SPEC, indent=2)[:800] + "\n  ... (truncated)",
    )

    # Run the pipeline
    result = run_pipeline(SAMPLE_SPEC)

    # Show full pipeline output
    print()
    print(result.summary())

    # Show generated code samples
    print_section("GENERATED CODE SAMPLES", "")
    for f in result.files:
        print(f"\n--- {f.path} ---")
        # Show first 25 lines
        lines = f.content.split("\n")
        for line in lines[:25]:
            print(f"  {line}")
        if len(lines) > 25:
            print(f"  ... ({len(lines) - 25} more lines)")

    # Token cost comparison
    print_section("TOKEN COST ANALYSIS (estimated)", "")
    spec_tokens = len(json.dumps(SAMPLE_SPEC)) // 4  # rough estimate
    vibe_tokens = spec_tokens * 6  # typical back-and-forth multiplier
    sdd_tokens = spec_tokens + sum(len(f.content) for f in result.files) // 4
    savings = round(100 * (1 - sdd_tokens / vibe_tokens))

    print(f"  Spec tokens (input):        ~{spec_tokens:,}")
    print(f"  Vibe coding estimate:        ~{vibe_tokens:,} tokens (6x back-and-forth)")
    print(f"  SDD pipeline estimate:       ~{sdd_tokens:,} tokens (spec + focused gen)")
    print(f"  Estimated savings:           ~{savings}%")
    print()
    print("  The spec-first approach eliminates rework and unnecessary")
    print("  context, dramatically reducing token usage.")

    print(f"\n{'=' * 60}")
    print(f"  Pipeline complete: {len(result.phases_completed)} phases, "
          f"{len(result.files)} files, "
          f"{result.coverage.percent}% coverage")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
