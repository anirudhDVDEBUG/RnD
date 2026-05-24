#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================"
echo "  HTML Description List Builder — Demo"
echo "============================================"
echo ""

python3 -c "
import json
from dl_builder import build_dl

with open('examples.json') as f:
    examples = json.load(f)

for i, ex in enumerate(examples, 1):
    print(f'--- Example {i}: {ex[\"label\"]} ---')
    print()
    cfg = ex['config']
    heading_id = cfg.get('heading_id')
    if heading_id:
        tag = cfg.get('heading_tag', 'h2')
        text = cfg.get('heading_text', heading_id.replace('-', ' ').title())
        print(f'<{tag} id=\"{heading_id}\">{text}</{tag}>')
    print(build_dl(
        cfg['items'],
        wrap_divs=cfg.get('wrap_divs', False),
        heading_id=heading_id,
    ))
    print()
"

echo "============================================"
echo "  Programmatic usage (pipe JSON via stdin)"
echo "============================================"
echo ""

echo '{"items":[{"term":"Tool","descriptions":"dl_builder.py"},{"term":"Version","descriptions":"1.0.0"}]}' \
  | python3 dl_builder.py

echo ""
echo "Done. All examples rendered successfully."
