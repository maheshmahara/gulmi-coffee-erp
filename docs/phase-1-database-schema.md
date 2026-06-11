# Phase-1 Database Schema

## 1. Purpose

This document defines the PostgreSQL schema for the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 traceability chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The schema is designed to support:

- immutable posted documents
- readable business codes
- UUID primary keys
- QIR-B quality rules
- bag-level traceability
- storage movement history
- inventory ledger truth
- audit history
- role-based sensitive field protection

## 2. Recommended Database

```text
PostgreSQL 16
```

Recommended UUID approach:

- Use application-generated UUIDv7 if available.
- Otherwise use PostgreSQL UUID with app-side readable code sequence.

The business must never depend on raw UUIDs in daily operation. Staff use readable `code` values.

## 3. Naming Conventions

Table names:

```text
snake_case singular or document-style table names
```

Recommended examples:

- `app_user`
- `farmer`
- `lot`
- `procurement`
- `qirb_summary`
- `qirb_reading`
- `bag`
- `storage_location`
- `storage_movement`
- `environment_log`
- `exception_log`
- `inventory_ledger`
- `audit_event`

Common readable codes:

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

## 4. Common Columns

Major master/document tables should include:

```sql
id UUID PRIMARY KEY,
code TEXT UNIQUE NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
created_by UUID REFERENCES app_user(id),
updated_at TIMESTAMPTZ,
updated_by UUID REFERENCES app_user(id),
status TEXT NOT NULL
```

Posted document tables should also include:

```sql
posted_at TIMESTAMPTZ,
posted_by UUID REFERENCES app_user(id)
```

## 5. Enum Values

These may be implemented as PostgreSQL enums, lookup tables, or Django choices. For MVP speed, Django choices with database check constraints are acceptable.

### user_role

```text
admin
manager
quality
storage
production
sales
viewer
```

### farmer_type

```text
farmer
collector
cooperative
supplier
```

### item_type

```text
fresh_cherry
dry_cherry
parchment
green_bean
roasted_bean
```

### lot_status

```text
draft
received
quality_pending
approved
hold
bagged
closed
```

### document_status

```text
draft
posted
cancelled
adjusted
```

### qirb_decision

```text
approved
monitor
hold
retake
```

### bag_status

```text
in_storage
on_hold
moved
consumed
lost
closed
```

### location_type

```text
warehouse
rack
drying_area
hold_area
production_area
finished_goods
```

### movement_type

```text
receive_to_storage
transfer
move_to_drying
return_from_drying
move_to_hulling
hold
release
adjustment
```

### environment_risk_flag

```text
dry_risk
ideal
monitor
risk
critical
```

### exception_status

```text
open
approved
resolved
cancelled
```

### exception_severity

```text
low
medium
high
critical
```

## 6. Tables

## 6.1 app_user

Stores staff and system users.

```sql
CREATE TABLE app_user (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  phone TEXT,
  role TEXT NOT NULL CHECK (role IN (
    'admin', 'manager', 'quality', 'storage', 'production', 'sales', 'viewer'
  )),
  password_hash TEXT,
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_app_user_role ON app_user(role);
CREATE INDEX idx_app_user_active ON app_user(active);
```

## 6.2 farmer

Stores farmers, collectors, cooperatives, and suppliers.

```sql
CREATE TABLE farmer (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  farmer_name TEXT NOT NULL,
  father_or_family_name TEXT,
  phone TEXT,
  village TEXT NOT NULL,
  municipality TEXT,
  district TEXT NOT NULL,
  ward_no TEXT,
  gps_location TEXT,
  photo_url TEXT,
  bank_or_wallet TEXT,
  farmer_type TEXT NOT NULL CHECK (farmer_type IN (
    'farmer', 'collector', 'cooperative', 'supplier'
  )),
  active BOOLEAN NOT NULL DEFAULT true,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_farmer_name ON farmer(farmer_name);
CREATE INDEX idx_farmer_phone ON farmer(phone);
CREATE INDEX idx_farmer_village ON farmer(village);
CREATE INDEX idx_farmer_active ON farmer(active);
```

## 6.3 storage_location

Stores warehouses, racks, drying areas, hold areas, and production areas.

```sql
CREATE TABLE storage_location (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  location_name TEXT NOT NULL,
  location_type TEXT NOT NULL CHECK (location_type IN (
    'warehouse', 'rack', 'drying_area', 'hold_area', 'production_area', 'finished_goods'
  )),
  parent_location_id UUID REFERENCES storage_location(id),
  active BOOLEAN NOT NULL DEFAULT true,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_storage_location_type ON storage_location(location_type);
CREATE INDEX idx_storage_location_parent ON storage_location(parent_location_id);
CREATE INDEX idx_storage_location_active ON storage_location(active);
```

## 6.4 lot

Represents one source batch from one farmer/collector.

```sql
CREATE TABLE lot (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  farmer_id UUID NOT NULL REFERENCES farmer(id),
  item_type TEXT NOT NULL CHECK (item_type IN (
    'fresh_cherry', 'dry_cherry', 'parchment', 'green_bean'
  )),
  harvest_year INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN (
    'draft', 'received', 'quality_pending', 'approved', 'hold', 'bagged', 'closed'
  )),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_lot_farmer ON lot(farmer_id);
CREATE INDEX idx_lot_item_type ON lot(item_type);
CREATE INDEX idx_lot_status ON lot(status);
CREATE INDEX idx_lot_harvest_year ON lot(harvest_year);
```

## 6.5 procurement

Records coffee received and purchase quantity/value.

```sql
CREATE TABLE procurement (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  lot_id UUID NOT NULL REFERENCES lot(id),
  farmer_id UUID NOT NULL REFERENCES farmer(id),
  item_type TEXT NOT NULL CHECK (item_type IN (
    'fresh_cherry', 'dry_cherry', 'parchment', 'green_bean'
  )),
  gross_kg NUMERIC(12,3) NOT NULL CHECK (gross_kg > 0),
  tare_kg NUMERIC(12,3) NOT NULL DEFAULT 0 CHECK (tare_kg >= 0),
  net_kg NUMERIC(12,3) GENERATED ALWAYS AS (gross_kg - tare_kg) STORED,
  rate_npr NUMERIC(12,2),
  total_npr NUMERIC(14,2) GENERATED ALWAYS AS ((gross_kg - tare_kg) * rate_npr) STORED,
  received_at TIMESTAMPTZ NOT NULL,
  received_by UUID REFERENCES app_user(id),
  status TEXT NOT NULL CHECK (status IN ('draft', 'posted', 'cancelled', 'adjusted')),
  posted_at TIMESTAMPTZ,
  posted_by UUID REFERENCES app_user(id),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id),
  CHECK (gross_kg > tare_kg)
);
```

Indexes:

```sql
CREATE INDEX idx_procurement_lot ON procurement(lot_id);
CREATE INDEX idx_procurement_farmer ON procurement(farmer_id);
CREATE INDEX idx_procurement_received_at ON procurement(received_at);
CREATE INDEX idx_procurement_status ON procurement(status);
```

Sensitive columns:

- `rate_npr`
- `total_npr`

Protection:

- API serializers must remove these fields for non-Admin/Manager users.
- Optional PostgreSQL column privileges can be added later.

## 6.6 qirb_summary

Stores calculated quality summary and decision.

```sql
CREATE TABLE qirb_summary (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  subject_type TEXT NOT NULL CHECK (subject_type IN (
    'lot', 'bag', 'green_batch', 'roast_batch'
  )),
  subject_id UUID NOT NULL,
  bean_stage TEXT NOT NULL CHECK (bean_stage IN (
    'fresh_cherry', 'dry_cherry', 'parchment', 'green', 'roasted'
  )),
  reading_count INT NOT NULL DEFAULT 0 CHECK (reading_count >= 0),
  avg_moisture NUMERIC(8,3),
  moisture_sd NUMERIC(8,3),
  avg_density NUMERIC(8,3),
  density_sd NUMERIC(8,3),
  avg_bean_temp NUMERIC(8,3),
  bean_temp_sd NUMERIC(8,3),
  estimated_green_yield_pct NUMERIC(8,3),
  decision TEXT CHECK (decision IN ('approved', 'monitor', 'hold', 'retake')),
  status TEXT NOT NULL CHECK (status IN ('draft', 'posted', 'cancelled')),
  checked_by UUID REFERENCES app_user(id),
  checked_at TIMESTAMPTZ,
  posted_at TIMESTAMPTZ,
  posted_by UUID REFERENCES app_user(id),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_qirb_subject ON qirb_summary(subject_type, subject_id);
CREATE INDEX idx_qirb_decision ON qirb_summary(decision);
CREATE INDEX idx_qirb_status ON qirb_summary(status);
CREATE INDEX idx_qirb_checked_at ON qirb_summary(checked_at);
```

Note:

`subject_id` is polymorphic. For Phase 1, it will mainly reference `lot.id`. Later phases may use `bag`, `green_batch`, and `roast_batch`.

## 6.7 qirb_reading

Stores individual QIR-B readings.

```sql
CREATE TABLE qirb_reading (
  id UUID PRIMARY KEY,
  qirb_id UUID NOT NULL REFERENCES qirb_summary(id) ON DELETE CASCADE,
  sequence_no INT NOT NULL CHECK (sequence_no > 0),
  moisture NUMERIC(8,3) NOT NULL,
  density NUMERIC(8,3) NOT NULL,
  bean_temp NUMERIC(8,3) NOT NULL,
  reading_time TIMESTAMPTZ NOT NULL,
  entered_by UUID REFERENCES app_user(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (qirb_id, sequence_no)
);
```

Indexes:

```sql
CREATE INDEX idx_qirb_reading_qirb ON qirb_reading(qirb_id);
CREATE INDEX idx_qirb_reading_time ON qirb_reading(reading_time);
```

## 6.8 bag

Stores physical bag records.

```sql
CREATE TABLE bag (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  lot_id UUID NOT NULL REFERENCES lot(id),
  qirb_id UUID NOT NULL REFERENCES qirb_summary(id),
  item_type TEXT NOT NULL CHECK (item_type IN (
    'fresh_cherry', 'dry_cherry', 'parchment', 'green_bean', 'roasted_bean'
  )),
  weight_kg NUMERIC(12,3) NOT NULL CHECK (weight_kg > 0),
  bag_type TEXT NOT NULL CHECK (bag_type IN (
    'jute', 'grainpro', 'plastic', 'paper', 'other'
  )),
  current_location_id UUID REFERENCES storage_location(id),
  sealed_at TIMESTAMPTZ,
  status TEXT NOT NULL CHECK (status IN (
    'in_storage', 'on_hold', 'moved', 'consumed', 'lost', 'closed'
  )),
  qr_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  updated_at TIMESTAMPTZ,
  updated_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_bag_lot ON bag(lot_id);
CREATE INDEX idx_bag_qirb ON bag(qirb_id);
CREATE INDEX idx_bag_current_location ON bag(current_location_id);
CREATE INDEX idx_bag_status ON bag(status);
```

Business rule:

- Bag can be created only if linked QIR-B decision is `approved`, or `monitor` with Manager/Admin approval.
- This requires service-layer validation or a trigger.

## 6.9 storage_movement

Records movement of bags between locations.

```sql
CREATE TABLE storage_movement (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  bag_id UUID NOT NULL REFERENCES bag(id),
  from_location_id UUID REFERENCES storage_location(id),
  to_location_id UUID NOT NULL REFERENCES storage_location(id),
  movement_type TEXT NOT NULL CHECK (movement_type IN (
    'receive_to_storage', 'transfer', 'move_to_drying', 'return_from_drying',
    'move_to_hulling', 'hold', 'release', 'adjustment'
  )),
  moved_at TIMESTAMPTZ NOT NULL,
  moved_by UUID REFERENCES app_user(id),
  reason TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_storage_movement_bag ON storage_movement(bag_id);
CREATE INDEX idx_storage_movement_to_location ON storage_movement(to_location_id);
CREATE INDEX idx_storage_movement_moved_at ON storage_movement(moved_at);
```

Business rule:

- After movement is posted, update `bag.current_location_id`.
- Keep the movement row immutable.

## 6.10 environment_log

Records room/area conditions.

```sql
CREATE TABLE environment_log (
  id UUID PRIMARY KEY,
  location_id UUID NOT NULL REFERENCES storage_location(id),
  temperature_c NUMERIC(8,2) NOT NULL,
  humidity_pct NUMERIC(8,2) NOT NULL CHECK (humidity_pct >= 0 AND humidity_pct <= 100),
  ac_status TEXT CHECK (ac_status IN ('on', 'off', 'not_available')),
  exhaust_status TEXT CHECK (exhaust_status IN ('on', 'off', 'not_available')),
  risk_flag TEXT NOT NULL CHECK (risk_flag IN (
    'dry_risk', 'ideal', 'monitor', 'risk', 'critical'
  )),
  logged_at TIMESTAMPTZ NOT NULL,
  logged_by UUID REFERENCES app_user(id),
  remarks TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id)
);
```

Indexes:

```sql
CREATE INDEX idx_environment_log_location ON environment_log(location_id);
CREATE INDEX idx_environment_log_logged_at ON environment_log(logged_at);
CREATE INDEX idx_environment_log_risk ON environment_log(risk_flag);
```

Risk logic:

```text
humidity < 45 -> dry_risk
humidity 45-49 -> monitor
humidity 50-60 -> ideal
humidity 61-65 -> monitor
humidity 66-70 -> risk
humidity > 70 -> critical
```

## 6.11 exception_log

Records quality, storage, override, and operational exceptions.

```sql
CREATE TABLE exception_log (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  subject_type TEXT NOT NULL CHECK (subject_type IN (
    'lot', 'bag', 'qirb', 'storage_location', 'hulling_batch',
    'green_batch', 'roast_batch', 'package', 'inventory'
  )),
  subject_id UUID,
  subject_code TEXT,
  exception_type TEXT NOT NULL CHECK (exception_type IN (
    'high_moisture', 'low_density', 'qirb_retake', 'storage_humidity',
    'manual_override', 'inventory_mismatch', 'damaged_bag', 'aging_stock', 'other'
  )),
  severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  reason TEXT NOT NULL,
  action_taken TEXT,
  raised_by UUID REFERENCES app_user(id),
  approved_by UUID REFERENCES app_user(id),
  status TEXT NOT NULL CHECK (status IN ('open', 'approved', 'resolved', 'cancelled')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  resolved_at TIMESTAMPTZ,
  notes TEXT
);
```

Indexes:

```sql
CREATE INDEX idx_exception_subject ON exception_log(subject_type, subject_id);
CREATE INDEX idx_exception_status ON exception_log(status);
CREATE INDEX idx_exception_severity ON exception_log(severity);
CREATE INDEX idx_exception_created_at ON exception_log(created_at);
```

## 6.12 inventory_ledger

The source of truth for stock movements.

```sql
CREATE TABLE inventory_ledger (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  item_type TEXT NOT NULL CHECK (item_type IN (
    'lot', 'bag', 'green_batch', 'roast_batch', 'package', 'husk', 'defect', 'dust'
  )),
  item_id UUID,
  item_code TEXT NOT NULL,
  location_id UUID REFERENCES storage_location(id),
  qty_delta NUMERIC(12,3) NOT NULL,
  uom TEXT NOT NULL CHECK (uom IN ('kg', 'gram', 'unit', 'bag')),
  movement_reason TEXT NOT NULL CHECK (movement_reason IN (
    'procurement_received', 'bag_created', 'storage_transfer', 'drying_loss',
    'hulling_input', 'hulling_output_green', 'hulling_output_husk',
    'hulling_output_defect', 'hulling_output_dust', 'roast_input', 'roast_output',
    'packaging_output', 'sale', 'count_adjustment', 'damage_loss', 'manual_adjustment'
  )),
  ref_doc_type TEXT NOT NULL,
  ref_doc_id UUID,
  ref_doc_code TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID REFERENCES app_user(id),
  notes TEXT
);
```

Indexes:

```sql
CREATE INDEX idx_inventory_item ON inventory_ledger(item_type, item_id);
CREATE INDEX idx_inventory_item_code ON inventory_ledger(item_code);
CREATE INDEX idx_inventory_location ON inventory_ledger(location_id);
CREATE INDEX idx_inventory_ref_doc ON inventory_ledger(ref_doc_type, ref_doc_id);
CREATE INDEX idx_inventory_created_at ON inventory_ledger(created_at);
```

Current stock view:

```sql
CREATE VIEW current_stock AS
SELECT
  item_type,
  item_id,
  item_code,
  location_id,
  uom,
  SUM(qty_delta) AS qty_on_hand
FROM inventory_ledger
GROUP BY item_type, item_id, item_code, location_id, uom;
```

Business rule:

- Do not update or delete ledger rows.
- Corrections require new ledger rows.

## 6.13 audit_event

Records important system actions.

```sql
CREATE TABLE audit_event (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  table_name TEXT NOT NULL,
  record_id UUID,
  record_code TEXT,
  action TEXT NOT NULL CHECK (action IN (
    'create', 'update_draft', 'post', 'cancel', 'adjust', 'approve', 'reject',
    'login', 'logout', 'export', 'print_qr', 'scan_qr', 'override', 'delete_draft'
  )),
  old_value_json JSONB,
  new_value_json JSONB,
  actor_id UUID REFERENCES app_user(id),
  action_time TIMESTAMPTZ NOT NULL DEFAULT now(),
  ip_address TEXT,
  device_id TEXT,
  notes TEXT
);
```

Indexes:

```sql
CREATE INDEX idx_audit_table_record ON audit_event(table_name, record_id);
CREATE INDEX idx_audit_record_code ON audit_event(record_code);
CREATE INDEX idx_audit_action ON audit_event(action);
CREATE INDEX idx_audit_actor ON audit_event(actor_id);
CREATE INDEX idx_audit_action_time ON audit_event(action_time);
```

## 7. Immutability Strategy

For MVP, enforce immutability in both:

1. service layer
2. database trigger

Tables that should become immutable after posting:

- `procurement`
- `qirb_summary`

Tables that should be append-only:

- `qirb_reading` after QIR-B posting
- `storage_movement`
- `inventory_ledger`
- `audit_event`

Example trigger concept:

```sql
CREATE OR REPLACE FUNCTION prevent_posted_update()
RETURNS trigger AS $$
BEGIN
  IF OLD.status = 'posted' THEN
    RAISE EXCEPTION 'Posted records cannot be updated';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

Apply to document tables:

```sql
CREATE TRIGGER trg_procurement_no_posted_update
BEFORE UPDATE ON procurement
FOR EACH ROW EXECUTE FUNCTION prevent_posted_update();
```

## 8. QIR-B Calculation Strategy

Recommended:

- Store individual readings in `qirb_reading`.
- Calculate summary in backend service.
- Save calculated values to `qirb_summary` when posting.
- Recalculate only while draft.

Calculations:

```text
reading_count = count(readings)
avg_moisture = average(moisture)
moisture_sd = sample standard deviation(moisture)
avg_density = average(density)
density_sd = sample standard deviation(density)
avg_bean_temp = average(bean_temp)
bean_temp_sd = sample standard deviation(bean_temp)
estimated_green_yield_pct = 70 + (avg_density / 50) - 0.5 * (avg_moisture - 11)
```

Decision logic:

```text
If reading_count < 5 -> block posting
If moisture_sd > 0.70 -> retake
If density_sd > 50 -> retake
If avg_density < 300 -> retake
If bean_stage = parchment and avg_moisture > 12.5 -> hold
If bean_stage = parchment and avg_moisture >= 11.6 and avg_moisture <= 12.5 -> monitor
Otherwise -> approved
```

## 9. QR Resolver Data Model

Phase-1 can use bag UUID or bag code:

```text
/r/{uuid_or_code}
```

Recommended resolver behavior:

1. Try match by UUID.
2. If not UUID, match by `bag.code`.
3. If logged-in user exists, return internal traceability.
4. If public user, return restricted safe response.

Phase-1 public response can be minimal:

```text
This is a Gulmi Coffee traceability code. Public coffee story will be available in Phase 2.
```

## 10. Migration Order

Recommended migration sequence:

1. `app_user`
2. `farmer`
3. `storage_location`
4. `lot`
5. `procurement`
6. `qirb_summary`
7. `qirb_reading`
8. `bag`
9. `storage_movement`
10. `environment_log`
11. `exception_log`
12. `inventory_ledger`
13. `audit_event`
14. views such as `current_stock`
15. triggers for immutability

## 11. Seed Data

Initial seed data should include:

### Users

```text
Admin
Manager
Quality
Storage
Viewer
```

### Storage Locations

```text
WH-001 Main Warehouse
RACK-PAR-001 Parchment Rack 1
RACK-GRN-001 Green Bean Rack 1
HOLD-001 Defect/Recheck Area
DRY-001 Solar Drying Area
PROD-HULL-001 Hulling Area
```

## 12. Security Notes

Sensitive data protection must happen in the API:

- Admin and Manager can receive `rate_npr` and `total_npr`.
- Other roles receive null/omitted fields.
- Reports and exports must use the same rule.

Optional advanced database hardening:

- PostgreSQL row-level security
- column privileges
- separate cost table

For MVP, API-level filtering plus tests is mandatory.

## 13. Developer Acceptance Criteria

The database implementation is accepted when:

- All Phase-1 tables exist.
- All unique code constraints exist.
- Required foreign keys exist.
- Check constraints exist for major dropdown fields.
- Procurement `net_kg` and `total_npr` are calculated correctly.
- QIR-B readings are linked to QIR-B summary.
- Current stock view works.
- Posted procurement cannot be edited.
- Inventory ledger rows are append-only by application policy.
- Audit event rows are created for post, print QR, and scan QR actions.
- Sensitive fields are hidden by API serializers for unauthorized roles.

