# Phase-1 Testing And QA Specification

## 1. Purpose

This document defines the testing and acceptance process for the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The MVP is not accepted just because screens exist. It is accepted only when the system enforces traceability, quality rules, role permissions, inventory ledger truth, and auditability.

## 2. Testing Goals

The test process must prove:

1. Staff can complete the real farmer-to-bag workflow.
2. QIR-B rules are enforced correctly.
3. Posted documents cannot be silently edited.
4. Sensitive fields are hidden from unauthorized roles.
5. Bag creation is blocked unless QIR-B allows it.
6. Inventory ledger rows explain stock changes.
7. QR scan opens complete internal traceability.
8. Environment risks create alerts/exceptions.
9. Audit events are created for important actions.
10. The MVP works on laptop and mobile/tablet browsers.

## 3. Test Environments

Use three environments:

```text
Development
Staging
Production
```

Testing should happen in staging before production.

Staging must have:

- test users for each role
- sample farmers
- sample storage locations
- sample lots
- sample QIR-B data
- sample bags

## 4. Test Users

Create these test accounts:

| User | Role | Purpose |
|---|---|---|
| Admin Test | admin | full access |
| Manager Test | manager | operational approval |
| Quality Test | quality | QIR-B entry |
| Storage Test | storage | bag and movement workflow |
| Viewer Test | viewer | read-only and sensitive-field checks |

## 5. Test Data

Seed minimum test data:

### Farmers

```text
FARM-2026-000001 Ram Bahadur
FARM-2026-000002 Sita Devi
```

### Storage Locations

```text
WH-001 Main Warehouse
RACK-PAR-001 Parchment Rack 1
RACK-PAR-002 Parchment Rack 2
RACK-GRN-001 Green Bean Rack 1
HOLD-001 Defect/Recheck Area
DRY-001 Solar Drying Area
PROD-HULL-001 Hulling Area
```

### Lots

```text
LOT-2026-000001 parchment, approved scenario
LOT-2026-000002 parchment, high moisture scenario
LOT-2026-000003 parchment, low density scenario
```

## 6. Test Categories

Required categories:

- unit tests
- service/business-rule tests
- API tests
- permission tests
- UI workflow tests
- QR tests
- inventory ledger tests
- audit tests
- mobile/PWA tests
- staging user acceptance tests
- pilot batch test

## 7. Unit Tests

## 7.1 QIR-B Calculation Tests

Test: reading count

```text
Given 5 readings
When summary is calculated
Then reading_count = 5
```

Test: average moisture

```text
Readings: 11.2, 11.4, 11.3, 11.5, 11.2
Expected average moisture: 11.32
```

Test: average density

```text
Readings: 670, 665, 668, 662, 671
Expected average density: 667.2
```

Test: expected yield formula

```text
Formula:
70 + (avg_density / 50) - 0.5 * (avg_moisture - 11)

For avg_density = 667.2 and avg_moisture = 11.32:
Expected yield = 83.284
```

Accept rounded display:

```text
83.28
```

## 7.2 QIR-B Decision Tests

Test: fewer than 5 readings

```text
Given 4 readings
When posting QIR-B
Then posting is blocked
And error code = QIRB_READING_COUNT_LOW
```

Test: moisture SD high

```text
Given moisture_sd > 0.70
When decision is calculated
Then decision = retake
```

Test: density SD high

```text
Given density_sd > 50
When decision is calculated
Then decision = retake
```

Test: parchment high moisture

```text
Given bean_stage = parchment
And avg_moisture > 12.5
Then decision = hold
```

Test: parchment monitor moisture

```text
Given bean_stage = parchment
And avg_moisture >= 11.6
And avg_moisture <= 12.5
Then decision = monitor
```

Test: low density

```text
Given avg_density < 300
Then decision = retake
```

Test: approved case

```text
Given reading_count >= 5
And moisture_sd <= 0.70
And density_sd <= 50
And avg_density >= 300
And parchment avg_moisture < 11.6
Then decision = approved
```

## 7.3 Procurement Calculation Tests

Test: net kg

```text
gross_kg = 705
tare_kg = 5
net_kg must be 700
```

Test: total NPR

```text
net_kg = 700
rate_npr = 1300
total_npr must be 910000
```

Test: invalid gross/tare

```text
gross_kg = 5
tare_kg = 10
Then validation fails
```

## 8. Service/Business-Rule Tests

## 8.1 Posted Document Lock

Test:

```text
Given procurement status = posted
When user tries PATCH /procurements/{id}
Then API returns POSTED_RECORD_LOCKED
```

## 8.2 Bag Creation Rule

Approved QIR-B:

```text
Given QIR-B decision = approved
When storage user creates bag
Then bag is created
And inventory ledger row is created
```

Hold QIR-B:

```text
Given QIR-B decision = hold
When storage user creates bag
Then bag creation is blocked
And error code = BAG_QIRB_NOT_APPROVED
```

Retake QIR-B:

```text
Given QIR-B decision = retake
When storage user creates bag
Then bag creation is blocked
```

Monitor QIR-B:

```text
Given QIR-B decision = monitor
When storage user creates bag without Manager/Admin approval
Then bag creation is blocked
```

## 8.3 Inventory Ledger Rule

Test:

```text
Given a bag of 60 kg is created
Then inventory_ledger has qty_delta = +60
And movement_reason = bag_created
And item_code = bag code
```

Test:

```text
Given inventory ledger row exists
When normal user tries to edit it
Then edit is blocked
```

## 8.4 Environment Risk Rule

Test: ideal humidity

```text
humidity_pct = 58
Then risk_flag = ideal
And no exception is created
```

Test: critical humidity

```text
humidity_pct = 72
Then risk_flag = critical
And exception is created
```

## 9. API Tests

## 9.1 Authentication

Tests:

- valid login succeeds
- invalid login fails
- inactive user cannot login
- logout succeeds
- current user endpoint returns role
- login creates audit event

## 9.2 Farmers

Tests:

- Admin can create farmer
- Manager can create farmer
- Quality cannot create farmer
- Storage cannot create farmer
- Viewer cannot create farmer
- all roles can view farmer list
- duplicate farmer code is rejected

## 9.3 Procurements

Tests:

- Admin can create procurement
- Manager can create procurement
- Quality cannot create procurement
- Storage cannot create procurement
- Viewer cannot create procurement
- net kg is calculated
- total NPR is calculated
- posting sets status to posted
- posted record cannot be edited
- non-Admin/Manager response hides rate and total

## 9.4 QIR-B

Tests:

- Quality can create QIR-B
- Quality can add readings
- Storage cannot add QIR-B readings
- QIR-B cannot post with fewer than 5 readings
- QIR-B calculation returns expected averages
- QIR-B post sets decision
- hold/retake creates exception

## 9.5 Bags

Tests:

- Storage can create bag from approved QIR-B
- Storage cannot create bag from hold QIR-B
- Bag creation creates QR URL
- Bag creation creates inventory ledger row
- Bag print QR creates audit event
- Bulk bag creation creates correct number of bags

## 9.6 Storage Movements

Tests:

- Storage can move bag
- Viewer cannot move bag
- Movement updates bag current location
- Movement creates audit event
- from-location mismatch requires Manager/Admin override

## 9.7 Environment Logs

Tests:

- Storage can create environment log
- risk flag is calculated by server
- humidity above 70 creates exception
- Viewer cannot create environment log

## 9.8 QR Resolver

Tests:

- valid bag code resolves
- valid bag UUID resolves
- unknown code returns not found
- QR scan creates audit event
- logged-in user gets internal response
- public user gets public-safe response
- public response does not expose sensitive fields

## 10. Permission Matrix Tests

Run every sensitive endpoint with every role.

| Action | Admin | Manager | Quality | Storage | Viewer |
|---|---:|---:|---:|---:|---:|
| create farmer | pass | pass | fail | fail | fail |
| create procurement | pass | pass | fail | fail | fail |
| see rate_npr | pass | pass | fail | fail | fail |
| add QIR-B reading | pass | pass | pass | fail | fail |
| create bag | pass | pass | fail | pass | fail |
| move bag | pass | pass | fail | pass | fail |
| create environment log | pass | pass | fail | pass | fail |
| view audit log | pass | pass | fail | fail | fail |

Fail means:

- request denied, or
- sensitive field hidden, depending on action

## 11. UI Workflow Tests

## 11.1 Full Happy Path

Script:

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
12. Create two bags.
13. Print QR for each bag.
14. Move first bag to RACK-PAR-001.
15. Enter environment log.
16. Scan first bag QR.
17. Confirm traceability page.
18. Login as Viewer.
19. Confirm cost fields hidden.
20. Login as Manager.
21. Confirm audit log.

Expected result:

- all steps complete without manual database edits
- traceability page shows full chain
- audit log records key actions

## 11.2 QIR-B Blocked Path

Script:

1. Create QIR-B.
2. Enter only 4 readings.
3. Try to post.

Expected:

- posting blocked
- message says at least 5 readings required

## 11.3 High Moisture Path

Script:

1. Create parchment QIR-B.
2. Enter readings with avg moisture above 12.5.
3. Post QIR-B.

Expected:

- decision = hold
- lot status = hold
- exception created
- bag creation blocked

## 11.4 Storage Risk Path

Script:

1. Login as Storage.
2. Create environment log with humidity 72.

Expected:

- risk flag = critical
- exception created
- dashboard shows risk

## 12. QR Test Cases

Test labels:

- QR for BAG-2026-000001
- QR for BAG-2026-000002

Tests:

1. Scan from logged-in Admin.
2. Scan from logged-in Storage.
3. Scan from logged-in Viewer.
4. Scan from public/incognito browser.
5. Enter bag code manually.
6. Enter invalid code.

Expected:

- internal users see traceability
- public user sees safe response
- invalid code shows not found
- every scan creates audit event

## 13. Mobile/PWA Tests

Devices:

- Android phone
- tablet
- laptop browser

Tests:

- login works
- navigation usable
- QR scan screen opens
- QIR-B readings can be entered
- bag movement can be posted
- environment log can be posted
- forms do not require horizontal scrolling for normal use
- buttons are large enough for touch

## 14. Offline-Ready Tests

If offline draft support is included in Phase 1:

Tests:

- create procurement draft offline
- create QIR-B draft offline
- add readings offline
- show pending sync count
- sync when network returns
- prevent duplicate submission
- show sync failure clearly

If offline draft support is not implemented yet:

Minimum acceptance:

- UI clearly shows network unavailable
- user does not think failed submission succeeded
- no duplicate records are created after retry

## 15. Data Integrity Tests

Run after happy-path workflow:

Check:

- farmer exists
- lot links to farmer
- procurement links to lot and farmer
- QIR-B links to lot
- readings link to QIR-B
- bag links to lot and QIR-B
- movement links to bag
- inventory ledger links to bag
- audit events exist for create/post/print/scan

No orphan records:

- QIR-B reading without QIR-B
- bag without lot
- bag without QIR-B
- movement without bag
- ledger row without item_code

## 16. Security Tests

Test:

- unauthenticated user cannot access internal API
- non-admin cannot view audit log
- non-admin cannot access cost export
- public QR cannot view procurement cost
- public QR cannot view internal exception details
- inactive user cannot login
- user cannot modify another role's permissions unless Admin

## 17. Backup And Restore Test

Before go-live:

1. Create staging database backup.
2. Restore backup to a fresh database.
3. Confirm application starts.
4. Confirm sample traceability page works.

Acceptance:

- restore completed successfully
- no missing tables
- no migration errors
- traceability data intact

## 18. Performance Smoke Tests

MVP target:

- list pages load under 2 seconds with 1,000 records
- bag QR traceability page loads under 3 seconds
- QIR-B calculation returns under 1 second

These are smoke targets, not enterprise-scale benchmarks.

## 19. Bug Severity

### Critical

- data loss
- sensitive cost leak
- posted records editable
- QR traceability broken
- inventory ledger incorrect
- login/security bypass

### High

- QIR-B decision wrong
- bag creation rule bypassed
- environment critical risk not flagged
- audit event missing for key action

### Medium

- dashboard count wrong
- filter issue
- export formatting issue
- mobile layout problem that has workaround

### Low

- spelling
- spacing
- minor visual polish

## 20. Go/No-Go Checklist

Go-live is allowed only if:

- all critical bugs fixed
- all high bugs fixed or formally accepted by owner
- sensitive field tests pass
- QIR-B rules pass
- inventory ledger tests pass
- QR scan tests pass
- posted lock tests pass
- backup restore test passes
- staff pilot workflow succeeds

No-go if:

- non-admin can see rate/total
- posted documents can be edited
- QIR-B can post with fewer than 5 readings
- bag can be created from hold/retake QIR-B
- inventory can be manually changed without ledger
- QR scan cannot show traceability
- backup restore fails

## 21. Pilot Batch Test

Run one real batch in parallel with old process.

Pilot steps:

1. Record farmer.
2. Create lot.
3. Create procurement.
4. Post procurement.
5. Perform QIR-B.
6. Create bags.
7. Print QR.
8. Move to storage.
9. Log environment.
10. Scan QR.
11. Compare ERP data with paper/Excel records.

Pilot acceptance:

- weights match
- farmer matches
- QIR-B readings match
- bag count matches
- storage location matches
- QR traceability works
- staff can operate without developer help

## 22. Final Phase-1 Acceptance

Phase-1 MVP is accepted when:

```text
A real bag in storage can be scanned and traced back to farmer, lot, procurement, QIR-B readings, QIR-B decision, storage location, movement history, inventory ledger, exceptions, and audit events, with sensitive cost data visible only to Admin/Manager.
```

