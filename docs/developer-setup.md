# Developer Setup

## Purpose

This document explains how to run the Gulmi Coffee ERP Phase 1 foundation locally.

## Prerequisites

- Docker
- Docker Compose
- Git

No global Python or Node installation is required when using Docker.

Default host ports avoid common conflicts with existing local PostgreSQL, Django, and Vite services. Change the `*_HOST_PORT` values in `.env` if your machine already uses these ports.

## First Run

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Frontend: `http://localhost:5174`
- Backend health: `http://localhost:8001/api/v1/health`
- Django admin: `http://localhost:8001/admin`
- PostgreSQL: `localhost:5433`

## Backend Health Check

```bash
curl http://localhost:8001/api/v1/health
```

Expected shape:

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

## Migrations

Docker Compose runs migrations automatically for local development.

Manual command:

```bash
docker compose run --rm backend python manage.py migrate
```

## Create Superuser

```bash
docker compose run --rm backend python manage.py createsuperuser
```

## Seed Phase-1 Users, Locations, And Demo Procurement

After migrations, create default users, storage locations, and one sample farmer/lot/procurement chain:

```bash
docker compose run --rm backend python manage.py seed_phase1
```

Default usernames:

```text
admin
manager
quality
storage
viewer
```

Default password:

```text
ChangeMe123!
```

Use these only for local/staging development. Change production credentials before go-live.

## Stop

```bash
docker compose down
```

## Remove Local Database

This deletes local development data:

```bash
docker compose down -v
```

## Sprint 0 Scope

Sprint 0 provides:

- Django backend foundation
- React PWA shell
- PostgreSQL Docker service
- health endpoint
- custom user role model
- audit event foundation
- code generator/sensitive field service skeletons
- deployment and backup script skeletons

## Sprint 1 Foundation

Sprint 1 adds:

- login/logout/current user endpoints
- user list/create/update endpoints for Admin
- audit event writes for login/logout/user/storage actions
- storage location model/API
- seed command for default users and locations
- frontend login form
- frontend storage locations list

## Sprint 2 Procurement Foundation

Sprint 2 adds:

- farmer master API/UI
- lot master API/UI
- procurement receipt API/UI
- backend net kg and total NPR calculation
- procurement post action
- posted procurement lock
- Admin/Manager-only cost visibility
