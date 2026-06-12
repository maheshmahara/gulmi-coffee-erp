# API Reference

## Base Path

```text
/api/v1
```

## Sprint 0 Endpoint

### Health

```text
GET /api/v1/health
```

Response:

```json
{
  "data": {
    "status": "ok",
    "database": "ok",
    "version": "0.1.0-sprint0",
    "service": "gulmi-coffee-erp-backend"
  },
  "meta": {}
}
```

If the database cannot be reached, `status` returns `degraded` and `database` returns `unavailable`.

## Sprint 1 Endpoints

### Auth

```text
POST /api/v1/auth/login
POST /api/v1/auth/logout
GET /api/v1/me
```

### Users

```text
GET /api/v1/users
POST /api/v1/users
GET /api/v1/users/{id}
PATCH /api/v1/users/{id}
```

Admin-only in Sprint 1.

### Storage Locations

```text
GET /api/v1/storage-locations
POST /api/v1/storage-locations
GET /api/v1/storage-locations/{id}
PATCH /api/v1/storage-locations/{id}
```

All authenticated users may list/view. Admin and Manager may create/update.

## Phase-1 API Contract

The complete planned Phase-1 API contract is documented in:

```text
docs/phase-1-api-specification.md
```
