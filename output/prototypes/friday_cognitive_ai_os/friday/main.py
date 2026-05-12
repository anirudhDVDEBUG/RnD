"""FRIDAY Autonomous Cognitive AI OS - Main entry point."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from config import GEMINI_API_KEY, MEMORY_FILE, MOCK_MODE
from modules.memory.memory_manager import MemoryManager
from modules.reasoning.cognitive_engine import CognitiveEngine
from modules.voice.voice_controller import VoiceController
from modules.cyber.scanner import scan_localhost_ports, system_info
from modules.automation.task_runner import TaskRunner


BANNER = r"""
  _____ ____  ___ ____    _ __   __
 |  ___|  _ \|_ _|  _ \  / \\ \ / /
 | |_  | |_) || || | | |/ _ \\ V /
 |  _| |  _ < | || |_| / ___ \| |
 |_|   |_| \_\___|____/_/   \_\_|

  Autonomous Cognitive AI Operating System
  =========================================
"""


def run_demo():
    """Non-interactive demo showcasing all subsystems."""
    print(BANNER)
    mode = "Gemini API" if not MOCK_MODE else "Mock (no API key)"
    print(f"  Mode: {mode}\n")

    # 1. Memory
    print("[1/5] Initializing Memory System...")
    memory = MemoryManager(MEMORY_FILE)
    print(f"  Loaded {memory.get_stats()['total_memories']} prior memories from {MEMORY_FILE}")

    # 2. Cognitive Engine
    print("[2/5] Starting Cognitive Engine...")
    brain = CognitiveEngine(memory, api_key=GEMINI_API_KEY)

    # 3. Demo reasoning with multi-turn memory
    print("[3/5] Running Reasoning Demo...\n")
    queries = [
        "How should I plan a new Python project with CI/CD?",
        "What security measures should I implement for a web API?",
        "Can you recall what we discussed about planning?",
    ]
    for q in queries:
        print(f"  You > {q}")
        response = brain.think(q)
        print(f"  FRIDAY > {response}\n")

    # 4. Self-reflection
    print("[4/5] Self-Reflection...")
    print(f"  {brain.self_reflect()}\n")

    # 5. System scan & automation
    print("[5/5] System Awareness & Automation...")
    info = system_info()
    print(f"  Platform: {info['platform']}")
    print(f"  Hostname: {info['hostname']}")
    print(f"  Python:   {info['python']}")

    runner = TaskRunner()
    runner.add_task("localhost_port_scan", scan_localhost_ports, [[80, 443, 8080]])
    results = runner.run_all()
    print("\n  Localhost Port Scan:")
    for r in results:
        if r["status"] == "ok":
            for p in r["result"]:
                print(f"    Port {p['port']:>5}: {p['status']}")
        else:
            print(f"    Error: {r['error']}")

    # Memory stats
    print(f"\n  Session complete. {memory.get_stats()['session_memories']} new memories stored.")
    print("  Memory file:", memory.get_stats()["file"])
    print("\n  FRIDAY is ready. Run interactively with: python friday/main.py --interactive\n")


def run_interactive():
    """Interactive REPL mode."""
    print(BANNER)
    memory = MemoryManager(MEMORY_FILE)
    brain = CognitiveEngine(memory, api_key=GEMINI_API_KEY)
    voice = VoiceController(use_audio=False)

    voice.speak("FRIDAY online. Type 'quit' to exit, 'reflect' for self-check, 'scan' for port scan.")
    while True:
        try:
            user_input = voice.listen()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input.strip():
            continue
        cmd = user_input.strip().lower()
        if cmd in ("quit", "exit", "shutdown"):
            voice.speak("Shutting down. Goodbye.")
            break
        elif cmd == "reflect":
            voice.speak(brain.self_reflect())
        elif cmd == "scan":
            ports = scan_localhost_ports()
            open_ports = [p for p in ports if p["status"] == "open"]
            if open_ports:
                voice.speak(f"Found {len(open_ports)} open ports: {', '.join(str(p['port']) for p in open_ports)}")
            else:
                voice.speak("No open ports detected on common ports.")
        else:
            response = brain.think(user_input)
            voice.speak(response)


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        run_interactive()
    else:
        run_demo()
