# Technical Details — CVE Triage Skill

## What it does

The CVE Triage skill is a structured prompt that instructs Claude Code to perform a 3-step vulnerability assessment: (1) fetch CVE metadata from NVD/MITRE APIs, (2) scan the local project for affected dependencies and compare versions, (3) produce a structured Markdown report with a clear verdict (AFFECTED / NOT AFFECTED / NOT APPLICABLE) and sourced reasoning.

The skill works by embedding a detailed procedure and output template into Claude's context. When triggered, Claude follows the procedure using its built-in web fetch capabilities (for API calls) and file-reading tools (for dependency scanning). No external tooling is installed — Claude itself is the execution engine.

## Architecture

### Skill file (SKILL.md)

A single Markdown file (~120 lines) containing:

- **Trigger patterns**: phrases that activate the skill ("should I care about CVE-...")
- **Step 1 — CVE lookup**: instructions to query NVD REST API (`services.nvd.nist.gov/rest/json/cves/2.0`) and MITRE CVE API (`cveawg.mitre.org/api/cve/`)
- **Step 2 — Environment scan**: instructions to parse dependency files (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, `*.csproj`) and compare versions
- **Step 3 — Report generation**: a structured template with verdict, applicability checklist, reasoning, actions, and source links
- **Guidelines**: rules about citing sources, version precision, transitive dependencies, and flagging unknowns

### Prototype implementation (this repo)

```
cve_triage.py        # CLI tool implementing the triage logic in Python
mock_cve_data.py     # 5 real CVEs with mock API response data
run.sh               # Demo runner — 4 scenarios, no API keys
requirements.txt     # No runtime deps (stdlib only)
SKILL.md             # The actual Claude Code skill file
```

**Data flow (prototype)**:
```
CLI args (CVE ID) --> lookup_cve() --> mock_cve_data.py
                  --> scan_project_deps() --> parse requirements.txt / package.json / go.mod
                  --> triage_cve() --> version comparison + verdict logic
                  --> formatted Markdown report to stdout
```

**Data flow (real Claude skill)**:
```
User prompt --> Claude activates skill
            --> WebFetch NVD API + MITRE API
            --> Read project dependency files
            --> Claude reasons about version ranges + applicability
            --> Structured Markdown report in chat
```

### Dependencies

- **Prototype**: Python 3.10+ (stdlib only — `json`, `re`, `argparse`, `pathlib`)
- **Skill**: No dependencies. Claude Code itself handles API calls and file reading.

### Supported dependency file formats

| File | Ecosystem | Parser |
|------|-----------|--------|
| `requirements.txt` | Python/pip | Regex-based, handles `==`, `>=`, `~=` |
| `package.json` | Node.js/npm | JSON parse, strips `^`, `~` prefixes |
| `go.mod` | Go | Line-based, extracts module basename |
| `Cargo.toml` | Rust | (skill instructs Claude; not in prototype) |
| `pom.xml` | Java/Maven | (skill instructs Claude; not in prototype) |
| `Gemfile` | Ruby | (skill instructs Claude; not in prototype) |
| `*.csproj` | .NET | (skill instructs Claude; not in prototype) |

## Limitations

- **No transitive dependency resolution**: The prototype only checks direct dependencies. The skill instructs Claude to consider transitive deps, but this depends on Claude's ability to trace the dependency tree.
- **Simplified version comparison**: The prototype uses numeric tuple comparison, which works for semver but may fail on non-standard versioning (e.g., date-based, alpha/beta tags).
- **Mock data only**: The prototype ships 5 CVEs. Real usage requires internet access for NVD/MITRE API calls, which Claude Code handles natively.
- **No VEX support**: The skill mentions VEX (Vulnerability Exploitability eXchange) documents but neither the prototype nor Claude can reliably locate and parse them today.
- **No reachability analysis**: Determining whether a vulnerable code path is actually reachable requires static analysis tooling beyond what the skill provides.

## Why it matters for Claude-driven products

- **Security-aware agent workflows**: Any agent factory deploying code-writing agents should triage CVEs before pulling in dependencies. This skill provides a reusable pattern for that.
- **Lead-gen / consulting**: Security consultancies can integrate CVE triage into client-facing Claude workflows — instant applicability assessments that would otherwise require a senior engineer.
- **Compliance automation**: For teams needing to document CVE impact assessments (SOC 2, FedRAMP), this skill produces audit-ready structured reports.
- **Developer experience**: Reduces the "is this CVE even relevant to us?" question from a 20-minute research task to a 30-second Claude prompt.
