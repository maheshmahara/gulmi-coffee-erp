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

## Phase-1 API Contract

The complete planned Phase-1 API contract is documented in:

```text
docs/phase-1-api-specification.md
```

