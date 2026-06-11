# Gulmi Coffee ERP SDLC Record

## Purpose

This repository is being prepared for the Gulmi Coffee ERP project: a custom, single-company ERP for farmer-to-package coffee traceability, quality control, storage, production, costing, sales, QR traceability, and BI.

The project is being guided step by step for a non-developer product owner with a network engineering background. The first goal is to create a disciplined Phase-0 workbook and developer-ready specification before building software.

## Core Traceability Chain

```text
Farmer -> Lot -> Procurement -> QIR-B Quality -> Bag -> Storage -> Hulling -> Green Batch -> Grading -> Roasting -> Packaging -> Sale -> Finance/BI
```

## Non-Negotiable ERP Principles

1. Every real-world activity creates a document record.
2. Posted records are immutable.
3. Corrections happen through adjustment or exception records.
4. Every major record uses both a UUID primary key and a readable business code.
5. Staff use readable codes, not raw UUIDs.
6. Inventory is never edited directly.
7. Stock is derived from inventory ledger rows.
8. Costs, rates, farmer payments, and margin are visible only to Admin and Manager roles.
9. QR pages are role-aware:
   - Logged-in staff see internal traceability.
   - Public visitors see only approved public information.
10. Rural workflows should support offline-first procurement and QR scanning.

## Phase-1 MVP Scope

The MVP is intentionally limited to the traceability backbone:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

MVP modules:

- Users and roles
- Farmer master
- Storage locations
- Lot master
- Procurement receipt
- QIR-B readings and summary
- Bag register
- Storage movement
- Environment logs
- Exception log
- Inventory ledger
- Audit log
- Internal QR scan
- Basic role dashboard

MVP exit test:

```text
Scan any bag QR and see farmer, lot, procurement, QIR-B, bag, storage, and movement history.
```

## Phase-0 Workbook Tabs

The Phase-0 workbook should contain one tab per future database table:

- Farmers
- Users
- Storage_Locations
- Lots
- Procurements
- QIRB_Readings
- QIRB_Summary
- Bags
- Storage_Movements
- Environment_Logs
- Exception_Log
- Inventory_Ledger
- Audit_Log

## Code Format Standard

Readable codes should follow this pattern:

```text
FARM-2026-000001
LOT-2026-000001
PROC-2026-000001
QIRB-2026-000001
BAG-2026-000001
MOVE-2026-000001
EXC-2026-000001
LEDGER-2026-000001
AUDIT-2026-000001
```

Later production modules will add:

```text
HULL-2026-000001
GREEN-2026-000001
GRADE-2026-000001
ROAST-2026-000001
PKG-2026-000001
SALE-2026-000001
PAY-2026-000001
```

## Phase-0 Workbook Color Convention

- Grey: system-generated fields
- Yellow: user-entered fields
- Green: calculated fields
- Red: sensitive Admin/Manager-only fields
- Blue: status/control fields

## QIR-B Rules

- Minimum 5 readings are required before posting.
- Readings include moisture, density, and bean temperature.
- The system calculates average and standard deviation.
- Moisture SD greater than 0.70 triggers retake or hold.
- Density SD greater than 50 g/L triggers retake or hold.
- Parchment moisture greater than 12.5% triggers hold.
- Parchment moisture from 11.6% to 12.5% triggers monitor.
- Density below 300 g/L triggers retake.
- Bag creation is allowed only after approved QIR-B, or manager-approved monitor.

Expected green yield formula:

```text
Expected yield = 70 + (avg_density / 50) - 0.5 * (avg_moisture - 11)
```

## Inventory Rule

Stock must be derived from `Inventory_Ledger`:

```text
current_stock = SUM(qty_delta) grouped by item_code and location_code
```

Examples:

- Bag created: `+60 kg`
- Bag consumed in hulling: `-60 kg`
- Green batch output: `+45 kg`
- Package created: `+10 units`
- Package sold: `-2 units`

## Audit Rule

Every important user/system action should create an `Audit_Log` row:

- create
- update_draft
- post
- cancel
- adjust
- approve
- reject
- login
- logout
- export
- print_qr
- scan_qr
- override
- delete_draft

Posted documents must not be deleted or silently edited.

## Recommended Build Order

1. Phase-0 workbook with validation rules
2. Developer-ready Software Requirements Specification
3. Database schema and ERD
4. API specification
5. UI wireframes
6. MVP software build
7. Pilot using one real coffee batch
8. Production, packaging, sales, costing, and BI modules

## Current Status

As of this record, the project is in Phase 0:

- ERP blueprint understood
- Workflow image reviewed
- CRM module design reviewed
- Accounting/costing workbook reviewed
- MVP scope selected
- Phase-0 workbook table list defined
- Inventory ledger and audit log design defined

## Next Step

Define workbook validation rules:

- dropdown values
- required fields
- formulas
- sensitive fields
- status transitions
- error checks

