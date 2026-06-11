# Phase-3 Roadmap: Finance-Lite, Costing, BI, And CRM Depth

## 1. Purpose

This document defines the recommended Phase-3 roadmap after Phase 1 and Phase 2 are stable.

Phase 1 proves:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

Phase 2 proves:

```text
Bag -> Hulling -> Green Batch -> Grading -> Roasting -> Packaging -> Public QR -> Sales Foundation
```

Phase 3 adds management intelligence:

```text
Costing -> Farmer Payables -> Sales Margin -> BI Dashboards -> CRM Depth -> Accounting Export
```

## 2. Do Not Start Phase 3 Until

Start Phase 3 only after:

- Phase 1 traceability is stable
- Phase 2 production/package traceability is stable
- inventory ledger explains stock movements
- sales foundation exists or is ready
- staff can use the system without developer help
- backup and restore process is tested
- package-level QR works

## 3. Phase-3 Main Goal

Phase 3 is accepted when:

```text
Gulmi Coffee can calculate actual cost and margin from procurement through package sale, view role-based BI dashboards, produce farmer payment statements, and export clean data for accounting.
```

## 4. Phase-3 Modules

Phase-3 modules:

1. Costing Engine
2. Finance-Lite
3. Farmer Payables
4. Customer Receivables
5. Sales Analytics
6. BI Dashboards
7. CRM Depth
8. Supplier Scorecards
9. Accounting Export
10. Optional Metabase Integration

## 5. Costing Engine

Purpose:

Convert the accounting/costing spreadsheet into ERP-driven calculations.

Cost layers:

- raw material cost
- transport cost
- processing cost
- hulling cost
- roasting cost
- packaging cost
- overhead allocation
- depreciation allocation, optional

Important:

- spreadsheet assumptions become configurable settings
- actual production data should override assumptions where available

Example cost roll-up:

```text
Procurement cost
+ inbound transport
+ hulling electricity/labour
+ roasting electricity/labour
+ packaging material
+ overhead allocation
= product cost
```

## 6. Cost Settings

Create configurable cost settings:

- transport cost per kg
- fresh cherry processing cost per kg
- dry cherry cleaning/sorting cost per kg
- hulling electricity cost per kg
- hulling labour cost per kg
- roasting electricity cost per kg
- roasting labour cost per kg
- packaging cost per kg or per unit
- monthly rent
- monthly salary
- other fixed overhead
- equipment capex
- useful life for depreciation

Each setting should have:

- effective_from date
- effective_to date
- value
- unit
- created_by
- approved_by

Reason:

Costs change over time. Historical costing should use the setting active at the time of production.

## 7. Product Costing

Cost outputs:

- cost per parchment kg
- cost per green kg
- cost per roasted kg
- cost per package
- cost per cup, optional for cafe model
- gross margin per SKU
- gross margin per channel

Required reports:

- Cost per roasted kg by input source
- Cost per package
- Margin by SKU
- Margin by sales channel
- Production loss impact
- Yield variance cost impact

## 8. Farmer Payables

Purpose:

Track what is owed to farmers/collectors.

Logic:

```text
Farmer payable = posted procurement total - payments made
```

Required features:

- farmer payable balance
- payable aging
- payment record
- farmer statement
- payment method
- payment notes

Payment methods:

```text
cash
bank
eSewa
Khalti
other
```

Sensitive:

- visible only to Admin/Manager

## 9. Customer Receivables

Purpose:

Track customer sales and payments.

Logic:

```text
Customer receivable = invoice/sales total - customer payments
```

Required features:

- customer balance
- payment status
- sales by customer
- receivable aging
- customer statement

Customer types:

```text
retail
cafe
wholesale
export
online
```

## 10. Sales Analytics

Reports:

- sales by SKU
- sales by channel
- sales by customer
- sales by period
- average selling price
- gross margin by SKU
- gross margin by channel
- package inventory sold vs available

Dashboards:

- monthly sales NPR
- top SKUs
- best customers
- slow-moving packages
- unpaid customers

## 11. BI Dashboards

Use the NAV-style pattern:

1. standard reports
2. KPI/cue tiles
3. ad-hoc Excel export

## 11.1 Admin Dashboard

Cards:

- total stock by stage
- bags on hold
- green batches resting
- today hulling kg
- today roasting kg
- packaged units available
- monthly sales NPR
- farmer payable balance
- customer receivable balance
- gross margin
- open exceptions

## 11.2 Quality Dashboard

Cards:

- QIR-B pass rate
- moisture risk lots
- density risk lots
- retake count
- hold count
- top moisture-risk farmers
- QIR-B trend

## 11.3 Storage Dashboard

Cards:

- stock by location
- aging stock
- humidity risk
- movement count
- bags on hold
- inventory adjustment count

## 11.4 Production Dashboard

Cards:

- hulling kg
- green bean output
- average green yield
- low yield batches
- roast batches
- roast loss percentage
- packages produced

## 11.5 Sales Dashboard

Cards:

- sales by channel
- sales by SKU
- unpaid invoices
- available packaged stock
- top customers
- reorder candidates

## 12. Standard Reports

Recommended reports:

- Procurement by farmer/period
- QIR-B pass rate
- Moisture/density trend
- Yield variance by lot
- Storage environment history
- Hulling report
- Roast log
- Packaging report
- Inventory valuation
- Farmer payment statement
- Customer sales statement
- Sales by SKU/channel
- Cost per package
- Margin report
- Exception register
- Traceability report

Every report should support:

- date filter
- CSV/Excel export
- role-based sensitive field filtering

## 13. CRM Depth

CRM in Gulmi Coffee should include both farmer-side and customer-side relationships.

## 13.1 Farmer CRM

Features:

- farmer profile
- procurement history
- QIR-B pass/fail history
- yield performance
- payment history
- notes/tags
- follow-up reminders
- training/support notes

Useful tags:

```text
high_quality
moisture_risk
payment_pending
needs_training
preferred_supplier
new_farmer
```

## 13.2 Customer CRM

Features:

- customer profile
- customer type
- order history
- payment history
- preferred products
- reorder reminders
- notes

Customer tags:

```text
retail
cafe
wholesale
export
high_value
payment_delay
subscription_candidate
```

## 14. Supplier Scorecards

Purpose:

Use operational data to improve next season's procurement decisions.

Scorecard metrics:

- total kg supplied
- QIR-B pass rate
- average moisture
- average density
- hold/retake count
- expected vs actual yield
- payment history
- exception count

Possible score:

```text
quality_score
yield_score
reliability_score
overall_supplier_score
```

Use:

- identify best farmers
- identify training needs
- guide procurement rates/priority
- reduce quality risk

## 15. Accounting Export

Purpose:

Provide clean data to accountant or accounting system.

Export targets:

- CSV/Excel for accountant
- Odoo integration later
- Tally or local accounting system if needed

Export types:

- procurement purchases
- farmer payments
- sales invoices
- customer payments
- inventory valuation
- COGS summary
- expense allocation

Important:

- exports must respect role permissions
- exports must create audit event

## 16. Optional Metabase BI

Metabase can be added for BI exploration.

Recommended setup:

- read-only database user
- SQL views for reporting
- no write access
- no sensitive tables unless protected

Suggested views:

- `vw_procurement_summary`
- `vw_qirb_summary`
- `vw_bag_traceability`
- `vw_current_stock`
- `vw_hulling_yield`
- `vw_roast_loss`
- `vw_package_margin`
- `vw_farmer_scorecard`
- `vw_sales_summary`

## 17. Phase-3 Database Additions

Tables:

- `cost_setting`
- `cost_allocation`
- `product_cost_summary`
- `farmer_payable`
- `customer_receivable`
- `farmer_statement`
- `customer_statement`
- `crm_note`
- `crm_reminder`
- `supplier_scorecard`
- `accounting_export_batch`
- `accounting_export_line`

Some of these can be views/materialized views instead of physical tables.

## 18. Phase-3 API Additions

Expected endpoints:

```text
GET/POST /cost-settings
GET /costing/package/{id}
GET /reports/margin
GET /reports/inventory-valuation

GET /farmers/{id}/statement
POST /farmer-payments

GET /customers/{id}/statement
POST /customer-payments

GET /crm/notes
POST /crm/notes
GET /crm/reminders
POST /crm/reminders

GET /reports/supplier-scorecards
POST /accounting-exports
```

## 19. Phase-3 UI Additions

Screens:

- Cost Settings
- Product Cost Summary
- Margin Report
- Farmer Payables
- Farmer Statement
- Customer Receivables
- Customer Statement
- Sales Analytics
- CRM Notes
- CRM Reminders
- Supplier Scorecards
- Accounting Export
- BI Dashboard

## 20. Phase-3 Acceptance Test

Developer must demonstrate:

1. Configure cost settings.
2. Select a packaged product.
3. Calculate cost per package.
4. Sell package to customer.
5. Show gross margin.
6. Show farmer payable from procurement.
7. Record farmer payment.
8. Generate farmer statement.
9. Show sales by SKU/channel.
10. Generate supplier scorecard.
11. Export accounting data.
12. Confirm non-Admin roles cannot see sensitive finance data.

## 21. Phase-3 Risks

| Risk | Mitigation |
|---|---|
| Costing becomes too complex | start with simple configurable assumptions |
| Wrong margin due to bad inventory data | do not start Phase 3 until ledger is stable |
| Finance data leaks | API-level field filtering and export audit |
| Reports disagree with operations | use SQL views from source documents |
| Staff ignore payment records | make farmer statement depend on ERP payments |
| BI tool exposes sensitive data | use read-only user and protected views |

## 22. Phase-3 Definition Of Done

Phase 3 is done when:

```text
Gulmi Coffee can see cost, margin, farmer payable, customer receivable, sales performance, supplier scorecards, and role-based BI reports from real ERP records, with accounting exports and sensitive financial data protected.
```

