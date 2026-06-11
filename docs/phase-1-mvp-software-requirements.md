# Phase-1 MVP Software Requirements Specification

## 1. Project Summary

Build the first working ERP application for Gulmi Coffee. The MVP must manage the traceability backbone:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The MVP should prove that Gulmi Coffee can receive coffee from a farmer, perform QIR-B quality checks, create physical bag records, move bags into storage, scan QR codes, and see the complete chain history.

## 2. MVP Goal

The MVP is accepted when:

```text
Scanning any bag QR shows farmer, lot, procurement, QIR-B, bag, storage location, storage movement, inventory ledger, and audit history.
```

## 3. Target Users

- Admin
- Manager
- Quality/Lab Technician
- Storage/Warehouse
- Viewer

Production and Sales roles may exist in the user table, but Phase-1 does not need hulling, roasting, packaging, or sales screens.

## 4. Technology Recommendation

Recommended implementation stack:

```text
Backend: Django + Django REST Framework
Frontend: React + TypeScript PWA
Database: PostgreSQL 16
Reporting: SQL views first, Metabase later
QR: server-side resolver
Deployment: Docker Compose on VPS for first production version
```

Reason:

- Django admin can help during early operations.
- PostgreSQL is reliable for audit and traceability.
- React PWA supports tablets and future offline-first workflows.
- Docker Compose is understandable and manageable for a network engineer.

## 5. Core Design Rules

1. Every activity creates a document record.
2. Posted documents are immutable.
3. Draft documents may be edited.
4. Corrections use adjustments or exception records.
5. Inventory is derived only from `Inventory_Ledger`.
6. Financial fields are filtered at API level.
7. QR pages are role-aware.
8. Staff see readable codes.
9. UUIDs are used internally.
10. Audit events are recorded for important actions.

## 6. Roles And Permissions

| Capability | Admin | Manager | Quality | Storage | Viewer |
|---|---:|---:|---:|---:|---:|
| Manage users | Yes | No | No | No | No |
| View farmers | Yes | Yes | Yes | Yes | Yes |
| Create/update farmers | Yes | Yes | No | No | No |
| Create procurement | Yes | Yes | No | No | No |
| View procurement cost/rate | Yes | Yes | No | No | No |
| Enter QIR-B readings | Yes | Yes | Yes | No | No |
| Post QIR-B | Yes | Yes | Yes | No | No |
| Create bags | Yes | Yes | No | Yes | No |
| Move bags | Yes | Yes | No | Yes | No |
| Enter environment logs | Yes | Yes | No | Yes | No |
| Raise exceptions | Yes | Yes | Yes | Yes | No |
| Approve exceptions | Yes | Yes | No | No | No |
| View audit log | Yes | Yes | No | No | No |
| Export sensitive reports | Yes | Yes | No | No | No |

Sensitive fields:

- `rate_npr`
- `total_npr`
- payments
- costs
- margins

These must not be returned by the API to unauthorized users.

## 7. Required Modules

### 7.1 Authentication And Users

Features:

- Login
- Logout
- Current user profile
- Role-based permissions
- Active/inactive user status

Required user fields:

- `id`
- `code`
- `full_name`
- `phone`
- `role`
- `active`
- `created_at`
- `created_by`

### 7.2 Farmer Master

Features:

- Create farmer
- Edit farmer while active
- Deactivate farmer
- Search by code, name, phone, village
- View farmer lots and procurement history

Required farmer fields:

- `id`
- `code`
- `farmer_name`
- `father_or_family_name`
- `phone`
- `village`
- `municipality`
- `district`
- `ward_no`
- `gps_location`
- `photo_url`
- `bank_or_wallet`
- `farmer_type`
- `active`
- `notes`

Validation:

- Farmer code unique.
- Farmer name required.
- Phone required for active farmer.
- Farmer type dropdown: `farmer`, `collector`, `cooperative`, `supplier`.

### 7.3 Storage Locations

Features:

- Create storage locations
- Maintain rack/area hierarchy
- Mark location active/inactive

Required fields:

- `id`
- `code`
- `location_name`
- `location_type`
- `parent_location`
- `active`
- `notes`

Location types:

- `warehouse`
- `rack`
- `drying_area`
- `hold_area`
- `production_area`
- `finished_goods`

### 7.4 Lot Master

Features:

- Create lot from farmer
- Track item type and harvest year
- View linked procurement, QIR-B, and bags

Required fields:

- `id`
- `code`
- `farmer`
- `item_type`
- `harvest_year`
- `status`
- `notes`

Item types:

- `fresh_cherry`
- `dry_cherry`
- `parchment`
- `green_bean`

Statuses:

- `draft`
- `received`
- `quality_pending`
- `approved`
- `hold`
- `bagged`
- `closed`

### 7.5 Procurement Receipt

Features:

- Create procurement receipt against lot
- Enter gross kg and tare kg
- Calculate net kg
- Enter rate only if Admin/Manager
- Calculate total NPR
- Post procurement
- Lock posted procurement

Required fields:

- `id`
- `code`
- `lot`
- `farmer`
- `item_type`
- `gross_kg`
- `tare_kg`
- `net_kg`
- `rate_npr`
- `total_npr`
- `received_at`
- `received_by`
- `status`
- `posted_at`
- `posted_by`

Formulas:

```text
net_kg = gross_kg - tare_kg
total_npr = net_kg * rate_npr
```

Validation:

- Gross kg > 0.
- Tare kg >= 0.
- Net kg > 0.
- Posted procurement cannot be edited.
- Rate and total hidden from non-Admin/Manager users.

### 7.6 QIR-B Quality

Features:

- Create QIR-B summary for a lot.
- Enter minimum 5 readings.
- Calculate averages and standard deviations.
- Calculate expected green yield.
- Auto-suggest decision.
- Post QIR-B.
- Create exception for hold/retake cases.

QIR-B reading fields:

- `id`
- `qirb`
- `sequence_no`
- `moisture`
- `density`
- `bean_temp`
- `reading_time`
- `entered_by`

QIR-B summary fields:

- `id`
- `code`
- `subject_type`
- `subject_id`
- `bean_stage`
- `reading_count`
- `avg_moisture`
- `moisture_sd`
- `avg_density`
- `density_sd`
- `avg_bean_temp`
- `bean_temp_sd`
- `estimated_green_yield_pct`
- `decision`
- `status`
- `checked_by`
- `checked_at`
- `posted_at`

Decision logic:

```text
If reading_count < 5 -> cannot post
If moisture_sd > 0.70 -> retake
If density_sd > 50 -> retake
If avg_density < 300 -> retake
If bean_stage = parchment and avg_moisture > 12.5 -> hold
If bean_stage = parchment and avg_moisture >= 11.6 and avg_moisture <= 12.5 -> monitor
Otherwise -> approved
```

Expected yield:

```text
70 + (avg_density / 50) - 0.5 * (avg_moisture - 11)
```

### 7.7 Bag Register

Features:

- Create bag from approved QIR-B.
- Assign bag code.
- Record weight and bag type.
- Assign initial storage location.
- Generate QR URL.
- Create inventory ledger row.
- Create audit event.

Required fields:

- `id`
- `code`
- `lot`
- `qirb`
- `item_type`
- `weight_kg`
- `bag_type`
- `current_location`
- `sealed_at`
- `status`
- `qr_url`

Validation:

- Linked QIR-B must be `approved`.
- If QIR-B is `monitor`, Manager/Admin approval is required.
- Bags cannot be created from `hold` or `retake` QIR-B.
- Bag weight > 0.
- Total bag weight should be checked against procurement net kg.

### 7.8 Storage Movement

Features:

- Scan/search bag.
- Move bag from one location to another.
- Record movement reason.
- Update bag current location.
- Create audit event.

Required fields:

- `id`
- `code`
- `bag`
- `from_location`
- `to_location`
- `movement_type`
- `moved_at`
- `moved_by`
- `reason`
- `notes`

Movement types:

- `receive_to_storage`
- `transfer`
- `move_to_drying`
- `return_from_drying`
- `move_to_hulling`
- `hold`
- `release`
- `adjustment`

### 7.9 Environment Logs

Features:

- Record temperature and humidity by location.
- Record AC/exhaust status.
- Calculate risk flag.
- Create exception for risk/critical humidity.

Required fields:

- `id`
- `location`
- `temperature_c`
- `humidity_pct`
- `ac_status`
- `exhaust_status`
- `risk_flag`
- `logged_at`
- `logged_by`
- `remarks`

Risk logic:

```text
humidity < 45 -> dry_risk
humidity 45-49 -> monitor
humidity 50-60 -> ideal
humidity 61-65 -> monitor
humidity 66-70 -> risk
humidity > 70 -> critical
```

### 7.10 Exception Log

Features:

- Create exception manually or from QIR-B/environment rule.
- Assign severity.
- Track action taken.
- Manager/Admin can approve or resolve.

Required fields:

- `id`
- `code`
- `subject_type`
- `subject_id`
- `exception_type`
- `severity`
- `reason`
- `action_taken`
- `raised_by`
- `approved_by`
- `status`
- `created_at`
- `resolved_at`

### 7.11 Inventory Ledger

Features:

- Create ledger rows automatically from bag creation and future stock events.
- No manual stock edits.
- Show current stock by summing ledger rows.

Required fields:

- `id`
- `code`
- `item_type`
- `item_id`
- `location`
- `qty_delta`
- `uom`
- `movement_reason`
- `ref_doc_type`
- `ref_doc_id`
- `created_at`
- `created_by`

Phase-1 ledger event:

```text
Bag created -> +weight_kg kg
```

### 7.12 Audit Log

Features:

- Record important system actions.
- Record QR print and scan.
- Record sensitive exports.
- Record posting.

Required fields:

- `id`
- `code`
- `table_name`
- `record_id`
- `record_code`
- `action`
- `old_value_json`
- `new_value_json`
- `actor`
- `action_time`
- `ip_address`
- `device_id`
- `notes`

Actions:

- `create`
- `update_draft`
- `post`
- `cancel`
- `adjust`
- `approve`
- `reject`
- `login`
- `logout`
- `export`
- `print_qr`
- `scan_qr`
- `override`
- `delete_draft`

## 8. QR Design

Internal bag URL:

```text
https://app.gulmicoffee.com/r/{uuid}
```

During Phase 0/early testing, readable code URLs are acceptable:

```text
https://app.gulmicoffee.com/r/BAG-2026-000001
```

Phase-1 QR behavior:

- If logged in, show internal bag traceability page.
- If not logged in, show a restricted placeholder or public-safe page.

Internal QR page must show:

- Bag code
- Farmer
- Lot
- Procurement summary
- QIR-B summary
- Storage location
- Movement history
- Inventory ledger rows
- Exceptions
- Audit events

Financial fields appear only for Admin/Manager.

## 9. Required Screens

### Admin/Manager

- Login
- Dashboard
- Users
- Farmers
- Storage Locations
- Lots
- Procurements
- QIR-B
- Bags
- Storage Movements
- Environment Logs
- Exceptions
- Inventory Ledger
- Audit Log
- QR Traceability View

### Quality

- Login
- Quality dashboard
- Lot lookup
- QIR-B creation
- QIR-B readings entry
- QIR-B summary
- Exception creation

### Storage

- Login
- Storage dashboard
- Bag lookup
- Bag creation
- QR print/download
- Storage movement
- Environment log
- Exception creation

### Viewer

- Login
- Read-only dashboard
- Read-only traceability view

## 10. Dashboard Requirements

Phase-1 dashboard cards:

- Total bags in storage
- Total kg in storage
- Bags on hold
- QIR-B pending
- QIR-B retake/hold count
- Open exceptions
- Latest environment risk
- Recent storage movements

Role filtering:

- Admin/Manager see all.
- Quality sees QIR-B and exception cards.
- Storage sees bag, movement, and environment cards.
- Viewer sees read-only non-sensitive cards.

## 11. API Endpoints

Minimum API endpoints:

```text
POST   /auth/login
POST   /auth/logout
GET    /me

GET    /users
POST   /users
PATCH  /users/{id}

GET    /farmers
POST   /farmers
GET    /farmers/{id}
PATCH  /farmers/{id}

GET    /storage-locations
POST   /storage-locations
PATCH  /storage-locations/{id}

GET    /lots
POST   /lots
GET    /lots/{id}

GET    /procurements
POST   /procurements
GET    /procurements/{id}
POST   /procurements/{id}/post

GET    /qirb
POST   /qirb
GET    /qirb/{id}
POST   /qirb/{id}/readings
POST   /qirb/{id}/calculate
POST   /qirb/{id}/post

GET    /bags
POST   /bags
GET    /bags/{id}
POST   /bags/{id}/print-qr

GET    /storage-movements
POST   /storage-movements

GET    /environment-logs
POST   /environment-logs

GET    /exceptions
POST   /exceptions
POST   /exceptions/{id}/approve
POST   /exceptions/{id}/resolve

GET    /inventory-ledger
GET    /audit-log

GET    /r/{uuid_or_code}
GET    /reports/dashboard
GET    /reports/traceability/bag/{id}
```

## 12. Database Constraints

Required constraints:

- Codes are unique.
- Gross kg > 0.
- Tare kg >= 0.
- Net kg > 0.
- Bag weight > 0.
- QIR-B reading sequence unique per QIR-B.
- QIR-B cannot post with fewer than 5 readings.
- Bag cannot be created from hold/retake QIR-B.
- Posted procurement cannot be updated.
- Posted QIR-B cannot be updated.
- Inventory ledger rows cannot be edited after creation.

## 13. Offline Requirements

Phase-1 should be designed for offline support, even if full sync is not completed immediately.

Minimum:

- React PWA installable on mobile/tablet.
- Local draft storage for procurement and QIR-B entry.
- Sync queue design documented in code.

Preferred Phase-1:

- Offline procurement drafts.
- Offline QIR-B readings.
- Sync when internet returns.

Sync rule:

```text
Client stores local draft -> server validates on sync -> server returns official UUID/code -> client replaces local ID.
```

## 14. Reports

Phase-1 reports:

- Farmer list
- Procurement by farmer/date
- QIR-B summary report
- Bags by location
- Environment risk report
- Open exception report
- Inventory ledger report
- Bag traceability report

All reports must respect role-based field visibility.

## 15. Testing Requirements

Required tests:

1. Farmer creation works.
2. Duplicate farmer code is rejected.
3. Procurement net kg is calculated correctly.
4. Non-Admin/Manager cannot see `rate_npr` or `total_npr`.
5. QIR-B with fewer than 5 readings cannot post.
6. QIR-B decision becomes `hold` when parchment moisture is above 12.5%.
7. QIR-B decision becomes `monitor` when parchment moisture is between 11.6 and 12.5%.
8. QIR-B decision becomes `retake` when density is below 300.
9. Bag cannot be created from hold/retake QIR-B.
10. Bag creation creates inventory ledger row.
11. Storage movement updates bag current location.
12. Environment humidity above 70 creates critical risk.
13. Posted procurement cannot be edited.
14. QR scan creates audit event.
15. Internal QR page hides cost fields from unauthorized users.

## 16. Phase-1 Acceptance Test Script

Developer must demonstrate:

1. Login as Admin.
2. Create farmer.
3. Create lot.
4. Create procurement receipt.
5. Post procurement.
6. Login as Quality.
7. Create QIR-B for lot.
8. Enter 5 readings.
9. Post QIR-B.
10. Login as Storage.
11. Create two bags from the approved QIR-B.
12. Generate QR for each bag.
13. Move bag to storage rack.
14. Enter environment log.
15. Scan bag QR.
16. Confirm full traceability page displays.
17. Login as Viewer.
18. Confirm sensitive cost fields are hidden.
19. Check inventory ledger.
20. Check audit log.

## 17. Deliverables From Developer

The Phase-1 developer should deliver:

- Source code repository
- Database migrations
- Seed data for roles and sample locations
- API documentation
- Basic user manual
- Test report
- Deployment instructions
- Backup instructions
- Running staging URL
- Production deployment package

## 18. Out Of Scope For Phase 1

Do not build these yet:

- Hulling
- Green batch resting
- Grading
- Roasting
- Packaging
- Sales orders
- Customer CRM
- Farmer payments
- Full costing engine
- BI dashboards beyond basic MVP cards
- SMS/WhatsApp
- Accounting integration

These belong in later phases after the traceability backbone is proven.

