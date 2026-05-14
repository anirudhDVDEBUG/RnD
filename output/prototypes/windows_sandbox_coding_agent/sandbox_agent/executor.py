"""Sandbox executor: simulates running coding tasks in an isolated environment.

On Windows with Sandbox enabled, this would launch WindowsSandbox.exe.
On other platforms (or without Sandbox), it runs in a simulated local sandbox
using subprocess isolation and chroot-like path restrictions.
"""

import json
import os
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from .config import SandboxConfig
from .validator import validate_changes, ValidationResult


@dataclass
class TaskResult:
    status: str  # "success", "error", "rejected"
    files_changed: list[str] = field(default_factory=list)
    output: str = ""
    validation: Optional[ValidationResult] = None
    duration_seconds: float = 0.0


class SandboxExecutor:
    """Executes coding tasks inside an isolated sandbox."""

    def __init__(self, config: SandboxConfig):
        self.config = config
        self.workspace = Path(config.workspace_host)

    def execute_task(self, task: dict) -> TaskResult:
        """
        Run a coding task. Task dict must have:
          - "type": "write_file" | "run_command" | "multi_step"
          - type-specific fields (see _execute_* methods)
        """
        start = time.time()

        task_type = task.get("type", "unknown")
        try:
            if task_type == "write_file":
                result = self._execute_write(task)
            elif task_type == "run_command":
                result = self._execute_command(task)
            elif task_type == "multi_step":
                result = self._execute_multi(task)
            else:
                result = TaskResult(status="error", output=f"Unknown task type: {task_type}")
        except Exception as e:
            result = TaskResult(status="error", output=f"Exception: {e}")

        result.duration_seconds = time.time() - start
        return result

    def _execute_write(self, task: dict) -> TaskResult:
        """Write or modify a file inside the workspace."""
        rel_path = task["path"]
        content = task["content"]
        target = self.workspace / rel_path

        # Pre-validate
        changes = [{"path": rel_path, "size_bytes": len(content.encode()), "action": "add"}]
        validation = validate_changes(changes, self.config.safety)
        if not validation.passed:
            return TaskResult(status="rejected", validation=validation,
                              output=str(validation))

        # Ensure path stays within workspace (path traversal guard)
        try:
            target.resolve().relative_to(self.workspace.resolve())
        except ValueError:
            return TaskResult(status="rejected",
                              output=f"Path traversal blocked: {rel_path}")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return TaskResult(status="success", files_changed=[rel_path],
                          validation=validation,
                          output=f"Wrote {len(content)} bytes to {rel_path}")

    def _execute_command(self, task: dict) -> TaskResult:
        """Run a command inside the sandbox workspace."""
        cmd = task["command"]

        # Block dangerous commands
        dangerous = ["rm -rf /", "sudo", "curl", "wget", "nc ", "ncat"]
        for d in dangerous:
            if d in cmd:
                return TaskResult(status="rejected",
                                  output=f"Blocked dangerous command fragment: {d}")

        try:
            proc = subprocess.run(
                cmd, shell=True, cwd=self.workspace,
                capture_output=True, text=True,
                timeout=min(task.get("timeout", 30), self.config.safety.timeout_seconds),
                env={**os.environ, "HOME": str(self.workspace)},
            )
            output = proc.stdout + proc.stderr
            status = "success" if proc.returncode == 0 else "error"
            return TaskResult(status=status, output=output.strip())
        except subprocess.TimeoutExpired:
            return TaskResult(status="error", output="Command timed out")

    def _execute_multi(self, task: dict) -> TaskResult:
        """Execute a sequence of sub-tasks."""
        steps = task.get("steps", [])
        all_files = []
        outputs = []

        for i, step in enumerate(steps):
            result = self.execute_task(step)
            outputs.append(f"[Step {i+1}] {result.status}: {result.output}")
            all_files.extend(result.files_changed)
            if result.status not in ("success",):
                return TaskResult(
                    status="error", files_changed=all_files,
                    output="\n".join(outputs),
                )

        return TaskResult(
            status="success", files_changed=all_files,
            output="\n".join(outputs),
        )

    def generate_wsb_file(self, output_path: str = "sandbox.wsb") -> str:
        """Generate a .wsb config file for Windows Sandbox."""
        xml = self.config.to_wsb_xml()
        p = Path(output_path)
        p.write_text(xml)
        return xml
