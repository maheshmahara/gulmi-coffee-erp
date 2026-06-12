#!/usr/bin/env sh
set -eu

if [ "${1:-}" = "" ]; then
  echo "Usage: scripts/restore_db.sh path/to/backup.sql.gz"
  exit 1
fi

backup_file="$1"
POSTGRES_DB="${POSTGRES_DB:-gulmi_erp}"
POSTGRES_USER="${POSTGRES_USER:-gulmi_erp}"
POSTGRES_HOST="${POSTGRES_HOST:-localhost}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"

gzip -dc "$backup_file" | PGPASSWORD="${POSTGRES_PASSWORD:-gulmi_erp}" psql \
  --host "$POSTGRES_HOST" \
  --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB"

echo "Restore completed from $backup_file"
