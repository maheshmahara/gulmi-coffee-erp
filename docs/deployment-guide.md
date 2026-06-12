# Deployment Guide

## Sprint 0 Deployment Shape

Local development:

```bash
cp .env.example .env
docker compose up --build
```

Production-style:

```bash
cp .env.example .env
docker compose -f docker-compose.prod.yml up --build -d
```

Before real production use:

- set strong secrets
- configure final domain
- configure HTTPS
- configure off-server backups
- test restore
- restrict PostgreSQL exposure

## Services

- `db`: PostgreSQL 16
- `backend`: Django API
- `frontend`: React app
- `nginx`: reverse proxy in production compose

## Health Check

```bash
curl http://localhost:8001/api/v1/health
```

## Production Notes

The current production compose is a Sprint 0 baseline. Before go-live, add:

- HTTPS certificates
- persistent backup target
- monitoring
- log rotation
- domain-specific Nginx config
