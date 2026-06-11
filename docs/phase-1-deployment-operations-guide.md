# Phase-1 Deployment And Operations Guide

## 1. Purpose

This document defines how to deploy, operate, back up, monitor, and support the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

This guide is written for an owner/operator with a network engineering background.

## 2. Deployment Philosophy

The ERP must be treated like production infrastructure:

- stable server
- controlled access
- HTTPS
- backups
- restore drills
- monitoring
- clear user roles
- documented go-live process

An ERP without backups and operational discipline is not an ERP. It is a fragile spreadsheet with a login page.

## 3. Recommended Environments

Use three environments:

```text
Development
Staging
Production
```

## 3.1 Development

Purpose:

- developer coding
- local testing
- not used by staff

Data:

- fake/sample data only

## 3.2 Staging

Purpose:

- owner review
- staff testing
- QA acceptance
- pilot simulation

Data:

- sample data
- optional copied production-like data with sensitive values removed

Rule:

- Every release must pass staging before production.

## 3.3 Production

Purpose:

- real factory operation
- real farmer/procurement/QIR-B/bag/storage records

Rule:

- no experimental changes directly in production

## 4. Recommended Hosting Architecture

Phase-1 simple deployment:

```text
Internet / Local Users
        |
      DNS
        |
     HTTPS
        |
     Nginx
        |
  Backend API + Frontend
        |
   PostgreSQL Database
        |
   Backup Storage
```

Recommended first production setup:

```text
Ubuntu VPS
Docker Compose
Nginx reverse proxy
PostgreSQL 16
Backend container
Frontend static build
Daily off-server backups
```

## 5. Server Sizing

For Phase 1:

```text
CPU: 2 vCPU minimum
RAM: 4 GB minimum
Disk: 80 GB SSD minimum
OS: Ubuntu LTS
```

Recommended:

```text
CPU: 4 vCPU
RAM: 8 GB
Disk: 160 GB SSD
```

Reason:

- PostgreSQL needs memory.
- Backups need disk room.
- Logs grow over time.
- Future modules will add load.

## 6. Domain And DNS

Choose the ERP domain before printing permanent QR codes.

Recommended:

```text
app.gulmicoffee.com
```

QR resolver:

```text
https://app.gulmicoffee.com/r/{uuid}
```

Important:

- Do not print QR codes with temporary URLs.
- QR URLs should remain valid for years.
- If domain changes, old QR labels become painful.

DNS records:

```text
A record: app.gulmicoffee.com -> server public IP
```

Optional:

```text
CNAME: qr.gulmicoffee.com -> app.gulmicoffee.com
```

## 7. SSL / HTTPS

HTTPS is mandatory.

Use:

```text
Let's Encrypt
Certbot
Nginx
```

Rules:

- redirect HTTP to HTTPS
- renew certificates automatically
- test renewal before go-live

## 8. Firewall Rules

Minimum inbound ports:

```text
22/tcp SSH, restricted to admin IP if possible
80/tcp HTTP, for redirect/certbot
443/tcp HTTPS
```

Do not expose PostgreSQL publicly.

PostgreSQL should listen only on:

```text
localhost
Docker internal network
private network
```

Recommended hardening:

- SSH key login only
- disable root SSH login
- fail2ban
- firewall allowlist for SSH if static admin IP is available

## 9. Docker Compose Services

Recommended services:

```text
nginx
backend
frontend
postgres
redis, optional for background jobs
backup
```

Example service responsibility:

| Service | Responsibility |
|---|---|
| nginx | HTTPS reverse proxy |
| backend | Django API |
| frontend | React build/static files |
| postgres | ERP database |
| redis | queue/cache, optional |
| backup | scheduled database backup |

## 10. Environment Variables

Production secrets must not be committed to git.

Use `.env` on the server or secret manager.

Required variables:

```text
APP_ENV=production
APP_DOMAIN=app.gulmicoffee.com
DATABASE_URL=postgres://...
SECRET_KEY=...
JWT_SECRET=...
ALLOWED_HOSTS=app.gulmicoffee.com
CORS_ALLOWED_ORIGINS=https://app.gulmicoffee.com
BACKUP_BUCKET=...
BACKUP_ACCESS_KEY=...
BACKUP_SECRET_KEY=...
```

Rules:

- never share production secrets in chat
- rotate secrets if leaked
- separate staging and production secrets

## 11. Database Operations

Database:

```text
PostgreSQL 16
```

Production rules:

- migrations are run during deployment
- no manual table edits unless emergency and documented
- no direct stock edits
- no direct deletion of posted records

Recommended database users:

```text
erp_app_user: app read/write
erp_readonly_user: reporting/Metabase read-only
erp_backup_user: backup-only if desired
```

## 12. Backup Policy

Minimum backup policy:

```text
Daily PostgreSQL backup
Weekly full server/application backup
Monthly restore drill
Off-server backup copy
```

Recommended backup retention:

```text
Daily backups: keep 14 days
Weekly backups: keep 8 weeks
Monthly backups: keep 12 months
```

Backup target:

- S3-compatible object storage
- separate VPS
- encrypted external storage

Do not keep the only backup on the same server.

## 13. Backup Command Pattern

Developer/admin should provide a script like:

```text
scripts/backup_db.sh
```

Expected behavior:

1. run `pg_dump`
2. compress output
3. timestamp filename
4. upload off-server
5. verify upload
6. log success/failure

Example backup filename:

```text
gulmi_erp_prod_2026-06-11_2300.sql.gz
```

## 14. Restore Drill

Monthly restore drill:

1. Create fresh test database.
2. Download latest backup.
3. Restore backup.
4. Run migrations if needed.
5. Start app against restored DB.
6. Open one bag traceability page.
7. Confirm data integrity.

Acceptance:

- restore completes
- app starts
- login works
- traceability works
- latest expected records exist

No-go:

- backup file missing
- restore fails
- restored app cannot show traceability

## 15. Logging

Required logs:

- backend application logs
- Nginx access/error logs
- PostgreSQL logs
- backup logs
- deployment logs
- audit_event table

Important:

- application logs are technical
- audit_event is business accountability

Do not confuse them.

## 16. Monitoring

Minimum monitoring:

- server CPU
- memory
- disk usage
- database availability
- app health endpoint
- SSL expiry
- backup success/failure

Recommended health endpoint:

```text
GET /api/v1/health
```

Response:

```json
{
  "status": "ok",
  "database": "ok",
  "version": "1.0.0"
}
```

Alert thresholds:

```text
Disk > 80% warning
Disk > 90% critical
Memory > 85% warning
Backup failed critical
SSL expires in < 14 days warning
App health check fails critical
```

## 17. Deployment Process

Recommended production deployment steps:

1. Developer merges tested release branch.
2. Build backend/frontend images.
3. Deploy to staging.
4. Run migrations on staging.
5. Run QA smoke test.
6. Owner approves.
7. Take production backup.
8. Deploy production.
9. Run production migrations.
10. Run health check.
11. Run smoke test.
12. Monitor logs.

Never deploy production before taking a backup.

## 18. Rollback Plan

Each release must have rollback instructions.

Rollback should include:

- previous container image version
- database migration rollback plan
- latest pre-deployment backup
- responsible person

Rule:

If database migration is not safely reversible, test restore plan before deployment.

## 19. Go-Live Preparation

Before go-live:

- domain configured
- HTTPS working
- production users created
- roles tested
- storage locations created
- backup tested
- restore tested
- QR print tested
- staff trained
- pilot batch completed
- critical/high bugs fixed

## 20. Production Seed Data

Before real use, create:

Users:

- Admin
- Manager
- Quality
- Storage
- Viewer

Storage locations:

- WH-001 Main Warehouse
- RACK-PAR-001 Parchment Rack 1
- RACK-PAR-002 Parchment Rack 2
- RACK-GRN-001 Green Bean Rack 1
- HOLD-001 Defect/Recheck Area
- DRY-001 Solar Drying Area
- PROD-HULL-001 Hulling Area

Business settings:

- code prefixes
- current year
- company name
- QR base URL

## 21. Staff Training Plan

Train by role.

## 21.1 Admin/Manager

Training topics:

- user roles
- farmer creation
- procurement posting
- sensitive field access
- exception approval
- audit log
- backup awareness
- go/no-go decisions

## 21.2 Quality

Training topics:

- QIR-B creation
- entering 5 readings
- understanding approved/monitor/hold/retake
- creating exceptions
- reading QIR-B dashboard

## 21.3 Storage

Training topics:

- creating bags
- printing QR labels
- moving bags
- logging environment
- scanning QR
- reporting damaged bags

## 21.4 Viewer

Training topics:

- search
- view traceability
- understand read-only access

## 22. Daily Operating Checklist

Every operating day:

- confirm app is reachable
- check dashboard
- review open exceptions
- enter environment log
- verify previous day's backup succeeded
- ensure QR scanner/phone works
- check bags on hold

## 23. Weekly Operating Checklist

Every week:

- review storage movements
- check inventory summary
- review QIR-B hold/retake trends
- check user access list
- check disk usage
- confirm backup storage has latest files

## 24. Monthly Operating Checklist

Every month:

- perform backup restore drill
- review audit log exports
- review inactive users
- review exception closure rate
- review storage location list
- clean old logs if needed
- update SOP if workflow changed

## 25. Incident Response

## 25.1 App Down

Steps:

1. Check internet/server reachability.
2. Check DNS.
3. Check Nginx.
4. Check backend container.
5. Check database container.
6. Check disk usage.
7. Check logs.
8. Escalate to developer if unresolved.

## 25.2 Database Error

Steps:

1. Stop write-heavy operations if data integrity risk exists.
2. Check PostgreSQL status.
3. Check disk space.
4. Check latest migrations.
5. Review backend errors.
6. Restore from backup only if necessary and approved.

## 25.3 Sensitive Data Leak

Steps:

1. Disable affected account if needed.
2. Review audit log.
3. Identify exported/downloaded data.
4. Fix permission bug.
5. Rotate credentials if required.
6. Document incident.

## 25.4 Wrong Procurement/QIR-B Posted

Steps:

1. Do not edit database directly.
2. Create exception.
3. Create adjustment workflow if available.
4. Manager/Admin approves correction.
5. Audit event records correction.

## 26. Emergency Paper Fallback

If ERP is unavailable:

- use numbered emergency paper forms
- record date/time/user
- record farmer/lot/weight/QIR-B/bag details
- back-enter same day when system returns
- manager verifies back-entry

Rule:

Paper fallback is emergency-only, not parallel permanent workflow.

## 27. QR Label Operations

Before printing production QR:

- confirm final domain
- confirm HTTPS works
- scan test QR
- verify internal traceability page
- verify public-safe page

Label should include:

- bag code
- item type
- weight
- lot code
- QR code

Do not print:

- rate
- cost
- farmer payment
- internal defects

## 28. Access Control Operations

When staff joins:

- create user
- assign least-privilege role
- temporary password/PIN
- train user

When staff leaves:

- deactivate account immediately
- do not delete user
- preserve audit history

Quarterly:

- review active users
- confirm roles are still correct

## 29. Production Acceptance Checklist

Production is ready when:

- app accessible at final domain
- HTTPS valid
- admin login works
- all role logins work
- farmer creation works
- procurement post works
- QIR-B post works
- bag creation works
- QR scan works
- storage movement works
- environment log works
- audit log works
- backup succeeds
- restore drill succeeds
- sensitive fields hidden for non-admin roles
- staff pilot completed

## 30. Phase-1 Operational Definition Of Done

Phase 1 is operationally done when:

```text
Gulmi Coffee can run one real farmer-to-bag storage workflow in production, scan the bag QR, see full internal traceability, protect sensitive cost data, and recover the system from a tested backup.
```

