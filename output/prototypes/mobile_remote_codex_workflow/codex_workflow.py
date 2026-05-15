#!/usr/bin/env python3
"""
Mobile & Remote Codex Workflow Manager

Simulates managing, monitoring, steering, and approving AI-assisted coding tasks
from any device (including mobile) using OpenAI Codex via the ChatGPT app.

This demo shows the full lifecycle: task creation, real-time monitoring,
mid-task steering, diff review, and approval/rejection — all via a
device-agnostic interface.
"""

import json
import time
import random
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from datetime import datetime, timedelta


class TaskStatus(Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    AWAITING_REVIEW = "awaiting_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_STEERING = "needs_steering"


class DeviceType(Enum):
    MOBILE_IOS = "iOS (ChatGPT App)"
    MOBILE_ANDROID = "Android (ChatGPT App)"
    DESKTOP_WEB = "Desktop (Web)"
    TABLET = "Tablet (ChatGPT App)"


@dataclass
class CodeDiff:
    file_path: str
    additions: int
    deletions: int
    diff_content: str
    language: str = "python"


@dataclass
class SteeringEvent:
    timestamp: str
    device: str
    instruction: str
    acknowledged: bool = True


@dataclass
class CodingTask:
    task_id: str
    description: str
    status: TaskStatus
    repo: str
    branch: str
    created_at: str
    device_origin: DeviceType
    progress_pct: int = 0
    files_read: int = 0
    files_modified: int = 0
    diffs: list = field(default_factory=list)
    steering_history: list = field(default_factory=list)
    estimated_completion: str = ""


class CodexWorkflowManager:
    """Manages remote Codex coding tasks across devices."""

    def __init__(self):
        self.tasks: list[CodingTask] = []
        self.active_device = DeviceType.MOBILE_IOS
        self.session_id = hashlib.sha256(
            datetime.now().isoformat().encode()
        ).hexdigest()[:12]

    def create_task(self, description: str, repo: str, branch: str = "codex/auto") -> CodingTask:
        task_id = f"ctx_{hashlib.md5(description.encode()).hexdigest()[:8]}"
        task = CodingTask(
            task_id=task_id,
            description=description,
            status=TaskStatus.QUEUED,
            repo=repo,
            branch=branch,
            created_at=datetime.now().isoformat(),
            device_origin=self.active_device,
        )
        self.tasks.append(task)
        return task

    def simulate_progress(self, task: CodingTask) -> dict:
        """Simulate Codex working on a task with realistic progress updates."""
        stages = [
            {"pct": 15, "msg": "Reading codebase and understanding context..."},
            {"pct": 30, "msg": "Planning implementation approach..."},
            {"pct": 50, "msg": "Writing code changes..."},
            {"pct": 70, "msg": "Running tests and validating..."},
            {"pct": 85, "msg": "Generating diffs for review..."},
            {"pct": 100, "msg": "Ready for review."},
        ]

        progress_log = []
        for stage in stages:
            task.progress_pct = stage["pct"]
            task.status = TaskStatus.IN_PROGRESS
            task.files_read = random.randint(5, 25)
            progress_log.append({
                "progress": stage["pct"],
                "message": stage["msg"],
                "files_read": task.files_read,
                "timestamp": datetime.now().isoformat(),
            })

        task.status = TaskStatus.AWAITING_REVIEW
        task.files_modified = random.randint(2, 6)
        task.estimated_completion = (
            datetime.now() + timedelta(minutes=random.randint(1, 5))
        ).strftime("%H:%M")

        return {"task_id": task.task_id, "stages": progress_log}

    def generate_mock_diffs(self, task: CodingTask) -> list[CodeDiff]:
        """Generate realistic mock diffs for the task."""
        diff_templates = [
            CodeDiff(
                file_path="src/auth/validators.py",
                additions=24,
                deletions=3,
                language="python",
                diff_content="""\
@@ -45,6 +45,27 @@ class SignupValidator:
+    def validate_email(self, email: str) -> bool:
+        \"\"\"Validate email format and domain.\"\"\"
+        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
+        if not re.match(pattern, email):
+            raise ValidationError("Invalid email format")
+        return True
+
+    def validate_password_strength(self, password: str) -> bool:
+        \"\"\"Enforce password complexity requirements.\"\"\"
+        if len(password) < 12:
+            raise ValidationError("Password must be at least 12 characters")
+        if not re.search(r'[A-Z]', password):
+            raise ValidationError("Password must contain uppercase letter")
+        if not re.search(r'[0-9]', password):
+            raise ValidationError("Password must contain a digit")
+        return True""",
            ),
            CodeDiff(
                file_path="tests/test_validators.py",
                additions=35,
                deletions=0,
                language="python",
                diff_content="""\
@@ -0,0 +1,35 @@
+import pytest
+from src.auth.validators import SignupValidator
+
+class TestSignupValidator:
+    def setup_method(self):
+        self.validator = SignupValidator()
+
+    def test_valid_email(self):
+        assert self.validator.validate_email("user@example.com")
+
+    def test_invalid_email_no_domain(self):
+        with pytest.raises(ValidationError):
+            self.validator.validate_email("user@")
+
+    def test_password_too_short(self):
+        with pytest.raises(ValidationError):
+            self.validator.validate_password_strength("short")
+
+    def test_password_valid(self):
+        assert self.validator.validate_password_strength("SecurePass123!")""",
            ),
            CodeDiff(
                file_path="src/auth/__init__.py",
                additions=2,
                deletions=1,
                language="python",
                diff_content="""\
@@ -1,3 +1,4 @@
-from .auth import authenticate
+from .auth import authenticate
+from .validators import SignupValidator
+__all__ = ["authenticate", "SignupValidator"]""",
            ),
        ]

        task.diffs = diff_templates[: random.randint(2, len(diff_templates))]
        return task.diffs

    def steer_task(self, task: CodingTask, instruction: str) -> SteeringEvent:
        """Send a steering instruction to a running task (e.g., from mobile)."""
        event = SteeringEvent(
            timestamp=datetime.now().isoformat(),
            device=self.active_device.value,
            instruction=instruction,
            acknowledged=True,
        )
        task.steering_history.append(event)
        task.status = TaskStatus.IN_PROGRESS
        return event

    def review_task(self, task: CodingTask, approve: bool, comment: str = "") -> dict:
        """Approve or reject a task's changes from any device."""
        if approve:
            task.status = TaskStatus.APPROVED
            action = "approved"
        else:
            task.status = TaskStatus.REJECTED
            action = "rejected"

        return {
            "task_id": task.task_id,
            "action": action,
            "reviewer_device": self.active_device.value,
            "comment": comment,
            "timestamp": datetime.now().isoformat(),
            "pr_url": f"https://github.com/myorg/{task.repo}/pull/{random.randint(100,999)}"
            if approve
            else None,
        }

    def get_dashboard(self) -> dict:
        """Generate a cross-device dashboard summary."""
        return {
            "session_id": self.session_id,
            "active_device": self.active_device.value,
            "total_tasks": len(self.tasks),
            "tasks_by_status": {
                status.value: len([t for t in self.tasks if t.status == status])
                for status in TaskStatus
            },
            "tasks": [
                {
                    "id": t.task_id,
                    "description": t.description[:60],
                    "status": t.status.value,
                    "progress": t.progress_pct,
                    "branch": t.branch,
                }
                for t in self.tasks
            ],
        }


def run_demo():
    """Run a full demo of the mobile remote Codex workflow."""
    print("=" * 70)
    print("  MOBILE & REMOTE CODEX WORKFLOW MANAGER — DEMO")
    print("  Manage AI coding tasks from any device")
    print("=" * 70)

    manager = CodexWorkflowManager()
    manager.active_device = DeviceType.MOBILE_IOS

    # Step 1: Create tasks from mobile
    print("\n[1] CREATING TASKS FROM MOBILE (iOS ChatGPT App)")
    print("-" * 50)

    task1 = manager.create_task(
        description="Add input validation to the signup form with email and password checks",
        repo="webapp-frontend",
        branch="codex/add-validation",
    )
    print(f"  Task created: {task1.task_id}")
    print(f"  Description: {task1.description}")
    print(f"  Repo: {task1.repo} | Branch: {task1.branch}")
    print(f"  Device: {task1.device_origin.value}")

    task2 = manager.create_task(
        description="Refactor database connection pool to use async context managers",
        repo="backend-api",
        branch="codex/async-db-pool",
    )
    print(f"\n  Task created: {task2.task_id}")
    print(f"  Description: {task2.description}")

    # Step 2: Monitor progress
    print("\n[2] MONITORING PROGRESS IN REAL TIME")
    print("-" * 50)

    progress = manager.simulate_progress(task1)
    for stage in progress["stages"]:
        print(f"  [{stage['progress']:3d}%] {stage['message']}")

    print(f"\n  Status: {task1.status.value}")
    print(f"  Files read: {task1.files_read} | Files modified: {task1.files_modified}")

    # Step 3: Steer the task mid-flight
    print("\n[3] STEERING TASK FROM MOBILE")
    print("-" * 50)

    steering = manager.steer_task(
        task1, "Focus on email validation first, use RFC 5322 regex pattern"
    )
    print(f"  Instruction: \"{steering.instruction}\"")
    print(f"  Sent from: {steering.device}")
    print(f"  Acknowledged: {steering.acknowledged}")

    steering2 = manager.steer_task(
        task1, "Add password strength meter with zxcvbn scoring"
    )
    print(f"\n  Instruction: \"{steering2.instruction}\"")
    print(f"  Acknowledged: {steering2.acknowledged}")

    # Step 4: Review diffs
    print("\n[4] REVIEWING CODE DIFFS ON MOBILE")
    print("-" * 50)

    diffs = manager.generate_mock_diffs(task1)
    total_add = sum(d.additions for d in diffs)
    total_del = sum(d.deletions for d in diffs)
    print(f"  Total changes: +{total_add} / -{total_del} across {len(diffs)} files\n")

    for diff in diffs:
        print(f"  --- {diff.file_path} (+{diff.additions}/-{diff.deletions})")
        # Show first few lines of diff
        lines = diff.diff_content.strip().split("\n")[:8]
        for line in lines:
            print(f"    {line}")
        if len(diff.diff_content.strip().split("\n")) > 8:
            print(f"    ... ({len(diff.diff_content.strip().split(chr(10)))} lines total)")
        print()

    # Step 5: Approve from mobile
    print("[5] APPROVING CHANGES FROM MOBILE")
    print("-" * 50)

    result = manager.review_task(
        task1, approve=True, comment="LGTM — validation logic looks solid"
    )
    print(f"  Action: {result['action'].upper()}")
    print(f"  Device: {result['reviewer_device']}")
    print(f"  Comment: {result['comment']}")
    print(f"  PR Created: {result['pr_url']}")

    # Step 6: Cross-device dashboard
    print("\n[6] CROSS-DEVICE DASHBOARD")
    print("-" * 50)

    # Simulate second task progress
    manager.simulate_progress(task2)
    dashboard = manager.get_dashboard()

    print(f"  Session: {dashboard['session_id']}")
    print(f"  Active Device: {dashboard['active_device']}")
    print(f"  Total Tasks: {dashboard['total_tasks']}")
    print(f"  Status Breakdown:")
    for status, count in dashboard["tasks_by_status"].items():
        if count > 0:
            print(f"    {status}: {count}")

    print(f"\n  Task Summary:")
    for t in dashboard["tasks"]:
        print(f"    [{t['status']:^16}] {t['description']} ({t['branch']})")

    # Output as JSON for programmatic consumption
    print("\n[7] JSON OUTPUT (for API/webhook integration)")
    print("-" * 50)
    print(json.dumps(dashboard, indent=2))

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE — All operations performed from simulated mobile device")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
