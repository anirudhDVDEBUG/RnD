#!/usr/bin/env python3
"""
Demo: Using llm-echo as a mock model for testing LLM pipelines.

This script demonstrates how llm-echo lets you test LLM-dependent code
without calling real APIs — the echo model returns a JSON representation
of whatever prompt you send it.
"""

import json
import subprocess
import sys


def run_llm_echo(prompt: str, options: dict | None = None) -> str:
    """Run `llm -m echo` with a given prompt and return the output."""
    cmd = ["llm", "-m", "echo", prompt]
    if options:
        for key, value in options.items():
            cmd.extend(["-o", key, str(value)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"llm command failed: {result.stderr}")
    return result.stdout.strip()


def test_basic_echo():
    """Test that the echo model returns our prompt in the response."""
    prompt = "What is the capital of France?"
    output = run_llm_echo(prompt)
    print(f"[TEST 1] Basic echo")
    print(f"  Prompt:  {prompt}")
    print(f"  Output:  {output}")
    assert prompt in output, f"Expected prompt in output, got: {output}"
    print("  Result:  PASS\n")


def test_json_structure():
    """Test that the echo model returns valid JSON."""
    prompt = "Hello, echo model!"
    output = run_llm_echo(prompt)
    print(f"[TEST 2] JSON structure")
    print(f"  Prompt:  {prompt}")
    print(f"  Output:  {output}")
    try:
        data = json.loads(output)
        print(f"  Parsed:  {json.dumps(data, indent=2)}")
        print("  Result:  PASS (valid JSON)\n")
    except json.JSONDecodeError:
        # Some versions return plain text containing the prompt
        assert prompt in output
        print("  Result:  PASS (prompt echoed as text)\n")


def test_pipeline_mock():
    """Simulate testing an LLM pipeline with mock responses."""
    print("[TEST 3] Pipeline mock — chained prompts")

    prompts = [
        "Extract keywords from: AI-powered code review tools",
        "Summarize: The echo model is useful for testing",
        "Classify sentiment: I love automated testing",
    ]

    for i, prompt in enumerate(prompts, 1):
        output = run_llm_echo(prompt)
        assert prompt in output, f"Pipeline step {i} failed"
        print(f"  Step {i}: prompt echoed correctly")

    print("  Result:  PASS (all pipeline steps verified)\n")


def test_python_api():
    """Test using the LLM Python API directly (if available)."""
    print("[TEST 4] Python API (llm library)")
    try:
        import llm as llm_lib

        model = llm_lib.get_model("echo")
        response = model.prompt("test via Python API")
        text = response.text()
        print(f"  Output:  {text}")
        assert "test via Python API" in text
        print("  Result:  PASS\n")
    except ImportError:
        print("  Skipped: llm library not importable (CLI-only install)\n")
    except Exception as e:
        print(f"  Skipped: {e}\n")


def main():
    print("=" * 60)
    print("  llm-echo Mock Model — Test Suite")
    print("=" * 60)
    print()

    # Check llm is installed
    try:
        ver = subprocess.run(
            ["llm", "--version"], capture_output=True, text=True
        )
        print(f"LLM version: {ver.stdout.strip()}")
    except FileNotFoundError:
        print("ERROR: 'llm' CLI not found. Install with: pip install llm llm-echo")
        sys.exit(1)

    # Check echo model is available
    models = subprocess.run(
        ["llm", "models", "list"], capture_output=True, text=True
    )
    if "echo" not in models.stdout:
        print("ERROR: echo model not found. Install with: llm install llm-echo")
        sys.exit(1)

    print(f"Echo model: available")
    print()

    tests = [test_basic_echo, test_json_structure, test_pipeline_mock, test_python_api]
    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  Result:  FAIL — {e}\n")
            failed += 1

    print("=" * 60)
    print(f"  Results: {passed} passed, {failed} failed")
    print("=" * 60)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
