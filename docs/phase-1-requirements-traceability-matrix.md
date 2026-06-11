# Phase-1 Requirements Traceability Matrix

## 1. Purpose

This matrix maps Gulmi Coffee ERP Phase-1 requirements to implementation areas and tests.

Use it during development and acceptance to confirm that important requirements are not missed.

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

## 2. Traceability Matrix

| ID | Requirement | Database | API | UI | Test Evidence | Status |
|---|---|---|---|---|---|---|
| RQ-001 | User can login/logout | `app_user`, `audit_event` | `/auth/login`, `/auth/logout`, `/me` | Login screen | Login/logout API tests, audit event check | Planned |
| RQ-002 | Inactive users cannot login | `app_user.active` | `/auth/login` | Login error state | Inactive user login test | Planned |
| RQ-003 | Role-based navigation | `app_user.role` | `/me` | App navigation | Role UI test | Planned |
| RQ-004 | Admin can manage users | `app_user` | `/users` | Users screen | Permission test | Planned |
| RQ-005 | Farmer can be created | `farmer` | `/farmers` | Farmer form | Farmer creation test | Planned |
| RQ-006 | Farmer code is unique | `farmer.code UNIQUE` | `/farmers` | Farmer form | Duplicate code test | Planned |
| RQ-007 | Storage locations can be created | `storage_location` | `/storage-locations` | Storage location screen | Location CRUD test | Planned |
| RQ-008 | Lot can be created for farmer | `lot.farmer_id` | `/lots` | Lot form | Lot creation test | Planned |
| RQ-009 | Procurement can be created for lot | `procurement` | `/procurements` | Procurement form | Procurement creation test | Planned |
| RQ-010 | Procurement net kg is calculated | `procurement.net_kg` | `/procurements` | Procurement form | Gross 705, tare 5, net 700 test | Planned |
| RQ-011 | Procurement total NPR is calculated | `procurement.total_npr` | `/procurements` | Procurement form | Net 700, rate 1300, total 910000 test | Planned |
| RQ-012 | Posted procurement is locked | `procurement.status`, trigger/service | `/procurements/{id}` | Posted locked view | Posted patch rejection test | Planned |
| RQ-013 | Rate and total hidden from non-admin roles | `procurement.rate_npr`, `total_npr` | serializers/reports | Procurement list/detail | Sensitive field tests for Quality/Storage/Viewer | Planned |
| RQ-014 | QIR-B can be created for lot | `qirb_summary` | `/qirb` | QIR-B wizard | QIR-B creation test | Planned |
| RQ-015 | QIR-B readings can be entered | `qirb_reading` | `/qirb/{id}/readings` | QIR-B readings screen | Reading entry test | Planned |
| RQ-016 | QIR-B requires at least 5 readings | `qirb_reading`, service validation | `/qirb/{id}/post` | QIR-B wizard | 4-reading post blocked test | Planned |
| RQ-017 | QIR-B averages are calculated | `qirb_summary` | `/qirb/{id}/calculate` | QIR-B summary | Calculation test | Planned |
| RQ-018 | QIR-B standard deviations are calculated | `qirb_summary` | `/qirb/{id}/calculate` | QIR-B summary | SD calculation test | Planned |
| RQ-019 | Expected yield is calculated | `qirb_summary.estimated_green_yield_pct` | `/qirb/{id}/calculate` | QIR-B summary | Formula test | Planned |
| RQ-020 | Moisture SD > 0.70 triggers retake | `qirb_summary.decision` | `/qirb/{id}/post` | QIR-B decision | Decision test | Planned |
| RQ-021 | Density SD > 50 triggers retake | `qirb_summary.decision` | `/qirb/{id}/post` | QIR-B decision | Decision test | Planned |
| RQ-022 | Parchment moisture > 12.5 triggers hold | `qirb_summary.decision` | `/qirb/{id}/post` | QIR-B decision | High moisture test | Planned |
| RQ-023 | Parchment moisture 11.6-12.5 triggers monitor | `qirb_summary.decision` | `/qirb/{id}/post` | QIR-B decision | Monitor decision test | Planned |
| RQ-024 | Density < 300 triggers retake | `qirb_summary.decision` | `/qirb/{id}/post` | QIR-B decision | Low density test | Planned |
| RQ-025 | Hold/retake QIR-B creates exception | `exception_log` | `/qirb/{id}/post` | Exception list | Exception auto-create test | Planned |
| RQ-026 | Bag can be created from approved QIR-B | `bag`, `qirb_summary` | `/bags` | Create bag form | Bag approved test | Planned |
| RQ-027 | Bag cannot be created from hold/retake QIR-B | `bag`, service validation | `/bags` | Create bag error | Bag blocked test | Planned |
| RQ-028 | Bulk bag creation works | `bag` | `/bags/bulk-create` | Bulk bag form | Bulk create test | Planned |
| RQ-029 | Bag QR URL is generated | `bag.qr_url` | `/bags`, `/bags/{id}/print-qr` | QR print view | QR generation test | Planned |
| RQ-030 | QR printing creates audit event | `audit_event` | `/bags/{id}/print-qr` | QR print view | Print QR audit test | Planned |
| RQ-031 | Bag creation creates inventory ledger row | `inventory_ledger` | `/bags` | Inventory ledger view | Ledger row test | Planned |
| RQ-032 | Current stock is derived from ledger | `current_stock` view | `/inventory/current-stock` | Current stock view | Stock sum test | Planned |
| RQ-033 | Inventory ledger is append-only | `inventory_ledger` | no edit endpoint | Inventory ledger read-only | Edit blocked test | Planned |
| RQ-034 | Storage movement can be created | `storage_movement` | `/storage-movements` | Move bag form | Movement creation test | Planned |
| RQ-035 | Storage movement updates bag current location | `bag.current_location_id` | `/storage-movements` | Bag detail | Current location test | Planned |
| RQ-036 | Environment log can be created | `environment_log` | `/environment-logs` | Environment log form | Environment creation test | Planned |
| RQ-037 | Humidity risk flag is calculated server-side | `environment_log.risk_flag` | `/environment-logs` | Risk display | Humidity 58/72 tests | Planned |
| RQ-038 | Critical humidity creates exception | `exception_log` | `/environment-logs` | Exception list | Critical humidity test | Planned |
| RQ-039 | Exceptions can be approved/resolved | `exception_log` | `/exceptions/{id}/approve`, `/resolve` | Exception detail | Approval/resolution test | Planned |
| RQ-040 | QR scan resolves bag by code/UUID | `bag` | `/r/{uuid_or_code}` | QR scan screen | QR resolver test | Planned |
| RQ-041 | QR scan creates audit event | `audit_event` | `/r/{uuid_or_code}` | Traceability page | Scan audit test | Planned |
| RQ-042 | Internal QR shows full traceability | multiple tables | `/r/{uuid_or_code}`, reports | Traceability page | Full chain test | Planned |
| RQ-043 | Public QR hides sensitive data | serializers | `/r/{uuid_or_code}` | Public-safe page | Public response test | Planned |
| RQ-044 | Dashboard is role-aware | reports/views | `/reports/dashboard` | Dashboard | Role dashboard test | Planned |
| RQ-045 | Reports respect sensitive field rules | reports/views | `/reports/*` | Report pages | Report permission tests | Planned |
| RQ-046 | Audit log is read-only | `audit_event` | `/audit-log` | Audit log screen | Audit edit blocked test | Planned |
| RQ-047 | Export creates audit event | `audit_event` | report export endpoints | Export buttons | Export audit test | Planned |
| RQ-048 | App supports mobile/tablet workflows | N/A | N/A | responsive PWA | Mobile smoke test | Planned |
| RQ-049 | Backup and restore process works | PostgreSQL backup | N/A | Operations guide | Restore drill evidence | Planned |
| RQ-050 | Pilot batch can be completed | all MVP tables | all MVP APIs | all MVP screens | Pilot batch sign-off | Planned |

## 3. Requirement Status Values

Use these status values during implementation:

```text
Planned
In Progress
Implemented
Tested
Accepted
Deferred
Rejected
```

## 4. Acceptance Evidence

For each requirement, collect one or more:

- automated test result
- QA checklist result
- staging demo
- screenshot
- API response sample
- database record check
- owner sign-off

## 5. Owner Review Rule

Do not accept a requirement as complete unless:

```text
implementation exists + test evidence exists + role permissions are correct
```

For sensitive requirements, test with at least:

- Admin
- Manager
- Quality
- Storage
- Viewer

## 6. Phase-1 Final Traceability Requirement

The most important end-to-end requirement is:

```text
A real bag in storage can be scanned and traced back to farmer, lot, procurement, QIR-B readings, QIR-B decision, storage location, movement history, inventory ledger, exceptions, and audit events, with sensitive cost data visible only to Admin/Manager.
```

