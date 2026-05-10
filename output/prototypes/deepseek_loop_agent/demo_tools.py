"""Demo: show built-in tools working standalone."""

from tools import ToolRegistry

reg = ToolRegistry()
print("Available tools:")
print(reg.describe_tools())
print()

# Demo: glob for Python files
print('>> glob("*.py"):')
print(reg.execute("glob", {"pattern": "*.py", "path": "."}))
print()

# Demo: file_read (first 5 lines of run.sh)
print('>> file_read("run.sh", limit=5):')
print(reg.execute("file_read", {"path": "run.sh", "limit": 5}))
print()

# Demo: bash
print('>> bash("echo Hello from DeepSeek Loop"):')
print(reg.execute("bash", {"command": "echo Hello from DeepSeek Loop"}))
