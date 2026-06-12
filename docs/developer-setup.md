# Developer Setup

## Purpose

This document explains how to run the Gulmi Coffee ERP Sprint 0 foundation locally.

## Prerequisites

- Docker
- Docker Compose
- Git

No global Python or Node installation is required when using Docker.

## First Run

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/api/v1/health`
- Django admin: `http://localhost:8000/admin`
- PostgreSQL: `localhost:5432`

## Backend Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected shape:

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

## Seed Phase-1 Users And Locations

After migrations, create default Sprint 1 users and storage locations:

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
