---
name: CVE Triage — Should I Care?
description: |
  Triages whether a CVE applies to your environment with sourced, verifiable reasoning.
  Triggers: "should I care about CVE", "triage this CVE", "is this vulnerability relevant", "CVE applicability check", "assess this CVE"
---

# CVE Triage — Should I Care?

An agent skill that triages whether a CVE applies to your environment, producing a sourced, verifiable applicability assessment with clear reasoning.

## When to use

- "Should I care about CVE-2024-XXXXX?"
- "Triage this CVE for my environment"
- "Is this vulnerability relevant to my stack?"
- "Assess whether CVE-2024-XXXXX affects us"
- "Check if this CVE applies to our systems"

## How to use

### Step 1: Gather CVE details

When given a CVE identifier (e.g. CVE-2024-12345):

1. Look up the CVE details from authoritative sources:
   - **NVD**: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-XXXX-XXXXX`
   - **MITRE CVE**: `https://cveawg.mitre.org/api/cve/CVE-XXXX-XXXXX`
   - **Vendor advisories** linked from the CVE record
2. Extract: affected product, affected versions, attack vector, CVSS score, CWE, and any known exploits.

### Step 2: Assess the local environment

1. Check if the affected software/library exists in the current project:
   - Search `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, `*.csproj`, or equivalent dependency files.
   - Check installed system packages if relevant (e.g. `dpkg -l`, `rpm -qa`).
2. Identify the **installed version** and compare it against the **affected version range** from the CVE.
3. Check for any mitigating factors:
   - Is the vulnerable code path actually reachable?
   - Is the vulnerable feature/configuration enabled?
   - Are there network-level mitigations (firewalls, WAF, etc.)?

### Step 3: Produce the triage report

Output a structured assessment:

```
## CVE Triage: CVE-XXXX-XXXXX

**Verdict**: 🔴 AFFECTED / 🟡 POTENTIALLY AFFECTED / 🟢 NOT AFFECTED / ⚪ NOT APPLICABLE

**CVE Summary**: [One-line description of the vulnerability]

**CVSS Score**: [Score] ([Severity])
**Attack Vector**: [Network/Adjacent/Local/Physical]
**Affected Product**: [Product name and affected versions]

### Applicability to This Environment
- **Software present?**: [Yes/No — which dependency file, what version]
- **Version in affected range?**: [Yes/No — installed version vs affected range]
- **Vulnerable code path reachable?**: [Yes/No/Unknown — reasoning]
- **Mitigations in place?**: [Any relevant mitigations]

### Reasoning
[2-4 sentences of sourced, verifiable reasoning for the verdict]

### Recommended Actions
- [Concrete next steps: upgrade to version X, apply patch, monitor, or no action needed]

### Sources
- [Links to NVD, vendor advisory, exploit databases consulted]
```

### Guidelines

- **Always cite sources.** Every claim about the CVE must link back to an authoritative reference (NVD, vendor advisory, MITRE).
- **Be precise about versions.** State exact version comparisons, not vague statements.
- **Distinguish "not present" from "not vulnerable".** Software may be present but on a non-affected version.
- **Flag unknowns.** If you cannot determine reachability or configuration, say so explicitly rather than guessing.
- **Consider transitive dependencies.** A direct dependency may pull in a vulnerable transitive dependency.
- **Check for VEX statements.** Vendors may publish Vulnerability Exploitability eXchange (VEX) documents clarifying applicability.

## References

- Source: [moltenbit/should-i-care](https://github.com/moltenbit/should-i-care) — Should you care about this CVE? An agent skill that triages whether a CVE applies to your environment, with sourced, verifiable reasoning.
- [NVD API](https://services.nvd.nist.gov/rest/json/cves/2.0)
- [MITRE CVE Program](https://www.cve.org/)
- [VEX specification](https://www.cisa.gov/sbom)
