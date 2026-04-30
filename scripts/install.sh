#!/usr/bin/env bash
# One-time setup for TrendForge.
set -euo pipefail

PROJECT_DIR="${TRENDFORGE_HOME:-$HOME/trendforge}"
cd "$PROJECT_DIR"

PYTHON="${PYTHON:-python3}"

echo "[install] creating venv..."
$PYTHON -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[install] installing requirements..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "[install] initializing DB..."
PYTHONPATH="$PROJECT_DIR" python -c "from trendforge.store import init_db; init_db()"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[install] created .env — fill in GITHUB_TOKEN, GMAIL_SENDER, GMAIL_APP_PASSWORD"
fi

chmod +x scripts/cron_runner.sh scripts/backup_db.sh

echo
echo "Done. Add to crontab (crontab -e):"
echo "  0 7 * * * $PROJECT_DIR/scripts/cron_runner.sh"
echo
echo "Verify with: bash scripts/cron_runner.sh --dry-run"
