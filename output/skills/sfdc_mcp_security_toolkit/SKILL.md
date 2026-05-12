---
name: SFDC MCP Security Toolkit
description: |
  Adversarial MCP integration testing toolkit for Salesforce. Seeds ~270 records across Account, Contact, Case, and Outreach Log with 14 attack payload categories including prompt injection, honeytoken leakage, encoding bypasses, and cross-tenant boundary probes.
  Triggers: salesforce mcp security, sfdc adversarial testing, mcp integration security audit, salesforce prompt injection test, sfdc honeytoken test
---

# SFDC MCP Security Toolkit

Adversarial MCP integration testing toolkit for Salesforce orgs. Seeds ~270 test records with 14 attack payload categories to validate that your Salesforce MCP server integration handles malicious data safely.

## When to use

- "Set up adversarial security testing for my Salesforce MCP integration"
- "Test my Salesforce org for prompt injection vulnerabilities via MCP"
- "Seed my Salesforce sandbox with attack payloads to test MCP security"
- "Run honeytoken leakage and encoding bypass tests against SFDC MCP"
- "Audit my Salesforce MCP server for cross-tenant boundary issues"

## How to use

### Prerequisites

1. A Salesforce sandbox or scratch org (never run against production)
2. Salesforce CLI (`sf`) authenticated to the target org
3. The SFDC-MCP-Security-Toolkit repository cloned locally

### Steps

1. **Clone the toolkit** (if not already available):
   ```bash
   git clone https://github.com/ccmalcom/SFDC-MCP-Security-Toolkit.git
   cd SFDC-MCP-Security-Toolkit
   ```

2. **Deploy the Apex classes and custom objects** to your sandbox:
   ```bash
   sf project deploy start --target-org <your-sandbox-alias>
   ```

3. **Run the seed script** to create ~270 adversarial test records across Account, Contact, Case, and Outreach Log objects:
   ```bash
   sf apex run --target-org <your-sandbox-alias> --file scripts/seed-data.apex
   ```

4. **Connect your MCP server** to the seeded Salesforce org and exercise queries against the test data. The 14 attack payload categories include:
   - Prompt injection (direct and indirect)
   - Honeytoken / canary leakage
   - Encoding bypasses (Unicode, HTML, Base64)
   - Cross-tenant boundary probes
   - SOQL injection attempts
   - PII exfiltration triggers
   - Tool-use hijacking payloads
   - Markdown/HTML rendering attacks
   - System prompt extraction attempts
   - Recursive/loop-inducing prompts
   - Context window overflow payloads
   - Multi-step social engineering chains
   - Data poisoning patterns
   - Privilege escalation probes

5. **Review MCP server responses** for any payload leakage, unauthorized data access, or instruction-following on injected prompts. Flag any case where the MCP server:
   - Returns raw attack payloads without sanitization
   - Follows injected instructions from record field values
   - Leaks honeytoken values outside expected boundaries
   - Allows cross-tenant data access
   - Executes or reflects encoded payloads

6. **Clean up** test data when done:
   ```bash
   sf apex run --target-org <your-sandbox-alias> --file scripts/cleanup.apex
   ```

### Tips

- Always use a **sandbox or scratch org** — never seed adversarial data into production
- Run tests iteratively: seed, probe via MCP, review, fix, re-test
- Combine with your MCP server's logging to trace how payloads flow through the system
- Use the toolkit as part of a broader security review before enabling MCP access to Salesforce data

## References

- **Repository**: https://github.com/ccmalcom/SFDC-MCP-Security-Toolkit
- **Attack categories**: 14 payload types covering OWASP-style adversarial inputs adapted for MCP/LLM contexts
- **Coverage**: Account, Contact, Case, and Outreach Log objects (~270 records)
