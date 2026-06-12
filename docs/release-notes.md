# Release Notes

## 0.1.0-sprint0

Initial implementation foundation:

- Django backend project
- PostgreSQL configuration
- custom user role model
- audit event model
- health endpoint
- React TypeScript PWA shell
- role-aware navigation preview
- Docker Compose local setup
- production compose baseline
- Nginx baseline config
- backup and restore script skeletons
- developer/architecture/deployment docs

## 0.2.0-sprint1

Sprint 1 foundation:

- login/logout/current user API
- Admin user list/create/update API
- real audit event writes for login/logout/user/storage actions
- storage location model and API
- Phase-1 seed command for default users and locations
- frontend login form wired to backend session auth
- frontend storage locations list wired to API
- CSRF-exempt session auth class added for local/staging PWA development flow

## 0.3.0-sprint2

Sprint 2 farmer-to-procurement workflow:

- farmer master model/API/UI
- lot master model/API/UI
- procurement receipt model/API/UI
- backend net kg and total NPR calculations
- procurement post action with posted lock
- lot moves to `quality_pending` after procurement posting
- non-Admin/Manager roles cannot see `rate_npr` or `total_npr`
- audit JSON serialization is UUID-safe
- seed command creates one sample farmer, lot, and draft procurement
- backend workflow tests for create/post/lock/sensitive redaction
