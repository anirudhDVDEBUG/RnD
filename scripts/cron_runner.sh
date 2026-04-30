#!/usr/bin/env bash
# Daily TrendForge cron entry point.
set -euo pipefail

# Cron strips PATH; load shell env first.
source "$HOME/.bashrc" 2>/dev/null || source "$HOME/.zshrc" 2>/dev/null || true

# CRITICAL: force Max-plan Claude auth, not API-key billing.
unset ANTHROPIC_API_KEY

PROJECT_DIR="${TRENDFORGE_HOME:-$HOME/trendforge}"
cd "$PROJECT_DIR"

# Load .env so GITHUB_TOKEN, GMAIL_*, etc. reach subprocesses (gh, smtplib, ...)
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
  # gh CLI uses GH_TOKEN; mirror GITHUB_TOKEN if not set
  export GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
fi

# Activate venv if present
if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

LOG_DIR="$PROJECT_DIR/data/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

PYTHON="${PYTHON:-python3}"

{
  echo "=== TrendForge run started at $(date -Iseconds) ==="
  PYTHONPATH="$PROJECT_DIR" "$PYTHON" -m trendforge.orchestrator "$@"
  echo "=== TrendForge run completed at $(date -Iseconds) ==="
} >> "$LOG_FILE" 2>&1

bash "$PROJECT_DIR/scripts/backup_db.sh" >> "$LOG_FILE" 2>&1 || true

# Push generated outputs to GitHub if configured
if [ -d "$PROJECT_DIR/.git" ]; then
  cd "$PROJECT_DIR"
  git add output/ 2>/dev/null || true
  git -c user.name="trendforge-bot" \
      -c user.email="bot@adroitec.local" \
      commit -m "Daily run: $(date +%Y-%m-%d)" >> "$LOG_FILE" 2>&1 || echo "Nothing to commit" >> "$LOG_FILE"
  git push origin main >> "$LOG_FILE" 2>&1 || true
fi
