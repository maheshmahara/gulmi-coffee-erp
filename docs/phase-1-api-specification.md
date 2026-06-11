# Phase-1 API Specification

## 1. Purpose

This document defines the REST API contract for the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 MVP chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The API must enforce:

- role-based permissions
- sensitive field protection
- document posting rules
- QIR-B validation
- bag creation rules
- inventory ledger creation
- audit event creation
- QR traceability behavior

## 2. API Style

Recommended style:

```text
REST JSON API
```

Base path:

```text
/api/v1
```

Example:

```text
GET /api/v1/farmers
POST /api/v1/procurements/{id}/post
GET /api/v1/r/{uuid_or_code}
```

## 3. Authentication

Recommended MVP authentication:

- session auth for web app, or
- JWT access token with refresh token

The API must identify:

- current user
- role
- active/inactive status

Inactive users cannot log in.

## 4. Standard Response Shape

Success response:

```json
{
  "data": {},
  "meta": {}
}
```

List response:

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "page_size": 50,
    "total": 125
  }
}
```

Error response:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "QIR-B requires at least 5 readings before posting.",
    "fields": {
      "reading_count": "Minimum 5 readings required."
    }
  }
}
```

## 5. Standard Error Codes

Use consistent error codes:

```text
AUTH_REQUIRED
PERMISSION_DENIED
NOT_FOUND
VALIDATION_ERROR
POSTED_RECORD_LOCKED
SENSITIVE_FIELD_FORBIDDEN
QIRB_READING_COUNT_LOW
QIRB_DECISION_BLOCKED
BAG_QIRB_NOT_APPROVED
INVENTORY_RULE_VIOLATION
DUPLICATE_CODE
SERVER_ERROR
```

## 6. Role Names

API role values:

```text
admin
manager
quality
storage
production
sales
viewer
```

Phase-1 active roles:

```text
admin
manager
quality
storage
viewer
```

## 7. Sensitive Field Rule

Sensitive fields must be hidden at the API serializer level.

Sensitive fields:

```text
rate_npr
total_npr
payment amounts
cost
margin
profit
```

Allowed roles:

```text
admin
manager
```

For unauthorized users, the API should either omit the field or return `null`.

Recommended:

```json
{
  "rate_npr": null,
  "total_npr": null
}
```

This makes the UI easier to build while still avoiding data leakage.

## 8. Audit Rule

The API must create audit events for:

- login
- logout
- create
- update draft
- post
- approve
- resolve
- export
- print QR
- scan QR
- override
- delete draft

Audit event creation should happen server-side, not from frontend trust.

## 9. Auth Endpoints

## 9.1 Login

```text
POST /api/v1/auth/login
```

Request:

```json
{
  "phone": "98XXXXXXXX",
  "password": "secret"
}
```

Response:

```json
{
  "data": {
    "access_token": "token",
    "refresh_token": "token",
    "user": {
      "id": "uuid",
      "code": "USER-2026-000001",
      "full_name": "Admin User",
      "role": "admin"
    }
  }
}
```

Rules:

- Reject inactive users.
- Create `login` audit event.

## 9.2 Logout

```text
POST /api/v1/auth/logout
```

Rules:

- Create `logout` audit event.

## 9.3 Current User

```text
GET /api/v1/me
```

Response:

```json
{
  "data": {
    "id": "uuid",
    "code": "USER-2026-000001",
    "full_name": "Admin User",
    "role": "admin",
    "active": true
  }
}
```

## 10. Users API

## 10.1 List Users

```text
GET /api/v1/users
```

Allowed:

- admin
- manager read-only optional

Query parameters:

```text
role
active
search
page
page_size
```

## 10.2 Create User

```text
POST /api/v1/users
```

Allowed:

- admin

Request:

```json
{
  "full_name": "Quality User",
  "phone": "98XXXXXXXX",
  "role": "quality",
  "password": "temporary-password",
  "active": true
}
```

Rules:

- Generate readable `code`.
- Create audit event.

## 10.3 Update User

```text
PATCH /api/v1/users/{id}
```

Allowed:

- admin

Rules:

- Can change active status.
- Can change role.
- Create audit event.

## 11. Farmers API

## 11.1 List Farmers

```text
GET /api/v1/farmers
```

Allowed:

- admin
- manager
- quality
- storage
- viewer

Query parameters:

```text
search
village
district
farmer_type
active
page
page_size
```

## 11.2 Create Farmer

```text
POST /api/v1/farmers
```

Allowed:

- admin
- manager

Request:

```json
{
  "farmer_name": "Ram Bahadur",
  "father_or_family_name": "Bahadur Family",
  "phone": "98XXXXXXXX",
  "village": "Tamghas",
  "municipality": "Resunga",
  "district": "Gulmi",
  "ward_no": "4",
  "gps_location": "",
  "photo_url": "",
  "bank_or_wallet": "eSewa/Bank",
  "farmer_type": "farmer",
  "active": true,
  "notes": "Good parchment supplier"
}
```

Response:

```json
{
  "data": {
    "id": "uuid",
    "code": "FARM-2026-000001",
    "farmer_name": "Ram Bahadur"
  }
}
```

Validation:

- `farmer_name` required.
- `village` required.
- `district` required.
- `farmer_type` must be valid.

## 11.3 Get Farmer

```text
GET /api/v1/farmers/{id}
```

Response includes:

- farmer details
- recent lots
- recent procurements
- recent QIR-B summaries

Sensitive procurement fields hidden unless Admin/Manager.

## 11.4 Update Farmer

```text
PATCH /api/v1/farmers/{id}
```

Allowed:

- admin
- manager

Rules:

- Create audit event.

## 12. Storage Locations API

## 12.1 List Locations

```text
GET /api/v1/storage-locations
```

Query parameters:

```text
location_type
active
parent_id
search
```

## 12.2 Create Location

```text
POST /api/v1/storage-locations
```

Allowed:

- admin
- manager

Request:

```json
{
  "location_name": "Parchment Rack 1",
  "location_type": "rack",
  "parent_location_id": "uuid",
  "active": true,
  "notes": "For parchment bags"
}
```

Rules:

- Generate `code`.
- Create audit event.

## 12.3 Update Location

```text
PATCH /api/v1/storage-locations/{id}
```

Allowed:

- admin
- manager

## 13. Lots API

## 13.1 List Lots

```text
GET /api/v1/lots
```

Query parameters:

```text
farmer_id
item_type
status
harvest_year
search
page
page_size
```

## 13.2 Create Lot

```text
POST /api/v1/lots
```

Allowed:

- admin
- manager

Request:

```json
{
  "farmer_id": "uuid",
  "item_type": "parchment",
  "harvest_year": 2026,
  "notes": "First lot from Tamghas"
}
```

Rules:

- Generate `LOT-YYYY-######`.
- Default status: `quality_pending` or `draft` depending on workflow.
- Create audit event.

## 13.3 Get Lot

```text
GET /api/v1/lots/{id}
```

Response includes:

- lot details
- farmer summary
- procurement summary
- QIR-B summaries
- bags

Sensitive fields hidden by role.

## 13.4 Update Lot

```text
PATCH /api/v1/lots/{id}
```

Allowed:

- admin
- manager

Rules:

- Do not allow arbitrary status jumps without workflow action.

## 14. Procurements API

## 14.1 List Procurements

```text
GET /api/v1/procurements
```

Query parameters:

```text
farmer_id
lot_id
item_type
status
received_from
received_to
page
page_size
```

Sensitive field behavior:

Admin/Manager response:

```json
{
  "rate_npr": 1300,
  "total_npr": 910000
}
```

Other roles:

```json
{
  "rate_npr": null,
  "total_npr": null
}
```

## 14.2 Create Procurement

```text
POST /api/v1/procurements
```

Allowed:

- admin
- manager

Request:

```json
{
  "lot_id": "uuid",
  "gross_kg": 705,
  "tare_kg": 5,
  "rate_npr": 1300,
  "received_at": "2026-06-11T09:45:00+05:45",
  "received_by": "uuid",
  "notes": "Received at factory"
}
```

Rules:

- `gross_kg > 0`
- `tare_kg >= 0`
- `gross_kg > tare_kg`
- `net_kg` calculated server/database-side.
- `total_npr` calculated server/database-side.
- Status defaults to `draft`.
- Create audit event.

## 14.3 Get Procurement

```text
GET /api/v1/procurements/{id}
```

## 14.4 Update Draft Procurement

```text
PATCH /api/v1/procurements/{id}
```

Allowed:

- admin
- manager

Rules:

- Allowed only if status is `draft`.
- If status is `posted`, return:

```json
{
  "error": {
    "code": "POSTED_RECORD_LOCKED",
    "message": "Posted procurement cannot be edited."
  }
}
```

## 14.5 Post Procurement

```text
POST /api/v1/procurements/{id}/post
```

Allowed:

- admin
- manager

Rules:

- Validate gross/tare/net.
- Set status to `posted`.
- Set `posted_at`, `posted_by`.
- Update lot status to `quality_pending`.
- Create audit event with action `post`.

## 15. QIR-B API

## 15.1 List QIR-B Summaries

```text
GET /api/v1/qirb
```

Query parameters:

```text
subject_type
subject_id
bean_stage
decision
status
checked_from
checked_to
page
page_size
```

## 15.2 Create QIR-B

```text
POST /api/v1/qirb
```

Allowed:

- admin
- manager
- quality

Request:

```json
{
  "subject_type": "lot",
  "subject_id": "uuid",
  "bean_stage": "parchment",
  "notes": "Initial quality check"
}
```

Rules:

- Generate QIR-B code.
- Status defaults to `draft`.
- Create audit event.

## 15.3 Add QIR-B Reading

```text
POST /api/v1/qirb/{id}/readings
```

Allowed:

- admin
- manager
- quality

Request:

```json
{
  "sequence_no": 1,
  "moisture": 11.2,
  "density": 670,
  "bean_temp": 24.5,
  "reading_time": "2026-06-11T10:00:00+05:45"
}
```

Rules:

- QIR-B must be draft.
- Sequence number unique within QIR-B.
- Moisture, density, bean temperature required.
- Create audit event.

## 15.4 Calculate QIR-B

```text
POST /api/v1/qirb/{id}/calculate
```

Allowed:

- admin
- manager
- quality

Response:

```json
{
  "data": {
    "reading_count": 5,
    "avg_moisture": 11.32,
    "moisture_sd": 0.13,
    "avg_density": 667.2,
    "density_sd": 3.63,
    "avg_bean_temp": 24.58,
    "bean_temp_sd": 0.08,
    "estimated_green_yield_pct": 83.28,
    "decision": "approved"
  }
}
```

Rules:

- May calculate while draft.
- Does not post record.

## 15.5 Post QIR-B

```text
POST /api/v1/qirb/{id}/post
```

Allowed:

- admin
- manager
- quality

Rules:

- Must have at least 5 readings.
- Calculate summary.
- Set decision.
- Set status `posted`.
- Set `posted_at`, `posted_by`.
- If decision is `approved`, update lot status to `approved`.
- If decision is `monitor`, update lot status to `hold` or `approved_with_monitor` if that status is added later.
- If decision is `hold` or `retake`, update lot status to `hold`.
- Create exception log for `hold` or `retake`.
- Create audit event.

If fewer than 5 readings:

```json
{
  "error": {
    "code": "QIRB_READING_COUNT_LOW",
    "message": "QIR-B requires at least 5 readings before posting."
  }
}
```

## 15.6 Get QIR-B Detail

```text
GET /api/v1/qirb/{id}
```

Response includes:

- summary
- readings
- linked subject
- exceptions

## 16. Bags API

## 16.1 List Bags

```text
GET /api/v1/bags
```

Query parameters:

```text
lot_id
qirb_id
item_type
status
location_id
search
page
page_size
```

## 16.2 Create Bag

```text
POST /api/v1/bags
```

Allowed:

- admin
- manager
- storage

Request:

```json
{
  "lot_id": "uuid",
  "qirb_id": "uuid",
  "item_type": "parchment",
  "weight_kg": 60,
  "bag_type": "jute",
  "current_location_id": "uuid",
  "sealed_at": "2026-06-11T11:00:00+05:45",
  "notes": "First bag from lot"
}
```

Rules:

- Linked QIR-B must be posted.
- Linked QIR-B decision must be `approved`, or `monitor` with Manager/Admin approval.
- Reject `hold` or `retake`.
- Generate bag code.
- Generate QR URL.
- Create initial inventory ledger row:

```text
item_type = bag
qty_delta = weight_kg
movement_reason = bag_created
```

- Create audit event.

If QIR-B is not approved:

```json
{
  "error": {
    "code": "BAG_QIRB_NOT_APPROVED",
    "message": "Bag cannot be created from hold or retake QIR-B."
  }
}
```

## 16.3 Bulk Create Bags

```text
POST /api/v1/bags/bulk-create
```

Allowed:

- admin
- manager
- storage

Purpose:

Create many bags from one lot/QIR-B.

Request:

```json
{
  "lot_id": "uuid",
  "qirb_id": "uuid",
  "item_type": "parchment",
  "bag_type": "jute",
  "current_location_id": "uuid",
  "sealed_at": "2026-06-11T11:00:00+05:45",
  "weights_kg": [60, 60, 60, 40]
}
```

Rules:

- Apply same QIR-B validation as single create.
- Each bag gets its own code.
- Each bag gets inventory ledger row.
- Return all created bags.

## 16.4 Get Bag Detail

```text
GET /api/v1/bags/{id}
```

Response includes:

- bag details
- lot
- farmer
- QIR-B summary
- current location
- movement history
- inventory ledger rows
- exceptions

Sensitive fields hidden by role.

## 16.5 Print QR

```text
POST /api/v1/bags/{id}/print-qr
```

Allowed:

- admin
- manager
- storage

Response:

```json
{
  "data": {
    "bag_code": "BAG-2026-000001",
    "qr_url": "https://app.gulmicoffee.com/r/uuid",
    "label_text": "BAG-2026-000001 | Parchment | 60 kg"
  }
}
```

Rules:

- Create audit event `print_qr`.

## 17. Storage Movements API

## 17.1 List Movements

```text
GET /api/v1/storage-movements
```

Query parameters:

```text
bag_id
from_location_id
to_location_id
movement_type
moved_from
moved_to
page
page_size
```

## 17.2 Create Movement

```text
POST /api/v1/storage-movements
```

Allowed:

- admin
- manager
- storage

Request:

```json
{
  "bag_id": "uuid",
  "from_location_id": "uuid",
  "to_location_id": "uuid",
  "movement_type": "transfer",
  "moved_at": "2026-06-12T09:00:00+05:45",
  "reason": "Moved to solar drying",
  "notes": "Moisture monitor lot"
}
```

Rules:

- Bag must exist.
- To location must be active.
- From location should match bag current location unless Manager/Admin override.
- Update bag current location.
- Create audit event.

## 18. Environment Logs API

## 18.1 List Environment Logs

```text
GET /api/v1/environment-logs
```

Query parameters:

```text
location_id
risk_flag
logged_from
logged_to
page
page_size
```

## 18.2 Create Environment Log

```text
POST /api/v1/environment-logs
```

Allowed:

- admin
- manager
- storage

Request:

```json
{
  "location_id": "uuid",
  "temperature_c": 24.5,
  "humidity_pct": 58,
  "ac_status": "off",
  "exhaust_status": "on",
  "logged_at": "2026-06-11T12:00:00+05:45",
  "remarks": "Normal condition"
}
```

Rules:

- Server calculates `risk_flag`.
- If risk_flag is `risk` or `critical`, create exception log.
- Create audit event.

Response:

```json
{
  "data": {
    "risk_flag": "ideal"
  }
}
```

## 19. Exception Log API

## 19.1 List Exceptions

```text
GET /api/v1/exceptions
```

Query parameters:

```text
subject_type
subject_id
exception_type
severity
status
created_from
created_to
page
page_size
```

## 19.2 Create Exception

```text
POST /api/v1/exceptions
```

Allowed:

- admin
- manager
- quality
- storage

Request:

```json
{
  "subject_type": "bag",
  "subject_id": "uuid",
  "exception_type": "damaged_bag",
  "severity": "medium",
  "reason": "Bag torn during movement",
  "action_taken": "Moved to hold area",
  "notes": "Needs rebagging"
}
```

Rules:

- Default status `open`.
- Create audit event.

## 19.3 Approve Exception

```text
POST /api/v1/exceptions/{id}/approve
```

Allowed:

- admin
- manager

Rules:

- Set status `approved`.
- Set approved_by.
- Create audit event.

## 19.4 Resolve Exception

```text
POST /api/v1/exceptions/{id}/resolve
```

Allowed:

- admin
- manager

Request:

```json
{
  "action_taken": "Moved bag to drying area and rechecked moisture."
}
```

Rules:

- Set status `resolved`.
- Set resolved_at.
- Create audit event.

## 20. Inventory Ledger API

## 20.1 List Ledger Rows

```text
GET /api/v1/inventory-ledger
```

Allowed:

- admin
- manager
- storage
- viewer read-only

Query parameters:

```text
item_type
item_id
item_code
location_id
movement_reason
created_from
created_to
page
page_size
```

Rules:

- Ledger rows are read-only through normal UI.
- Manual creation should be disabled in Phase 1 except admin-only adjustment workflow if implemented.

## 20.2 Current Stock

```text
GET /api/v1/inventory/current-stock
```

Response:

```json
{
  "data": [
    {
      "item_type": "bag",
      "item_code": "BAG-2026-000001",
      "location_code": "RACK-PAR-001",
      "qty_on_hand": 60,
      "uom": "kg"
    }
  ]
}
```

## 21. Audit Log API

## 21.1 List Audit Events

```text
GET /api/v1/audit-log
```

Allowed:

- admin
- manager

Query parameters:

```text
table_name
record_code
action
actor_id
action_from
action_to
page
page_size
```

Rules:

- Audit events are read-only.
- No update/delete endpoint.

## 22. QR Resolver API

## 22.1 Resolve QR

```text
GET /api/v1/r/{uuid_or_code}
```

Examples:

```text
GET /api/v1/r/BAG-2026-000001
GET /api/v1/r/018f8c6e-...-uuid
```

Rules:

- Resolve by UUID first.
- If not UUID, resolve by readable bag code.
- Create audit event `scan_qr`.
- If logged in, return internal traceability response.
- If public visitor, return public-safe response.

Internal response:

```json
{
  "data": {
    "view_type": "internal",
    "bag": {},
    "farmer": {},
    "lot": {},
    "procurement": {},
    "qirb": {},
    "movements": [],
    "inventory_ledger": [],
    "exceptions": []
  }
}
```

Public Phase-1 response:

```json
{
  "data": {
    "view_type": "public",
    "message": "This is a Gulmi Coffee traceability code. Public coffee story will be available in Phase 2.",
    "bag_code": "BAG-2026-000001"
  }
}
```

Public response must never include:

- cost
- rate
- farmer payment
- internal defects
- internal exception notes
- yield percentage

## 23. Reports API

## 23.1 Dashboard

```text
GET /api/v1/reports/dashboard
```

Response should be role-aware.

Admin/Manager cards:

- total bags in storage
- total kg in storage
- bags on hold
- QIR-B pending
- QIR-B hold/retake count
- open exceptions
- latest environment risk
- recent storage movements

Quality cards:

- QIR-B pending
- QIR-B hold/retake count
- latest QIR-B results
- open quality exceptions

Storage cards:

- bags in storage
- kg in storage
- bags on hold
- latest environment risk
- recent movements

## 23.2 Bag Traceability Report

```text
GET /api/v1/reports/traceability/bag/{id}
```

Returns the complete internal chain:

- bag
- lot
- farmer
- procurement
- QIR-B summary
- QIR-B readings
- storage movements
- environment logs near storage dates if useful
- inventory ledger rows
- exceptions
- audit events

Sensitive fields hidden unless Admin/Manager.

## 23.3 Procurement By Farmer

```text
GET /api/v1/reports/procurement-by-farmer
```

Query:

```text
farmer_id
date_from
date_to
item_type
```

Sensitive totals hidden unless Admin/Manager.

## 23.4 QIR-B Summary Report

```text
GET /api/v1/reports/qirb-summary
```

Query:

```text
decision
bean_stage
date_from
date_to
```

## 23.5 Bags By Location

```text
GET /api/v1/reports/bags-by-location
```

## 23.6 Environment Risk Report

```text
GET /api/v1/reports/environment-risk
```

## 24. Export Rule

Any endpoint that exports CSV/Excel must:

- respect role-based sensitive field filtering
- create audit event `export`

Suggested export pattern:

```text
GET /api/v1/reports/qirb-summary?export=csv
```

## 25. Posting And Immutability Rules

Posted records:

- cannot be edited
- cannot be deleted
- can only be corrected through adjustment or exception workflow

Affected Phase-1 records:

- procurement
- qirb_summary

Append-only records:

- inventory_ledger
- audit_event
- storage_movement

## 26. API Acceptance Tests

Backend developer must prove these pass:

1. Login creates audit event.
2. Inactive user cannot login.
3. Admin can create farmer.
4. Quality user cannot create procurement.
5. Procurement net kg is calculated from gross minus tare.
6. Viewer cannot see `rate_npr` or `total_npr`.
7. Posted procurement cannot be patched.
8. QIR-B cannot post with fewer than 5 readings.
9. QIR-B with parchment moisture above 12.5 becomes hold.
10. QIR-B with density below 300 becomes retake.
11. Bag cannot be created from hold QIR-B.
12. Bag creation creates inventory ledger row.
13. Storage movement updates bag current location.
14. Environment humidity above 70 creates critical risk and exception.
15. QR scan creates audit event.
16. Public QR response does not include sensitive fields.
17. Admin internal QR response includes allowed financial fields.
18. Non-admin internal QR response hides financial fields.
19. Export creates audit event.
20. Audit log cannot be modified through API.

## 27. Developer Implementation Notes

Recommended Django apps:

```text
accounts
farmers
storage
procurement
quality
bags
inventory
audit
reports
qr
```

Recommended service classes:

```text
CodeGeneratorService
QirbCalculationService
ProcurementPostingService
BagCreationService
StorageMovementService
InventoryLedgerService
AuditService
QrResolverService
SensitiveFieldFilterService
```

Important:

- Do not put all business logic in views.
- Posting actions should use service methods.
- Every service method that changes business state should create audit events.
- Serializers must filter sensitive fields by user role.

