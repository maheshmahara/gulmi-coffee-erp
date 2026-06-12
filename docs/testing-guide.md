# Testing Guide

## Sprint 0 Verification

Required checks:

```bash
docker compose up --build
curl http://localhost:8001/api/v1/health
```

Expected:

- backend health endpoint responds
- database status is `ok`
- frontend loads at `http://localhost:5174`

## Static Checks Used In This Commit

In this environment, dependency installation was not run. Sprint 0 files were checked structurally by repository inspection.

Future CI should run:

```bash
docker compose run --rm backend python manage.py test
docker compose run --rm frontend npm run build
```

## Sprint 1 Manual Smoke

After `docker compose up --build`:

```bash
docker compose run --rm backend python manage.py seed_phase1
```

Then verify:

1. Open `http://localhost:5174`.
2. Login as `admin` with `ChangeMe123!`.
3. Confirm session strip shows Admin User.
4. Open Storage navigation.
5. Confirm seeded storage locations are listed.
6. Open `http://localhost:8001/admin` and confirm audit events exist after login/logout.

## Full Phase-1 QA

Use:

```text
docs/phase-1-testing-qa-specification.md
docs/phase-1-requirements-traceability-matrix.md
```
