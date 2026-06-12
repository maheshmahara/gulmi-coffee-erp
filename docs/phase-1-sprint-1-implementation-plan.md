# Phase-1 Sprint 1 Implementation Plan

## 1. Goal

Implement the first access-control and master-data foundation:

```text
Users -> Roles -> Audit Events -> Storage Locations
```

## 2. Source Documents

Primary references:

- `docs/phase-1-developer-task-breakdown-sprint-plan.md`
- `docs/phase-1-api-specification.md`
- `docs/phase-1-ui-workflow-specification.md`
- `docs/phase-1-database-schema.md`
- `docs/phase-1-testing-qa-specification.md`

## 3. Implemented Scope

Backend:

- login/logout/current-user endpoints
- Admin-only user list/create/update endpoints
- real audit event writes for login/logout/user/storage actions
- `StorageLocation` model
- storage location list/create/detail/update endpoints
- seed command for default users and storage locations

Frontend:

- login form wired to backend
- logout action
- current user session strip
- role-aware nav updates from logged-in user
- storage locations list wired to backend

Documentation:

- API reference updates
- developer setup updates
- testing guide updates
- release notes and known limitations

## 4. Acceptance Criteria

Sprint 1 is accepted when:

- Admin can log in.
- Logout works.
- `/api/v1/me` returns the current user.
- Admin can create users through API.
- Audit events are created for login/logout/user/storage actions.
- Storage locations can be listed.
- Admin/Manager can create/update storage locations.
- Non-Admin/Manager users cannot create/update storage locations.
- Seed command creates default users and default storage locations.

## 5. Verification Commands

Static checks:

```bash
python3 -m compileall -q backend
git diff --check
docker compose config
```

Manual smoke after dependency build:

```bash
docker compose up --build
docker compose run --rm backend python manage.py seed_phase1
```

Then open:

```text
Frontend: http://localhost:5173
Health: http://localhost:8000/api/v1/health
```

Login:

```text
username: admin
password: ChangeMe123!
```

## 6. Known Limitations

- Full user-management UI is deferred.
- Storage create/edit UI is deferred.
- Count-based code generation is not production-concurrency safe.
- Full automated test suite is deferred to QA hardening unless dependency installation is available.

## 7. Next Step

Sprint 2:

```text
Farmers, Lots, and Procurement
```

