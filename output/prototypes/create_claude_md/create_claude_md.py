#!/usr/bin/env python3
"""
create_claude_md — Generate a lean, high-signal CLAUDE.md for any repository.

Scans codebase structure (manifests, configs, CI, docs) and produces a
ready-to-use CLAUDE.md with project overview, tech stack, commands,
conventions, and workflow notes.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Optional


# ── Manifest detection ──────────────────────────────────────────────
MANIFEST_FILES = {
    "package.json": "node",
    "Cargo.toml": "rust",
    "pyproject.toml": "python",
    "setup.py": "python",
    "setup.cfg": "python",
    "requirements.txt": "python",
    "go.mod": "go",
    "Gemfile": "ruby",
    "pom.xml": "java",
    "build.gradle": "java",
    "composer.json": "php",
    "mix.exs": "elixir",
    "Package.swift": "swift",
    "CMakeLists.txt": "cpp",
}

LINTER_CONFIGS = [
    ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml",
    "ruff.toml", "pyproject.toml",  # ruff section
    ".prettierrc", ".prettierrc.json", ".prettierrc.js",
    ".flake8", ".pylintrc", "tslint.json",
    ".stylelintrc", ".rubocop.yml",
    "biome.json", "deno.json",
]

FORMAT_CONFIGS = [
    ".editorconfig", ".clang-format", "rustfmt.toml",
    ".prettierrc", ".prettierrc.json",
]

CI_PATHS = [
    ".github/workflows", ".gitlab-ci.yml", ".circleci",
    "Jenkinsfile", ".travis.yml", "azure-pipelines.yml",
    "bitbucket-pipelines.yml",
]

BUILD_FILES = ["Makefile", "justfile", "Taskfile.yml", "Rakefile"]


def file_exists(root: Path, name: str) -> bool:
    return (root / name).exists()


def dir_exists(root: Path, name: str) -> bool:
    return (root / name).is_dir()


def read_file(root: Path, name: str) -> Optional[str]:
    p = root / name
    if p.is_file():
        try:
            return p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None
    return None


def read_json(root: Path, name: str) -> Optional[dict]:
    text = read_file(root, name)
    if text:
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None
    return None


# ── Scanner ─────────────────────────────────────────────────────────
class RepoScanner:
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.data: dict = {}

    def scan(self) -> dict:
        self.data = {
            "project_name": self.root.name,
            "languages": [],
            "frameworks": [],
            "dependencies": [],
            "dev_dependencies": [],
            "scripts": {},
            "structure": [],
            "linters": [],
            "formatters": [],
            "ci": [],
            "build_tools": [],
            "has_tests": False,
            "test_dirs": [],
            "readme_summary": "",
            "contributing_notes": "",
        }
        self._detect_manifests()
        self._detect_structure()
        self._detect_linters()
        self._detect_ci()
        self._detect_build_tools()
        self._detect_tests()
        self._read_docs()
        return self.data

    def _detect_manifests(self):
        for mf, lang in MANIFEST_FILES.items():
            if file_exists(self.root, mf):
                if lang not in self.data["languages"]:
                    self.data["languages"].append(lang)
                self._parse_manifest(mf, lang)

    def _parse_manifest(self, mf: str, lang: str):
        if mf == "package.json":
            pkg = read_json(self.root, mf)
            if not pkg:
                return
            deps = pkg.get("dependencies", {})
            dev_deps = pkg.get("devDependencies", {})
            self.data["dependencies"] = list(deps.keys())
            self.data["dev_dependencies"] = list(dev_deps.keys())
            self.data["scripts"] = pkg.get("scripts", {})
            # Detect frameworks
            all_deps = {**deps, **dev_deps}
            for fw in ["react", "next", "vue", "nuxt", "angular", "svelte",
                        "express", "fastify", "nestjs", "astro", "remix",
                        "gatsby", "electron", "vite"]:
                if fw in all_deps or f"@{fw}/core" in all_deps:
                    self.data["frameworks"].append(fw)
            if "typescript" in all_deps or file_exists(self.root, "tsconfig.json"):
                if "typescript" not in self.data["languages"]:
                    self.data["languages"].append("typescript")

        elif mf == "requirements.txt":
            text = read_file(self.root, mf)
            if text:
                self.data["dependencies"] = [
                    l.split("==")[0].split(">=")[0].strip()
                    for l in text.splitlines()
                    if l.strip() and not l.startswith("#")
                ]
                for fw in ["django", "flask", "fastapi", "streamlit", "gradio",
                            "pytorch", "tensorflow", "pandas", "numpy"]:
                    if any(fw in d.lower() for d in self.data["dependencies"]):
                        self.data["frameworks"].append(fw)

        elif mf == "pyproject.toml":
            text = read_file(self.root, mf)
            if text:
                # Simple TOML parsing for common fields
                if "poetry" in text.lower():
                    self.data["frameworks"].append("poetry")
                if "ruff" in text.lower():
                    self.data["linters"].append("ruff")
                if "pytest" in text.lower():
                    self.data["frameworks"].append("pytest")

        elif mf == "go.mod":
            text = read_file(self.root, mf)
            if text:
                for line in text.splitlines():
                    if line.startswith("module "):
                        self.data["project_name"] = line.split()[-1].split("/")[-1]

        elif mf == "Cargo.toml":
            text = read_file(self.root, mf)
            if text:
                if "tokio" in text:
                    self.data["frameworks"].append("tokio")
                if "actix" in text:
                    self.data["frameworks"].append("actix")
                if "axum" in text:
                    self.data["frameworks"].append("axum")

    def _detect_structure(self):
        """List top-level directories and notable files."""
        dirs = []
        for item in sorted(self.root.iterdir()):
            name = item.name
            if name.startswith(".") and name not in (".github",):
                continue
            if item.is_dir():
                dirs.append(name + "/")
            elif name in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml"):
                self.data["build_tools"].append("docker")
        self.data["structure"] = dirs

    def _detect_linters(self):
        for cfg in LINTER_CONFIGS:
            if file_exists(self.root, cfg):
                tool = cfg.lstrip(".").split("rc")[0].split(".")[0]
                if tool and tool not in self.data["linters"]:
                    self.data["linters"].append(tool)
        for cfg in FORMAT_CONFIGS:
            if file_exists(self.root, cfg):
                tool = cfg.lstrip(".").split(".")[0].replace("rc", "")
                if tool and tool not in self.data["formatters"]:
                    self.data["formatters"].append(tool)

    def _detect_ci(self):
        for ci in CI_PATHS:
            if file_exists(self.root, ci) or dir_exists(self.root, ci):
                self.data["ci"].append(ci)

    def _detect_build_tools(self):
        for bf in BUILD_FILES:
            if file_exists(self.root, bf):
                self.data["build_tools"].append(bf.lower().replace("file", ""))

    def _detect_tests(self):
        for d in ["tests", "test", "__tests__", "spec", "specs", "test_"]:
            if dir_exists(self.root, d):
                self.data["has_tests"] = True
                self.data["test_dirs"].append(d)
        # Check scripts
        scripts = self.data.get("scripts", {})
        if "test" in scripts:
            self.data["has_tests"] = True

    def _read_docs(self):
        readme = read_file(self.root, "README.md") or read_file(self.root, "readme.md")
        if readme:
            # Take first meaningful paragraph
            lines = []
            for line in readme.splitlines():
                if line.strip() and not line.startswith("#") and not line.startswith("!["):
                    lines.append(line.strip())
                    if len(lines) >= 3:
                        break
            self.data["readme_summary"] = " ".join(lines)

        contrib = read_file(self.root, "CONTRIBUTING.md")
        if contrib:
            self.data["contributing_notes"] = contrib[:500]


# ── Generator ───────────────────────────────────────────────────────
class ClaudeMdGenerator:
    def __init__(self, scan_data: dict):
        self.d = scan_data

    def generate(self) -> str:
        sections = []
        sections.append("# CLAUDE.md\n")
        sections.append(self._project_overview())
        sections.append(self._tech_stack())
        sections.append(self._project_structure())
        sections.append(self._dev_commands())
        sections.append(self._code_style())
        sections.append(self._testing())
        sections.append(self._git_workflow())
        sections.append(self._important_notes())
        # Filter empty sections
        return "\n".join(s for s in sections if s.strip())

    def _project_overview(self) -> str:
        name = self.d["project_name"]
        langs = ", ".join(self.d["languages"]) if self.d["languages"] else "unknown"
        fws = ", ".join(self.d["frameworks"]) if self.d["frameworks"] else ""
        summary = self.d.get("readme_summary", "")

        desc = summary if summary else f"A {langs} project."
        if fws:
            desc += f" Built with {fws}."

        return f"## Project Overview\n\n{name} — {desc}\n"

    def _tech_stack(self) -> str:
        items = []
        if self.d["languages"]:
            items.append(f"- **Languages:** {', '.join(self.d['languages'])}")
        if self.d["frameworks"]:
            items.append(f"- **Frameworks:** {', '.join(self.d['frameworks'])}")
        if self.d["dependencies"]:
            top = self.d["dependencies"][:10]
            items.append(f"- **Key dependencies:** {', '.join(top)}")
        if self.d["build_tools"]:
            items.append(f"- **Build tools:** {', '.join(self.d['build_tools'])}")

        if not items:
            return ""
        return "## Tech Stack\n\n" + "\n".join(items) + "\n"

    def _project_structure(self) -> str:
        dirs = self.d.get("structure", [])
        if not dirs:
            return ""
        lines = ["## Project Structure\n", "```"]
        for d in dirs:
            lines.append(f"  {d}")
        lines.append("```\n")
        return "\n".join(lines)

    def _dev_commands(self) -> str:
        scripts = self.d.get("scripts", {})
        lines = ["## Development Commands\n"]
        cmds_found = False

        if scripts:
            for key in ["dev", "start", "build", "test", "lint", "format",
                         "typecheck", "type-check", "check"]:
                if key in scripts:
                    lines.append(f"- `npm run {key}` — {scripts[key]}")
                    cmds_found = True

        # Check for Makefile targets
        if "make" in self.d.get("build_tools", []):
            lines.append("- `make` — see Makefile for available targets")
            cmds_found = True

        # Python defaults
        if "python" in self.d.get("languages", []):
            if self.d["has_tests"]:
                lines.append("- `pytest` — run tests")
                cmds_found = True
            for linter in self.d.get("linters", []):
                lines.append(f"- `{linter} .` — lint")
                cmds_found = True

        if not cmds_found:
            return ""
        lines.append("")
        return "\n".join(lines)

    def _code_style(self) -> str:
        items = []
        if self.d["linters"]:
            items.append(f"- **Linters:** {', '.join(self.d['linters'])}")
        if self.d["formatters"]:
            items.append(f"- **Formatters:** {', '.join(self.d['formatters'])}")
        if "typescript" in self.d.get("languages", []):
            items.append("- Use TypeScript strict mode where possible")
        if "python" in self.d.get("languages", []):
            items.append("- Follow PEP 8 naming conventions")

        if not items:
            return ""
        return "## Code Style & Conventions\n\n" + "\n".join(items) + "\n"

    def _testing(self) -> str:
        if not self.d["has_tests"]:
            return ""
        lines = ["## Testing\n"]
        if self.d["test_dirs"]:
            lines.append(f"- Test directories: `{', '.join(self.d['test_dirs'])}`")
        scripts = self.d.get("scripts", {})
        if "test" in scripts:
            lines.append(f"- Run tests: `npm test` ({scripts['test']})")
        elif "python" in self.d.get("languages", []):
            lines.append("- Run tests: `pytest`")
        lines.append("")
        return "\n".join(lines)

    def _git_workflow(self) -> str:
        lines = []
        if self.d.get("ci"):
            lines.append(f"- **CI:** {', '.join(self.d['ci'])}")
        if lines:
            return "## Git & Workflow\n\n" + "\n".join(lines) + "\n"
        return ""

    def _important_notes(self) -> str:
        notes = []
        if self.d.get("contributing_notes"):
            notes.append("- See CONTRIBUTING.md for detailed contribution guidelines")
        if "docker" in self.d.get("build_tools", []):
            notes.append("- Docker configuration available for containerized development")
        if not notes:
            return ""
        return "## Important Notes\n\n" + "\n".join(notes) + "\n"


# ── Main ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Generate a CLAUDE.md for a repository"
    )
    parser.add_argument(
        "repo_path",
        nargs="?",
        default=".",
        help="Path to the repository root (default: current directory)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path (default: <repo>/CLAUDE.md). Use '-' for stdout.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to stdout without writing a file",
    )
    args = parser.parse_args()

    repo = Path(args.repo_path).resolve()
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {repo} ...", file=sys.stderr)
    scanner = RepoScanner(str(repo))
    data = scanner.scan()

    print(f"  Languages: {data['languages']}", file=sys.stderr)
    print(f"  Frameworks: {data['frameworks']}", file=sys.stderr)
    print(f"  Structure: {len(data['structure'])} top-level dirs", file=sys.stderr)
    print(f"  Tests found: {data['has_tests']}", file=sys.stderr)
    print(f"  CI: {data['ci']}", file=sys.stderr)

    gen = ClaudeMdGenerator(data)
    output = gen.generate()

    if args.dry_run or args.output == "-":
        print(output)
    else:
        out_path = Path(args.output) if args.output else repo / "CLAUDE.md"
        out_path.write_text(output, encoding="utf-8")
        print(f"\nWrote {out_path} ({len(output.splitlines())} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
