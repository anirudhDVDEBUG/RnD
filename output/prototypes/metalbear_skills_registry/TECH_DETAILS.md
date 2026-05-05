# Technical Details

## What It Does

The MetalBear Skills Registry is a community-curated collection of reusable Claude Code skill definitions hosted on GitHub. Each skill is a `SKILL.md` file following Anthropic's skill conventions (YAML frontmatter with name/description/triggers, plus structured usage sections). The registry provides a discovery and installation layer so users can find and adopt pre-built agent behaviors without writing them from scratch.

This prototype provides a Python CLI that mirrors what the installed Claude Code skill does conversationally: list available skills, search by keyword, inspect details, and install skills into the local `.claude/skills/` directory.

## Architecture

```
skills_registry.py          # Main CLI - list/search/show/install commands
registry_data.py            # Mock registry index (simulates git clone of metalbear-co/skills)
SKILL.md                    # The actual Claude Code skill definition to install
```

### Data Flow

1. **List/Search**: Reads the registry index (in production: clones `metalbear-co/skills` to `/tmp/metalbear-skills`, reads directory structure). In this demo: uses `registry_data.py` mock.
2. **Show**: Parses the SKILL.md frontmatter (YAML between `---` delimiters) to extract name, description, and trigger conditions.
3. **Install**: Copies the target SKILL.md into `.claude/skills/<name>.md` (project-local) or `~/.claude/skills/<name>/SKILL.md` (global).

### Dependencies

- Python 3.8+ (standard library only for core functionality)
- `pyyaml` - for parsing SKILL.md frontmatter
- No external API keys required

### Key Design Decisions

- The skill instructs Claude to use `git clone --depth 1` for minimal bandwidth
- Skills are identified by folder name, making namespacing simple
- Installation is just a file copy — no package manager, no lock files, no build step

## Limitations

- **No versioning**: Skills are fetched at HEAD; there's no pinning to a specific commit
- **No dependency resolution**: Skills don't declare dependencies on other skills
- **No validation**: The install command doesn't verify the SKILL.md is well-formed beyond basic frontmatter parsing
- **No authentication**: Contributing requires manual fork + PR workflow
- **Registry size**: Currently ~20 community skills; discovery is grep-based, not indexed

## Why It Matters

For teams building Claude-driven products:

- **Agent factories**: Pre-built skills accelerate spinning up specialized agents. Instead of writing custom SKILL.md files for common tasks (k8s debugging, test generation, Docker management), pull from the registry.
- **Lead-gen / marketing**: A skills marketplace creates network effects — contributors get visibility, adopters get productivity. The registry model could be extended to private enterprise registries.
- **Composability**: Skills are the atom of Claude Code's capability system. A searchable registry makes it practical to compose multiple skills into domain-specific agent configurations.
- **Standards alignment**: Following Anthropic's official skill conventions means these skills work with any Claude Code-compatible tooling, not just MetalBear's ecosystem.
