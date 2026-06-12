# Frontend Architecture

## Stack

- React
- TypeScript
- Vite
- PWA-ready responsive shell

## Project Layout

```text
frontend/
  index.html
  package.json
  vite.config.ts
  src/
    App.tsx
    main.tsx
    styles.css
    components/
    lib/
    pages/
```

## Sprint 0 UI

Sprint 0 provides:

- app shell
- brand header
- role preview selector
- role-aware navigation scaffold
- dashboard preview cards
- login placeholder
- backend health badge
- responsive mobile layout foundation

## Sprint 2 UI

Sprint 2 adds API-backed workflow panels:

- Farmers list/create
- Lots list/create
- Procurements list/create/post
- posted receipt locked state
- cost columns hidden outside Admin/Manager roles

## Phase-1 UI Direction

The frontend must implement screens from:

```text
docs/phase-1-ui-workflow-specification.md
```

Mobile-priority screens:

- QR Scan
- QIR-B Wizard
- Create Bag
- Move Bag
- Environment Log

## API Client

The initial API client is in:

```text
frontend/src/lib/api.ts
```

Implemented API client methods include:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/me`
- `GET/POST /api/v1/farmers`
- `GET/POST /api/v1/lots`
- `GET/POST /api/v1/procurements`
- `POST /api/v1/procurements/{id}/post`
