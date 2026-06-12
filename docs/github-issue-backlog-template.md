# GitHub Issue Backlog Template

## 1. Purpose

Use this document to create GitHub issues for the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The goal is to manage development work in GitHub without losing the business rules.

## 2. Recommended GitHub Labels

Create these labels in GitHub:

```text
phase-1
sprint-0
sprint-1
sprint-2
sprint-3
sprint-4
sprint-5
sprint-6
sprint-7
backend
frontend
database
api
ui
qa
devops
security
documentation
bug
enhancement
blocked
owner-review
accepted
```

Priority labels:

```text
P0-critical
P1-high
P2-medium
P3-low
```

Domain labels:

```text
auth
farmer
procurement
qirb
bag
storage
inventory
audit
qr
reporting
deployment
training
```

## 3. Recommended GitHub Milestones

Create these milestones:

```text
Sprint 0 - Setup and Architecture
Sprint 1 - Users Roles Audit Storage Locations
Sprint 2 - Farmers Lots Procurement
Sprint 3 - QIR-B Quality
Sprint 4 - Bags QR Inventory
Sprint 5 - Storage Environment Exceptions
Sprint 6 - Traceability Reports Audit QA
Sprint 7 - Pilot Deployment Go-Live
Phase 1 Acceptance
Phase 2 Backlog
Phase 3 Backlog
```

## 4. Standard Issue Format

Every issue should use this format:

```markdown
## Goal

What should be achieved?

## Scope

What is included?

## Out Of Scope

What should not be done in this issue?

## Requirements

- ...

## Acceptance Criteria

- [ ] ...
- [ ] ...

## Tests

- [ ] Unit/API/UI test listed
- [ ] Permission test if relevant
- [ ] Sensitive field test if relevant

## Notes

Links to relevant docs.
```

## 5. Sprint 0 Issues

## Issue: Create Backend Project

Labels:

```text
phase-1, sprint-0, backend, api
```

Acceptance:

- [ ] Django project created
- [ ] Django REST Framework configured
- [ ] environment variable loading configured
- [ ] local run command documented
- [ ] health endpoint returns app status

Docs:

- `docs/phase-1-developer-task-breakdown-sprint-plan.md`
- `docs/phase-1-api-specification.md`

## Issue: Create Frontend Project

Labels:

```text
phase-1, sprint-0, frontend, ui
```

Acceptance:

- [ ] React TypeScript project created
- [ ] app shell loads
- [ ] routing configured
- [ ] API client created
- [ ] login page placeholder exists

## Issue: Create Local Docker Compose

Labels:

```text
phase-1, sprint-0, devops
```

Acceptance:

- [ ] backend service defined
- [ ] frontend service or dev server documented
- [ ] PostgreSQL service defined
- [ ] `.env.example` included
- [ ] developer can start stack from documentation

## 6. Sprint 1 Issues

## Issue: Implement Users And Roles

Labels:

```text
phase-1, sprint-1, backend, auth, security
```

Acceptance:

- [ ] `app_user` model exists
- [ ] roles defined
- [ ] active/inactive user supported
- [ ] seed users can be created
- [ ] inactive user cannot login

## Issue: Implement Authentication API

Labels:

```text
phase-1, sprint-1, backend, api, auth
```

Acceptance:

- [ ] `POST /auth/login`
- [ ] `POST /auth/logout`
- [ ] `GET /me`
- [ ] login creates audit event
- [ ] logout creates audit event

## Issue: Implement Role-Based Navigation

Labels:

```text
phase-1, sprint-1, frontend, ui, security
```

Acceptance:

- [ ] Admin sees all Phase-1 nav items
- [ ] Quality sees QIR-B-focused nav
- [ ] Storage sees bag/storage/environment nav
- [ ] Viewer sees read-only nav

## Issue: Implement Storage Locations

Labels:

```text
phase-1, sprint-1, backend, frontend, storage
```

Acceptance:

- [ ] storage location model/API exists
- [ ] storage location list screen exists
- [ ] create/edit location form exists
- [ ] location type dropdown works
- [ ] default storage locations seeded

## 7. Sprint 2 Issues

## Issue: Implement Farmer Master

Labels:

```text
phase-1, sprint-2, backend, frontend, farmer
```

Acceptance:

- [ ] farmer model/API exists
- [ ] farmer list screen exists
- [ ] farmer form exists
- [ ] farmer detail screen exists
- [ ] farmer code is unique

## Issue: Implement Lot Master

Labels:

```text
phase-1, sprint-2, backend, frontend, procurement
```

Acceptance:

- [ ] lot model/API exists
- [ ] lot links to farmer
- [ ] lot list/detail/form exists
- [ ] item type dropdown works
- [ ] lot status displayed

## Issue: Implement Procurement Receipt

Labels:

```text
phase-1, sprint-2, backend, frontend, procurement, security
```

Acceptance:

- [ ] procurement model/API exists
- [ ] gross/tare/net workflow works
- [ ] total NPR calculated
- [ ] posting sets status to posted
- [ ] posted procurement cannot be edited
- [ ] rate/total hidden from non-Admin/Manager

## 8. Sprint 3 Issues

## Issue: Implement QIR-B Models And API

Labels:

```text
phase-1, sprint-3, backend, api, qirb
```

Acceptance:

- [ ] QIR-B summary model exists
- [ ] QIR-B reading model exists
- [ ] readings link to summary
- [ ] sequence number unique per QIR-B
- [ ] APIs match specification

## Issue: Implement QIR-B Calculation Service

Labels:

```text
phase-1, sprint-3, backend, qirb, qa
```

Acceptance:

- [ ] reading count calculated
- [ ] averages calculated
- [ ] standard deviations calculated
- [ ] expected yield calculated
- [ ] decision calculated
- [ ] unit tests exist

## Issue: Implement QIR-B Wizard UI

Labels:

```text
phase-1, sprint-3, frontend, ui, qirb
```

Acceptance:

- [ ] select lot/subject step
- [ ] select bean stage step
- [ ] enter 5 readings step
- [ ] calculate summary step
- [ ] post decision step
- [ ] hold/retake warning shown

## 9. Sprint 4 Issues

## Issue: Implement Bag Register

Labels:

```text
phase-1, sprint-4, backend, frontend, bag
```

Acceptance:

- [ ] bag model/API exists
- [ ] bag can be created from approved QIR-B
- [ ] hold/retake QIR-B blocks bag creation
- [ ] bag list/detail/form exists
- [ ] bag status displayed

## Issue: Implement Bulk Bag Creation

Labels:

```text
phase-1, sprint-4, frontend, backend, bag
```

Acceptance:

- [ ] user enters standard bag weight
- [ ] system previews bag split
- [ ] multiple bags created
- [ ] total weight warning works

## Issue: Implement QR Print

Labels:

```text
phase-1, sprint-4, frontend, backend, qr
```

Acceptance:

- [ ] QR URL generated
- [ ] QR print view exists
- [ ] label includes bag code, lot code, item type, weight
- [ ] print QR creates audit event

## Issue: Implement Inventory Ledger

Labels:

```text
phase-1, sprint-4, backend, frontend, inventory
```

Acceptance:

- [ ] inventory ledger model/API exists
- [ ] bag creation creates ledger row
- [ ] current stock view/API exists
- [ ] ledger is read-only in UI

## 10. Sprint 5 Issues

## Issue: Implement Storage Movements

Labels:

```text
phase-1, sprint-5, backend, frontend, storage
```

Acceptance:

- [ ] storage movement model/API exists
- [ ] move bag form exists
- [ ] movement updates current location
- [ ] movement creates audit event

## Issue: Implement Environment Logs

Labels:

```text
phase-1, sprint-5, backend, frontend, storage
```

Acceptance:

- [ ] environment log model/API exists
- [ ] risk flag calculated server-side
- [ ] humidity 58 = ideal
- [ ] humidity 72 = critical
- [ ] critical creates exception

## Issue: Implement Exception Workflow

Labels:

```text
phase-1, sprint-5, backend, frontend, qa
```

Acceptance:

- [ ] exception model/API exists
- [ ] create exception works
- [ ] approve exception works
- [ ] resolve exception works
- [ ] high/critical visible on dashboard

## 11. Sprint 6 Issues

## Issue: Implement QR Resolver

Labels:

```text
phase-1, sprint-6, backend, frontend, qr
```

Acceptance:

- [ ] resolves by UUID
- [ ] resolves by bag code
- [ ] internal user sees traceability
- [ ] public user sees safe response
- [ ] scan creates audit event

## Issue: Implement Traceability Page

Labels:

```text
phase-1, sprint-6, frontend, reporting, qr
```

Acceptance:

- [ ] shows bag
- [ ] shows farmer
- [ ] shows lot
- [ ] shows procurement
- [ ] shows QIR-B summary/readings
- [ ] shows movement history
- [ ] shows inventory ledger
- [ ] hides sensitive data by role

## Issue: Implement Phase-1 Reports

Labels:

```text
phase-1, sprint-6, backend, frontend, reporting
```

Acceptance:

- [ ] dashboard endpoint/screen exists
- [ ] procurement by farmer report exists
- [ ] QIR-B summary report exists
- [ ] bags by location report exists
- [ ] environment risk report exists
- [ ] exports create audit events

## Issue: QA Hardening

Labels:

```text
phase-1, sprint-6, qa
```

Acceptance:

- [ ] full happy-path test passes
- [ ] permission matrix tests pass
- [ ] QR tests pass
- [ ] sensitive field tests pass
- [ ] mobile smoke tests pass

## 12. Sprint 7 Issues

## Issue: Pilot Batch Test

Labels:

```text
phase-1, sprint-7, qa, owner-review
```

Acceptance:

- [ ] one real batch recorded
- [ ] farmer/lot/procurement/QIR-B/bag/storage data matches reality
- [ ] QR scan works
- [ ] staff can operate without developer help
- [ ] owner signs off

## Issue: Production Deployment

Labels:

```text
phase-1, sprint-7, devops, deployment
```

Acceptance:

- [ ] production server provisioned
- [ ] DNS configured
- [ ] HTTPS configured
- [ ] app deployed
- [ ] production seed data loaded
- [ ] smoke test passes

## Issue: Backup And Restore Drill

Labels:

```text
phase-1, sprint-7, devops, qa
```

Acceptance:

- [ ] backup script works
- [ ] backup stored off-server
- [ ] restore to fresh database works
- [ ] restored app opens traceability page

## 13. Owner Review Issue

Create one issue per sprint:

```text
Owner review: Sprint X
```

Acceptance:

- [ ] demo completed
- [ ] test evidence reviewed
- [ ] open bugs reviewed
- [ ] owner decisions recorded
- [ ] sprint accepted or rejected

## 14. Phase-1 Acceptance Issue

Create final issue:

```text
Phase 1 acceptance: farmer-to-bag traceability MVP
```

Acceptance:

- [ ] real bag QR scan opens full traceability
- [ ] sensitive fields hidden for non-Admin/Manager
- [ ] posted records locked
- [ ] inventory ledger explains stock
- [ ] audit log shows key actions
- [ ] backup restore test passed
- [ ] pilot batch signed off

