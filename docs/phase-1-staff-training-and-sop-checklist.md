# Phase-1 Staff Training And SOP Checklist

## 1. Purpose

This document defines the staff training plan and operating SOP checklist for the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 workflow:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The system succeeds only if staff use it consistently at the real workflow points.

## 2. Training Principle

Train by role, using one real or realistic coffee batch.

Do not train only by showing screens. Staff should physically follow the process:

```text
receive coffee -> enter data -> test quality -> create bag -> print QR -> move bag -> scan QR
```

## 3. Roles To Train

Phase-1 roles:

- Admin
- Manager
- Quality/Lab Technician
- Storage/Warehouse
- Viewer

## 4. Training Materials Needed

Prepare before training:

- staging ERP URL
- test user accounts
- Phase-0 workbook
- QR label sample
- sample farmer data
- sample lot/procurement data
- moisture/density/temperature sample readings
- storage location list
- emergency paper fallback form

## 5. Admin Training Checklist

Admin must know how to:

- login/logout
- create users
- deactivate users
- assign roles
- create storage locations
- view all dashboards
- view audit log
- view sensitive procurement fields
- export reports
- confirm backups
- approve go-live checklist

Admin must understand:

- non-admin roles cannot see cost/rate/payment data
- posted records are locked
- corrections require exception/adjustment
- user accounts are deactivated, not deleted

Training pass criteria:

```text
Admin can create a user, assign role, view audit log, and confirm sensitive data is hidden from Viewer.
```

## 6. Manager Training Checklist

Manager must know how to:

- create farmer
- create lot
- create procurement
- post procurement
- view QIR-B decisions
- approve/resolve exceptions
- view dashboard
- check sensitive cost fields
- review daily operating status

Manager must understand:

- posting locks documents
- manager approval may be required for monitor/override cases
- exceptions must be resolved, not ignored

Training pass criteria:

```text
Manager can post procurement, approve/resolve an exception, and explain why posted records are locked.
```

## 7. Quality Training Checklist

Quality/Lab Technician must know how to:

- login
- find a lot
- create QIR-B
- enter at least 5 readings
- calculate QIR-B summary
- understand average and standard deviation fields
- understand decisions: approved, monitor, hold, retake
- post QIR-B
- create exception if needed

Quality must understand:

- fewer than 5 readings cannot be posted
- high moisture can put lot on hold
- low density can trigger retake
- QIR-B data affects bagging permission

Training pass criteria:

```text
Quality user can create QIR-B, enter 5 readings, post a decision, and explain why hold/retake blocks bagging.
```

## 8. Storage Training Checklist

Storage/Warehouse staff must know how to:

- login
- search/scan bag
- create bag from approved QIR-B
- bulk create bags
- print QR label
- move bag to storage location
- enter environment log
- report damaged bag or storage issue
- scan QR to view traceability

Storage must understand:

- bag cannot be created from hold/retake QIR-B
- bag current location comes from movements
- humidity risk can create exception
- QR labels must be attached to the correct bag

Training pass criteria:

```text
Storage user can create two bags, print QR, move a bag, log environment, and scan QR to open traceability.
```

## 9. Viewer Training Checklist

Viewer must know how to:

- login
- search farmers/lots/bags
- scan QR
- view traceability
- understand read-only access

Viewer must understand:

- viewer cannot create or edit records
- viewer cannot see cost/rate/payment data

Training pass criteria:

```text
Viewer can scan QR and confirm cost fields are hidden.
```

## 10. Daily SOP

Every operating day:

1. Manager/Admin checks dashboard.
2. Storage logs environment conditions.
3. Quality completes pending QIR-B checks.
4. Storage creates bags only from approved QIR-B.
5. Storage prints and attaches QR labels immediately.
6. Bag movements are entered when they happen.
7. Open exceptions are reviewed before end of day.
8. Backup status is checked.

## 11. Procurement SOP

When coffee is received:

1. Search farmer.
2. Create farmer if not found.
3. Create lot.
4. Enter procurement gross kg and tare kg.
5. Confirm net kg.
6. Enter rate if Admin/Manager.
7. Post procurement.
8. Send lot for QIR-B.

Do not:

- enter one lot for multiple unrelated farmers
- edit posted procurement
- share rate/cost screen with unauthorized staff

## 12. QIR-B SOP

For each QIR-B:

1. Select subject, usually lot in Phase 1.
2. Select bean stage.
3. Enter at least 5 readings.
4. Calculate summary.
5. Review decision.
6. Post QIR-B.
7. If hold/retake, create or confirm exception.

Do not:

- post with fewer than 5 readings
- override high-risk result silently
- create bags before QIR-B approval

## 13. Bagging SOP

After QIR-B approval:

1. Select lot.
2. Select approved QIR-B.
3. Enter bag weight.
4. Select bag type.
5. Select initial storage location.
6. Create bag.
7. Print QR.
8. Attach QR to the correct physical bag.
9. Confirm inventory ledger entry.

Do not:

- reuse bag codes
- attach QR to wrong bag
- create bag from hold/retake QIR-B

## 14. Storage Movement SOP

When moving a bag:

1. Scan/search bag.
2. Confirm current location.
3. Select destination location.
4. Select movement type.
5. Enter reason if needed.
6. Submit movement.
7. Confirm current location updated.

Do not:

- move bags physically without ERP movement
- manually edit bag location

## 15. Environment Log SOP

At least once per operating day:

1. Select storage location.
2. Enter temperature.
3. Enter humidity.
4. Enter AC/exhaust status.
5. Submit log.
6. Review risk flag.
7. If risk/critical, notify Manager.

## 16. Exception SOP

Create exception for:

- high moisture
- low density
- QIR-B retake
- storage humidity risk
- manual override
- damaged bag
- inventory mismatch

Exception must include:

- subject
- reason
- severity
- action taken
- status

Manager/Admin must review high and critical exceptions.

## 17. QR SOP

QR must be printed immediately after bag creation.

Before attaching label:

- confirm bag code
- confirm lot code
- confirm weight
- scan QR once

Do not print QR containing:

- rate
- cost
- farmer payment
- internal defects

## 18. Emergency Paper Fallback SOP

Use only if ERP is unavailable.

Rules:

- use numbered paper forms
- record date/time
- record staff name
- record farmer/lot/weight/QIR-B/bag details
- back-enter into ERP same day if possible
- Manager verifies back-entry

Paper fallback is not a permanent parallel system.

## 19. Training Sign-Off

Use this table during training.

| Staff Name | Role | Training Date | Trainer | Passed | Notes |
|---|---|---|---|---|---|
| TBD | Admin | TBD | TBD | TBD | TBD |
| TBD | Manager | TBD | TBD | TBD | TBD |
| TBD | Quality | TBD | TBD | TBD | TBD |
| TBD | Storage | TBD | TBD | TBD | TBD |
| TBD | Viewer | TBD | TBD | TBD | TBD |

## 20. Go-Live Staff Readiness

Staff are ready when:

- Admin can manage users and audit
- Manager can post procurement and resolve exceptions
- Quality can complete QIR-B
- Storage can create/move/scan bags
- Viewer can view traceability without sensitive data
- everyone understands emergency fallback

