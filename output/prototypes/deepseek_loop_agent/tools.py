"""
Built-in tools for the DeepSeek agent loop.
Mirrors Claude Code's tool set: file_read, file_write, bash, grep, glob.
"""

import fnmatch
import os
import subprocess
from typing import Any


def tool_file_read(path: str, limit: int = 200) -> str:
    """Read a file and return its contents (up to `limit` lines)."""
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        return f"Error: file not found: {path}"
    try:
        with open(path, "r", errors="replace") as f:
            lines = f.readlines()[:limit]
        numbered = [f"{i+1:4d} | {line}" for i, line in enumerate(lines)]
        return "".join(numbered)
    except Exception as e:
        return f"Error reading {path}: {e}"


def tool_file_write(path: str, content: str) -> str:
    """Write content to a file, creating directories as needed."""
    path = os.path.expanduser(path)
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


def tool_bash(command: str, timeout: int = 30) -> str:
    """Execute a bash command and return stdout+stderr."""
    try:
        result = subprocess.run(
            ["bash", "-c", command],
            capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout + result.stderr
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {timeout}s"
    except Exception as e:
        return f"Error running command: {e}"


def tool_grep(pattern: str, path: str = ".", max_results: int = 50) -> str:
    """Search for a pattern in files under a directory."""
    path = os.path.expanduser(path)
    results = []
    try:
        for root, _, files in os.walk(path):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", errors="replace") as f:
                        for i, line in enumerate(f, 1):
                            if pattern in line:
                                results.append(f"{fpath}:{i}: {line.rstrip()}")
                                if len(results) >= max_results:
                                    return "\n".join(results)
                except (OSError, UnicodeDecodeError):
                    continue
    except Exception as e:
        return f"Error: {e}"
    return "\n".join(results) if results else f"No matches for '{pattern}'"


def tool_glob(pattern: str, path: str = ".") -> str:
    """Find files matching a glob pattern."""
    path = os.path.expanduser(path)
    matches = []
    for root, _, files in os.walk(path):
        for fname in files:
            if fnmatch.fnmatch(fname, pattern):
                matches.append(os.path.join(root, fname))
    return "\n".join(sorted(matches)[:100]) if matches else f"No files matching '{pattern}'"


# Registry of all built-in tools
BUILTIN_TOOLS = {
    "file_read": {
        "fn": tool_file_read,
        "description": "Read a file's contents",
        "parameters": {"path": "string (file path)", "limit": "int (max lines, default 200)"},
    },
    "file_write": {
        "fn": tool_file_write,
        "description": "Write content to a file",
        "parameters": {"path": "string (file path)", "content": "string (file content)"},
    },
    "bash": {
        "fn": tool_bash,
        "description": "Execute a bash command",
        "parameters": {"command": "string (bash command)", "timeout": "int (seconds, default 30)"},
    },
    "grep": {
        "fn": tool_grep,
        "description": "Search for a text pattern in files",
        "parameters": {"pattern": "string", "path": "string (directory, default '.')", "max_results": "int (default 50)"},
    },
    "glob": {
        "fn": tool_glob,
        "description": "Find files matching a glob pattern",
        "parameters": {"pattern": "string (glob)", "path": "string (directory, default '.')"},
    },
}


class ToolRegistry:
    """Registry that holds tool definitions and executes them."""

    def __init__(self):
        self.tools = dict(BUILTIN_TOOLS)

    def describe_tools(self) -> str:
        lines = []
        for name, info in self.tools.items():
            params = ", ".join(f"{k}: {v}" for k, v in info["parameters"].items())
            lines.append(f"- {name}({params}): {info['description']}")
        return "\n".join(lines)

    def execute(self, tool_name: str, arguments: dict) -> str:
        if tool_name not in self.tools:
            return f"Unknown tool: {tool_name}"
        fn = self.tools[tool_name]["fn"]
        try:
            return fn(**arguments)
        except TypeError as e:
            return f"Error calling {tool_name}: {e}"
