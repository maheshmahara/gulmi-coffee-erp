# Phase-1 Sprint 2 Implementation Record

## Goal

Implement the farmer-to-procurement workflow:

```text
Farmer -> Lot -> Procurement Receipt -> Post -> Quality Pending
```

## Implemented Backend Scope

- `apps.procurement` Django app.
- Farmer master model/API.
- Lot master model/API.
- Procurement receipt model/API.
- Procurement net kg calculation:

```text
net_kg = gross_kg - tare_kg
```

- Procurement total calculation:

```text
total_npr = net_kg * rate_npr
```

- Procurement post action:
  - validates weights
  - sets status to `posted`
  - records `posted_at` and `posted_by`
  - moves lot status to `quality_pending`
  - writes audit event
- Posted procurement edit lock.
- Sensitive field redaction for non-Admin/Manager users:
  - `rate_npr`
  - `total_npr`
- UUID primary keys and readable codes:
  - `FARM-YYYY-######`
  - `LOT-YYYY-######`
  - `PROC-YYYY-######`

## Implemented Frontend Scope

- Farmers screen with create form and list.
- Lots screen with create form and list.
- Procurements screen with create form, calculated values, and post action.
- Cost fields hidden unless current role is Admin or Manager.
- Posted procurements show locked state.

## API Endpoints

```text
GET/POST   /api/v1/farmers
GET/PATCH  /api/v1/farmers/{id}
GET/POST   /api/v1/lots
GET/PATCH  /api/v1/lots/{id}
GET/POST   /api/v1/procurements
GET/PATCH  /api/v1/procurements/{id}
POST       /api/v1/procurements/{id}/post
```

## Seed Data

`python manage.py seed_phase1` now creates:

- default users
- storage locations
- sample farmer
- sample parchment lot
- sample draft procurement receipt

## Verification

Run:

```bash
docker compose run --rm backend python manage.py makemigrations --check --dry-run
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py test apps.procurement
docker compose run --rm frontend npm run build
```

## Acceptance Criteria

Accepted when:

- Admin can create farmer, lot, and procurement receipt.
- Admin can post procurement receipt.
- Posted procurement cannot be edited.
- Lot moves to `quality_pending` after posting.
- Viewer can list procurement but sees `rate_npr = null` and `total_npr = null`.
