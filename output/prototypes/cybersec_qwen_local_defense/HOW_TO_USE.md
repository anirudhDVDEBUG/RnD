# How to Use CyberSecQwen-4B

## Installation

### Mock demo (no GPU needed)

```bash
# Clone or copy this directory, then:
bash run.sh
```

The demo uses Python 3.8+ stdlib only — no external packages required.

### Real model inference

```bash
pip install torch transformers accelerate
# Then run with:
USE_REAL_MODEL=1 bash run.sh
```

**Hardware requirement:** 12 GB VRAM (e.g. RTX 3060 12GB, RTX 4070, RX 7800 XT). For edge/low-VRAM: quantize to Q4_K_M (~2.5 GB).

### High-throughput serving (optional)

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model lablab-ai-amd-developer-hackathon/CyberSecQwen-4B
# Query at http://localhost:8000/v1/chat/completions
```

## Claude Code Skill Setup

This is a **Claude Code Skill**. To install:

1. Copy the skill folder:
   ```bash
   mkdir -p ~/.claude/skills/cybersec_qwen_local_defense
   cp SKILL.md ~/.claude/skills/cybersec_qwen_local_defense/SKILL.md
   ```

2. Trigger phrases that activate the skill:
   - "Classify this vulnerability to a CWE category locally"
   - "Set up a local model for CVE triage"
   - "Deploy CyberSecQwen-4B for air-gapped security analysis"
   - "Map CVE descriptions to CWE IDs without cloud APIs"
   - "I need a defensive cybersecurity LLM on consumer hardware"

3. Claude will walk you through loading the model and querying it for CWE classification, CVE mapping, or defensive Q&A.

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output (abbreviated):**
```
======================================================================
  CyberSecQwen-4B Demo (Mock Mode)
======================================================================
  Simulating model responses with curated CWE knowledge base.

======================================================================
  Task 1: CWE Classification
======================================================================

  Query: Path traversal in a Java web app where user-controlled input
         concatenates into a File() path. What's the CWE?
  CWE-ID: CWE-22
  Name: Path Traversal
  Confidence: 0.80
  Justification: Improper limitation of a pathname to a restricted directory.

======================================================================
  Task 2: CVE-to-CWE Mapping
======================================================================

  CVE ID               Mapped CWE   CWE Name                            Conf.
  -------------------- ------------ ----------------------------------- -----
  CVE-2024-21762       CWE-119      Buffer Overflow                     0.70
  CVE-2023-44487       CWE-NVD      Insufficient Information            0.30
  CVE-2024-3400        CWE-78       OS Command Injection                0.70

======================================================================
  Task 3: Defensive Analyst Q&A
======================================================================

  Q: What is the difference between CWE-79 (XSS) and CWE-89 (SQL Injection)?

  CWE-79 targets the client-side: malicious scripts execute in a victim's
  browser. CWE-89 targets the server-side database layer...
```

**With real model:**
```bash
USE_REAL_MODEL=1 python3 cybersec_demo.py
```
This downloads the 4B model (~8 GB), loads it onto your GPU, and runs actual inference on the same sample queries.

## Programmatic Usage

```python
from cybersec_demo import classify_cwe, map_cve_to_cwe

# CWE classification
result = classify_cwe("Buffer overflow in memcpy call with unchecked length")
print(result)
# {'cwe_id': 'CWE-119', 'cwe_name': 'Buffer Overflow', 'confidence': 0.80, ...}

# CVE-to-CWE mapping
cve = {"cve_id": "CVE-2024-3400", "description": "Command injection in PAN-OS..."}
print(map_cve_to_cwe(cve))
```
