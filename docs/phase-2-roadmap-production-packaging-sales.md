# Phase-2 Roadmap: Production, Packaging, Public QR, And Sales Foundation

## 1. Purpose

This document defines the recommended Phase-2 roadmap after the Phase-1 MVP is accepted.

Phase 1 proves:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

Phase 2 extends the system into factory production and package-level traceability:

```text
Storage Bag -> Hulling -> Green Batch -> Grading -> Roasting -> Packaging -> Public QR -> Sales Foundation
```

## 2. Do Not Start Phase 2 Until

Start Phase 2 only after:

- Phase 1 is used with real coffee
- staff can create farmer/lot/procurement/QIR-B/bag records
- QR scan works reliably
- sensitive fields are protected
- backup restore has been tested
- at least one pilot batch is completed
- owner accepts Phase 1

## 3. Phase-2 Main Goal

Phase 2 is accepted when:

```text
A retail package can be traced internally back to farmer, lot, procurement, QIR-B, bag, hulling batch, green batch, grading, roast batch, and packaging record; public QR shows only safe customer information.
```

## 4. Phase-2 Modules

Phase-2 modules:

1. Hulling
2. Green Batch
3. Green Batch 24-hour Rest
4. Green Quality Check
5. Grading
6. Roasting
7. Roast Input Split
8. Packaging
9. Public QR
10. Expanded Inventory Ledger
11. Basic Sales Foundation

## 5. Hulling Module

Purpose:

Convert parchment/dry cherry input bags into green bean output and by-products.

Inputs:

- bag code
- input kg
- operator
- hulling start/end time

Outputs:

- green bean kg
- husk kg
- broken/defect kg
- dust kg

Required tables:

- `hulling_batch`
- `hulling_input`

Important rules:

- hulling consumes bag stock
- hulling creates green batch stock
- hulling creates husk/defect/dust stock if tracked
- actual yield is calculated
- variance against expected yield is calculated
- large variance creates exception

Key formula:

```text
actual_yield_pct = output_green_kg / input_parchment_kg * 100
variance_pct = actual_yield_pct - expected_yield_pct
```

## 6. Green Batch Module

Purpose:

Create traceable green coffee after hulling.

Required fields:

- green_batch_code
- hulling_batch
- kg
- rest_until
- qirb_id
- status

Status values:

```text
resting
ready
hold
consumed
```

Important rule:

```text
rest_until = hulled_at + 24 hours
```

Roasting is blocked until current time is greater than or equal to `rest_until`.

## 7. Green Quality Check

Purpose:

Perform QIR-B after green batch rest if needed.

Reuse existing QIR-B system:

```text
subject_type = green_batch
bean_stage = green
```

Rules:

- minimum 5 readings
- calculate average moisture/density/temperature
- hold/retake creates exception
- green batch cannot be roasted if on hold

## 8. Grading Module

Purpose:

Record green bean quality and grade after hulling/resting.

Required fields:

- grading_code
- green_batch
- screen_size
- defect_count
- grade
- graded_by
- graded_at

Possible grade values:

```text
specialty
premium
standard
reject
```

Rules:

- grading links to green batch
- reject grade creates exception

## 9. Roasting Module

Purpose:

Convert green coffee into roasted coffee.

Required table:

- `roast_batch`

Required fields:

- roast_batch_code
- roast_profile
- charge_kg
- output_kg
- loss_pct
- roast_level
- roasted_at
- operator
- status

Formula:

```text
loss_pct = (charge_kg - output_kg) / charge_kg * 100
```

Rules:

- output_kg must be less than charge_kg
- roast batch links to one or more green batches through roast input split
- roast loss is calculated
- abnormal loss creates exception

## 10. Roast Input Split

Purpose:

Support one roast using green coffee from one or more green batches while enforcing the Gulmi rule.

Required table:

- `roast_input_split`

Fields:

- roast_batch
- green_batch
- kg

Critical rule:

```text
SUM(kg) per roast_batch <= 1.5 kg
```

Additional rules:

- green batch must be ready
- green batch must not be on hold
- green stock must be available
- inventory ledger decreases green batch stock

## 11. Packaging Module

Purpose:

Convert roasted coffee into saleable retail/wholesale packages.

Required table:

- `package`

Required fields:

- package_code
- roast_batch
- pack_size_g
- units
- roast_date
- expiry_date
- sku
- public_qr_slug
- status

Rules:

- package units create finished goods inventory
- package links to roast batch
- package QR resolves to public-safe page
- internal scan shows full traceability

Example:

```text
PKG-2026-000001
Roast batch: ROAST-2026-000001
Pack size: 250g
Units: 20
SKU: GULMI-250-MEDIUM
```

## 12. Public QR Module

Purpose:

Show customer-safe coffee story.

Public QR may show:

- coffee name
- origin: Gulmi, Nepal
- roast date
- roast level
- flavor notes
- brew guide
- package size
- farmer story if approved
- region story

Public QR must not show:

- cost
- rate
- farmer payment
- yield percentage
- internal defects
- internal exception notes
- exact sensitive supplier data

Recommended URL:

```text
https://app.gulmicoffee.com/r/{uuid}
```

Server decides whether viewer gets:

- internal traceability view
- public story view

## 13. Expanded Inventory Ledger

Phase 2 adds ledger events:

```text
hulling_input
hulling_output_green
hulling_output_husk
hulling_output_defect
hulling_output_dust
roast_input
roast_output
packaging_output
```

Examples:

Bag consumed in hulling:

```text
item_type = bag
qty_delta = -60 kg
movement_reason = hulling_input
```

Green batch created:

```text
item_type = green_batch
qty_delta = +45 kg
movement_reason = hulling_output_green
```

Roast consumes green:

```text
item_type = green_batch
qty_delta = -1.5 kg
movement_reason = roast_input
```

Roast output:

```text
item_type = roast_batch
qty_delta = +1.25 kg
movement_reason = roast_output
```

Package output:

```text
item_type = package
qty_delta = +20 units
movement_reason = packaging_output
```

## 14. Basic Sales Foundation

Phase 2 may include light sales foundation if packaging is stable.

Minimum:

- customer master
- sales order
- sales line
- payment placeholder

Recommended customer types:

```text
retail
cafe
wholesale
export
```

Rules:

- sales line links to package
- sale decreases package inventory
- payment tracking can be simple in Phase 2 or moved to Phase 3

## 15. Phase-2 Database Additions

Tables to add:

- `hulling_batch`
- `hulling_input`
- `green_batch`
- `grading`
- `roast_batch`
- `roast_input_split`
- `package`
- `customer`
- `sales_order`
- `sales_line`
- `payment`, optional

## 16. Phase-2 API Additions

Expected endpoints:

```text
POST /hulling-batches
POST /hulling-batches/{id}/inputs
POST /hulling-batches/{id}/post

GET /green-batches
POST /green-batches/{id}/quality-check

POST /grading

POST /roast-batches
POST /roast-batches/{id}/inputs
POST /roast-batches/{id}/post

POST /packages
GET /packages/{id}

GET /public/coffee/{slug}

POST /customers
POST /sales-orders
POST /sales-orders/{id}/lines
```

## 17. Phase-2 UI Additions

Screens:

- Hulling Batch
- Hulling Input Scan
- Hulling Output
- Green Batch List
- Green Rest Countdown
- Green QIR-B
- Grading
- Roast Batch
- Roast Input Split
- Packaging
- Public QR Preview
- Package Traceability
- Basic Customer
- Basic Sales Order

## 18. Phase-2 Acceptance Test

Developer must demonstrate:

1. Select stored parchment bag.
2. Create hulling batch.
3. Consume input bag.
4. Record green/husk/defect/dust output.
5. Create green batch.
6. Confirm green batch locked for 24 hours.
7. After rest, perform green QIR-B.
8. Grade green batch.
9. Create roast batch.
10. Add roast input split not exceeding 1.5 kg.
11. Record roasted output.
12. Package roasted coffee.
13. Generate public QR.
14. Public QR shows safe customer page.
15. Internal QR shows full chain back to farmer.
16. Inventory ledger explains every stock movement.

## 19. Phase-2 Risks

| Risk | Mitigation |
|---|---|
| Operators bypass 24-hour rest | hard block with manager override and exception |
| Roast input exceeds 1.5 kg | database/service validation |
| Package QR leaks internal data | public allow-list serializer |
| Inventory mismatch | ledger-only stock changes |
| Production workflow too complex | pilot one batch before full use |
| Costing requested too early | keep detailed costing in Phase 3 unless core flow is stable |

## 20. Phase-2 Definition Of Done

Phase 2 is done when:

```text
A retail package can be scanned publicly to show safe customer information, and scanned internally to show complete farmer-to-package traceability including procurement, QIR-B, bag, storage, hulling, green batch, grading, roasting, packaging, and inventory ledger.
```

