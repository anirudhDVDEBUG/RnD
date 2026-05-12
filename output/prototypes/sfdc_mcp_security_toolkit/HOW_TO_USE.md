# How to Use

## Install (local demo)

```bash
git clone <this-repo>
cd sfdc_mcp_security_toolkit
# No pip install needed — stdlib only, Python 3.8+
bash run.sh
```

## Install (full Salesforce toolkit)

```bash
# 1. Clone the upstream repo
git clone https://github.com/ccmalcom/SFDC-MCP-Security-Toolkit.git
cd SFDC-MCP-Security-Toolkit

# 2. Authenticate Salesforce CLI to a SANDBOX (never production)
sf org login web --alias my-sandbox

# 3. Deploy Apex classes and custom objects
sf project deploy start --target-org my-sandbox

# 4. Seed ~270 adversarial records
sf apex run --target-org my-sandbox --file scripts/seed-data.apex

# 5. Connect your MCP server to the sandbox and test

# 6. Clean up when done
sf apex run --target-org my-sandbox --file scripts/cleanup.apex
```

## As a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/sfdc-mcp-security-toolkit
cp SKILL.md ~/.claude/skills/sfdc-mcp-security-toolkit/SKILL.md
```

**Trigger phrases** that activate the skill:

- "Set up adversarial security testing for my Salesforce MCP integration"
- "Test my Salesforce org for prompt injection vulnerabilities via MCP"
- "Seed my Salesforce sandbox with attack payloads to test MCP security"
- "Run honeytoken leakage and encoding bypass tests against SFDC MCP"
- "Audit my Salesforce MCP server for cross-tenant boundary issues"

## First 60 Seconds

```
$ bash run.sh

SFDC MCP Security Toolkit — Local Demo
=======================================

PAYLOAD CATEGORIES
------------------------------------------------------------------------
  [!!] Direct Prompt Injection                    critical   5 payloads
  [!!] Indirect Prompt Injection                  critical   5 payloads
  [! ] Honeytoken / Canary Leakage                high       5 payloads
  [! ] Encoding Bypasses (Unicode / HTML / Base64) high       5 payloads
  [!!] Cross-Tenant Boundary Probes               critical   5 payloads
  ...

  Total: 70 adversarial payloads across 14 categories

Generated 70 adversarial Salesforce records (mock data).

Running simulated MCP security scan...

SCAN RESULTS
------------------------------------------------------------------------
  Records scanned:    70
  Vulnerable:         27
  Secure:             43
  Pass rate:          61.4%

  Findings by severity:
    CRITICAL     14
    HIGH         9
    MEDIUM       4

TOP FINDINGS (first 15)
------------------------------------------------------------------------
  [!!] LEAK-001 | Honeytoken Leaked
       Record: REC-0011 (Case) | Category: honeytoken_leakage
       A honeytoken or canary value appeared in output...

  [!!] EXEC-001 | Instruction Following Detected
       Record: REC-0006 (Contact) | Category: prompt_injection_indirect
       The LLM appears to have followed injected instructions...
  ...

RECOMMENDATIONS
------------------------------------------------------------------------
  1. Sanitize all Salesforce field values before passing to LLM context.
  2. Implement output filtering to catch honeytoken/canary leakage.
  ...

Full JSON report exported to: report.json
```

The JSON report (`report.json`) contains per-record results for CI integration or further analysis.
