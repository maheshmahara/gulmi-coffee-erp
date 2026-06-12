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

Sprint 1 should add authentication methods for:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/me`

