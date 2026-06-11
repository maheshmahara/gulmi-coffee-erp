# Owner Step-By-Step Execution Checklist

## 1. Purpose

This checklist is for the Gulmi Coffee owner/operator.

It explains what to do next, in order, to move from planning into actual ERP development, testing, pilot, and go-live.

You do not need to be a software developer to follow this. Treat it like a network deployment project:

```text
requirements -> design -> lab/staging -> test -> pilot -> production -> monitoring
```

## 2. Current Status

Completed planning assets:

- Phase-0 workbook prototype
- Phase-0 validation guide
- Phase-1 software requirements
- Phase-1 database schema
- Phase-1 API specification
- Phase-1 UI/workflow specification
- Phase-1 testing/QA specification
- Phase-1 deployment/operations guide
- Phase-1 developer sprint plan
- Developer handoff package

## 3. Immediate Next Actions

Do these first:

1. Open the Phase-0 workbook.
2. Review every tab name.
3. Review the sample farmer-to-bag workflow.
4. Confirm the columns match your real factory process.
5. Mark missing fields.
6. Confirm storage location names.
7. Confirm QIR-B thresholds.
8. Confirm who should see costs.
9. Decide final ERP domain.
10. Decide whether Phase 1 stack is approved.

Workbook:

```text
outputs/gulmi-coffee-erp-phase-0/gulmi-coffee-erp-phase-0-workbook.xlsx
```

## 4. Owner Decision 1: Approve MVP Scope

Approve this Phase-1 scope:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

Say no to adding these before Phase 1 is working:

- hulling
- roasting
- packaging
- sales
- payments
- full costing
- public QR story
- BI dashboards

Reason:

The traceability backbone must work first.

## 5. Owner Decision 2: Approve Technology Stack

Recommended:

```text
Backend: Django + Django REST Framework
Frontend: React + TypeScript PWA
Database: PostgreSQL 16
Deployment: Docker Compose + Nginx
```

Approve this unless your developer has a strong reason to change.

If developer proposes a different stack, ask:

1. Is it easy to hire future developers for this stack?
2. Does it support PostgreSQL well?
3. Can it enforce role-based API field hiding?
4. Can it support offline-ready PWA workflows?
5. Can it be deployed and backed up simply?

## 6. Owner Decision 3: Choose Domain

Choose final domain before printing real QR labels.

Recommended:

```text
app.gulmicoffee.com
```

QR pattern:

```text
https://app.gulmicoffee.com/r/{uuid}
```

Do not use temporary URLs for permanent QR labels.

## 7. Prepare For Developer Search

Before contacting developers, prepare:

- developer handoff package
- Phase-1 SRS
- database schema
- API spec
- UI workflow spec
- QA spec
- sprint plan
- workbook

Send this first:

```text
docs/developer-handoff-package.md
```

Then tell them to read the documents in the order listed there.

## 8. Questions To Ask Developers

Ask every developer/vendor:

1. Have you built Django + PostgreSQL business apps before?
2. Have you built role-based permissions before?
3. Can you enforce sensitive-field hiding in the backend API?
4. Can you build a React PWA?
5. Can you create Docker Compose deployment?
6. Can you write tests for business rules?
7. Can you provide staging before production?
8. Can you provide database backup and restore scripts?
9. Can you follow the sprint plan instead of inventing scope?
10. Can you demo every sprint?

Reject developers who say:

- "We will decide everything after starting."
- "Testing can be done at the end."
- "Frontend hiding is enough for cost fields."
- "You do not need PostgreSQL."
- "We can build all modules at once quickly."

## 9. Developer Selection Criteria

Choose based on:

- business understanding
- database discipline
- permission/security discipline
- ability to show previous work
- willingness to follow the documents
- clear timeline
- clear deliverables
- test-first mindset
- communication quality

Do not choose only the cheapest quote.

## 10. Contract / Work Order Structure

Structure the work by milestones:

1. Sprint 0 setup
2. Sprint 1 users/roles/storage
3. Sprint 2 farmers/lots/procurement
4. Sprint 3 QIR-B
5. Sprint 4 bags/QR/inventory
6. Sprint 5 storage/environment/exceptions
7. Sprint 6 traceability/reports/audit/QA
8. Sprint 7 pilot/deployment/go-live

Payment should be tied to accepted deliverables, not just time spent.

## 11. Weekly Owner Review Routine

Every week, ask developer:

```text
What is complete?
What can you demo?
What tests passed?
What failed?
What is blocked?
What decision do you need from me?
Is anything outside Phase-1 scope?
```

Ask for proof:

- staging URL
- demo video or live demo
- test results
- git commits
- updated documentation

## 12. Sprint Demo Acceptance

Never accept a sprint based only on screenshots.

Require:

- live demo
- test evidence
- role-based login test
- data saved in database
- audit event if relevant
- no sensitive data leak

For example, for procurement sprint, developer must show:

1. Admin creates procurement.
2. Net kg calculates.
3. Total NPR calculates.
4. Procurement posts.
5. Posted procurement cannot be edited.
6. Viewer cannot see rate or total.

## 13. Red Flags During Development

Stop and review if:

- developer avoids staging demos
- developer says tests will come later
- cost fields are hidden only in UI
- posted records can still be edited
- inventory quantity is manually editable
- QR scan does not create audit event
- database schema does not match docs
- developer starts Phase 2 before Phase 1 works
- no backup plan exists

## 14. Your Role In Each Sprint

## Sprint 0

You confirm:

- stack
- app name
- roles
- local/staging setup works

## Sprint 1

You confirm:

- users
- roles
- storage locations
- login
- audit events

## Sprint 2

You confirm:

- farmer fields
- lot fields
- procurement workflow
- cost visibility
- posted lock

## Sprint 3

You confirm:

- QIR-B readings
- calculations
- threshold decisions
- exceptions

## Sprint 4

You confirm:

- bag creation
- bulk bag creation
- QR label
- inventory ledger

## Sprint 5

You confirm:

- bag movement
- environment log
- humidity risk
- exception approval/resolution

## Sprint 6

You confirm:

- QR traceability page
- dashboards
- reports
- audit log
- mobile usability

## Sprint 7

You confirm:

- staging accepted
- backup restore works
- pilot batch works
- production go-live approved

## 15. Staff Preparation

Before go-live, prepare:

- list of staff users
- role for each staff member
- storage location names
- farmer list
- first pilot lot
- QR label printer or printing method
- emergency paper fallback forms

## 16. Pilot Batch Checklist

Pick one real batch.

Run:

1. Farmer record
2. Lot record
3. Procurement
4. QIR-B
5. Bag creation
6. QR print
7. Storage movement
8. Environment log
9. QR scan
10. Traceability review

Compare ERP against paper/Excel:

- farmer
- lot
- weight
- QIR-B readings
- bag count
- bag weight
- storage location

## 17. Go-Live Checklist

Go live only when:

- final domain works
- HTTPS works
- production users created
- role permissions tested
- backup succeeds
- restore drill succeeds
- pilot batch succeeds
- QR label scan works
- staff trained
- critical/high bugs fixed
- cost fields hidden from non-admin roles
- posted records locked

## 18. After Go-Live Daily Routine

Every day:

- check dashboard
- check open exceptions
- confirm environment log entered
- confirm backup completed
- scan one bag QR randomly
- review bags on hold

## 19. After Go-Live Weekly Routine

Every week:

- review QIR-B hold/retake rate
- review storage movements
- review inventory summary
- review active users
- review backup storage

## 20. When To Start Phase 2

Start Phase 2 only after:

- Phase 1 used successfully for real coffee
- staff can operate without developer help
- QR traceability works consistently
- data is clean
- backup restore has been tested

Phase 2 will add:

- hulling
- green batch
- grading
- roasting
- packaging
- public QR
- inventory expansion

## 21. Your Final Control Rule

Whenever unsure, ask:

```text
Can we scan a real bag and trust the traceability?
```

If the answer is no, keep focus on Phase 1.

