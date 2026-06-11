# Developer RFQ And Evaluation Template

## 1. Purpose

Use this document when requesting proposals from developers, freelancers, or software companies for the Gulmi Coffee ERP Phase-1 MVP.

The goal is to compare vendors clearly and avoid vague promises.

## 2. Project Summary To Send

```text
We are building the Gulmi Coffee ERP, a traceability-first ERP for a vertically integrated coffee business in Nepal.

Phase-1 MVP scope:
Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR

The system must support role-based access, QIR-B quality rules, immutable posted documents, inventory ledger, audit log, internal QR traceability, and sensitive financial field protection.

Recommended stack:
Django + Django REST Framework, React + TypeScript PWA, PostgreSQL 16, Docker Compose, Nginx.
```

Send these files with the RFQ:

- `docs/developer-handoff-package.md`
- `docs/phase-1-mvp-software-requirements.md`
- `docs/phase-1-database-schema.md`
- `docs/phase-1-api-specification.md`
- `docs/phase-1-ui-workflow-specification.md`
- `docs/phase-1-testing-qa-specification.md`
- `docs/phase-1-developer-task-breakdown-sprint-plan.md`

## 3. Required Vendor Response Format

Ask every vendor to respond using this structure:

```text
1. Understanding of the project
2. Proposed technology stack
3. Team members and roles
4. Relevant previous experience
5. Development timeline by sprint
6. Deliverables by sprint
7. Testing approach
8. Deployment and backup approach
9. Assumptions
10. Exclusions
11. Risks
12. Price breakdown
13. Post-go-live support terms
```

Reject responses that only provide a total price without explaining scope.

## 4. Mandatory Capabilities

Vendor must be able to demonstrate:

- Django or equivalent backend experience
- PostgreSQL schema design
- React PWA development
- role-based permissions
- API-level sensitive field filtering
- audit logs
- immutable posted records
- QR generation/scanning workflow
- Docker deployment
- backup and restore process
- business-rule testing

## 5. Questions To Ask Vendor

Ask these directly:

1. How will you prevent non-admin users from seeing cost/rate/payment data?
2. How will you prevent posted documents from being edited?
3. How will inventory be calculated?
4. How will QIR-B decisions be tested?
5. How will QR scans be logged?
6. How will staging differ from production?
7. How will backups be created and restored?
8. What happens if internet is weak at collection points?
9. Which parts of Phase 1 are you excluding?
10. What do you need from us before Sprint 0?

## 6. Required Quote Breakdown

Ask vendor to break price by sprint:

| Sprint | Scope | Price | Duration |
|---|---|---:|---|
| Sprint 0 | Setup and architecture | TBD | 2 weeks |
| Sprint 1 | Users, roles, audit, storage locations | TBD | 2 weeks |
| Sprint 2 | Farmers, lots, procurement | TBD | 2 weeks |
| Sprint 3 | QIR-B | TBD | 2 weeks |
| Sprint 4 | Bags, QR, inventory ledger | TBD | 2 weeks |
| Sprint 5 | Storage, environment, exceptions | TBD | 2 weeks |
| Sprint 6 | Traceability, reports, audit, QA | TBD | 2 weeks |
| Sprint 7 | Pilot, deployment, go-live | TBD | 2 weeks |

Also ask for:

- monthly support cost
- bug-fix warranty period
- cost for Phase 2 estimate, optional
- hosting cost, if they provide hosting

## 7. Evaluation Scorecard

Score each vendor from 1 to 5.

| Category | Weight | Score | Weighted Score |
|---|---:|---:|---:|
| Understands coffee traceability workflow | 15 |  |  |
| Database/PostgreSQL discipline | 15 |  |  |
| Permission/security approach | 15 |  |  |
| Django/React experience | 10 |  |  |
| Testing/QA seriousness | 15 |  |  |
| Deployment/backup approach | 10 |  |  |
| Communication clarity | 10 |  |  |
| Price/value | 10 |  |  |
| Total | 100 |  |  |

Recommended rule:

```text
Do not select a vendor scoring below 70/100.
```

## 8. Red Flags

Be careful if vendor says:

- "No need for detailed requirements."
- "We can build everything quickly in one phase."
- "Frontend hiding is enough for sensitive data."
- "Inventory can just be a quantity field."
- "Testing will be done at the end."
- "Backups are your hosting provider's problem."
- "We do not need staging."
- "We will decide database later."
- "QR can be added at the end."

These are serious warning signs.

## 9. Preferred Contract Terms

Recommended:

- milestone-based payments
- staging demos required
- source code belongs to Gulmi Coffee
- database schema belongs to Gulmi Coffee
- documentation included
- deployment instructions included
- backup/restore instructions included
- test report included
- 30 to 60 day bug-fix warranty after go-live

Avoid:

- paying full amount upfront
- vendor owning source code
- no staging access
- no written acceptance criteria
- vague support terms

## 10. Minimum Acceptance Before Payment

For each sprint payment, require:

- working demo
- code committed
- tests or QA checklist passed
- documentation updated if needed
- owner acceptance

Example:

```text
Sprint 3 QIR-B payment is released only after QIR-B can be created, 5 readings entered, calculation works, hold/monitor/retake/approved decisions work, and tests pass.
```

## 11. Final Vendor Selection Rule

Choose the vendor who best protects these five things:

1. traceability truth
2. quality rule enforcement
3. inventory ledger accuracy
4. sensitive financial data
5. backup/restore reliability

Lowest price is not the same as lowest risk.

