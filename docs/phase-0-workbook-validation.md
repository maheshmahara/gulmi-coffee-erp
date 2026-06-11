# Phase-0 Workbook Validation Guide

## Goal

The Phase-0 workbook is the temporary operating system and future database import source for the Gulmi Coffee ERP MVP.

It must be structured like the future ERP:

```text
One sheet = one table
One row = one document or master record
Posted rows are not edited
Corrections use adjustment or exception rows
```

## Workbook Tabs

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

## Color Convention

- Grey: system-generated fields
- Yellow: user-entered fields
- Green: calculated fields
- Red: sensitive Admin/Manager-only fields
- Blue: status/control fields

## Shared Validation Rules

Use these rules across the workbook:

- `*_code` fields must be unique where they identify records.
- `created_at`, `posted_at`, `checked_at`, `moved_at`, and `logged_at` should use a consistent date/time format.
- Status fields must use dropdowns, not free typing.
- Reference fields should match existing readable codes from other sheets.
- Financial fields should be marked sensitive.
- Posted rows should be locked or clearly marked as no-edit.

Recommended date/time format:

```text
yyyy-mm-dd hh:mm
```

## Farmers

Required fields:

- farmer_code
- farmer_name
- phone
- village
- district
- farmer_type
- active_status

Dropdowns:

```text
farmer_type: farmer, collector, cooperative, supplier
active_status: active, inactive
```

Checks:

- `farmer_code` must be unique.
- `phone` should not be blank for active farmers.

## Users

Required fields:

- user_code
- full_name
- phone
- role
- active_status

Dropdowns:

```text
role: Admin, Manager, Quality, Storage, Production, Sales, Viewer
active_status: active, inactive
```

Checks:

- Only Admin and Manager are allowed to view sensitive fields.

## Storage_Locations

Required fields:

- location_code
- location_name
- location_type
- active_status

Dropdowns:

```text
location_type: warehouse, rack, drying_area, hold_area, production_area, finished_goods
active_status: active, inactive
```

Checks:

- `location_code` must be unique.
- `parent_location_code` should be blank only for top-level areas.

## Lots

Required fields:

- lot_code
- farmer_code
- item_type
- harvest_year
- lot_status

Dropdowns:

```text
item_type: fresh_cherry, dry_cherry, parchment, green_bean
lot_status: draft, received, quality_pending, approved, hold, bagged, closed
```

Checks:

- `farmer_code` must exist in Farmers.
- One delivery from one farmer should create one lot.

## Procurements

Required fields:

- procurement_code
- lot_code
- farmer_code
- item_type
- gross_kg
- tare_kg
- net_kg
- received_date
- received_by
- status

Dropdowns:

```text
status: draft, posted, cancelled, adjusted
```

Sensitive fields:

- rate_npr
- total_npr

Formulas:

```text
net_kg = gross_kg - tare_kg
total_npr = net_kg * rate_npr
```

Checks:

- `gross_kg` must be greater than 0.
- `tare_kg` must be greater than or equal to 0.
- `net_kg` must be greater than 0.
- If status is `posted`, do not edit the row.

## QIRB_Readings

Required fields:

- qirb_code
- sequence_no
- moisture
- density
- bean_temp
- reading_time
- entered_by

Checks:

- Each QIR-B must have at least 5 readings before posting summary.
- `sequence_no` should start at 1 and increase by 1.
- `moisture`, `density`, and `bean_temp` must be numeric.

## QIRB_Summary

Required fields:

- qirb_code
- subject_type
- subject_code
- bean_stage
- reading_count
- avg_moisture
- moisture_sd
- avg_density
- density_sd
- avg_bean_temp
- decision
- status
- checked_by

Dropdowns:

```text
subject_type: lot, bag, green_batch, roast_batch
bean_stage: fresh_cherry, dry_cherry, parchment, green, roasted
decision: approved, monitor, hold, retake
status: draft, posted, cancelled
```

Formulas:

```text
reading_count = count readings by qirb_code
avg_moisture = average moisture by qirb_code
moisture_sd = standard deviation of moisture by qirb_code
avg_density = average density by qirb_code
density_sd = standard deviation of density by qirb_code
avg_bean_temp = average bean_temp by qirb_code
estimated_green_yield_pct = 70 + (avg_density / 50) - 0.5 * (avg_moisture - 11)
```

Decision rules:

- If `reading_count < 5`, cannot post.
- If `moisture_sd > 0.70`, decision should be `retake` or `hold`.
- If `density_sd > 50`, decision should be `retake` or `hold`.
- If `bean_stage = parchment` and `avg_moisture > 12.5`, decision should be `hold`.
- If `bean_stage = parchment` and `avg_moisture >= 11.6` and `avg_moisture <= 12.5`, decision should be `monitor`.
- If `avg_density < 300`, decision should be `retake`.
- Otherwise decision may be `approved`.

## Bags

Required fields:

- bag_code
- lot_code
- qirb_code
- item_type
- weight_kg
- bag_type
- current_location_code
- sealed_at
- status
- qr_url

Dropdowns:

```text
item_type: fresh_cherry, dry_cherry, parchment, green_bean, roasted_bean
bag_type: jute, grainpro, plastic, paper, other
status: in_storage, on_hold, moved, consumed, lost, closed
```

Checks:

- `qirb_code` must exist in QIRB_Summary.
- Linked QIR-B decision should be `approved`, or `monitor` with manager approval.
- Total bag weight for a lot should equal procurement `net_kg`, unless explained.

## Storage_Movements

Required fields:

- movement_code
- bag_code
- from_location_code
- to_location_code
- movement_type
- moved_at
- moved_by

Dropdowns:

```text
movement_type: receive_to_storage, transfer, move_to_drying, return_from_drying, move_to_hulling, hold, release, adjustment
```

Checks:

- `bag_code` must exist in Bags.
- `from_location_code` and `to_location_code` must exist in Storage_Locations, except special receiving placeholder if used.
- Bag current location should be derived from latest movement.

## Environment_Logs

Required fields:

- location_code
- temperature_c
- humidity_pct
- risk_flag
- logged_at
- logged_by

Dropdowns:

```text
ac_status: on, off, not_available
exhaust_status: on, off, not_available
risk_flag: dry_risk, ideal, monitor, risk, critical
```

Risk rule:

```text
humidity < 45 = dry_risk
humidity 45-49 = monitor
humidity 50-60 = ideal
humidity 61-65 = monitor
humidity 66-70 = risk
humidity > 70 = critical
```

Checks:

- If risk_flag is `risk` or `critical`, create an Exception_Log row.

## Exception_Log

Required fields:

- exception_code
- subject_type
- subject_code
- exception_type
- severity
- reason
- raised_by
- status
- created_at

Dropdowns:

```text
subject_type: lot, bag, qirb, storage_location, hulling_batch, green_batch, roast_batch, package, inventory
exception_type: high_moisture, low_density, qirb_retake, storage_humidity, manual_override, inventory_mismatch, damaged_bag, aging_stock, other
severity: low, medium, high, critical
status: open, approved, resolved, cancelled
```

Checks:

- High and critical exceptions should require Manager/Admin review.

## Inventory_Ledger

Required fields:

- ledger_code
- item_type
- item_code
- location_code
- qty_delta
- uom
- movement_reason
- ref_doc_type
- ref_doc_code
- created_at
- created_by

Dropdowns:

```text
item_type: lot, bag, green_batch, roast_batch, package, husk, defect, dust
uom: kg, gram, unit, bag
movement_reason: procurement_received, bag_created, storage_transfer, drying_loss, hulling_input, hulling_output_green, hulling_output_husk, hulling_output_defect, hulling_output_dust, roast_input, roast_output, packaging_output, sale, count_adjustment, damage_loss, manual_adjustment
```

Checks:

- Stock is derived from ledger rows.
- Positive `qty_delta` means stock increases.
- Negative `qty_delta` means stock decreases.
- Manual adjustment should create an Exception_Log row.

## Audit_Log

Required fields:

- audit_code
- table_name
- record_code
- action
- actor
- action_time

Dropdowns:

```text
action: create, update_draft, post, cancel, adjust, approve, reject, login, logout, export, print_qr, scan_qr, override, delete_draft
```

Checks:

- Sensitive exports should always create an audit row.
- QR printing and QR scanning should create audit rows.
- Posted document changes should be blocked by policy.

## Phase-0 Acceptance Criteria

The workbook is ready when:

- All tabs exist.
- All headers are present.
- Dropdowns are applied for status/type fields.
- Sensitive fields are marked red.
- Calculated fields are marked green.
- At least one sample farmer-to-bag workflow can be entered.
- Inventory ledger rows explain every stock change.
- Audit log rows explain key actions.
- A non-developer can follow the workflow without guessing field meanings.

