# Technical Details

## What it does

Skill Router is a meta-skill that acts as a dispatcher layer on top of Claude Code's skill system. When a user has multiple skills installed and isn't sure which one to invoke, Skill Router scans the project's `.claude/skills/` directory, parses every `SKILL.md` frontmatter (name, description, trigger phrases), and scores each skill against the user's natural-language request. It returns ranked suggestions or auto-routes to the highest-confidence match.

The core value is **discoverability at scale**: once you have 5-10+ skills installed, remembering trigger phrases becomes a burden. Skill Router eliminates that friction.

## Architecture

### Key files

| File | Purpose |
|------|---------|
| `skill_router.py` | Full implementation: parser, scorer, router, CLI, and demo |
| `SKILL.md` | The skill definition Claude Code reads to activate routing |
| `mock_skills/` | Four sample SKILL.md files for the standalone demo |
| `run.sh` | Runs the demo end-to-end |

### Data flow

```
User request
    |
    v
scan_skills_dir()  -->  parse_skill_md() per file
    |                         |
    |                   Skill(name, description, triggers)
    v
score_skill(skill, query)   x N skills
    |
    |   Scoring layers:
    |   1. Exact trigger-phrase match  (0.70 - 1.00)
    |   2. Skill name substring match  (0.80)
    |   3. Jaccard keyword overlap on description  (0 - 0.85)
    |   4. Fuzzy SequenceMatcher on name  (0 - 0.50)
    |
    v
route()  -->  sort by score  -->  suggest top-3 or auto-route
```

### Scoring algorithm

1. **Exact trigger match** (highest priority): If a skill's trigger phrase appears as a substring of the query, score starts at 0.70 and scales up to 1.0 based on how much of the query the trigger covers.
2. **Name match**: If the skill's name appears in the query, score is 0.80.
3. **Description keyword overlap**: Jaccard similarity between description words and query words, capped at 0.85.
4. **Fuzzy name similarity**: `SequenceMatcher` ratio between skill name and query, capped at 0.50 (tiebreaker only).

The highest score across all four layers wins. Auto-routing requires >= 0.70 confidence.

### Dependencies

- **Python 3.10+** (for `X | Y` type union syntax)
- **No external packages** — uses only `re`, `json`, `pathlib`, `dataclasses`, `difflib` from stdlib

### No LLM calls

The routing logic is entirely deterministic — no API calls, no model inference, no tokens consumed. This is intentional: Skill Router runs *before* the LLM processes the request, so it must be fast and free.

## Limitations

- **No semantic understanding**: Scoring is keyword/substring-based, not embeddings-based. "Help me make my site faster" won't match an "seo-audit" skill unless overlapping keywords exist. A future version could use embeddings for semantic matching.
- **Flat directory scan only**: Expects skills in `<dir>/<skill-name>/SKILL.md` structure. Doesn't parse CLAUDE.md `@import` references or nested skill hierarchies.
- **YAML-ish parsing**: The frontmatter parser is regex-based, not a full YAML parser. Complex multi-line descriptions or nested YAML may not parse correctly.
- **No learning**: Doesn't track which skills you actually use or adjust rankings over time. Every query is scored fresh.
- **Single-skill routing**: Always picks one best skill. Doesn't compose multiple skills for complex multi-step requests.

## Why it matters

For teams building **Claude-driven products** (lead-gen pipelines, marketing automation, ad creative factories, agent scaffolding), the skill ecosystem is growing fast. Installing 10-20 skills per project is already common. Without a routing layer, users either memorize trigger phrases or resort to trial-and-error. Skill Router is the missing index — it turns a bag of skills into a navigable toolkit.

Particularly relevant for:
- **Agent factories**: Route sub-tasks to specialized skills automatically
- **Marketing/ad teams**: Match "generate Facebook ads" to the right creative skill without knowing its name
- **Voice AI builders**: Quickly find the right scaffolding skill among many installed options
