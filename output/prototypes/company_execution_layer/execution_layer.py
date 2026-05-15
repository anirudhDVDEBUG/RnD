#!/usr/bin/env python3
"""
Company Execution Layer Builder

Scaffolds a company brain with separate context (knowledge) and execution (skills)
layers, then lets you list, inspect, validate, and run skills against live context.

Usage:
    python execution_layer.py scaffold <project_dir>
    python execution_layer.py list <project_dir>
    python execution_layer.py inspect <project_dir> <skill_name>
    python execution_layer.py validate <project_dir>
    python execution_layer.py run <project_dir> <skill_name> [--dry-run]
    python execution_layer.py add-skill <project_dir> <skill_name> <description>
"""

import argparse
import os
import sys
import json
import textwrap
from pathlib import Path
from datetime import datetime

# ── Templates ────────────────────────────────────────────────────────────────

CLAUDE_MD_TEMPLATE = textwrap.dedent("""\
# {project_name} — Execution Layer

## Context (read these for company knowledge)
{context_entries}

## Available Skills (run these to ship work)
{skill_entries}

When a user invokes a skill, read its SKILL.md and follow the steps exactly.
Always pull live context from the context/ directory — never hard-code company info.
""")

SKILL_TEMPLATE = textwrap.dedent("""\
---
name: {skill_name}
description: |
  {description}
  Triggers: "{triggers}"
---

# {title}

## Inputs
- (Define what the user needs to provide)

## Steps
1. Read relevant context files (see references below)
2. (Add your step-by-step instructions here)
3. Output results to `output/{skill_name}/`

## Context References
- `context/` — (link to specific context docs this skill needs)

## Output
- Results saved to `output/{skill_name}/` with dated filenames
""")

CONTEXT_FILES = {
    "brand/voice-and-tone.md": textwrap.dedent("""\
        # Brand Voice & Tone

        ## Core Voice Attributes
        - **Professional** but approachable
        - **Clear** over clever — plain language wins
        - **Confident** without arrogance
        - **Helpful** — always lead with value

        ## Tone by Channel
        | Channel | Tone | Example |
        |---------|------|---------|
        | Blog | Educational, conversational | "Here's how to get started..." |
        | Email | Direct, warm | "Quick update on your project..." |
        | Social | Punchy, engaging | "Ship faster. Iterate smarter." |
        | Docs | Precise, scannable | Step 1. Install dependencies... |

        ## Words We Use / Avoid
        - Use: build, ship, automate, streamline, leverage
        - Avoid: synergy, disrupt, paradigm, pivot (overused)
    """),
    "products/product-specs.md": textwrap.dedent("""\
        # Product Specifications

        ## Core Product: WorkflowAI Platform
        - **Category**: AI-powered workflow automation
        - **Target**: Mid-market teams (20-200 employees)
        - **Pricing**: Starter $49/mo, Pro $149/mo, Enterprise custom
        - **Key Features**:
          - Natural language workflow builder
          - 50+ integrations (Slack, Notion, GitHub, Jira)
          - Custom skill marketplace
          - Team knowledge base with live sync

        ## Technical Stack
        - Frontend: React + TypeScript
        - Backend: Python (FastAPI)
        - Database: PostgreSQL + pgvector
        - AI: Claude API (Sonnet for speed, Opus for depth)
    """),
    "processes/sops.md": textwrap.dedent("""\
        # Standard Operating Procedures

        ## Content Publishing SOP
        1. Draft content in Google Docs
        2. Run through brand voice checklist
        3. Internal review (min 1 reviewer)
        4. Schedule in CMS with SEO metadata
        5. Promote on social channels within 24h

        ## Client Onboarding SOP
        1. Send welcome email within 2 hours of signup
        2. Schedule kickoff call within 48 hours
        3. Share onboarding checklist and resource links
        4. First check-in at Day 7
        5. Full review at Day 30

        ## Incident Response SOP
        1. Acknowledge within 15 minutes
        2. Classify severity (P0-P3)
        3. Assemble response team for P0/P1
        4. Post status update every 30 minutes
        5. Write postmortem within 48 hours
    """),
    "team/org-chart.md": textwrap.dedent("""\
        # Team Structure

        ## Leadership
        - **CEO** — Alex Chen
        - **CTO** — Jordan Park
        - **VP Marketing** — Sam Rivera

        ## Teams
        | Team | Lead | Size | Focus |
        |------|------|------|-------|
        | Engineering | Jordan Park | 12 | Platform development |
        | Product | Mia Torres | 4 | Roadmap & specs |
        | Marketing | Sam Rivera | 6 | Growth & content |
        | Sales | Chris Dunn | 5 | Revenue & partnerships |
        | Support | Ava Lin | 3 | Customer success |

        ## Communication
        - **Slack**: Primary async communication
        - **Weekly All-Hands**: Mondays 10am PT
        - **Sprint Reviews**: Fridays 2pm PT
    """),
}

DEFAULT_SKILLS = {
    "content-creation": {
        "name": "content_creation",
        "description": "Create on-brand content using company voice guidelines and product knowledge.",
        "triggers": "write a blog post, draft social copy, create content",
        "title": "Content Creation Skill",
        "steps": [
            "Read `context/brand/voice-and-tone.md` for brand voice rules",
            "Read `context/products/product-specs.md` for accurate product details",
            "Ask the user for: topic, format (blog/social/email), target audience, length",
            "Draft the content following brand guidelines",
            "Output the finished piece to `output/content-creation/` with a dated filename",
        ],
        "context_refs": [
            "`context/brand/voice-and-tone.md` — Brand voice rules",
            "`context/products/product-specs.md` — Product details",
        ],
    },
    "client-onboarding": {
        "name": "client_onboarding",
        "description": "Run the full client onboarding checklist from welcome to 30-day review.",
        "triggers": "onboard a client, new client setup, client onboarding",
        "title": "Client Onboarding Skill",
        "steps": [
            "Read `context/processes/sops.md` for the onboarding SOP",
            "Read `context/products/product-specs.md` for product details to share",
            "Ask the user for: client name, plan tier, primary contact email",
            "Generate welcome email draft using brand voice",
            "Create onboarding checklist with timeline",
            "Output all materials to `output/client-onboarding/`",
        ],
        "context_refs": [
            "`context/processes/sops.md` — Onboarding SOP steps",
            "`context/products/product-specs.md` — Product info for client",
            "`context/brand/voice-and-tone.md` — Email tone",
        ],
    },
    "weekly-report": {
        "name": "weekly_report",
        "description": "Generate the weekly status report from team updates and metrics.",
        "triggers": "weekly report, status update, team summary",
        "title": "Weekly Report Skill",
        "steps": [
            "Read `context/team/org-chart.md` for team structure",
            "Ask the user for: week number, key wins, blockers, metrics",
            "Format report with sections per team",
            "Include action items for next week",
            "Output report to `output/weekly-report/`",
        ],
        "context_refs": [
            "`context/team/org-chart.md` — Team structure",
        ],
    },
    "proposal-generator": {
        "name": "proposal_generator",
        "description": "Build a client proposal from product specs and pricing.",
        "triggers": "create proposal, client proposal, write proposal",
        "title": "Proposal Generator Skill",
        "steps": [
            "Read `context/products/product-specs.md` for product details and pricing",
            "Read `context/brand/voice-and-tone.md` for professional tone",
            "Ask the user for: client name, requirements, budget range",
            "Generate proposal with executive summary, solution overview, pricing, timeline",
            "Output proposal to `output/proposal-generator/`",
        ],
        "context_refs": [
            "`context/products/product-specs.md` — Product specs & pricing",
            "`context/brand/voice-and-tone.md` — Professional tone",
        ],
    },
}


# ── Core Functions ───────────────────────────────────────────────────────────

def scaffold(project_dir: str) -> dict:
    """Scaffold a complete company brain with context + skills layers."""
    root = Path(project_dir)
    created = []

    # Create context files
    for rel_path, content in CONTEXT_FILES.items():
        fpath = root / "context" / rel_path
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content)
        created.append(str(fpath.relative_to(root)))

    # Create skill files
    for skill_slug, skill_info in DEFAULT_SKILLS.items():
        skill_md = _render_skill(skill_info)
        fpath = root / "skills" / skill_slug / "SKILL.md"
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(skill_md)
        created.append(str(fpath.relative_to(root)))

    # Create output directory
    (root / "output").mkdir(parents=True, exist_ok=True)
    created.append("output/")

    # Generate CLAUDE.md
    claude_md = _generate_claude_md(root)
    (root / "CLAUDE.md").write_text(claude_md)
    created.append("CLAUDE.md")

    return {"project_dir": str(root), "files_created": created, "skill_count": len(DEFAULT_SKILLS), "context_count": len(CONTEXT_FILES)}


def _render_skill(skill_info: dict) -> str:
    """Render a SKILL.md from structured skill info."""
    lines = [
        f"---",
        f"name: {skill_info['name']}",
        f"description: |",
        f"  {skill_info['description']}",
        f"  Triggers: \"{skill_info['triggers']}\"",
        f"---",
        f"",
        f"# {skill_info['title']}",
        f"",
        f"## Steps",
    ]
    for i, step in enumerate(skill_info["steps"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("## Context References")
    for ref in skill_info["context_refs"]:
        lines.append(f"- {ref}")
    lines.append("")
    lines.append("## Output")
    lines.append(f"- Results saved to `output/{skill_info['name'].replace('_', '-')}/` with dated filenames")
    lines.append("")
    return "\n".join(lines)


def _generate_claude_md(root: Path) -> str:
    """Generate CLAUDE.md from current context and skills."""
    # Context entries
    context_entries = []
    context_dir = root / "context"
    if context_dir.exists():
        for subdir in sorted(context_dir.iterdir()):
            if subdir.is_dir():
                context_entries.append(f"- `context/{subdir.name}/` — {subdir.name.replace('-', ' ').title()}")

    # Skill entries
    skill_entries = []
    skills_dir = root / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                desc = skill_dir.name.replace("-", " ").title()
                if skill_md.exists():
                    # Parse description from SKILL.md front matter
                    content = skill_md.read_text()
                    for line in content.split("\n"):
                        if line.strip().startswith("description:"):
                            break
                    else:
                        pass
                skill_entries.append(f"- `/{skill_dir.name}` — {desc}")

    return CLAUDE_MD_TEMPLATE.format(
        project_name=root.name.replace("-", " ").replace("_", " ").title(),
        context_entries="\n".join(context_entries) if context_entries else "- (none yet)",
        skill_entries="\n".join(skill_entries) if skill_entries else "- (none yet)",
    )


def list_skills(project_dir: str) -> list:
    """List all available skills in the project."""
    root = Path(project_dir)
    skills_dir = root / "skills"
    results = []

    if not skills_dir.exists():
        return results

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        info = {"name": skill_dir.name, "has_skill_md": skill_md.exists()}

        if skill_md.exists():
            content = skill_md.read_text()
            # Parse front matter
            in_fm = False
            for line in content.split("\n"):
                if line.strip() == "---":
                    in_fm = not in_fm
                    continue
                if in_fm and ":" in line:
                    key, _, val = line.partition(":")
                    key = key.strip()
                    val = val.strip()
                    if key == "name":
                        info["skill_name"] = val
                    elif key == "description" and not val.endswith("|"):
                        info["description"] = val

            # Count steps
            step_count = 0
            for line in content.split("\n"):
                if line.strip() and line.strip()[0].isdigit() and ". " in line:
                    step_count += 1
            info["step_count"] = step_count

            # Find context references
            refs = []
            in_refs = False
            for line in content.split("\n"):
                if "Context Reference" in line:
                    in_refs = True
                    continue
                if in_refs and line.startswith("- "):
                    refs.append(line[2:].strip())
                elif in_refs and line.startswith("#"):
                    break
            info["context_refs"] = refs

        results.append(info)

    return results


def inspect_skill(project_dir: str, skill_name: str) -> dict:
    """Get detailed info about a specific skill."""
    root = Path(project_dir)
    skill_dir = root / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return {"error": f"Skill '{skill_name}' not found at {skill_md}"}

    content = skill_md.read_text()

    # Check context references exist
    refs_status = []
    for line in content.split("\n"):
        if "`context/" in line:
            # Extract path
            start = line.index("`context/") + 1
            end = line.index("`", start)
            ref_path = line[start:end]
            exists = (root / ref_path).exists()
            refs_status.append({"path": ref_path, "exists": exists})

    return {
        "name": skill_name,
        "path": str(skill_md),
        "content": content,
        "context_refs": refs_status,
        "output_dir": str(root / "output" / skill_name),
    }


def validate(project_dir: str) -> dict:
    """Validate the execution layer structure and references."""
    root = Path(project_dir)
    issues = []
    stats = {"skills": 0, "context_files": 0, "broken_refs": 0}

    # Check CLAUDE.md
    if not (root / "CLAUDE.md").exists():
        issues.append({"level": "error", "msg": "Missing CLAUDE.md root config"})

    # Check context
    context_dir = root / "context"
    if context_dir.exists():
        for f in context_dir.rglob("*.md"):
            stats["context_files"] += 1
    else:
        issues.append({"level": "warning", "msg": "No context/ directory found"})

    # Check skills
    skills_dir = root / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            stats["skills"] += 1
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                issues.append({"level": "error", "msg": f"Skill '{skill_dir.name}' missing SKILL.md"})
                continue

            # Check context references
            content = skill_md.read_text()
            for line in content.split("\n"):
                if "`context/" in line:
                    try:
                        start = line.index("`context/") + 1
                        end = line.index("`", start)
                        ref_path = line[start:end]
                        if not (root / ref_path).exists():
                            issues.append({
                                "level": "warning",
                                "msg": f"Skill '{skill_dir.name}' references missing context: {ref_path}",
                            })
                            stats["broken_refs"] += 1
                    except ValueError:
                        pass
    else:
        issues.append({"level": "warning", "msg": "No skills/ directory found"})

    # Check output dir
    if not (root / "output").exists():
        issues.append({"level": "info", "msg": "No output/ directory — will be created on first skill run"})

    return {"valid": len([i for i in issues if i["level"] == "error"]) == 0, "stats": stats, "issues": issues}


def run_skill(project_dir: str, skill_name: str, dry_run: bool = False) -> dict:
    """Simulate running a skill (dry-run by default in demo mode)."""
    root = Path(project_dir)
    skill_md = root / "skills" / skill_name / "SKILL.md"

    if not skill_md.exists():
        return {"error": f"Skill '{skill_name}' not found"}

    content = skill_md.read_text()

    # Collect steps
    steps = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped and stripped[0].isdigit() and ". " in stripped:
            step_text = stripped.split(". ", 1)[1]
            steps.append(step_text)

    # Collect and read context files
    context_data = {}
    for line in content.split("\n"):
        if "`context/" in line:
            try:
                start = line.index("`context/") + 1
                end = line.index("`", start)
                ref_path = line[start:end]
                full_path = root / ref_path
                if full_path.exists():
                    ctx_content = full_path.read_text()
                    context_data[ref_path] = {
                        "loaded": True,
                        "size": len(ctx_content),
                        "preview": ctx_content[:200] + "..." if len(ctx_content) > 200 else ctx_content,
                    }
                else:
                    context_data[ref_path] = {"loaded": False, "error": "File not found"}
            except ValueError:
                pass

    # Create output directory and sample output
    output_dir = root / "output" / skill_name
    output_file = None

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_file = output_dir / f"{skill_name}_{timestamp}.md"
        output_file.write_text(
            f"# {skill_name.replace('-', ' ').title()} — Output\n\n"
            f"Generated: {datetime.now().isoformat()}\n\n"
            f"## Context Loaded\n"
            + "\n".join(f"- {k}: {v.get('size', 'N/A')} bytes" for k, v in context_data.items())
            + "\n\n## Steps Executed\n"
            + "\n".join(f"- [x] {s}" for s in steps)
            + "\n\n---\n*This is a demo output. In production, Claude would execute each step against live context.*\n"
        )

    return {
        "skill": skill_name,
        "dry_run": dry_run,
        "steps": steps,
        "context_loaded": context_data,
        "output_file": str(output_file) if output_file else None,
        "status": "simulated" if dry_run else "completed",
    }


def add_skill(project_dir: str, skill_name: str, description: str) -> dict:
    """Add a new skill to the execution layer."""
    root = Path(project_dir)
    slug = skill_name.lower().replace(" ", "-").replace("_", "-")
    skill_dir = root / "skills" / slug
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md_content = SKILL_TEMPLATE.format(
        skill_name=slug.replace("-", "_"),
        description=description,
        triggers=slug.replace("-", " "),
        title=skill_name.replace("-", " ").replace("_", " ").title(),
    )

    (skill_dir / "SKILL.md").write_text(skill_md_content)

    # Regenerate CLAUDE.md
    claude_md = _generate_claude_md(root)
    (root / "CLAUDE.md").write_text(claude_md)

    return {
        "skill_slug": slug,
        "path": str(skill_dir / "SKILL.md"),
        "registered_in_claude_md": True,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def _print_json(data):
    print(json.dumps(data, indent=2))


def _print_header(text):
    width = 60
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def _print_section(title):
    print(f"\n{'─' * 40}")
    print(f"  {title}")
    print(f"{'─' * 40}")


def main():
    parser = argparse.ArgumentParser(description="Company Execution Layer Builder")
    sub = parser.add_subparsers(dest="command")

    p_scaffold = sub.add_parser("scaffold", help="Scaffold a new company brain")
    p_scaffold.add_argument("project_dir")

    p_list = sub.add_parser("list", help="List available skills")
    p_list.add_argument("project_dir")

    p_inspect = sub.add_parser("inspect", help="Inspect a specific skill")
    p_inspect.add_argument("project_dir")
    p_inspect.add_argument("skill_name")

    p_validate = sub.add_parser("validate", help="Validate execution layer")
    p_validate.add_argument("project_dir")

    p_run = sub.add_parser("run", help="Run a skill")
    p_run.add_argument("project_dir")
    p_run.add_argument("skill_name")
    p_run.add_argument("--dry-run", action="store_true")

    p_add = sub.add_parser("add-skill", help="Add a new skill")
    p_add.add_argument("project_dir")
    p_add.add_argument("skill_name")
    p_add.add_argument("description")

    p_demo = sub.add_parser("demo", help="Run full interactive demo")
    p_demo.add_argument("project_dir")

    args = parser.parse_args()

    if args.command == "scaffold":
        result = scaffold(args.project_dir)
        _print_header("Scaffolded Company Brain")
        print(f"  Directory: {result['project_dir']}")
        print(f"  Skills:    {result['skill_count']}")
        print(f"  Context:   {result['context_count']} files")
        print(f"\n  Files created:")
        for f in result["files_created"]:
            print(f"    + {f}")

    elif args.command == "list":
        skills = list_skills(args.project_dir)
        _print_header("Skills Marketplace")
        for s in skills:
            status = "OK" if s["has_skill_md"] else "MISSING SKILL.md"
            print(f"  /{s['name']:25s} [{status}]  {s.get('step_count', '?')} steps  {len(s.get('context_refs', []))} refs")

    elif args.command == "inspect":
        result = inspect_skill(args.project_dir, args.skill_name)
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        _print_header(f"Skill: {result['name']}")
        print(result["content"])
        if result["context_refs"]:
            print("\n  Context Reference Status:")
            for ref in result["context_refs"]:
                icon = "OK" if ref["exists"] else "MISSING"
                print(f"    [{icon}] {ref['path']}")

    elif args.command == "validate":
        result = validate(args.project_dir)
        _print_header("Validation Results")
        print(f"  Valid:         {'YES' if result['valid'] else 'NO'}")
        print(f"  Skills:        {result['stats']['skills']}")
        print(f"  Context files: {result['stats']['context_files']}")
        print(f"  Broken refs:   {result['stats']['broken_refs']}")
        if result["issues"]:
            print("\n  Issues:")
            for issue in result["issues"]:
                level = issue["level"].upper()
                print(f"    [{level}] {issue['msg']}")
        else:
            print("\n  No issues found!")

    elif args.command == "run":
        result = run_skill(args.project_dir, args.skill_name, dry_run=args.dry_run)
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        mode = "DRY RUN" if result["dry_run"] else "EXECUTED"
        _print_header(f"Skill Run: {result['skill']} [{mode}]")
        print(f"\n  Steps ({len(result['steps'])}):")
        for i, step in enumerate(result["steps"], 1):
            print(f"    {i}. {step}")
        print(f"\n  Context loaded ({len(result['context_loaded'])}):")
        for path, info in result["context_loaded"].items():
            if info.get("loaded"):
                print(f"    [OK] {path} ({info['size']} bytes)")
            else:
                print(f"    [FAIL] {path} — {info.get('error')}")
        if result.get("output_file"):
            print(f"\n  Output: {result['output_file']}")

    elif args.command == "add-skill":
        result = add_skill(args.project_dir, args.skill_name, args.description)
        _print_header("Skill Added")
        print(f"  Slug: {result['skill_slug']}")
        print(f"  Path: {result['path']}")
        print(f"  Registered in CLAUDE.md: {result['registered_in_claude_md']}")

    elif args.command == "demo":
        run_demo(args.project_dir)

    else:
        parser.print_help()


def run_demo(project_dir: str):
    """Full end-to-end demo of the execution layer."""
    _print_header("COMPANY EXECUTION LAYER — FULL DEMO")
    print("  Concept: Separate what your company KNOWS (context)")
    print("  from what it DOES (skills). Wire them together with CLAUDE.md.")
    print("  Source: youtube.com/watch?v=gMm50Sy_GmQ")

    # Step 1: Scaffold
    _print_section("Step 1: Scaffold Company Brain")
    result = scaffold(project_dir)
    print(f"  Created {result['skill_count']} skills + {result['context_count']} context files")
    print(f"  Directory structure:")

    root = Path(project_dir)
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root)
            depth = len(rel.parts) - 1
            indent = "  " + "  " * depth
            print(f"  {indent}{rel}")

    # Step 2: List skills
    _print_section("Step 2: Skills Marketplace")
    skills = list_skills(project_dir)
    print(f"  {len(skills)} skills available:\n")
    for s in skills:
        print(f"    /{s['name']:25s}  {s.get('step_count', '?')} steps | {len(s.get('context_refs', []))} context refs")

    # Step 3: Validate
    _print_section("Step 3: Validate Execution Layer")
    val = validate(project_dir)
    print(f"  Valid: {'YES' if val['valid'] else 'NO'}")
    print(f"  {val['stats']['skills']} skills, {val['stats']['context_files']} context files, {val['stats']['broken_refs']} broken refs")
    if val["issues"]:
        for issue in val["issues"]:
            print(f"    [{issue['level'].upper()}] {issue['msg']}")
    else:
        print("  All references intact!")

    # Step 4: Dry run a skill
    _print_section("Step 4: Dry-Run 'content-creation' Skill")
    run_result = run_skill(project_dir, "content-creation", dry_run=True)
    print(f"  Steps:")
    for i, step in enumerate(run_result["steps"], 1):
        print(f"    {i}. {step}")
    print(f"\n  Context loaded:")
    for path, info in run_result["context_loaded"].items():
        status = f"{info['size']} bytes" if info.get("loaded") else "MISSING"
        print(f"    {path} — {status}")

    # Step 5: Actually run a skill
    _print_section("Step 5: Execute 'weekly-report' Skill")
    run_result = run_skill(project_dir, "weekly-report", dry_run=False)
    print(f"  Status: {run_result['status']}")
    print(f"  Output: {run_result.get('output_file', 'none')}")

    # Step 6: Add a new skill
    _print_section("Step 6: Add Custom Skill 'competitor-analysis'")
    add_result = add_skill(project_dir, "competitor-analysis", "Analyze competitors using product specs and market data.")
    print(f"  Created: {add_result['path']}")
    print(f"  Registered in CLAUDE.md: {add_result['registered_in_claude_md']}")

    # Final summary
    skills_final = list_skills(project_dir)
    _print_section("Final State: Skills Marketplace")
    for s in skills_final:
        print(f"    /{s['name']:25s}  {s.get('step_count', '?')} steps")

    # Show CLAUDE.md
    _print_section("Generated CLAUDE.md")
    print((root / "CLAUDE.md").read_text())

    _print_header("DEMO COMPLETE")
    print("  Your execution layer is live at:")
    print(f"  {project_dir}/")
    print()
    print("  Key takeaways:")
    print("  1. Context layer = what your company KNOWS (docs, SOPs, specs)")
    print("  2. Skills layer  = what your company DOES (runnable playbooks)")
    print("  3. CLAUDE.md     = the wiring that connects them")
    print("  4. Skills REFERENCE context — never hard-code company info")
    print("  5. Anyone on the team can run any skill instantly")
    print()


if __name__ == "__main__":
    main()
