# Project Master Index And Decision Log

## 1. Purpose

This document is the control index for the Gulmi Coffee ERP project.

Use it to track:

- available documents
- project phases
- approved decisions
- pending decisions
- change requests
- owner approvals

## 2. Project Summary

Project:

```text
Gulmi Coffee ERP
```

Business:

```text
Vertically integrated coffee business in Nepal
```

Core traceability chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Hulling -> Green Batch -> Grading -> Roasting -> Packaging -> Sale -> Finance/BI
```

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

## 3. Document Index

## 3.1 Start Here

| Document | Purpose |
|---|---|
| `README.md` | Repository overview |
| `docs/developer-handoff-package.md` | First document for developers/software vendors |
| `docs/owner-step-by-step-execution-checklist.md` | Owner's execution checklist |

## 3.2 Phase 0

| Document/File | Purpose |
|---|---|
| `docs/phase-0-workbook-validation.md` | Phase-0 workbook structure, dropdowns, formulas, and validation |
| `scripts/build_phase0_workbook.mjs` | Script that generates the Phase-0 Excel workbook |
| `outputs/gulmi-coffee-erp-phase-0/gulmi-coffee-erp-phase-0-workbook.xlsx` | Generated Phase-0 workbook prototype |

## 3.3 Phase 1

| Document | Purpose |
|---|---|
| `docs/phase-1-mvp-software-requirements.md` | Phase-1 software requirements |
| `docs/phase-1-database-schema.md` | PostgreSQL database schema |
| `docs/phase-1-api-specification.md` | REST API contract |
| `docs/phase-1-ui-workflow-specification.md` | UI screens and staff workflows |
| `docs/phase-1-testing-qa-specification.md` | QA tests and acceptance criteria |
| `docs/phase-1-deployment-operations-guide.md` | Deployment, backup, monitoring, operations |
| `docs/phase-1-developer-task-breakdown-sprint-plan.md` | Sprint-by-sprint implementation plan |

## 3.4 Later Phases

| Document | Purpose |
|---|---|
| `docs/phase-2-roadmap-production-packaging-sales.md` | Phase-2 roadmap for production, packaging, public QR, and sales foundation |
| `docs/phase-3-roadmap-finance-bi-crm.md` | Phase-3 roadmap for costing, finance, BI, CRM, and accounting export |

## 3.5 General Project Record

| Document | Purpose |
|---|---|
| `docs/gulmi-coffee-erp-sdlc-record.md` | SDLC record, principles, and current status |

## 4. Approved Decisions

| ID | Decision | Status | Notes |
|---|---|---|---|
| D-001 | Phase-1 MVP is farmer-to-bag traceability | Approved | Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR |
| D-002 | Phase 1 excludes hulling, roasting, packaging, sales, and full costing | Approved | These are Phase 2/3 |
| D-003 | Every business activity creates a document record | Approved | Core ERP design rule |
| D-004 | Posted documents are immutable | Approved | Corrections use adjustment/exception records |
| D-005 | Inventory is ledger-derived only | Approved | No direct stock edits |
| D-006 | Costs/rates/payments/margins are Admin/Manager-only | Approved | Must be enforced by API |
| D-007 | QIR-B requires at least 5 readings | Approved | Cannot post below 5 |
| D-008 | QR resolver is role-aware | Approved | Internal vs public response |
| D-009 | Phase-0 workbook will be used as prototype and import reference | Approved | Generated workbook exists |
| D-010 | PostgreSQL is recommended database | Approved | PostgreSQL 16 recommended |
| D-011 | Django + DRF + React PWA is recommended stack | Recommended | Final vendor confirmation still needed |

## 5. Pending Owner Decisions

| ID | Decision Needed | Options | Target Timing |
|---|---|---|---|
| P-001 | Final ERP domain | `app.gulmicoffee.com`, other | Before QR printing |
| P-002 | Final technology stack approval | Django/React/PostgreSQL or alternative | Before developer contract |
| P-003 | Hosting model | VPS, managed app platform, managed database | Before deployment planning |
| P-004 | QR label printing method | normal printer, label printer, external print shop | Before pilot |
| P-005 | First pilot batch | choose farmer/lot/date | Before Phase-1 UAT |
| P-006 | Staff user list | names and roles | Before staging training |
| P-007 | Emergency paper fallback format | numbered pad/template | Before go-live |
| P-008 | Sensitive report export policy | Admin only, Admin+Manager | Before reports |

## 6. Change Request Log

Use this table for scope changes.

| ID | Date | Request | Phase | Decision | Notes |
|---|---|---|---|---|---|
| CR-001 | TBD | TBD | TBD | TBD | TBD |

Decision values:

```text
approved
rejected
deferred
needs review
```

Rule:

Phase-2 or Phase-3 requests should usually be deferred until Phase 1 is accepted.

## 7. Risk Log

| ID | Risk | Impact | Mitigation | Status |
|---|---|---|---|---|
| R-001 | Scope creep before Phase 1 works | High | Use handoff package and sprint plan | Open |
| R-002 | Sensitive cost data leak | High | API-level filtering and QA tests | Open |
| R-003 | Staff bypass ERP | High | QR/receipt process and training | Open |
| R-004 | Weak connectivity | Medium | PWA/offline-ready design | Open |
| R-005 | Backup not restorable | High | Monthly restore drill | Open |
| R-006 | Developer ignores document rules | High | Sprint acceptance gates | Open |
| R-007 | QR domain changes later | High | Decide final domain before printing | Open |

## 8. Phase Gate Checklist

## 8.1 Phase 0 Complete When

- workbook tabs are reviewed
- columns are approved
- validation rules are approved
- sample farmer-to-bag flow is understandable

## 8.2 Phase 1 Complete When

```text
A real bag in storage can be scanned and traced back to farmer, lot, procurement, QIR-B readings, QIR-B decision, storage location, movement history, inventory ledger, exceptions, and audit events, with sensitive cost data visible only to Admin/Manager, and the system can be restored from backup.
```

## 8.3 Phase 2 Complete When

```text
A retail package can be scanned publicly to show safe customer information, and scanned internally to show complete farmer-to-package traceability including procurement, QIR-B, bag, storage, hulling, green batch, grading, roasting, packaging, and inventory ledger.
```

## 8.4 Phase 3 Complete When

```text
Gulmi Coffee can see cost, margin, farmer payable, customer receivable, sales performance, supplier scorecards, and role-based BI reports from real ERP records, with accounting exports and sensitive financial data protected.
```

## 9. Owner Approval Log

Use this during the project.

| ID | Date | Item Approved | Approved By | Notes |
|---|---|---|---|---|
| A-001 | TBD | Phase-1 MVP scope | TBD | TBD |
| A-002 | TBD | Technology stack | TBD | TBD |
| A-003 | TBD | Developer/vendor | TBD | TBD |
| A-004 | TBD | Sprint 0 | TBD | TBD |
| A-005 | TBD | Sprint 1 | TBD | TBD |
| A-006 | TBD | Sprint 2 | TBD | TBD |
| A-007 | TBD | Sprint 3 | TBD | TBD |
| A-008 | TBD | Sprint 4 | TBD | TBD |
| A-009 | TBD | Sprint 5 | TBD | TBD |
| A-010 | TBD | Sprint 6 | TBD | TBD |
| A-011 | TBD | Sprint 7 / Go-live | TBD | TBD |

## 10. Current Next Step

Recommended next action:

```text
Review the Phase-0 workbook and approve or adjust the columns before hiring/building.
```

Then:

```text
Use docs/developer-handoff-package.md to brief developers.
```

