# Backup And Restore Guide

## Backup

Run:

```bash
POSTGRES_PASSWORD=... scripts/backup_db.sh
```

Defaults:

- database: `gulmi_erp`
- user: `gulmi_erp`
- host: `localhost`
- port: `5432`
- output directory: `./backups`

## Restore

Run:

```bash
POSTGRES_PASSWORD=... scripts/restore_db.sh backups/gulmi_erp_YYYY-MM-DD_HHMMSS.sql.gz
```

## Restore Drill Rule

Before go-live, restore a backup to a fresh database and confirm:

- app starts
- login works
- health endpoint works
- traceability page works once Phase 1 is complete

