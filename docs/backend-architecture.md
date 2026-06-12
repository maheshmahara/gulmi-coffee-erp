# Backend Architecture

## Stack

- Django
- Django REST Framework
- PostgreSQL 16
- Gunicorn for production runtime

## Project Layout

```text
backend/
  manage.py
  requirements.txt
  gulmi_erp/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  apps/
    accounts/
    audit/
    common/
    core/
    storage/
```

## Sprint 0 Apps

### accounts

Defines the `AppUser` model and Phase-1 role choices:

- admin
- manager
- quality
- storage
- production
- sales
- viewer

### audit

Defines `AuditEvent` and audit action choices. Sprint 1 will wire real login/logout/create events through `AuditService`.

### common

Contains shared service contracts:

- `CodeGeneratorService`
- `SensitiveFieldFilterService`

### core

Contains the public health endpoint:

```text
GET /api/v1/health
```

### storage

Defines `StorageLocation`, the first Phase-1 operational master data model.

Sprint 1 endpoints:

- `GET /api/v1/storage-locations`
- `POST /api/v1/storage-locations`
- `GET /api/v1/storage-locations/{id}`
- `PATCH /api/v1/storage-locations/{id}`

## Service Layer Rule

Business logic must live in service classes, not directly in views.

Planned services:

- CodeGeneratorService
- QirbCalculationService
- ProcurementPostingService
- BagCreationService
- StorageMovementService
- InventoryLedgerService
- AuditService
- QrResolverService
- SensitiveFieldFilterService

## Sensitive Field Rule

Sensitive financial fields must be filtered in backend serializers/services. Frontend-only hiding is not acceptable.
