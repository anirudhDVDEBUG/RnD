# Technical Details

## What it does

This project provides two complementary tools for applying the AWS Well-Architected Framework:

1. **A Claude Code skill** (`SKILL.md`) — a structured prompt that teaches Claude to systematically evaluate AWS architectures against all six Well-Architected pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability. When triggered, Claude reads your IaC files and produces a prioritized list of findings with concrete fix recommendations.

2. **A standalone Python analyzer** (`wa_reviewer.py`) — a zero-dependency static analysis tool that scans Terraform (`.tf`), IAM policy JSON (`.json`), and Python source files for common anti-patterns mapped to Well-Architected pillars.

## Architecture

```
SKILL.md              Claude Code skill definition (drop into ~/.claude/skills/)
wa_reviewer.py        Static analyzer (Python 3.10+, stdlib only)
  +-- check_terraform()   Regex-based Terraform checks
  +-- check_iam_json()    JSON parsing of IAM policy documents
  +-- check_python()      Source code scanning for secrets/injection
  +-- print_report()      Terminal report generator
samples/              Intentionally insecure IaC for demo purposes
  +-- bad_s3.tf           Public bucket, no encryption/versioning
  +-- bad_ec2.tf          Open security group, no auto-scaling
  +-- bad_rds.tf          Public DB, hardcoded password, no backups
  +-- bad_iam.json        Wildcard admin policy
  +-- bad_app.py          Hardcoded AWS keys, SQL injection
```

**Data flow:** `wa_reviewer.py` reads files from disk, applies regex and JSON checks per file type, collects `Finding` objects, sorts by risk level, and prints a structured report to stdout. No network calls, no API keys.

**Dependencies:** Python 3.10+ standard library only (`json`, `re`, `pathlib`, `dataclasses`). No pip packages.

**Model calls:** The skill itself uses no model calls — it's a prompt that augments Claude's behavior. The Python analyzer makes no API calls either.

## Limitations

- **Static analysis only** — the Python analyzer uses regex matching, not an AST parser or policy simulator. It catches common patterns but will miss indirect references, dynamic resource names, or module-level abstractions.
- **No CloudFormation YAML support** — only Terraform HCL and IAM JSON are parsed. CloudFormation templates in YAML/JSON are not analyzed by the CLI tool (but Claude handles them via the skill).
- **No CDK/Pulumi** — high-level IaC constructs are not resolved.
- **No live AWS account scanning** — this does not query AWS APIs, Config rules, or Security Hub. It only analyzes files on disk.
- **The skill requires Claude Code** — it won't work in the Claude web UI or API directly, though the structured prompt could be adapted.

## Source project

The skill definition is derived from [aws-samples/sample-well-architected-skills-and-steering](https://github.com/aws-samples/sample-well-architected-skills-and-steering), which provides reusable skills and steering files for multiple AI coding agents (Claude Code, Cursor, Kiro, Codex, etc.).

## Why this matters for Claude-driven products

- **Agent factories / internal tools:** Any team shipping IaC through an agent pipeline can add this skill to catch security and reliability issues before deployment — effectively an AI-powered pre-commit gate.
- **Lead-gen / consulting:** MSPs and cloud consultants can offer automated Well-Architected Reviews as a lead-gen tool — scan a prospect's Terraform repo and generate a branded findings report.
- **DevOps automation:** Combine with CI/CD to run the analyzer on every PR that touches `.tf` or IAM policy files. Claude can then suggest fixes inline via PR comments.
- **Cost optimization services:** The cost pillar findings (over-provisioned instances, missing lifecycle rules) directly translate into savings recommendations — useful for FinOps dashboards.
