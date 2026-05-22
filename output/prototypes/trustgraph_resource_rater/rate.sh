#!/usr/bin/env bash
# TrustGraph Resource Rater — PostToolUse hook script
# Rates external resources and appends scores to a JSONL ledger.
set -euo pipefail

TOOL_NAME="${1:-}"
TOOL_INPUT="${2:-}"
TOOL_OUTPUT="${3:-}"
LEDGER="${TRUSTGRAPH_LEDGER:-$HOME/.claude/trustgraph_ledger.jsonl}"

# Extract first URL domain from combined input+output
DOMAIN=$(echo "$TOOL_INPUT $TOOL_OUTPUT" \
  | grep -oP 'https?://[^/\s"'"'"']+' \
  | head -1 \
  | sed 's|https\?://||' \
  | cut -d/ -f1) || true

[ -z "$DOMAIN" ] && exit 0

# Ensure ledger directory exists
mkdir -p "$(dirname "$LEDGER")"

# Build rating prompt
PROMPT="Rate the trustworthiness of this resource on a scale of 1-10. Domain: $DOMAIN. Tool: $TOOL_NAME. Respond with ONLY a JSON object: {\"domain\": \"...\", \"score\": N, \"reason\": \"one sentence\"}."

# Backend selection: Anthropic API key or claude -p fallback
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  ESCAPED_PROMPT=$(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$PROMPT")
  RESULT=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{\"model\":\"claude-haiku-4-5-20251001\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":$ESCAPED_PROMPT}]}" \
    | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['content'][0]['text'])" 2>/dev/null) || RESULT=""
elif command -v claude &>/dev/null; then
  RESULT=$(echo "$PROMPT" | claude -p 2>/dev/null) || RESULT=""
else
  echo "trustgraph: no backend available (set ANTHROPIC_API_KEY or install claude CLI)" >&2
  exit 0
fi

[ -z "$RESULT" ] && exit 0

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"ts\":\"$TIMESTAMP\",\"tool\":\"$TOOL_NAME\",\"domain\":\"$DOMAIN\",\"rating\":$RESULT}" >> "$LEDGER"
