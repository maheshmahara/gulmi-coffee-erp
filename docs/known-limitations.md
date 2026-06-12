# Known Limitations

## Sprint 0

- Code generator service is a skeleton and not concurrency-safe yet.
- Docker builds require internet access to install Python and Node dependencies.
- Production compose is a baseline and still needs HTTPS/certificate integration before real go-live.

## Sprint 1

- Login uses CSRF-exempt session authentication for the local/staging PWA foundation; production must add explicit CSRF handling or token/JWT support.
- User management UI is not implemented yet, though backend endpoints exist.
- Storage location create/edit UI is not implemented yet, though backend endpoints exist.
- Audit code generation is count-based and must be replaced with a locked counter before high-concurrency production use.
- CSRF hardening should be revisited before production; Sprint 1 prioritizes local/staging workflow validation.

## Sprint 2

- Farmer, lot, and procurement screens are functional but still list/form focused; detail pages and edit forms are deferred.
- Procurement posting does not yet create inventory ledger rows; inventory starts in the later bag/storage sprint.
- Procurement rate/total are hidden for non-Admin/Manager roles, but export-level permission checks still need to be implemented when exports are added.
- Code generation remains count-based and should be replaced with a transaction-safe counter before multi-user production.
