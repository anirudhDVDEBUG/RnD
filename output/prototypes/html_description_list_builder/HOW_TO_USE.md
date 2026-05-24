# How to Use

## As a Claude Code Skill (primary use)

### Install

```bash
mkdir -p ~/.claude/skills/html_description_list_builder
cp SKILL.md ~/.claude/skills/html_description_list_builder/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code and the skill activates automatically:

- "Create a description list for these key-value pairs"
- "Build an accessible definition list in HTML"
- "Generate dt/dd markup for this data"
- "What's the correct way to use the dl element?"
- "How do I have multiple values for one term in a dl?"

### What happens

Claude generates clean, indented `<dl>` HTML following the rules in the skill:

- One `<dt>` per term, one or more `<dd>` per term
- Optional `<div>` wrappers when you need CSS hooks (grid/flexbox)
- `aria-labelledby` pointing to a nearby heading for accessibility

---

## As a standalone Python tool

### Requirements

- Python 3.9+
- No external dependencies

### CLI usage

Pipe JSON to stdin:

```bash
echo '{"items":[{"term":"Name","descriptions":"Ada Lovelace"},{"term":"Born","descriptions":"1815"}]}' \
  | python3 dl_builder.py
```

Or pass a JSON file:

```bash
python3 dl_builder.py my_data.json
```

### JSON format

```json
{
  "items": [
    { "term": "Author", "descriptions": ["Alice", "Bob"] },
    { "term": "License", "descriptions": "MIT" }
  ],
  "wrap_divs": true,
  "heading_id": "credits",
  "heading_text": "Credits",
  "heading_tag": "h2"
}
```

| Field | Required | Description |
|---|---|---|
| `items` | Yes | Array of `{term, descriptions}` objects |
| `items[].term` | Yes | The `<dt>` text |
| `items[].descriptions` | Yes | String or array of strings for `<dd>` elements |
| `wrap_divs` | No | Wrap each group in `<div>` (default: false) |
| `heading_id` | No | Generates a heading + `aria-labelledby` |
| `heading_text` | No | Heading text (defaults to title-cased heading_id) |
| `heading_tag` | No | `h1`-`h6` (default: `h2`) |

### Python API

```python
from dl_builder import build_dl

html = build_dl(
    items=[
        {"term": "Tool", "descriptions": ["Claude Code", "Python"]},
        {"term": "Status", "descriptions": "Active"},
    ],
    wrap_divs=True,
    heading_id="stack",
)
print(html)
```

---

## First 60 seconds

```bash
git clone <this-repo> && cd html_description_list_builder
bash run.sh
```

Output (truncated):

```
--- Example 1: Basic description list (no divs, no ARIA) ---

<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language</dd>
  <dt>CSS</dt>
  <dd>Cascading Style Sheets</dd>
  <dt>JS</dt>
  <dd>JavaScript</dd>
</dl>

--- Example 4: ARIA-labeled list with heading ---

<h2 id="project-metadata">Project Metadata</h2>
<dl aria-labelledby="project-metadata">
  <div>
    <dt>License</dt>
    <dd>MIT</dd>
  </div>
  <div>
    <dt>Language</dt>
    <dd>Python</dd>
    <dd>HTML</dd>
  </div>
</dl>
```
