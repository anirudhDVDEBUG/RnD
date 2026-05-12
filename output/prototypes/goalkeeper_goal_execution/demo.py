#!/usr/bin/env python3
"""
Demo: Goalkeeper contract-driven goal execution.

Scenario: Build a user registration module.  The executor intentionally
produces incomplete work on the first pass so you can watch the judge
reject it, then iterate to full completion.
"""

import json
import os
import re
import sys

from goalkeeper import (
    CriterionStatus,
    Criterion,
    Goal,
    GoalkeeperEngine,
)


# ---------------------------------------------------------------------------
# Verifiers -- each returns (passed: bool, feedback: str)
# ---------------------------------------------------------------------------

def verify_endpoint_exists(artifacts: dict) -> tuple[bool, str]:
    code = artifacts.get("source_code", "")
    if "def register(" in code and "POST" in code:
        return True, "POST /register endpoint found"
    return False, "Missing POST /register endpoint"


def verify_password_hashing(artifacts: dict) -> tuple[bool, str]:
    code = artifacts.get("source_code", "")
    if "hash_password" in code or "bcrypt" in code:
        return True, "Password hashing implemented"
    return False, "Passwords stored in plaintext -- must hash"


def verify_email_validation(artifacts: dict) -> tuple[bool, str]:
    code = artifacts.get("source_code", "")
    if "validate_email" in code or "email_regex" in code:
        return True, "Email validation present"
    return False, "No email validation found"


def verify_duplicate_check(artifacts: dict) -> tuple[bool, str]:
    code = artifacts.get("source_code", "")
    if "already_exists" in code or "duplicate" in code:
        return True, "Duplicate user check implemented"
    return False, "No duplicate-user guard"


def verify_tests(artifacts: dict) -> tuple[bool, str]:
    tests = artifacts.get("tests", "")
    has_success = "test_register_success" in tests
    has_failure = "test_register_failure" in tests
    if has_success and has_failure:
        return True, "Success + failure test cases present"
    missing = []
    if not has_success:
        missing.append("success path")
    if not has_failure:
        missing.append("failure path")
    return False, f"Missing test cases: {', '.join(missing)}"


# ---------------------------------------------------------------------------
# Executor -- simulates an agent writing code
# ---------------------------------------------------------------------------

# Iteration 1: deliberately incomplete (no email validation, no dupe check)
INCOMPLETE_SOURCE = """\
# auth/register.py  (iteration 1 -- incomplete)
from flask import request, jsonify

def register():
    \"\"\"POST /register -- create a new user.\"\"\"
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    # TODO: hash password
    # TODO: validate email
    # TODO: check duplicates
    save_user(email, password)
    return jsonify({"status": "created"}), 201
"""

INCOMPLETE_TESTS = """\
# tests/test_register.py  (iteration 1 -- incomplete)
def test_register_success():
    resp = client.post("/register", json={"email": "a@b.com", "password": "s3cure"})
    assert resp.status_code == 201
"""

# Iteration 2+: complete
COMPLETE_SOURCE = """\
# auth/register.py  (iteration 2 -- complete)
import re
from flask import request, jsonify

email_regex = re.compile(r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$")

def validate_email(email: str) -> bool:
    return bool(email_regex.match(email))

def hash_password(pw: str) -> str:
    import hashlib
    return hashlib.sha256(pw.encode()).hexdigest()

def register():
    \"\"\"POST /register -- create a new user.\"\"\"
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    if not validate_email(email):
        return jsonify({"error": "invalid email"}), 400

    if user_already_exists(email):
        return jsonify({"error": "duplicate"}), 409

    hashed = hash_password(password)
    save_user(email, hashed)
    return jsonify({"status": "created"}), 201
"""

COMPLETE_TESTS = """\
# tests/test_register.py  (iteration 2 -- complete)
def test_register_success():
    resp = client.post("/register", json={"email": "a@b.com", "password": "s3cure"})
    assert resp.status_code == 201

def test_register_failure():
    # invalid email
    resp = client.post("/register", json={"email": "bad", "password": "s3cure"})
    assert resp.status_code == 400
    # duplicate
    resp = client.post("/register", json={"email": "a@b.com", "password": "s3cure"})
    assert resp.status_code == 409
"""


def executor(goal: Goal) -> Goal:
    """Simulate an agent producing work artifacts.
    First call returns incomplete code; subsequent calls fix it."""
    if goal.iteration == 0:
        print("  [executor] Producing initial (incomplete) implementation...")
        goal.artifacts["source_code"] = INCOMPLETE_SOURCE
        goal.artifacts["tests"] = INCOMPLETE_TESTS
    else:
        # Look at judge feedback and fix
        print("  [executor] Fixing issues identified by judge...")
        goal.artifacts["source_code"] = COMPLETE_SOURCE
        goal.artifacts["tests"] = COMPLETE_TESTS
    return goal


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    goal = Goal(
        title="User Registration Endpoint",
        description="Implement a secure POST /register endpoint with full validation.",
        criteria=[
            Criterion("POST /register endpoint exists", verifier=verify_endpoint_exists),
            Criterion("Passwords are hashed before storage", verifier=verify_password_hashing),
            Criterion("Email addresses are validated", verifier=verify_email_validation),
            Criterion("Duplicate users are rejected", verifier=verify_duplicate_check),
            Criterion("Unit tests cover success and failure paths", verifier=verify_tests),
        ],
    )

    engine = GoalkeeperEngine()
    final = engine.run(goal, executor)

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(final.summary())
    print(f"\nCompleted in {final.iteration} iteration(s)")
    status = "SUCCESS" if final.is_complete else "INCOMPLETE"
    print(f"Status: {status}")

    # Write a JSON report
    report = {
        "goal": final.title,
        "status": status,
        "iterations": final.iteration,
        "criteria": [
            {"description": c.description, "status": c.status.value, "feedback": c.feedback}
            for c in final.criteria
        ],
    }
    report_path = os.path.join(os.path.dirname(__file__) or ".", "goal_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()
