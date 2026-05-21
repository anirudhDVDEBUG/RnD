#!/usr/bin/env python3
"""
update-skills: Scan and update Claude Code custom skills from their source repos.

This module provides the core logic for:
1. Scanning a skills directory for installed skills
2. Detecting source repositories from SKILL.md frontmatter or body URLs
3. Fetching latest versions via git pull or HTTP download
4. Validating updated SKILL.md files
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError


class UpdateMethod(Enum):
    GIT = "git"
    CURL = "curl"
    NONE = "none"


class UpdateStatus(Enum):
    UPDATED = "updated"
    UP_TO_DATE = "up-to-date"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class SkillInfo:
    name: str
    path: Path
    source_repo: Optional[str] = None
    update_method: UpdateMethod = UpdateMethod.NONE
    status: UpdateStatus = UpdateStatus.SKIPPED
    message: str = ""
    old_content: str = ""
    new_content: str = ""


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter fields from a SKILL.md file."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    frontmatter = {}
    for line in match.group(1).strip().splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def detect_github_repo(content: str) -> Optional[str]:
    """Find a GitHub owner/repo reference in SKILL.md content."""
    # Check frontmatter source field
    fm = parse_frontmatter(content)
    if 'source' in fm:
        repo_match = re.search(r'([\w.-]+/[\w.-]+)', fm['source'])
        if repo_match:
            return repo_match.group(1)

    # Scan body for GitHub URLs
    patterns = [
        r'github\.com/([\w.-]+/[\w.-]+)',
        r'\[([\w.-]+/[\w.-]+)\]\(https://github\.com/',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)

    return None


def has_valid_frontmatter(content: str) -> bool:
    """Check that content has valid SKILL.md YAML frontmatter."""
    return bool(re.match(r'^---\s*\n.*?\n---', content, re.DOTALL))


def scan_skills(skills_dir: Path) -> list[SkillInfo]:
    """Scan the skills directory and build a list of SkillInfo objects."""
    skills = []
    if not skills_dir.is_dir():
        return skills

    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue

        skill = SkillInfo(name=entry.name, path=entry)
        skill_md = entry / "SKILL.md"

        if skill_md.exists():
            content = skill_md.read_text()
            skill.old_content = content
            skill.source_repo = detect_github_repo(content)

            if (entry / ".git").is_dir():
                skill.update_method = UpdateMethod.GIT
            elif skill.source_repo:
                skill.update_method = UpdateMethod.CURL
        skills.append(skill)

    return skills


def fetch_via_git(skill: SkillInfo) -> SkillInfo:
    """Update a git-cloned skill via git pull."""
    try:
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=str(skill.path),
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            skill_md = skill.path / "SKILL.md"
            if skill_md.exists():
                skill.new_content = skill_md.read_text()
            if "Already up to date" in result.stdout:
                skill.status = UpdateStatus.UP_TO_DATE
                skill.message = "already up to date"
            else:
                skill.status = UpdateStatus.UPDATED
                skill.message = "pulled latest changes"
        else:
            skill.status = UpdateStatus.ERROR
            skill.message = result.stderr.strip()[:100]
    except Exception as e:
        skill.status = UpdateStatus.ERROR
        skill.message = str(e)[:100]
    return skill


def fetch_via_curl(skill: SkillInfo, dry_run: bool = False) -> SkillInfo:
    """Update a skill by downloading the latest SKILL.md from GitHub."""
    if not skill.source_repo:
        skill.status = UpdateStatus.SKIPPED
        skill.message = "no source repo"
        return skill

    url = f"https://raw.githubusercontent.com/{skill.source_repo}/main/SKILL.md"
    try:
        req = Request(url, headers={"User-Agent": "update-skills/1.0"})
        with urlopen(req, timeout=15) as resp:
            new_content = resp.read().decode("utf-8")

        if not has_valid_frontmatter(new_content):
            skill.status = UpdateStatus.ERROR
            skill.message = "fetched content has invalid frontmatter"
            return skill

        skill.new_content = new_content

        if new_content.strip() == skill.old_content.strip():
            skill.status = UpdateStatus.UP_TO_DATE
            skill.message = "already up to date"
        elif dry_run:
            skill.status = UpdateStatus.UP_TO_DATE
            skill.message = "update available (dry run)"
        else:
            skill_md = skill.path / "SKILL.md"
            skill_md.write_text(new_content)
            skill.status = UpdateStatus.UPDATED
            skill.message = "updated SKILL.md"

    except URLError:
        skill.status = UpdateStatus.ERROR
        skill.message = f"could not fetch from {skill.source_repo}"
    except Exception as e:
        skill.status = UpdateStatus.ERROR
        skill.message = str(e)[:100]
    return skill


def update_skills(skills_dir: Path, dry_run: bool = False) -> list[SkillInfo]:
    """Main entry point: scan and update all skills."""
    skills = scan_skills(skills_dir)

    for skill in skills:
        if skill.update_method == UpdateMethod.GIT:
            fetch_via_git(skill)
        elif skill.update_method == UpdateMethod.CURL:
            fetch_via_curl(skill, dry_run=dry_run)
        else:
            skill.status = UpdateStatus.SKIPPED
            skill.message = "no source repo detected"

    return skills


def print_report(skills: list[SkillInfo]) -> None:
    """Print a human-readable update report."""
    if not skills:
        print("No skills found.")
        return

    status_icons = {
        UpdateStatus.UPDATED: "+",
        UpdateStatus.UP_TO_DATE: "=",
        UpdateStatus.SKIPPED: "-",
        UpdateStatus.ERROR: "!",
    }

    max_name = max(len(s.name) for s in skills)

    print(f"\n{'='*60}")
    print(f"  Claude Code Skill Update Report")
    print(f"{'='*60}\n")

    print(f"  Found {len(skills)} installed skill(s):\n")
    for s in skills:
        source = s.source_repo or "(no source)"
        print(f"    - {s.name:<{max_name}}  source: {source}")

    print(f"\n  Update results:\n")
    for s in skills:
        icon = status_icons.get(s.status, "?")
        print(f"    [{icon}] {s.name:<{max_name}}  {s.status.value}: {s.message}")

    updated = sum(1 for s in skills if s.status == UpdateStatus.UPDATED)
    current = sum(1 for s in skills if s.status == UpdateStatus.UP_TO_DATE)
    skipped = sum(1 for s in skills if s.status == UpdateStatus.SKIPPED)
    errors = sum(1 for s in skills if s.status == UpdateStatus.ERROR)

    print(f"\n  Summary: {updated} updated, {current} up-to-date, "
          f"{skipped} skipped, {errors} errors")
    print(f"{'='*60}\n")


def run_demo(mock_dir: Path) -> None:
    """Run a demo with mock skill directories."""
    print("Setting up mock skills directory...")
    mock_dir.mkdir(parents=True, exist_ok=True)

    # Skill 1: git-cloned skill (simulated)
    s1 = mock_dir / "code-review"
    s1.mkdir(exist_ok=True)
    (s1 / "SKILL.md").write_text(
        "---\nname: code-review\ndescription: AI-powered code review\n"
        "source: acme/code-review-skill\n---\n\n# Code Review\n\n"
        "Review code for quality and bugs.\n\n"
        "Source: [acme/code-review-skill](https://github.com/acme/code-review-skill)\n"
    )

    # Skill 2: URL-installed skill with repo reference
    s2 = mock_dir / "test-gen"
    s2.mkdir(exist_ok=True)
    (s2 / "SKILL.md").write_text(
        "---\nname: test-gen\ndescription: Generate unit tests\n---\n\n"
        "# Test Generator\n\nAuto-generate tests.\n\n"
        "Source: [acme/test-gen](https://github.com/acme/test-gen)\n"
    )

    # Skill 3: no source repo
    s3 = mock_dir / "my-notes"
    s3.mkdir(exist_ok=True)
    (s3 / "SKILL.md").write_text(
        "---\nname: my-notes\ndescription: Personal notes skill\n---\n\n"
        "# My Notes\n\nA personal skill with no upstream repo.\n"
    )

    # Skill 4: skill with update-skills itself
    s4 = mock_dir / "update-skills"
    s4.mkdir(exist_ok=True)
    (s4 / "SKILL.md").write_text(
        "---\nname: update-skills\ndescription: Keep skills up-to-date\n"
        "source: pcx-wave/update-skills\n---\n\n# Update Skills\n\n"
        "Sync skills from source repos.\n\n"
        "Source: [pcx-wave/update-skills](https://github.com/pcx-wave/update-skills)\n"
    )

    # Skill 5: has a .git dir (simulated)
    s5 = mock_dir / "seo-agent"
    s5.mkdir(exist_ok=True)
    (s5 / ".git").mkdir(exist_ok=True)  # fake .git dir
    (s5 / "SKILL.md").write_text(
        "---\nname: seo-agent\ndescription: SEO content pipeline\n---\n\n"
        "# SEO Agent\n\nMulti-stage SEO pipeline.\n\n"
        "Source: [loganriebel/seo-agent-pipeline](https://github.com/loganriebel/seo-agent-pipeline)\n"
    )

    print(f"Mock skills directory: {mock_dir}\n")

    # Run scan (network calls will fail gracefully since repos are fake)
    skills = scan_skills(mock_dir)

    # Simulate results since we can't actually fetch from fake repos
    for skill in skills:
        if skill.update_method == UpdateMethod.GIT:
            skill.status = UpdateStatus.UP_TO_DATE
            skill.message = "already up to date (simulated)"
        elif skill.update_method == UpdateMethod.CURL:
            if skill.name == "code-review":
                skill.status = UpdateStatus.UPDATED
                skill.message = "updated SKILL.md (3 lines changed) [simulated]"
                skill.new_content = skill.old_content + "\n## Updated Section\nNew content.\n"
            elif skill.name == "update-skills":
                skill.status = UpdateStatus.UP_TO_DATE
                skill.message = "already up to date (simulated)"
            else:
                skill.status = UpdateStatus.UPDATED
                skill.message = "updated SKILL.md (new section added) [simulated]"
        else:
            skill.status = UpdateStatus.SKIPPED
            skill.message = "no source repo detected"

    print_report(skills)

    # Show detected source repos
    print("Detected update methods:")
    for s in skills:
        print(f"  {s.name}: {s.update_method.value} -> {s.source_repo or 'n/a'}")
    print()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Update Claude Code skills")
    parser.add_argument("--skills-dir", type=Path,
                        default=Path.home() / ".claude" / "skills",
                        help="Path to skills directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview updates without applying")
    parser.add_argument("--demo", action="store_true",
                        help="Run with mock data for demonstration")
    args = parser.parse_args()

    if args.demo:
        mock = Path(tempfile.mkdtemp(prefix="skills_demo_"))
        try:
            run_demo(mock)
        finally:
            shutil.rmtree(mock, ignore_errors=True)
    else:
        skills = update_skills(args.skills_dir, dry_run=args.dry_run)
        print_report(skills)
