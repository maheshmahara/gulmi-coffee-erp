# Developer Handoff Package

## 1. Start Here

You are building the Gulmi Coffee ERP Phase-1 MVP.

This is not a generic ERP. It is a traceability-first coffee operations system for a vertically integrated coffee business in Nepal.

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The first goal is simple but strict:

```text
Scan any bag QR and see farmer, lot, procurement, QIR-B, bag, storage, inventory ledger, exceptions, and audit history.
```

## 2. Read Documents In This Order

Read the repo documents in this order:

1. `README.md`
2. `docs/gulmi-coffee-erp-sdlc-record.md`
3. `docs/phase-1-mvp-software-requirements.md`
4. `docs/phase-1-database-schema.md`
5. `docs/phase-1-api-specification.md`
6. `docs/phase-1-ui-workflow-specification.md`
7. `docs/phase-1-testing-qa-specification.md`
8. `docs/phase-1-deployment-operations-guide.md`
9. `docs/phase-1-developer-task-breakdown-sprint-plan.md`
10. `docs/phase-0-workbook-validation.md`

Also inspect:

```text
outputs/gulmi-coffee-erp-phase-0/gulmi-coffee-erp-phase-0-workbook.xlsx
```

The workbook is the Phase-0 operational prototype and sample data reference.

## 3. Build Scope

Build only Phase 1:

- authentication
- users and roles
- farmer master
- storage locations
- lot master
- procurement receipt
- QIR-B summary
- QIR-B readings
- bag register
- storage movement
- environment logs
- exception log
- inventory ledger
- audit log
- internal QR resolver
- basic dashboards
- Phase-1 reports

## 4. Do Not Build Yet

Do not build these in Phase 1:

- hulling
- green batch resting
- grading
- roasting
- packaging
- sales order
- customer CRM
- farmer payments
- full costing engine
- public coffee story QR page
- Metabase BI
- SMS/WhatsApp
- Odoo/accounting integration

These are later phases.

Scope creep will make Phase 1 fail.

## 5. Recommended Stack

Use:

```text
Backend: Django + Django REST Framework
Frontend: React + TypeScript PWA
Database: PostgreSQL 16
Deployment: Docker Compose
Reverse proxy: Nginx
```

Alternative backend such as NestJS is acceptable only if approved before development starts.

## 6. Core Rules You Must Enforce

1. Every activity creates a document row.
2. Posted records are immutable.
3. Draft records may be edited.
4. Corrections use exception/adjustment records.
5. Inventory is derived only from `inventory_ledger`.
6. Cost/rate/payment/margin fields are Admin/Manager-only.
7. QR responses are role-aware.
8. Staff see readable codes.
9. UUIDs are used internally.
10. Audit events are created by the server.

## 7. Sensitive Data Rule

Sensitive fields:

- `rate_npr`
- `total_npr`
- payment amounts
- cost
- margin
- profit

Allowed roles:

- Admin
- Manager

Forbidden:

- hiding sensitive fields only in frontend

Required:

- filter sensitive fields in backend serializer/API response
- test this with Quality, Storage, and Viewer roles

## 8. QIR-B Rules

QIR-B must enforce:

- minimum 5 readings before posting
- readings include moisture, density, bean temperature
- average and standard deviation calculation
- moisture SD > 0.70 triggers retake
- density SD > 50 triggers retake
- parchment moisture > 12.5 triggers hold
- parchment moisture 11.6 to 12.5 triggers monitor
- density < 300 triggers retake

Expected yield:

```text
70 + (avg_density / 50) - 0.5 * (avg_moisture - 11)
```

## 9. QR Rule

QR resolver:

```text
/r/{uuid_or_code}
```

Logged-in users:

- internal traceability page

Public visitor:

- Phase-1 safe placeholder response

Public response must not include:

- cost
- rate
- farmer payment
- internal defects
- internal exception notes
- yield percentage

## 10. Required Demo Flow

Every serious demo should show this complete flow:

1. Login as Admin.
2. Create farmer.
3. Create lot.
4. Create procurement.
5. Post procurement.
6. Login as Quality.
7. Create QIR-B for lot.
8. Enter 5 readings.
9. Calculate QIR-B.
10. Post QIR-B.
11. Login as Storage.
12. Create two bags from approved QIR-B.
13. Print QR for each bag.
14. Move bag to storage rack.
15. Enter environment log.
16. Scan bag QR.
17. Confirm full traceability page.
18. Login as Viewer.
19. Confirm cost fields are hidden.
20. Login as Manager.
21. Confirm audit log contains post, print QR, and scan QR events.

## 11. Required Deliverables

Developer must deliver:

- source code
- database migrations
- seed data
- API docs
- frontend app
- deployment instructions
- `.env.example`
- backup script
- restore instructions
- test report
- staging deployment
- production deployment package
- short user manual

## 12. Sprint Plan

Follow:

```text
docs/phase-1-developer-task-breakdown-sprint-plan.md
```

Summary:

- Sprint 0: setup and architecture
- Sprint 1: users, roles, audit, storage locations
- Sprint 2: farmers, lots, procurement
- Sprint 3: QIR-B
- Sprint 4: bags, QR, inventory ledger
- Sprint 5: storage, environment, exceptions
- Sprint 6: traceability, reports, audit, QA
- Sprint 7: pilot, deployment, go-live

## 13. Acceptance Gates

Phase 1 is not accepted until:

- QIR-B rules pass
- sensitive field tests pass
- posted record lock tests pass
- bag creation rules pass
- inventory ledger tests pass
- QR traceability tests pass
- audit event tests pass
- backup restore test passes
- pilot batch succeeds

Go/no-go checklist:

```text
docs/phase-1-testing-qa-specification.md
```

## 14. Owner Review Process

At the end of each sprint, developer must provide:

```text
Completed:
- ...

Demo:
- ...

Tests passed:
- ...

Blocked:
- ...

Owner decisions needed:
- ...

Next sprint:
- ...
```

Owner should reject vague status like:

```text
Almost done
Mostly working
Need small fixes
```

Owner should ask:

- Can you demo it?
- Which acceptance criteria passed?
- Which tests failed?
- Is sensitive data protected?
- Are posted records locked?
- Is this inside Phase-1 scope?

## 15. Final Definition Of Done

Phase 1 is complete only when:

```text
A real bag in storage can be scanned and traced back to farmer, lot, procurement, QIR-B readings, QIR-B decision, storage location, movement history, inventory ledger, exceptions, and audit events, with sensitive cost data visible only to Admin/Manager, and the system can be restored from backup.
```

