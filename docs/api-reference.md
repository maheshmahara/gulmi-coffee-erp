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
    "version": "0.3.0-sprint2",
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
## Sprint 2 Farmer, Lot, And Procurement Endpoints

All endpoints require an authenticated session.

### Farmers

```text
GET /api/v1/farmers
POST /api/v1/farmers
GET /api/v1/farmers/{id}
PATCH /api/v1/farmers/{id}
```

Create/update are Admin/Manager only. List/detail are available to authenticated staff.

Required create fields:

```json
{
  "farmer_name": "Ram Bahadur",
  "phone": "9800000000",
  "village": "Tamghas",
  "district": "Gulmi",
  "farmer_type": "farmer"
}
```

### Lots

```text
GET /api/v1/lots
POST /api/v1/lots
GET /api/v1/lots/{id}
PATCH /api/v1/lots/{id}
```

Create/update are Admin/Manager only.

Required create fields:

```json
{
  "farmer_id": "uuid",
  "item_type": "parchment",
  "harvest_year": 2026
}
```

### Procurement Receipts

```text
GET /api/v1/procurements
POST /api/v1/procurements
GET /api/v1/procurements/{id}
PATCH /api/v1/procurements/{id}
POST /api/v1/procurements/{id}/post
```

Create/update/post are Admin/Manager only. Posted procurements cannot be edited.

Required create fields:

```json
{
  "lot_id": "uuid",
  "gross_kg": "705.000",
  "tare_kg": "5.000",
  "rate_npr": "1300.00"
}
```

Server calculations:

```text
net_kg = gross_kg - tare_kg
total_npr = net_kg * rate_npr
```

Sensitive fields:

- Admin/Manager receive `rate_npr` and `total_npr`.
- Other roles receive `rate_npr: null` and `total_npr: null`.

Posted lock error:

```json
{
  "error": {
    "code": "POSTED_RECORD_LOCKED",
    "message": "Posted procurement cannot be edited."
  }
}
```
