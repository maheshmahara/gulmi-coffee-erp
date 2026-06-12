# Testing Guide

## Sprint 0 Verification

Required checks:

```bash
docker compose up --build
curl http://localhost:8000/api/v1/health
```

Expected:

- backend health endpoint responds
- database status is `ok`
- frontend loads at `http://localhost:5173`

## Static Checks Used In This Commit

In this environment, dependency installation was not run. Sprint 0 files were checked structurally by repository inspection.

Future CI should run:

```bash
docker compose run --rm backend python manage.py test
docker compose run --rm frontend npm run build
```

## Full Phase-1 QA

Use:

```text
docs/phase-1-testing-qa-specification.md
docs/phase-1-requirements-traceability-matrix.md
```

