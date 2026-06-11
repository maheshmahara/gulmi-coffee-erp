# Phase-1 UI And Workflow Specification

## 1. Purpose

This document defines the user interface and operational workflows for the Gulmi Coffee ERP Phase-1 MVP.

Phase-1 chain:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

The UI must be simple enough for factory staff and structured enough to enforce traceability rules.

## 2. UI Principles

1. Staff should work with readable codes, not UUIDs.
2. Each workflow should feel like filling a controlled form, not editing a database.
3. Posted documents should look locked.
4. Sensitive financial fields should not appear for unauthorized roles.
5. QR scanning should be available from the main navigation.
6. Mobile/tablet screens must work well for storage and quality users.
7. Dashboards should show daily work and alerts, not decorative charts.
8. Every critical screen should show status clearly.

## 3. Supported Devices

Minimum:

- laptop browser
- tablet browser
- Android phone browser

Recommended frontend:

```text
React + TypeScript PWA
```

PWA expectations:

- installable shortcut on tablet/phone
- responsive layout
- QR scanner-ready layout
- local draft support planned for procurement and QIR-B

## 4. Navigation

Primary navigation items:

- Dashboard
- QR Scan
- Farmers
- Lots
- Procurements
- QIR-B
- Bags
- Storage
- Environment
- Exceptions
- Inventory
- Audit
- Settings

Role-specific visibility:

| Nav Item | Admin | Manager | Quality | Storage | Viewer |
|---|---:|---:|---:|---:|---:|
| Dashboard | Yes | Yes | Yes | Yes | Yes |
| QR Scan | Yes | Yes | Yes | Yes | Yes |
| Farmers | Yes | Yes | View | View | View |
| Lots | Yes | Yes | View | View | View |
| Procurements | Yes | Yes | View no cost | View no cost | View no cost |
| QIR-B | Yes | Yes | Yes | View | View |
| Bags | Yes | Yes | View | Yes | View |
| Storage | Yes | Yes | View | Yes | View |
| Environment | Yes | Yes | View | Yes | View |
| Exceptions | Yes | Yes | Raise/View | Raise/View | View |
| Inventory | Yes | Yes | View | View | View |
| Audit | Yes | Yes | No | No | No |
| Settings | Yes | Limited | No | No | No |

## 5. Login Screen

Purpose:

Authenticate staff and load their role.

Fields:

- phone
- password or PIN

Actions:

- Login
- Forgot password / contact admin

Success:

- redirect to role dashboard

Errors:

- invalid credentials
- inactive user
- network unavailable

Audit:

- successful login creates `login` audit event
- logout creates `logout` audit event

## 6. Dashboard

Purpose:

Show the user's daily operating picture.

## 6.1 Admin/Manager Dashboard

Cards:

- Total bags in storage
- Total kg in storage
- Bags on hold
- QIR-B pending
- QIR-B hold/retake count
- Open exceptions
- Latest environment risk
- Recent storage movements

Tables:

- Recent procurements
- Recent QIR-B summaries
- Recent bags
- Open exceptions

Sensitive cards:

- Procurement value may appear only for Admin/Manager.

## 6.2 Quality Dashboard

Cards:

- QIR-B drafts
- QIR-B pending posting
- Hold/retake results
- Open quality exceptions

Primary action:

- New QIR-B

## 6.3 Storage Dashboard

Cards:

- Bags in storage
- Bags by location
- Bags on hold
- Latest humidity risk
- Recent movements

Primary actions:

- Create bag
- Move bag
- Log environment
- Scan QR

## 6.4 Viewer Dashboard

Read-only:

- total bags
- QIR-B summary count
- recent movements
- open non-sensitive exceptions

No financial values.

## 7. QR Scan Screen

Purpose:

Fast lookup of bag traceability.

Inputs:

- camera scanner
- manual code entry

Accepted values:

- bag QR URL
- bag code
- UUID

Actions:

- Scan
- Search

Results:

- if bag found: open traceability page
- if not found: show not found message

Audit:

- scan creates `scan_qr` audit event

Error states:

- camera permission denied
- invalid QR
- code not found
- network unavailable

## 8. Farmer Screens

## 8.1 Farmer List

Purpose:

Find farmer/collector records.

Columns:

- farmer_code
- farmer_name
- phone
- village
- district
- farmer_type
- active_status

Filters:

- search
- village
- district
- farmer_type
- active_status

Actions:

- Add Farmer
- View Farmer
- Export, Admin/Manager only

## 8.2 Farmer Detail

Sections:

- Basic information
- Contact/location
- Bank/wallet
- Lots
- Procurements
- Notes

Sensitive:

- procurement rates/totals visible only to Admin/Manager

Actions:

- Edit farmer, Admin/Manager
- Deactivate farmer, Admin/Manager
- Create lot for farmer, Admin/Manager

## 8.3 Farmer Form

Fields:

- farmer_name
- father_or_family_name
- phone
- village
- municipality
- district
- ward_no
- gps_location
- photo_url
- bank_or_wallet
- farmer_type
- active
- notes

Validation:

- farmer_name required
- village required
- district required
- farmer_type required

Success:

- show generated farmer code

## 9. Lot Screens

## 9.1 Lot List

Columns:

- lot_code
- farmer_code
- farmer_name
- item_type
- harvest_year
- status
- created_at

Filters:

- farmer
- item_type
- status
- harvest_year

Actions:

- Add Lot
- View Lot

## 9.2 Lot Detail

Sections:

- Lot summary
- Farmer summary
- Procurement
- QIR-B summaries
- Bags
- Exceptions

Actions:

- Create procurement
- Create QIR-B
- View traceability

Status display:

- draft
- received
- quality_pending
- approved
- hold
- bagged
- closed

## 9.3 Lot Form

Fields:

- farmer
- item_type
- harvest_year
- notes

Validation:

- farmer required
- item_type required
- harvest_year required

## 10. Procurement Screens

## 10.1 Procurement List

Columns:

- procurement_code
- lot_code
- farmer_code
- item_type
- gross_kg
- tare_kg
- net_kg
- rate_npr, Admin/Manager only
- total_npr, Admin/Manager only
- received_at
- status

Filters:

- farmer
- lot
- item_type
- status
- date range

Actions:

- New Procurement, Admin/Manager
- View
- Export, Admin/Manager for cost export

## 10.2 Procurement Form

Workflow:

1. Select lot.
2. System fills farmer and item type.
3. Enter gross kg.
4. Enter tare kg.
5. System calculates net kg.
6. Admin/Manager enters rate.
7. System calculates total.
8. Save draft.
9. Post when verified.

Fields:

- lot
- gross_kg
- tare_kg
- net_kg calculated
- rate_npr Admin/Manager only
- total_npr calculated, Admin/Manager only
- received_at
- received_by
- notes

Validation:

- gross_kg > 0
- tare_kg >= 0
- gross_kg > tare_kg
- net_kg > 0

Buttons:

- Save Draft
- Post
- Cancel

Posted view:

- display lock icon or "Posted - locked"
- no edit button

Error:

- if user tries to edit posted procurement, show: "Posted procurement cannot be edited. Create an adjustment or exception."

## 11. QIR-B Screens

## 11.1 QIR-B List

Columns:

- qirb_code
- subject_type
- subject_code
- bean_stage
- reading_count
- avg_moisture
- avg_density
- decision
- status
- checked_at

Filters:

- subject_type
- bean_stage
- decision
- status
- date range

Actions:

- New QIR-B
- Continue Draft
- View

## 11.2 QIR-B Wizard

Purpose:

Guide quality staff through a controlled quality check.

Steps:

1. Select subject
2. Select bean stage
3. Enter readings
4. Review calculated summary
5. Post decision

### Step 1: Select Subject

Fields:

- subject_type, Phase 1 default `lot`
- subject_code / searchable lot

Display:

- farmer
- item type
- procurement net kg
- lot status

### Step 2: Bean Stage

Fields:

- bean_stage

Allowed:

- fresh_cherry
- dry_cherry
- parchment
- green
- roasted

Phase-1 common value:

- parchment

### Step 3: Readings

Table fields:

- sequence_no
- moisture
- density
- bean_temp
- reading_time

Minimum:

- 5 readings

Buttons:

- Add Reading
- Remove Draft Reading
- Save Draft
- Calculate

Validation:

- moisture numeric
- density numeric
- bean_temp numeric
- cannot post with fewer than 5 readings

### Step 4: Summary

Display:

- reading_count
- avg_moisture
- moisture_sd
- avg_density
- density_sd
- avg_bean_temp
- bean_temp_sd
- estimated_green_yield_pct
- suggested decision

Color status:

- approved: green
- monitor: amber
- hold: red
- retake: red

### Step 5: Post

Buttons:

- Post QIR-B
- Save Draft
- Cancel

Rules:

- If decision is hold or retake, prompt to create exception.
- If decision is monitor, show manager review warning.

Success:

- show QIR-B code and decision
- update lot status

## 12. Bag Screens

## 12.1 Bag List

Columns:

- bag_code
- lot_code
- qirb_code
- item_type
- weight_kg
- bag_type
- current_location
- status
- sealed_at

Filters:

- lot
- location
- status
- item_type

Actions:

- Create Bag
- Bulk Create Bags
- Print QR
- View Traceability

## 12.2 Create Bag Form

Workflow:

1. Select lot.
2. Select approved QIR-B.
3. Enter bag weight.
4. Select bag type.
5. Select initial location.
6. Save and create bag.
7. System creates QR URL.
8. System creates inventory ledger row.

Fields:

- lot
- qirb
- item_type
- weight_kg
- bag_type
- current_location
- sealed_at
- notes

Validation:

- QIR-B must be posted.
- QIR-B decision must be approved.
- Monitor QIR-B requires Manager/Admin approval.
- Hold/retake QIR-B blocks bag creation.
- weight_kg > 0.

Success:

- show bag code
- show QR URL
- offer Print QR

## 12.3 Bulk Create Bags

Purpose:

Quickly split one lot into many physical bags.

Fields:

- lot
- qirb
- standard_bag_weight_kg
- number_of_full_bags
- remaining_weight_kg
- initial_location
- bag_type

Example:

```text
Net lot kg = 700
Standard bag kg = 60
Full bags = 11
Remaining kg = 40
Total bags = 12
```

Preview table:

- bag sequence
- weight_kg
- generated bag code preview

Buttons:

- Generate Preview
- Create Bags
- Cancel

Validation:

- total preview weight should match intended lot weight or require note.

## 12.4 QR Print View

Display:

- bag_code
- item_type
- weight_kg
- lot_code
- QR code
- qr_url

Actions:

- Print
- Download label

Audit:

- print creates `print_qr` event

## 13. Storage Screens

## 13.1 Storage Movement List

Columns:

- movement_code
- bag_code
- from_location
- to_location
- movement_type
- moved_at
- moved_by
- reason

Filters:

- bag
- from location
- to location
- movement type
- date range

## 13.2 Move Bag Form

Workflow:

1. Scan or search bag.
2. System shows current location.
3. Select destination.
4. Select movement type.
5. Enter reason.
6. Submit movement.
7. System updates bag current location.

Fields:

- bag
- current_location display
- to_location
- movement_type
- moved_at
- reason
- notes

Validation:

- destination required
- movement type required
- storage user can move only active bags
- Manager/Admin override required if from location mismatch

Success:

- show movement code
- show updated bag location

## 14. Environment Log Screens

## 14.1 Environment Log List

Columns:

- location_code
- temperature_c
- humidity_pct
- ac_status
- exhaust_status
- risk_flag
- logged_at
- logged_by

Filters:

- location
- risk flag
- date range

## 14.2 Environment Log Form

Fields:

- location
- temperature_c
- humidity_pct
- ac_status
- exhaust_status
- logged_at
- remarks

Server-calculated:

- risk_flag

Risk display:

- dry_risk
- ideal
- monitor
- risk
- critical

Rules:

- If risk or critical, system creates exception.

Success:

- show risk flag
- show created exception if applicable

## 15. Exception Screens

## 15.1 Exception List

Columns:

- exception_code
- subject_type
- subject_code
- exception_type
- severity
- status
- raised_by
- approved_by
- created_at
- resolved_at

Filters:

- subject type
- exception type
- severity
- status
- date range

## 15.2 Exception Detail

Sections:

- subject
- reason
- action taken
- status history
- approval/resolution

Actions:

- Approve, Admin/Manager
- Resolve, Admin/Manager
- Add action note

## 15.3 Create Exception Form

Fields:

- subject_type
- subject_code
- exception_type
- severity
- reason
- action_taken
- notes

Validation:

- reason required
- severity required

## 16. Inventory Screens

## 16.1 Inventory Ledger

Purpose:

Show stock movement truth.

Columns:

- ledger_code
- item_type
- item_code
- location
- qty_delta
- uom
- movement_reason
- ref_doc_type
- ref_doc_code
- created_at
- created_by

Rules:

- read-only in Phase 1
- no edit/delete

## 16.2 Current Stock View

Columns:

- item_type
- item_code
- location
- qty_on_hand
- uom

Filters:

- item type
- location
- item code

## 17. Audit Screens

## 17.1 Audit Log

Allowed:

- Admin
- Manager

Columns:

- audit_code
- table_name
- record_code
- action
- actor
- action_time
- ip_address
- device_id
- notes

Filters:

- table
- record code
- action
- actor
- date range

Rules:

- read-only
- no edit/delete

## 18. Traceability Page

Purpose:

One complete internal view from bag back to farmer.

Access:

- logged-in users

Sections:

1. Bag summary
2. Current location
3. Farmer
4. Lot
5. Procurement
6. QIR-B summary
7. QIR-B readings
8. Storage movement timeline
9. Inventory ledger rows
10. Exceptions
11. Audit events

Sensitive display:

- Admin/Manager: show rate and total
- Other roles: hide rate and total

Timeline format:

```text
Procurement posted
QIR-B posted
Bag created
QR printed
Moved to storage
Environment logged
QR scanned
```

## 19. Settings Screens

Phase-1 settings:

- code prefixes, Admin only
- storage locations
- user management
- basic company information

Do not include advanced costing/settings yet.

## 20. Empty States

Every list should have a clear empty state.

Examples:

Farmers:

```text
No farmers found. Add the first farmer to begin procurement.
```

QIR-B:

```text
No QIR-B records yet. Create a QIR-B from a lot after procurement.
```

Bags:

```text
No bags created yet. Bags can be created only after approved QIR-B.
```

## 21. Error States

Common errors:

- permission denied
- validation failed
- network unavailable
- posted record locked
- QIR-B requires 5 readings
- QIR-B not approved for bagging
- bag not found
- QR camera permission denied

Messages should be plain and operational.

Example:

```text
This QIR-B has only 4 readings. Add at least 5 readings before posting.
```

Example:

```text
This procurement is posted and locked. Create an adjustment or exception instead of editing it.
```

## 22. Mobile Layout Requirements

For phone/tablet:

- navigation collapses to bottom tabs or drawer
- QR Scan remains easy to access
- forms use large touch targets
- QIR-B readings table becomes stacked input cards
- bag movement workflow should fit one screen when possible
- avoid wide tables as the only way to operate

Mobile-priority screens:

- QR Scan
- QIR-B Wizard
- Create Bag
- Move Bag
- Environment Log

## 23. Offline-Ready UI Requirements

Phase-1 should prepare for offline behavior:

- show online/offline status
- save local drafts for procurement and QIR-B if implemented
- show pending sync count
- prevent duplicate submission
- show sync errors clearly

Draft states:

```text
saved locally
pending sync
sync failed
synced
```

## 24. Phase-1 UI Acceptance Test

The frontend is accepted when the team can perform this script:

1. Login as Admin.
2. Create a farmer.
3. Create a lot for that farmer.
4. Create procurement.
5. Post procurement.
6. Login as Quality.
7. Create QIR-B for the lot.
8. Enter 5 readings.
9. Calculate QIR-B.
10. Post QIR-B.
11. Login as Storage.
12. Create two bags from approved QIR-B.
13. Print QR for each bag.
14. Move bag to storage rack.
15. Enter environment log.
16. Scan bag QR.
17. Confirm traceability page opens.
18. Login as Viewer.
19. Confirm procurement cost fields are hidden.
20. Login as Manager.
21. Confirm audit log shows post, print QR, and scan QR events.

## 25. Out Of Scope For Phase 1 UI

Do not build these screens yet:

- hulling
- green batch rest
- grading
- roasting
- packaging
- public coffee story page
- sales order
- customer CRM
- farmer payment
- full costing dashboard
- BI charts
- SMS/WhatsApp automation

