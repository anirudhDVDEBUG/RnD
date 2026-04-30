#!/usr/bin/env bash
# Backup data/trendforge.db to data/archive/<date>.db.gz
set -euo pipefail

PROJECT_DIR="${TRENDFORGE_HOME:-$HOME/trendforge}"
DB="$PROJECT_DIR/data/trendforge.db"
ARCHIVE="$PROJECT_DIR/data/archive"

if [ ! -f "$DB" ]; then
  echo "No DB to back up: $DB"
  exit 0
fi

mkdir -p "$ARCHIVE"
DATE=$(date +%Y-%m-%d)
OUT="$ARCHIVE/$DATE.db.gz"

# sqlite .backup is safe under writers; falls back to plain copy if sqlite3 absent
if command -v sqlite3 >/dev/null 2>&1; then
  TMP=$(mktemp)
  sqlite3 "$DB" ".backup '$TMP'"
  gzip -c "$TMP" > "$OUT"
  rm -f "$TMP"
else
  gzip -c "$DB" > "$OUT"
fi

echo "Backup: $OUT ($(du -h "$OUT" | cut -f1))"

# keep last 30 backups
ls -1t "$ARCHIVE"/*.db.gz 2>/dev/null | tail -n +31 | xargs -r rm -f
