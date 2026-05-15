"""
Sample multi-agent harness with intentional token waste patterns.
This file is designed to trigger multiple audit findings.
"""

# === Category 1: Redundant Context ===
# Reading the same config file in multiple places
config = read_file("config.yaml")
settings = read_file("config.yaml")  # duplicate read!

# === Category 2: Oversized Prompts ===
SYSTEM_PROMPT = """
You are a helpful AI assistant. Please be concise and thorough.
Think step by step about every problem.
You are a code review expert. Your role is to analyze code.
Act as a senior software engineer with 20 years of experience.
Take a deep breath and think carefully about each response.
Answer carefully and be thorough in your analysis.

Example 1: When reviewing a function, check for edge cases.
Example 2: When reviewing a class, check for SOLID principles.
Example 3: When reviewing tests, check for coverage.
Example 4: When reviewing docs, check for accuracy.
"""

# === Category 3: Unbounded History ===
messages = []

def chat(user_input):
    messages.append({"role": "user", "content": user_input})
    # No truncation, no windowing, no summarization
    response = call_llm(messages=messages)
    messages.append({"role": "assistant", "content": response})
    return response

def process_batch(items):
    for item in items:
        messages.append({"role": "user", "content": item})
        messages.append({"role": "assistant", "content": "processed"})
    # Messages grow without bound!

# === Category 4: Duplicate Tool Results ===
def analyze_codebase():
    result1 = tool_call("grep", pattern="TODO")
    result2 = tool_call("grep", pattern="FIXME")
    result3 = tool_call("grep", pattern="TODO")  # duplicate!
    # No caching of any kind
    tool_call("read_file", path="main.py")
    tool_call("read_file", path="main.py")  # duplicate!

# === Category 5: Verbose Output ===
def format_response(question, answer):
    return f"""
    You asked: {question}
    Let me repeat your question to make sure I understand.
    Your question was about: {question}
    As you mentioned, this is important.
    Here is my detailed answer: {answer}
    """

# === Category 6: Unnecessary Re-reads ===
def process_files():
    data1 = open("data.json").read()
    # ... some processing ...
    data2 = open("data.json").read()  # re-read same file!
    config = open("settings.yaml").read()
    # ... more processing ...
    config_again = open("settings.yaml").read()  # re-read!

# === Category 7: Broad File Inclusion ===
import glob as glob_mod
all_files = glob_mod.glob("**/*")  # grabs everything!
# Including node_modules and __pycache__ without filtering

# === Category 8: Uncompressed Examples ===
FEW_SHOT_EXAMPLES = """
Example 1: Input: "Hello" -> Output: "Hi there!"
Example 2: Input: "How are you?" -> Output: "I'm doing well!"
Example 3: Input: "What's up?" -> Output: "Not much!"
Example 4: Input: "Good morning" -> Output: "Good morning to you!"
Example 5: Input: "Hey" -> Output: "Hey there!"
"""

# === Category 9: Idle Agent Overhead ===
def run_pipeline():
    Agent("format text")
    Agent("add period")
    delegate("capitalize first letter")

# === Category 10: Retry Amplification ===
max_retries = 3
retry = 0
def call_with_retry(prompt):
    retries = 0
    while retries < max_retries:
        try:
            return call_llm(prompt)
        except Exception:
            retries += 1
            # No context reduction on retry!
            # Full prompt resent every time
