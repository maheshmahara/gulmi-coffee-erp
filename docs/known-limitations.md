# Known Limitations

## Sprint 0

- Authentication API is not implemented yet.
- Business modules are not implemented yet.
- Frontend screens are placeholders.
- Audit service is a skeleton and does not yet write events.
- Code generator service is a skeleton and not concurrency-safe yet.
- Docker builds require internet access to install Python and Node dependencies.
- Production compose is a baseline and still needs HTTPS/certificate integration before real go-live.

## Sprint 1

- Login uses session authentication for the PWA foundation; token/JWT support is not implemented.
- User management UI is not implemented yet, though backend endpoints exist.
- Storage location create/edit UI is not implemented yet, though backend endpoints exist.
- Audit code generation is count-based and must be replaced with a locked counter before high-concurrency production use.
- CSRF hardening should be revisited before production; Sprint 1 prioritizes local/staging workflow validation.
