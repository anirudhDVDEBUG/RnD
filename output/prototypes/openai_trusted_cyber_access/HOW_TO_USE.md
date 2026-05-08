# How to Use

## Install

```bash
git clone <this-repo>
cd openai_trusted_cyber_access
pip install -r requirements.txt   # just `openai>=1.0.0`
```

## Run the Demo

```bash
bash run.sh
# or directly:
python cyber_analyzer.py
```

No API key is required — the demo runs with realistic mock data by default. To use the real GPT-5.5-Cyber model:

```bash
export OPENAI_API_KEY=sk-...
python cyber_analyzer.py
```

## As a Claude Skill

This is packaged as a Claude Code skill. To install:

1. Copy the skill folder:
   ```bash
   mkdir -p ~/.claude/skills/openai_trusted_cyber_access
   cp SKILL.md ~/.claude/skills/openai_trusted_cyber_access/SKILL.md
   ```

2. Trigger phrases that activate the skill:
   - "openai cyber"
   - "trusted access vulnerability"
   - "gpt-5.5 cyber"
   - "defensive security openai"
   - "vulnerability research openai"
   - "How do I get access to OpenAI's GPT-5.5-Cyber model?"
   - "What is OpenAI's Trusted Access for Cyber program?"
   - "Help me set up a defensive cybersecurity workflow using GPT-5.5-Cyber"

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output** (abridged):
```
======================================================================
  OpenAI Trusted Access for Cyber -- GPT-5.5-Cyber Demo
======================================================================

  Mode: MOCK (no API key)

----------------------------------------------------------------------
  DEMO 1: Vulnerability Discovery in Source Code
----------------------------------------------------------------------

  Target: auth_handler.c

  ***[CRITICAL] VULN-001: Buffer Overflow (CWE-120)***
    Line 42: strncpy(session_token, user_input, sizeof(session_token));
    Suggested patch:
      + strncpy(session_token, user_input, sizeof(session_token) - 1);
      + session_token[sizeof(session_token) - 1] = '\0';

  **[HIGH] VULN-002: SQL Injection (CWE-89)**
    Line 87: snprintf(query, ..., "SELECT * FROM users WHERE name='%s'", username);
    Suggested patch:
      + sqlite3_prepare_v2(db, "SELECT * FROM users WHERE name=?", ...);

  *[MEDIUM] VULN-003: Time-of-Check Time-of-Use Race (CWE-367)*
    Line 134: if (access(filepath, R_OK) == 0) { fd = open(filepath, O_RDONLY); }
    Suggested patch:
      + fd = open(filepath, O_RDONLY | O_NOFOLLOW);

----------------------------------------------------------------------
  DEMO 2: CVE Exploit Analysis (CVE-2024-3094 -- XZ Backdoor)
----------------------------------------------------------------------

  CVE:      CVE-2024-3094
  CVSS:     10.0
  Mechanism: The backdoor modifies liblzma to intercept RSA_public_decrypt()...
  Detection Signatures:
    - Check xz --version for 5.6.0 or 5.6.1
    - YARA rule: match on bytes {f4 8d 83 c6 8d 83} in liblzma.so

----------------------------------------------------------------------
  DEMO 3: Kubernetes Deployment Hardening Audit
----------------------------------------------------------------------

  Security Score: 2/10
  [CRITICAL] Container runs as root
  [HIGH] No resource limits
  [HIGH] hostNetwork: true exposes all host ports
```

## Using the OpenAI API Directly

Once approved for Trusted Access, integrate into your own tools:

```python
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-5.5-cyber",  # specialized cyber model
    messages=[
        {
            "role": "system",
            "content": "You are a defensive security analyst helping identify "
                       "vulnerabilities in authorized target systems."
        },
        {
            "role": "user",
            "content": "Analyze this code for memory safety vulnerabilities "
                       "and suggest patches:\n\n<your code here>"
        }
    ],
    temperature=0.2,
)

print(response.choices[0].message.content)
```

Key difference from standard GPT-5.5: the `gpt-5.5-cyber` model has reduced safety refusals for legitimate defensive security queries that the base model would decline.
