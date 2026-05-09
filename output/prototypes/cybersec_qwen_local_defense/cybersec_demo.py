#!/usr/bin/env python3
"""
CyberSecQwen-4B Demo — Mock inference for CWE classification, CVE-to-CWE mapping,
and defensive analyst Q&A.

When the real model is available (12 GB VRAM + `pip install torch transformers accelerate`),
set USE_REAL_MODEL=1 to load lablab-ai-amd-developer-hackathon/CyberSecQwen-4B from HF.
"""

import os
import json
import sys
import textwrap
from typing import List, Dict

# ---------------------------------------------------------------------------
# Mock knowledge base — curated CWE mapping data
# ---------------------------------------------------------------------------

CWE_DB: Dict[str, Dict] = {
    "CWE-22": {
        "name": "Path Traversal",
        "keywords": ["path traversal", "directory traversal", "../", "file path", "file()"],
        "description": "Improper limitation of a pathname to a restricted directory.",
    },
    "CWE-79": {
        "name": "Cross-site Scripting (XSS)",
        "keywords": ["xss", "cross-site scripting", "script injection", "innerhtml", "document.write"],
        "description": "Improper neutralization of input during web page generation.",
    },
    "CWE-89": {
        "name": "SQL Injection",
        "keywords": ["sql injection", "sqli", "string concatenation sql", "unsanitized query"],
        "description": "Improper neutralization of special elements used in an SQL command.",
    },
    "CWE-78": {
        "name": "OS Command Injection",
        "keywords": ["command injection", "os.system", "subprocess", "shell=true", "exec("],
        "description": "Improper neutralization of special elements used in an OS command.",
    },
    "CWE-287": {
        "name": "Improper Authentication",
        "keywords": ["authentication bypass", "auth bypass", "missing authentication", "credential"],
        "description": "When an actor claims to have a given identity, the product does not prove that claim is correct.",
    },
    "CWE-502": {
        "name": "Deserialization of Untrusted Data",
        "keywords": ["deserialization", "pickle", "yaml.load", "unserialize", "objectinputstream"],
        "description": "The product deserializes untrusted data without sufficiently verifying that the resulting data will be valid.",
    },
    "CWE-200": {
        "name": "Exposure of Sensitive Information",
        "keywords": ["information disclosure", "sensitive data", "error message", "stack trace", "verbose error"],
        "description": "The product exposes sensitive information to an actor not authorized to access it.",
    },
    "CWE-119": {
        "name": "Buffer Overflow",
        "keywords": ["buffer overflow", "buffer overrun", "out-of-bounds write", "memcpy", "strcpy"],
        "description": "The product performs operations on a memory buffer without restricting the size of input.",
    },
}

# Sample CVEs for demo
SAMPLE_CVES = [
    {
        "cve_id": "CVE-2024-21762",
        "description": "A out-of-bounds write vulnerability in Fortinet FortiOS allows attacker to execute unauthorized code via specially crafted HTTP requests.",
        "expected_cwe": "CWE-119",
    },
    {
        "cve_id": "CVE-2023-44487",
        "description": "The HTTP/2 protocol allows a denial of service (server resource consumption) because request cancellation can reset many streams quickly. aka Rapid Reset Attack.",
        "expected_cwe": "CWE-400",
    },
    {
        "cve_id": "CVE-2024-3400",
        "description": "A command injection vulnerability in Palo Alto Networks PAN-OS allows an unauthenticated attacker to execute arbitrary OS commands with root privileges.",
        "expected_cwe": "CWE-78",
    },
]

SAMPLE_QUERIES = [
    {
        "task": "CWE Classification",
        "query": "Path traversal in a Java web app where user-controlled input concatenates into a File() path. What's the CWE?",
    },
    {
        "task": "CWE Classification",
        "query": "A PHP application directly embeds user-supplied data into SQL queries using string concatenation without parameterized statements.",
    },
    {
        "task": "Defensive Analyst Q&A",
        "query": "What is the difference between CWE-79 (XSS) and CWE-89 (SQL Injection) in terms of attack surface?",
    },
]

QA_RESPONSES = {
    "xss.*sql|sql.*xss": (
        "CWE-79 (XSS) targets the client-side: malicious scripts execute in a victim's browser "
        "when the application reflects or stores unsanitized input in HTML output. The attack surface "
        "is any user-facing page that renders dynamic content.\n\n"
        "CWE-89 (SQL Injection) targets the server-side database layer: attacker-supplied input "
        "modifies the structure of SQL queries. The attack surface is any endpoint that constructs "
        "SQL from user input.\n\n"
        "Key distinction: XSS compromises the user's session/browser; SQLi compromises the backend data store."
    ),
}


def classify_cwe(description: str) -> Dict:
    """Mock CWE classification — keyword matching against CWE database."""
    desc_lower = description.lower()
    best_match = None
    best_score = 0

    for cwe_id, info in CWE_DB.items():
        score = sum(1 for kw in info["keywords"] if kw in desc_lower)
        if score > best_score:
            best_score = score
            best_match = (cwe_id, info)

    if best_match:
        cwe_id, info = best_match
        return {
            "cwe_id": cwe_id,
            "cwe_name": info["name"],
            "confidence": min(0.95, 0.6 + best_score * 0.1),
            "justification": info["description"],
        }
    return {
        "cwe_id": "CWE-NVD",
        "cwe_name": "Insufficient Information",
        "confidence": 0.3,
        "justification": "Could not confidently map to a specific CWE. Manual analyst review recommended.",
    }


def map_cve_to_cwe(cve: Dict) -> Dict:
    """Mock CVE-to-CWE mapping."""
    result = classify_cwe(cve["description"])
    return {
        "cve_id": cve["cve_id"],
        "mapped_cwe": result["cwe_id"],
        "cwe_name": result["cwe_name"],
        "confidence": result["confidence"],
        "description_snippet": cve["description"][:100] + "...",
    }


def answer_qa(query: str) -> str:
    """Mock defensive analyst Q&A."""
    import re
    for pattern, answer in QA_RESPONSES.items():
        if re.search(pattern, query.lower()):
            return answer
    # Generic fallback
    result = classify_cwe(query)
    if result["cwe_id"] != "CWE-NVD":
        return (
            f"Based on your query, the most relevant weakness is {result['cwe_id']} "
            f"({result['cwe_name']}): {result['justification']}"
        )
    return "This query requires deeper analysis. In production, CyberSecQwen-4B would provide a detailed response."


def print_section(title: str) -> None:
    width = 70
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}")


def print_result(label: str, value: str, indent: int = 2) -> None:
    prefix = " " * indent
    wrapped = textwrap.fill(value, width=66, initial_indent="", subsequent_indent=prefix)
    print(f"{prefix}{label}: {wrapped}")


def run_real_model():
    """Load and run the actual CyberSecQwen-4B model."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        print("ERROR: torch and transformers required. Run: pip install torch transformers accelerate")
        sys.exit(1)

    model_id = "lablab-ai-amd-developer-hackathon/CyberSecQwen-4B"
    print(f"Loading {model_id} ...")
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.bfloat16, device_map="auto"
    )

    for sample in SAMPLE_QUERIES:
        messages = [
            {"role": "system", "content": "You are a defensive cybersecurity assistant. Answer with the canonical CWE-ID first, then 1-3 sentences of justification."},
            {"role": "user", "content": sample["query"]},
        ]
        prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        out = model.generate(
            **tok(prompt, return_tensors="pt").to(model.device),
            max_new_tokens=256,
            temperature=0.3,
        )
        print_section(sample["task"])
        print(f"  Query: {sample['query']}")
        print(f"  Response: {tok.decode(out[0], skip_special_tokens=True)}")


def run_mock_demo():
    """Run the mock demo — no GPU or model download needed."""
    print_section("CyberSecQwen-4B Demo (Mock Mode)")
    print("  Simulating model responses with curated CWE knowledge base.")
    print("  Set USE_REAL_MODEL=1 to use the actual 4B model (requires GPU).\n")

    # --- Task 1: CWE Classification ---
    print_section("Task 1: CWE Classification")
    for sample in SAMPLE_QUERIES:
        if sample["task"] != "CWE Classification":
            continue
        result = classify_cwe(sample["query"])
        print(f"\n  Query: {sample['query']}")
        print_result("CWE-ID", result["cwe_id"])
        print_result("Name", result["cwe_name"])
        print_result("Confidence", f"{result['confidence']:.2f}")
        print_result("Justification", result["justification"])

    # --- Task 2: CVE-to-CWE Mapping ---
    print_section("Task 2: CVE-to-CWE Mapping")
    print(f"\n  {'CVE ID':<20} {'Mapped CWE':<12} {'CWE Name':<35} {'Conf.'}")
    print(f"  {'-'*20} {'-'*12} {'-'*35} {'-'*5}")
    for cve in SAMPLE_CVES:
        result = map_cve_to_cwe(cve)
        print(f"  {result['cve_id']:<20} {result['mapped_cwe']:<12} {result['cwe_name']:<35} {result['confidence']:.2f}")

    # --- Task 3: Defensive Analyst Q&A ---
    print_section("Task 3: Defensive Analyst Q&A")
    qa_query = SAMPLE_QUERIES[2]["query"]
    print(f"\n  Q: {qa_query}\n")
    answer = answer_qa(qa_query)
    for line in answer.split("\n"):
        print(f"  {line}")

    # --- Summary ---
    print_section("Performance (from published benchmarks)")
    print("  CTI-MCQ (2,500 items):    0.587  (+8.7pp over Foundation-Sec-8B)")
    print("  CTI-RCM (1,000 CVE->CWE): 0.666  (97.3% of 8B accuracy @ half params)")
    print("  Base model: Qwen3-4B-Instruct-2507 + LoRA (r=64, alpha=64)")
    print("  License: Apache 2.0\n")

    # --- JSON output sample ---
    print_section("Sample JSON Output (for integration)")
    sample_output = {
        "model": "CyberSecQwen-4B",
        "task": "cwe_classification",
        "input": SAMPLE_QUERIES[0]["query"],
        "result": classify_cwe(SAMPLE_QUERIES[0]["query"]),
    }
    print(json.dumps(sample_output, indent=2))
    print()


def main():
    if os.environ.get("USE_REAL_MODEL", "0") == "1":
        run_real_model()
    else:
        run_mock_demo()


if __name__ == "__main__":
    main()
