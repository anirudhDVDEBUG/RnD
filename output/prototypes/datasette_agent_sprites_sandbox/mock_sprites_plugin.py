"""
Mock demonstration of datasette-agent-sprites plugin lifecycle.
Simulates plugin registration, command dispatch, and sandboxed execution
without requiring a Fly.io account or live API keys.
"""

import json
import time
import random
import hashlib


class MockSpritesClient:
    """Simulates the Fly Sprites API for demo purposes."""

    def __init__(self, region="iad"):
        self.region = region
        self.machines = {}

    def create_machine(self):
        machine_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        self.machines[machine_id] = {
            "id": machine_id,
            "region": self.region,
            "state": "running",
            "created_at": time.time(),
        }
        return machine_id

    def exec_command(self, machine_id, command):
        """Simulate command execution inside a sprite VM."""
        boot_time = random.uniform(0.8, 2.1)
        time.sleep(0.3)  # Simulate network + boot (shortened for demo)

        # Simulated command outputs
        outputs = {
            "ls /tmp": "sprite-session.lock\nagent-workspace/\n",
            "python --version": "Python 3.12.3\n",
            "uname -a": "Linux sprite-vm 6.1.0 #1 SMP x86_64 GNU/Linux\n",
            "whoami": "sprite-user\n",
            "cat /etc/os-release": 'NAME="Debian GNU/Linux"\nVERSION="12 (bookworm)"\n',
            "echo $HOME": "/home/sprite-user\n",
        }

        stdout = outputs.get(command, f"[executed: {command}]\n")
        return {
            "exit_code": 0,
            "stdout": stdout,
            "stderr": "",
            "duration_ms": int(boot_time * 1000),
            "machine_id": machine_id,
        }

    def destroy_machine(self, machine_id):
        if machine_id in self.machines:
            self.machines[machine_id]["state"] = "destroyed"
            del self.machines[machine_id]


class DatasetteAgentSpritesPlugin:
    """
    Mock of the datasette-agent-sprites plugin.
    Demonstrates the plugin registration and execution flow.
    """

    name = "datasette-agent-sprites"
    version = "0.1a0"

    def __init__(self):
        self.client = MockSpritesClient()
        self.execution_log = []

    def register(self):
        """Simulate plugin registration with Datasette Agent."""
        return {
            "plugin": self.name,
            "version": self.version,
            "capabilities": ["sandbox_execution"],
            "hook": "execute_command",
        }

    def execute_command(self, command: str) -> dict:
        """Execute a command in a sandboxed Fly Sprites VM."""
        # 1. Create ephemeral machine
        machine_id = self.client.create_machine()

        # 2. Execute command
        result = self.client.exec_command(machine_id, command)

        # 3. Destroy machine (ephemeral)
        self.client.destroy_machine(machine_id)

        # 4. Log execution
        self.execution_log.append({
            "command": command,
            "machine_id": machine_id,
            "result": result,
        })

        return result


def run_demo():
    """Run a full demonstration of the plugin lifecycle."""
    print("=" * 60)
    print("  datasette-agent-sprites 0.1a0 -- Demo")
    print("  Sandboxed command execution via Fly Sprites")
    print("=" * 60)
    print()

    # Step 1: Plugin registration
    print("[1] Plugin Registration")
    print("-" * 40)
    plugin = DatasetteAgentSpritesPlugin()
    reg = plugin.register()
    print(f"    Plugin: {reg['plugin']} v{reg['version']}")
    print(f"    Capabilities: {reg['capabilities']}")
    print(f"    Hook: {reg['hook']}")
    print()

    # Step 2: Simulate datasette plugins output
    print("[2] Plugin Discovery (datasette plugins)")
    print("-" * 40)
    plugins_output = [
        {"name": "datasette-agent", "version": "0.3.0"},
        {"name": "datasette-agent-sprites", "version": "0.1a0"},
    ]
    print(f"    {json.dumps(plugins_output, indent=4)}")
    print()

    # Step 3: Execute commands in sandbox
    print("[3] Sandboxed Command Execution")
    print("-" * 40)
    commands = [
        "whoami",
        "uname -a",
        "python --version",
        "ls /tmp",
        "cat /etc/os-release",
    ]

    for cmd in commands:
        result = plugin.execute_command(cmd)
        print(f"    $ {cmd}")
        print(f"      -> VM: {result['machine_id']} | "
              f"exit: {result['exit_code']} | "
              f"{result['duration_ms']}ms")
        print(f"      stdout: {result['stdout'].strip()}")
        print()

    # Step 4: Summary
    print("[4] Execution Summary")
    print("-" * 40)
    print(f"    Commands executed: {len(plugin.execution_log)}")
    print(f"    All in isolated VMs: Yes")
    print(f"    Host filesystem touched: No")
    print(f"    VMs destroyed after use: Yes")
    print(f"    Active machines remaining: {len(plugin.client.machines)}")
    print()
    print("=" * 60)
    print("  All commands ran in ephemeral sandboxes.")
    print("  No host system was modified.")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
