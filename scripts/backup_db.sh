#!/usr/bin/env sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-./backups}"
POSTGRES_DB="${POSTGRES_DB:-gulmi_erp}"
POSTGRES_USER="${POSTGRES_USER:-gulmi_erp}"
POSTGRES_HOST="${POSTGRES_HOST:-localhost}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"

mkdir -p "$BACKUP_DIR"

timestamp="$(date +%Y-%m-%d_%H%M%S)"
output="$BACKUP_DIR/gulmi_erp_${timestamp}.sql.gz"

PGPASSWORD="${POSTGRES_PASSWORD:-gulmi_erp}" pg_dump \
  --host "$POSTGRES_HOST" \
  --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --no-owner \
  --no-privileges \
  | gzip > "$output"

echo "Backup written to $output"
