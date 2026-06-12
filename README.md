# Gulmi Coffee ERP

This repository contains the planning, workbook prototype, and developer-ready requirements for the Gulmi Coffee ERP.

The ERP is designed for a vertically integrated coffee business in Nepal and focuses on farmer-to-package traceability:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Hulling -> Green Batch -> Grading -> Roasting -> Packaging -> Sale -> Finance/BI
```

## Current Phase

The project is currently in Phase 1 Sprint 2 implementation:

- Phase 0: structured workbook prototype
- Phase 1: MVP software implementation foundation

The Phase-1 MVP scope is:

```text
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR
```

## Key Files

- `docs/developer-handoff-package.md` - start-here package for developers/software vendors
- `docs/developer-rfq-and-evaluation-template.md` - RFQ and scoring template for selecting developers/vendors
- `docs/github-issue-backlog-template.md` - GitHub labels, milestones, and starter issues by sprint
- `docs/owner-step-by-step-execution-checklist.md` - owner checklist for hiring, supervising, testing, and go-live
- `docs/project-master-index-and-decision-log.md` - master document index, approved decisions, pending decisions, and risks
- `docs/gulmi-coffee-erp-sdlc-record.md` - project SDLC record and principles
- `docs/phase-0-workbook-validation.md` - workbook tabs, formulas, dropdowns, and validation rules
- `docs/phase-1-mvp-software-requirements.md` - developer-facing MVP software requirements
- `docs/phase-1-sprint-0-implementation-plan.md` - Sprint 0 implementation plan and verification record
- `docs/phase-1-sprint-1-implementation-plan.md` - Sprint 1 implementation plan and verification record
- `docs/phase-1-sprint-2-implementation-plan.md` - Sprint 2 farmer, lot, and procurement implementation record
- `docs/phase-1-database-schema.md` - PostgreSQL schema, constraints, indexes, and migration order
- `docs/phase-1-api-specification.md` - REST API endpoints, permissions, request/response shapes, and API tests
- `docs/phase-1-ui-workflow-specification.md` - screen-by-screen UI and staff workflow specification
- `docs/phase-1-testing-qa-specification.md` - test cases, QA process, pilot script, and go/no-go checklist
- `docs/phase-1-requirements-traceability-matrix.md` - matrix mapping requirements to database/API/UI/tests
- `docs/phase-1-deployment-operations-guide.md` - hosting, backups, monitoring, go-live, and daily operations guide
- `docs/phase-1-developer-task-breakdown-sprint-plan.md` - sprint-by-sprint developer task plan
- `docs/phase-1-staff-training-and-sop-checklist.md` - staff training checklist and daily operating SOP
- `docs/phase-2-roadmap-production-packaging-sales.md` - roadmap for hulling, roasting, packaging, public QR, and sales foundation
- `docs/phase-3-roadmap-finance-bi-crm.md` - roadmap for costing, finance-lite, BI, CRM, and accounting export
- `docs/developer-setup.md` - local Docker setup and first-run instructions
- `docs/backend-architecture.md` - backend project structure and service-layer rules
- `docs/frontend-architecture.md` - frontend project structure and UI shell notes
- `docs/database-migrations.md` - migration plan and current schema migrations
- `docs/api-reference.md` - implemented API reference, starting with health
- `docs/deployment-guide.md` - local and production-style deployment commands
- `docs/backup-restore-guide.md` - database backup and restore commands
- `docs/testing-guide.md` - Sprint 0 verification and future test commands
- `docs/user-manual-admin.md` - Admin user manual starter
- `docs/user-manual-manager.md` - Manager user manual starter
- `docs/user-manual-quality.md` - Quality user manual starter
- `docs/user-manual-storage.md` - Storage user manual starter
- `docs/release-notes.md` - release notes
- `docs/known-limitations.md` - current known limitations
- `scripts/build_phase0_workbook.mjs` - reproducible builder for the Phase-0 Excel workbook
- `outputs/gulmi-coffee-erp-phase-0/gulmi-coffee-erp-phase-0-workbook.xlsx` - generated Phase-0 workbook

## Implementation Structure

- `backend/` - Django + Django REST Framework backend foundation
- `frontend/` - React + TypeScript PWA frontend foundation
- `infra/nginx/` - Nginx reverse proxy baseline
- `docker-compose.yml` - local development stack
- `docker-compose.prod.yml` - production-style stack baseline
- `.env.example` - environment variable template
- `scripts/backup_db.sh` - PostgreSQL backup helper
- `scripts/restore_db.sh` - PostgreSQL restore helper

## Sprint 2 Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Then open:

```text
Frontend: http://localhost:5174
Backend health: http://localhost:8001/api/v1/health
```

Seed demo users, storage, and a sample procurement chain:

```bash
docker compose run --rm backend python manage.py seed_phase1
```

## Core Rules

- Every activity creates a document record.
- Posted records are immutable.
- Corrections use adjustment or exception records.
- Inventory is derived from ledger rows.
- Cost and payment fields are Admin/Manager-only.
- QR traceability is role-aware.
