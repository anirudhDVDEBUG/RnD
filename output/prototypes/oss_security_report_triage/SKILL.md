---
name: oss_security_report_triage
description: |
  Triage and respond to AI-assisted security vulnerability reports for open-source projects.
  TRIGGER: user mentions "security report triage", "vulnerability report", "bug bounty triage",
  "CVE assessment", "security report flood", or "AI-generated security reports"
---

# OSS Security Report Triage

Help open-source maintainers efficiently triage, assess, and respond to security vulnerability reports — especially the growing volume of AI-assisted reports.

## When to use

- "Help me triage this security vulnerability report"
- "Assess the severity of this bug report against my project"
- "Draft a response to this security disclosure"
- "Prioritize these incoming CVE candidates"
- "Help me manage the flood of AI-generated security reports"

## How to use

### Step 1: Intake and classify the report

Collect the key details from the security report:

1. **Affected component** — which file, function, or module is implicated?
2. **Attack vector** — what input or condition triggers the issue?
3. **Claimed impact** — what does the reporter say can happen (RCE, DoS, info leak, etc.)?
4. **Proof of concept** — is a PoC provided? Is it reproducible?
5. **Reporter context** — does this look AI-generated (very long, highly detailed, generic phrasing)?

### Step 2: Assess severity

Use the CVSS v3.1 framework to score severity:

- **Attack Vector**: Network / Adjacent / Local / Physical
- **Attack Complexity**: Low / High
- **Privileges Required**: None / Low / High
- **User Interaction**: None / Required
- **Scope**: Unchanged / Changed
- **Impact (CIA)**: None / Low / High for each of Confidentiality, Integrity, Availability

Assign a severity label: **CRITICAL** / **HIGH** / **MEDIUM** / **LOW** / **INFORMATIONAL**

As Daniel Stenberg notes about curl: almost all recent vulnerabilities have been LOW or MEDIUM severity. Many AI-generated reports sound alarming but describe low-impact issues. Don't let report length or detail bias your severity assessment upward.

### Step 3: Verify reproducibility

1. Read the referenced source code to confirm the vulnerable code path exists
2. Check if the described conditions are reachable in practice
3. Attempt to reproduce the PoC if provided
4. Check if existing mitigations (bounds checks, sanitization, compiler flags) already cover the issue
5. Determine if the issue is a true positive, false positive, or theoretical-only

### Step 4: Draft a response

For **valid reports**:
- Acknowledge the report and thank the reporter
- Confirm severity assessment
- Outline remediation timeline
- Assign a CVE ID if warranted
- Prepare an advisory draft

For **invalid/low-quality reports**:
- Explain clearly why the report does not constitute a vulnerability
- Reference specific code or documentation that addresses the concern
- Be professional — many AI-assisted reporters are acting in good faith

### Step 5: Track and manage volume

For projects experiencing high report volume (as curl sees 1+ reports/day):

- Maintain a triage queue with status labels: NEW → ANALYZING → CONFIRMED → FIXED → REJECTED
- Set response-time SLAs by severity (e.g., CRITICAL: 24h, HIGH: 72h, MEDIUM/LOW: 1 week)
- Create response templates for common false-positive patterns
- Document recurring false-positive patterns to share with reporters and bug bounty platforms
- Consider maintainer well-being — delegate, rotate triage duty, set boundaries

## Key principles

- **Report length != severity.** AI-generated reports are often very long and detailed but describe low-impact issues.
- **Verify before you worry.** Many reported code paths are unreachable in practice.
- **Batch similar reports.** AI tools often find the same class of issue repeatedly.
- **Protect maintainer health.** The pressure from high-volume reporting is real and unsustainable without process.

## References

- [The pressure — Daniel Stenberg](https://daniel.haxx.se/blog/2026/05/26/the-pressure/) — On the unprecedented flood of AI-assisted security reports facing the curl project
- [Simon Willison's commentary](https://simonwillison.net/2026/May/26/the-pressure/#atom-everything)
- [curl security advisories](https://curl.se/docs/security.html)
- [CVSS v3.1 Calculator](https://www.first.org/cvss/calculator/3.1)
