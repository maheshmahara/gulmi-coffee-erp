# Database Migrations

## Sprint 0

Sprint 0 introduces:

- custom `accounts.AppUser`
- `audit.AuditEvent`
- `storage.StorageLocation`

Migrations:

```text
backend/apps/accounts/migrations/0001_initial.py
backend/apps/audit/migrations/0001_initial.py
backend/apps/storage/migrations/0001_initial.py
```

## Migration Rule

All schema changes must be represented as migrations.

Do not manually change production database structure.

## Planned Phase-1 Migration Order

1. users and audit foundation
2. storage locations
3. farmers
4. lots
5. procurements
6. QIR-B summary/readings
7. bags
8. storage movements
9. environment logs
10. exceptions
11. inventory ledger
12. reports/views
