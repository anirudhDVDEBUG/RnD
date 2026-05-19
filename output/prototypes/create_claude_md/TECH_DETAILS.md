# Technical Details

## What it does

`create_claude_md` scans a repository's filesystem to detect its tech stack,
build commands, linter/formatter configs, CI pipelines, test setup, and
documentation — then generates a structured `CLAUDE.md` file that gives Claude
(or any LLM) the context it needs to work effectively in that codebase.

The skill version (SKILL.md) adds an interactive interview step: Claude asks
3-5 targeted questions about preferences not discoverable from code alone
(commit conventions, testing expectations, off-limits files) and folds the
answers into the output.

## Architecture

```
create_claude_md.py
  ├── RepoScanner          # Walks the repo root, reads manifests/configs
  │     ├── _detect_manifests()    → languages, frameworks, deps
  │     ├── _detect_structure()    → top-level directory map
  │     ├── _detect_linters()      → ESLint, Ruff, Prettier, etc.
  │     ├── _detect_ci()           → GitHub Actions, GitLab CI, etc.
  │     ├── _detect_build_tools()  → Make, Docker, justfile
  │     ├── _detect_tests()        → test dirs, test scripts
  │     └── _read_docs()           → README summary, CONTRIBUTING notes
  │
  └── ClaudeMdGenerator    # Takes scan data → Markdown string
        ├── _project_overview()
        ├── _tech_stack()
        ├── _project_structure()
        ├── _dev_commands()
        ├── _code_style()
        ├── _testing()
        ├── _git_workflow()
        └── _important_notes()
```

### Key files

| File | Purpose |
|------|---------|
| `create_claude_md.py` | Scanner + generator (single-file, ~300 lines) |
| `SKILL.md` | Claude Code skill definition (interview + scan flow) |
| `sample_project/` | Bundled React/TS fixture for demo |
| `run.sh` | One-command demo runner |

### Data flow

1. `RepoScanner` reads manifest files (`package.json`, `pyproject.toml`, etc.)
   and config files (`.eslintrc`, `.prettierrc`, CI YAML) from disk.
2. It produces a flat dict with detected languages, frameworks, dependencies,
   scripts, directory structure, linters, CI info, and docs summary.
3. `ClaudeMdGenerator` takes that dict and emits Markdown sections.
   Empty sections are skipped automatically.
4. Output goes to stdout or a file.

### Dependencies

- **Python 3.8+** (stdlib only — `json`, `pathlib`, `argparse`)
- No external packages, no API keys, no network calls

### Supported manifests

`package.json` (Node), `Cargo.toml` (Rust), `pyproject.toml` / `requirements.txt`
(Python), `go.mod` (Go), `Gemfile` (Ruby), `pom.xml` / `build.gradle` (Java),
`composer.json` (PHP), `mix.exs` (Elixir), `Package.swift` (Swift),
`CMakeLists.txt` (C++).

## Limitations

- **No deep AST analysis.** It reads manifests and config files, not source code.
  It won't detect patterns like "this project uses the repository pattern" or
  "functions are grouped by domain."
- **No TOML/YAML parser.** Manifest parsing for `pyproject.toml` and `Cargo.toml`
  uses string matching, not a full TOML parser, so edge cases may be missed.
- **Interview requires Claude Code.** The interactive Q&A (Step 2 in SKILL.md)
  only works when installed as a Claude Code skill. The CLI produces scan-only
  output.
- **Monorepo support is shallow.** It scans the root directory; it won't
  recursively discover sub-packages in a monorepo workspace.

## Why it matters

For anyone building Claude-driven products — whether that's agent factories,
lead-gen pipelines, marketing automation, or ad-creative generators — the
quality of Claude's output is directly proportional to the context it receives.
A well-written CLAUDE.md eliminates the "cold start" problem: Claude immediately
knows the stack, the conventions, and the gotchas, so it writes code that fits
the project on the first try.

This tool automates 80% of that work. Instead of spending 30 minutes writing a
CLAUDE.md by hand, you get a solid first draft in seconds and refine from there.
