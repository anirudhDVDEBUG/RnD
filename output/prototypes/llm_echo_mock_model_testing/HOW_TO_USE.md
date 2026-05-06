# How to Use llm-echo

## Install

```bash
# Option A: pip install (permanent)
pip install llm llm-echo

# Option B: uvx one-liner (ephemeral, nothing installed globally)
uvx --with llm --with llm-echo llm -m echo "hello"
```

Requires Python 3.9+. No API keys needed.

## As a Claude Skill

Drop the skill file into your Claude Code skills directory:

```
~/.claude/skills/llm_echo_mock_model_testing/SKILL.md
```

**Trigger phrases that activate it:**

- "I need a mock model to test my LLM pipeline"
- "How do I write automated tests for code that uses the llm CLI?"
- "Set up a test harness for LLM-based automation"
- "I want a fake LLM model that echoes back my prompt"

Once installed, Claude Code will automatically suggest using `llm-echo` when you ask about mocking or testing LLM pipelines.

## First 60 Seconds

### 1. Install and verify

```bash
pip install llm llm-echo
llm models list | grep echo
# → echo: echo
```

### 2. Run basic echo

```bash
$ llm -m echo "What is 2+2?"
{"prompt": "What is 2+2?"}
```

### 3. Test with thinking/reasoning blocks (v0.5a0+)

```bash
$ llm -m echo "explain gravity" -o thinking 1
# stderr shows a simulated reasoning block
# stdout shows the echoed JSON response
```

### 4. Use in a test script

```bash
result=$(llm -m echo "expected input")
if echo "$result" | grep -q "expected input"; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi
```

### 5. Use in Python

```python
import llm

model = llm.get_model("echo")
response = model.prompt("test prompt")
text = response.text()
assert "test prompt" in text  # passes every time, no API call
```

### 6. Run the full demo

```bash
bash run.sh
```

Expected output:

```
==============================================================
  llm-echo Mock Model — Test Suite
==============================================================

LLM version: llm, version 0.x
Echo model: available

[TEST 1] Basic echo
  Prompt:  What is the capital of France?
  Output:  {"prompt": "What is the capital of France?"}
  Result:  PASS

[TEST 2] JSON structure
  ...
  Result:  PASS (valid JSON)

[TEST 3] Pipeline mock — chained prompts
  Step 1: prompt echoed correctly
  Step 2: prompt echoed correctly
  Step 3: prompt echoed correctly
  Result:  PASS (all pipeline steps verified)

[TEST 4] Python API (llm library)
  ...
  Result:  PASS

==============================================================
  Results: 4 passed, 0 failed
==============================================================
```
