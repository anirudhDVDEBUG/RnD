"""
Specialist Agent: represents an isolated agent with its own workspace, memory, and tools.
In mock mode, simulates Claude-powered reasoning without API calls.
"""

import os
import json
import time
from datetime import datetime


class AgentMemory:
    """Persistent per-agent memory stored as JSON in the agent's workspace."""

    def __init__(self, workspace):
        self.path = os.path.join(workspace, ".agent_memory.json")
        self.entries = []
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.entries = json.load(f)

    def add(self, key, value):
        self.entries.append({"key": key, "value": value, "ts": datetime.now().isoformat()})

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def recall(self, key=None):
        if key:
            return [e for e in self.entries if e["key"] == key]
        return self.entries


class SpecialistAgent:
    """An isolated specialist agent with workspace, memory, and scoped tools."""

    def __init__(self, name, workspace, tools, prompt, use_api=False):
        self.name = name
        self.workspace = os.path.abspath(workspace)
        self.tools = tools
        self.prompt = prompt
        self.use_api = use_api
        self.memory = AgentMemory(self.workspace)
        self.log = []

    def setup_workspace(self):
        os.makedirs(self.workspace, exist_ok=True)

    def execute_subtask(self, subtask):
        """Execute a subtask. Uses mock reasoning by default."""
        self.setup_workspace()
        start = time.time()

        self._log(f"Starting subtask: {subtask['title']}")
        self.memory.add("subtask_started", subtask["title"])

        if self.use_api:
            result = self._call_claude(subtask)
        else:
            result = self._mock_execute(subtask)

        elapsed = time.time() - start
        self.memory.add("subtask_completed", {
            "title": subtask["title"],
            "elapsed_s": round(elapsed, 2),
            "status": result["status"],
        })
        self.memory.save()

        # Write artifact to workspace
        artifact_path = os.path.join(self.workspace, f"{subtask['id']}_result.md")
        with open(artifact_path, "w") as f:
            f.write(f"# {subtask['title']}\n\n")
            f.write(f"Agent: {self.name}\n")
            f.write(f"Status: {result['status']}\n\n")
            f.write(result["output"])

        self._log(f"Completed: {result['status']} ({elapsed:.2f}s)")
        return result

    def _mock_execute(self, subtask):
        """Simulate agent work without API calls."""
        mock_outputs = {
            "backend-specialist": (
                "## Implementation Plan\n\n"
                "1. Created data model `User` with fields: id, email, password_hash, created_at\n"
                "2. Added REST endpoints: POST /auth/register, POST /auth/login, GET /auth/me\n"
                "3. Implemented JWT token generation and validation middleware\n"
                "4. Added input validation with Pydantic schemas\n\n"
                "```python\n"
                "class User(BaseModel):\n"
                "    id: int\n"
                "    email: str\n"
                "    password_hash: str\n"
                "    created_at: datetime\n"
                "```\n"
            ),
            "frontend-specialist": (
                "## UI Components Created\n\n"
                "1. `LoginForm` component with email/password fields\n"
                "2. `RegisterForm` component with validation\n"
                "3. `AuthContext` provider for session state management\n"
                "4. Protected route wrapper `RequireAuth`\n\n"
                "```jsx\n"
                "function LoginForm({ onSuccess }) {\n"
                "  const [email, setEmail] = useState('');\n"
                "  const [password, setPassword] = useState('');\n"
                "  // ...\n"
                "}\n"
                "```\n"
            ),
            "reviewer": (
                "## Code Review Summary\n\n"
                "### Backend\n"
                "- [PASS] Data model follows conventions\n"
                "- [PASS] Endpoints use proper HTTP methods\n"
                "- [WARN] Consider rate-limiting on /auth/login\n"
                "- [PASS] JWT expiry is set correctly\n\n"
                "### Frontend\n"
                "- [PASS] Components are well-structured\n"
                "- [WARN] Add loading state to LoginForm\n"
                "- [PASS] Auth context properly clears on logout\n\n"
                "**Verdict: Approved with minor suggestions**\n"
            ),
        }

        output = mock_outputs.get(self.name, f"Completed subtask: {subtask['title']}")
        time.sleep(0.1)  # Simulate work
        return {"status": "completed", "output": output, "agent": self.name}

    def _call_claude(self, subtask):
        """Call Claude API for real agent work (requires ANTHROPIC_API_KEY)."""
        try:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=self.prompt,
                messages=[{"role": "user", "content": f"Complete this subtask:\n\n{json.dumps(subtask)}"}],
            )
            return {
                "status": "completed",
                "output": response.content[0].text,
                "agent": self.name,
            }
        except Exception as e:
            return {
                "status": "error",
                "output": f"API call failed: {e}",
                "agent": self.name,
            }

    def _log(self, message):
        entry = f"[{self.name}] {message}"
        self.log.append(entry)
        print(f"  {entry}")
