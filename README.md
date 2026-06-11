# Gulmi Coffee ERP

This repository contains the planning, workbook prototype, and developer-ready requirements for the Gulmi Coffee ERP.

The ERP is designed for a vertically integrated coffee business in Nepal and focuses on farmer-to-package traceability:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Hulling -> Green Batch -> Grading -> Roasting -> Packaging -> Sale -> Finance/BI
```

## Current Phase

The project is currently in Phase 0 and Phase 1 planning:

- Phase 0: structured workbook prototype
- Phase 1: MVP software requirements

The Phase-1 MVP scope is:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

## Key Files

- `docs/developer-handoff-package.md` - start-here package for developers/software vendors
- `docs/developer-rfq-and-evaluation-template.md` - RFQ and scoring template for selecting developers/vendors
- `docs/owner-step-by-step-execution-checklist.md` - owner checklist for hiring, supervising, testing, and go-live
- `docs/project-master-index-and-decision-log.md` - master document index, approved decisions, pending decisions, and risks
- `docs/gulmi-coffee-erp-sdlc-record.md` - project SDLC record and principles
- `docs/phase-0-workbook-validation.md` - workbook tabs, formulas, dropdowns, and validation rules
- `docs/phase-1-mvp-software-requirements.md` - developer-facing MVP software requirements
- `docs/phase-1-database-schema.md` - PostgreSQL schema, constraints, indexes, and migration order
- `docs/phase-1-api-specification.md` - REST API endpoints, permissions, request/response shapes, and API tests
- `docs/phase-1-ui-workflow-specification.md` - screen-by-screen UI and staff workflow specification
- `docs/phase-1-testing-qa-specification.md` - test cases, QA process, pilot script, and go/no-go checklist
- `docs/phase-1-deployment-operations-guide.md` - hosting, backups, monitoring, go-live, and daily operations guide
- `docs/phase-1-developer-task-breakdown-sprint-plan.md` - sprint-by-sprint developer task plan
- `docs/phase-2-roadmap-production-packaging-sales.md` - roadmap for hulling, roasting, packaging, public QR, and sales foundation
- `docs/phase-3-roadmap-finance-bi-crm.md` - roadmap for costing, finance-lite, BI, CRM, and accounting export
- `scripts/build_phase0_workbook.mjs` - reproducible builder for the Phase-0 Excel workbook
- `outputs/gulmi-coffee-erp-phase-0/gulmi-coffee-erp-phase-0-workbook.xlsx` - generated Phase-0 workbook

## Core Rules

- Every activity creates a document record.
- Posted records are immutable.
- Corrections use adjustment or exception records.
- Inventory is derived from ledger rows.
- Cost and payment fields are Admin/Manager-only.
- QR traceability is role-aware.
