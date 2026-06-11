# Phase-1 Developer Task Breakdown And Sprint Plan

## 1. Purpose

This document converts the Gulmi Coffee ERP Phase-1 requirements into sprint-by-sprint implementation tasks.

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

This plan is intended for:

- product owner
- project manager
- backend developer
- frontend developer
- QA/tester
- deployment/support engineer

## 2. Team Assumption

Small practical team:

```text
1 backend developer
1 frontend developer
1 QA/tester, part-time acceptable
Product owner: Gulmi Coffee owner/operator
```

Optional:

- UI designer
- DevOps support

## 3. Sprint Duration

Recommended sprint length:

```text
2 weeks
```

Phase-1 expected duration:

```text
12 to 14 weeks
```

This includes:

- setup
- development
- QA
- pilot
- deployment preparation

## 4. Working Rules

1. Every sprint ends with a demo.
2. Every sprint must update documentation if behavior changes.
3. No feature is complete without tests.
4. Sensitive field hiding must be tested every sprint once procurement exists.
5. Product owner approves workflows using realistic coffee examples.
6. Production deployment happens only after staging acceptance.

## 5. Definition Of Done

A task is done only when:

- code is implemented
- database migration exists if needed
- API endpoint works
- frontend screen works if applicable
- permission rules are enforced
- tests are written or QA checklist is passed
- audit event is created where required
- documentation is updated if behavior changed
- product owner can demo it in staging

## 6. Sprint 0: Project Setup And Architecture

Duration:

```text
2 weeks
```

Goal:

Create the technical foundation.

Backend tasks:

- create backend project
- configure Django + Django REST Framework
- configure PostgreSQL
- configure environment variables
- create base app structure
- add authentication foundation
- add role model/choices
- create code generator service skeleton
- create audit service skeleton
- create health endpoint

Frontend tasks:

- create React + TypeScript project
- configure routing
- create layout shell
- create login page shell
- create role-aware navigation shell
- create API client
- create error handling pattern

DevOps tasks:

- create Docker Compose for local development
- create database container
- create backend container
- create frontend container or dev server
- create `.env.example`
- create README startup instructions

QA tasks:

- verify local setup works
- verify backend health endpoint
- verify frontend loads
- verify database connection

Deliverables:

- running local app
- health endpoint
- login screen shell
- project structure
- local Docker Compose

Acceptance:

```text
Developer can start the full app locally with documented commands.
Backend health endpoint confirms database connection.
Frontend login page loads.
```

Owner review:

- confirm app name
- confirm basic navigation labels
- confirm role names

## 7. Sprint 1: Users, Roles, Audit Foundation, Storage Locations

Duration:

```text
2 weeks
```

Goal:

Create access control and base master data.

Backend tasks:

- implement `app_user`
- implement login/logout/current user
- implement role permissions
- implement audit_event table
- implement audit service
- implement storage_location model/API
- implement code generator for users and locations
- seed default roles/users
- seed default storage locations

Frontend tasks:

- implement login/logout
- implement current user display
- implement role-based navigation
- implement user list/detail, Admin only
- implement storage location list/form
- implement dashboard placeholder by role

QA tasks:

- login success/failure tests
- inactive user cannot login
- Admin can create user
- non-admin cannot create user
- storage location CRUD tests
- audit event created for login/logout/create

Deliverables:

- working login
- role-aware navigation
- user management
- storage location management
- audit foundation

Acceptance:

```text
Admin can create users and locations.
Quality/Storage/Viewer see only allowed navigation.
Login/logout audit events are recorded.
```

Owner review:

- confirm user roles
- confirm default storage locations
- confirm login workflow

## 8. Sprint 2: Farmers, Lots, Procurement

Duration:

```text
2 weeks
```

Goal:

Implement farmer-to-procurement workflow.

Backend tasks:

- implement farmer model/API
- implement lot model/API
- implement procurement model/API
- implement procurement calculations
- implement procurement posting service
- implement posted record lock for procurement
- implement sensitive field filtering for procurement
- create audit events for farmer/lot/procurement actions

Frontend tasks:

- farmer list/detail/form
- lot list/detail/form
- procurement list/detail/form
- procurement post action
- hide cost fields by role
- show posted locked state

QA tasks:

- Admin/Manager can create farmer
- Quality/Storage/Viewer cannot create farmer
- Admin/Manager can create lot
- procurement net kg calculation
- procurement total NPR calculation
- posted procurement cannot edit
- non-admin cannot see rate/total

Deliverables:

- farmer workflow
- lot workflow
- procurement workflow
- sensitive field protection

Acceptance:

```text
Admin creates farmer, lot, procurement, posts procurement, and Viewer cannot see rate_npr or total_npr.
```

Owner review:

- enter one real sample farmer
- enter one sample procurement
- confirm fields match factory process

## 9. Sprint 3: QIR-B Quality Module

Duration:

```text
2 weeks
```

Goal:

Implement QIR-B readings, calculations, decisions, and posting.

Backend tasks:

- implement qirb_summary model/API
- implement qirb_reading model/API
- implement QirbCalculationService
- implement QIR-B decision logic
- implement QIR-B posting service
- block posting with fewer than 5 readings
- create exception for hold/retake
- update lot status based on decision
- audit QIR-B actions

Frontend tasks:

- QIR-B list
- QIR-B detail
- QIR-B wizard
- reading entry table/cards
- calculate summary screen
- decision color display
- post QIR-B action
- exception prompt for hold/retake

QA tasks:

- 4 readings cannot post
- 5 readings can calculate
- approved scenario
- monitor scenario
- hold scenario
- retake scenario
- low density scenario
- exception auto-created for hold/retake

Deliverables:

- complete QIR-B workflow
- quality dashboard cards
- QIR-B tests

Acceptance:

```text
Quality user creates QIR-B, enters 5 readings, sees calculated decision, and posts it. Hold/retake creates exception.
```

Owner review:

- confirm QIR-B field names
- confirm threshold behavior
- confirm decision language is understandable to staff

## 10. Sprint 4: Bags, QR, Inventory Ledger

Duration:

```text
2 weeks
```

Goal:

Turn approved lots into physical bag records with QR and stock ledger.

Backend tasks:

- implement bag model/API
- implement single bag creation
- implement bulk bag creation
- enforce QIR-B approved/monitor rule
- block hold/retake QIR-B
- generate QR URL
- implement inventory_ledger model/API
- create ledger row on bag creation
- create current_stock view/API
- audit bag creation and QR print

Frontend tasks:

- bag list/detail
- create bag form
- bulk create bag form
- QR print view
- inventory ledger view
- current stock view

QA tasks:

- bag created from approved QIR-B
- bag blocked from hold QIR-B
- bulk create creates correct bag count
- inventory ledger row created per bag
- QR URL generated
- print QR audit event created

Deliverables:

- bag register
- QR generation
- inventory ledger
- current stock view

Acceptance:

```text
Storage user creates bags from approved QIR-B, prints QR, and inventory ledger shows +kg for each bag.
```

Owner review:

- confirm bag label data
- test QR scan on phone
- confirm bag split workflow

## 11. Sprint 5: Storage Movement, Environment Logs, Exceptions

Duration:

```text
2 weeks
```

Goal:

Implement storage operations and environmental risk control.

Backend tasks:

- implement storage_movement model/API
- update bag current location on movement
- enforce active destination location
- implement from-location mismatch manager override
- implement environment_log model/API
- calculate humidity risk flag
- auto-create exception for risk/critical
- complete exception API approve/resolve workflow
- audit storage movement/environment/exception actions

Frontend tasks:

- storage movement list/form
- scan/search bag before movement
- environment log list/form
- exception list/detail/form
- approve/resolve exception actions
- storage dashboard cards

QA tasks:

- storage user moves bag
- viewer cannot move bag
- movement updates current location
- humidity 58 is ideal
- humidity 72 is critical
- critical creates exception
- manager can approve/resolve exception

Deliverables:

- storage movement workflow
- environment logging
- exception management
- storage dashboard

Acceptance:

```text
Storage user moves bag, logs environment, critical humidity creates exception, and Manager resolves it.
```

Owner review:

- walk through real warehouse movement
- confirm environment thresholds
- confirm exception workflow

## 12. Sprint 6: Traceability, Reports, Audit, QA Hardening

Duration:

```text
2 weeks
```

Goal:

Complete internal traceability and prepare for pilot.

Backend tasks:

- implement QR resolver
- implement bag traceability report
- implement dashboard report endpoint
- implement procurement by farmer report
- implement QIR-B summary report
- implement bags by location report
- implement environment risk report
- complete audit log API
- export audit events for reports/exports
- tighten sensitive field filtering across reports

Frontend tasks:

- QR scan screen
- internal traceability page
- dashboard cards by role
- report pages
- audit log screen for Admin/Manager
- empty/error states
- mobile layout improvements

QA tasks:

- full happy path
- QR scan as Admin/Storage/Viewer/Public
- sensitive fields hidden in traceability
- reports respect permissions
- audit log read-only
- mobile smoke tests
- backup smoke test with DevOps

Deliverables:

- complete internal traceability
- basic reports
- audit screen
- dashboard
- QA bug fix round

Acceptance:

```text
Scanning a bag QR opens complete traceability from bag to farmer, and sensitive procurement values are visible only to Admin/Manager.
```

Owner review:

- run complete acceptance test script
- approve pilot readiness

## 13. Sprint 7: Pilot, Deployment Preparation, Go-Live

Duration:

```text
2 weeks
```

Goal:

Pilot the MVP with a real batch and prepare production deployment.

Backend tasks:

- fix pilot bugs
- finalize seed data
- finalize backup script
- finalize deployment settings
- finalize migration scripts

Frontend tasks:

- fix pilot UI issues
- improve staff-facing labels
- finalize print labels
- finalize mobile usability issues

DevOps tasks:

- provision staging/production server
- configure DNS
- configure HTTPS
- deploy staging
- deploy production after approval
- configure backups
- perform restore drill
- configure monitoring

QA tasks:

- full regression
- go/no-go checklist
- pilot batch test
- backup restore test
- production smoke test

Deliverables:

- production-ready MVP
- deployed staging
- deployed production
- backup and restore verified
- staff training completed

Acceptance:

```text
One real farmer-to-bag workflow is completed in production, QR traceability works, and backup restore has been tested.
```

Owner review:

- approve go-live
- approve emergency fallback procedure
- approve production QR label format

## 14. Backlog For Later Phases

Do not pull these into Phase 1 unless MVP is complete:

- hulling batch
- green batch
- 24-hour rest lock
- grading
- roasting
- roast input split 1.5 kg
- packaging
- public QR story page
- sales orders
- customer CRM
- farmer payments
- costing engine
- margin dashboard
- Metabase BI
- SMS/WhatsApp
- Odoo/accounting integration

## 15. Product Owner Weekly Review Checklist

Every week, owner should ask:

1. What was completed?
2. What can be demoed?
3. Which acceptance criteria passed?
4. Which tests failed?
5. Are sensitive fields still protected?
6. Are posted records still locked?
7. Are we adding anything outside MVP?
8. What decision is needed from owner?

## 16. Developer Reporting Format

Developer should report each sprint like:

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

## 17. Phase-1 Final Acceptance

Phase 1 is accepted only when:

```text
A real bag in storage can be scanned and traced back to farmer, lot, procurement, QIR-B readings, QIR-B decision, storage location, movement history, inventory ledger, exceptions, and audit events, with sensitive cost data visible only to Admin/Manager.
```

